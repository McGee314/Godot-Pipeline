extends Control

# UDP Settings
var udp_socket := PacketPeerUDP.new()
var udp_port := 5000
var is_connected := false
var last_received_time := 0.0
var timeout_duration := 3.0

# UI References
@onready var status_label = $MarginContainer/VBoxContainer/StatusPanel/VBoxContainer/StatusLabel
@onready var connection_label = $MarginContainer/VBoxContainer/StatusPanel/VBoxContainer/ConnectionLabel
@onready var video_rect = $MarginContainer/VBoxContainer/VideoContainer/VideoPanel/TextureRect
@onready var placeholder_label = $MarginContainer/VBoxContainer/VideoContainer/VideoPanel/PlaceholderLabel
@onready var connect_button = $MarginContainer/VBoxContainer/ButtonPanel/ConnectButton
@onready var login_button = $MarginContainer/VBoxContainer/ButtonPanel/LoginButton
@onready var retry_button = $MarginContainer/VBoxContainer/ButtonPanel/RetryButton
@onready var quit_button = $MarginContainer/VBoxContainer/ButtonPanel/QuitButton

# Animation
var entrance_tween: Tween
var button_tween: Tween
var status_tween: Tween
var is_transitioning := false

# Login state
var login_successful := false
var gesture_detected := ""
var camera_connected := false
var face_detected_frames := 0
var required_frames := 60  # 60 frames = ~2 seconds
var is_processing_login := false

# Video processing
var current_image := Image.new()
var current_texture := ImageTexture.new()
var receiving_video := false

# Frame reassembly (for fragmented UDP packets)
var frame_buffers: Dictionary = {}  # seq_num -> {total_packets, received_packets, data_parts}
var last_completed_sequence: int = 0
var frame_timeout: float = 1.0  # 1 second timeout for incomplete frames

func _ready():
	# Setup initial UI state
	modulate.a = 0.0
	login_button.disabled = true
	retry_button.visible = false
	connect_button.disabled = false
	
	# Connect button signals
	connect_button.pressed.connect(_on_connect_button_pressed)
	login_button.pressed.connect(_on_login_button_pressed)
	retry_button.pressed.connect(_on_retry_button_pressed)
	quit_button.pressed.connect(_on_quit_button_pressed)
	
	# Setup hover effects
	_setup_button_hover_effects()
	
	# Start entrance animation
	await get_tree().process_frame
	animate_entrance()
	
	# Wait for manual connection instead of auto-connect
	_update_status("📹 Click 'CONNECT CAMERA' to start", Color.CYAN)

func _setup_button_hover_effects():
	for button in [connect_button, login_button, retry_button, quit_button]:
		if not button.mouse_entered.is_connected(_on_button_hover.bind(button)):
			button.mouse_entered.connect(_on_button_hover.bind(button))
		if not button.mouse_exited.is_connected(_on_button_unhover.bind(button)):
			button.mouse_exited.connect(_on_button_unhover.bind(button))

func animate_entrance():
	entrance_tween = create_tween()
	entrance_tween.set_parallel(true)
	entrance_tween.tween_property(self, "modulate:a", 1.0, 1.0).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	
	# Pulse status label
	await get_tree().create_timer(0.5).timeout
	_pulse_status_label()

func _pulse_status_label():
	if status_tween:
		status_tween.kill()
	status_tween = create_tween()
	status_tween.set_loops()
	status_tween.tween_property(status_label, "modulate:a", 0.5, 0.8).set_ease(Tween.EASE_IN_OUT)
	status_tween.tween_property(status_label, "modulate:a", 1.0, 0.8).set_ease(Tween.EASE_IN_OUT)

func _start_udp_connection():
	var error = udp_socket.bind(udp_port)
	if error != OK:
		_update_status("❌ Failed to bind UDP port %d" % udp_port, Color.RED)
		retry_button.visible = true
		connect_button.disabled = false
		camera_connected = false
		return
	
	is_connected = true
	camera_connected = true
	_update_status("📸 Silahkan tunjukkan wajah Anda ke kamera", Color.ORANGE)
	connection_label.text = "📡 UDP Port: %d | Status: Listening" % udp_port
	print("UDP Server started on port: ", udp_port)
	
	# Update connect button
	connect_button.text = "✅ CAMERA CONNECTED"
	connect_button.disabled = true
	
	# Stop pulsing
	if status_tween:
		status_tween.kill()

func _on_connect_button_pressed():
	if is_transitioning or camera_connected:
		return
	
	# Button press feedback
	var press_tween = create_tween()
	press_tween.tween_property(connect_button, "scale", Vector2(0.95, 0.95), 0.08).set_ease(Tween.EASE_OUT)
	press_tween.tween_property(connect_button, "scale", Vector2.ONE, 0.15).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	
	_update_status("🔄 Connecting to camera...", Color.CYAN)
	_start_udp_connection()

func _update_status(message: String, color: Color = Color.WHITE):
	status_label.text = message
	status_label.modulate = color
	
	# Flash effect
	var flash_tween = create_tween()
	flash_tween.tween_property(status_label, "scale", Vector2(1.05, 1.05), 0.1).set_ease(Tween.EASE_OUT)
	flash_tween.tween_property(status_label, "scale", Vector2.ONE, 0.2).set_ease(Tween.EASE_IN_OUT)

func _process(delta):
	if not is_connected:
		return
	
	# Check for UDP packets
	while udp_socket.get_available_packet_count() > 0:
		var packet = udp_socket.get_packet()
		_process_packet(packet)
		last_received_time = Time.get_ticks_msec() / 1000.0
	
	# Check timeout
	if last_received_time > 0:
		var current_time = Time.get_ticks_msec() / 1000.0
		if current_time - last_received_time > timeout_duration and not login_successful:
			_update_status("⏰ Connection timeout. Please try again.", Color.ORANGE)
			receiving_video = false
			placeholder_label.visible = true

func _process_packet(packet: PackedByteArray):
	"""
	Process incoming UDP packet.
	Handles both fragmented video frames and text messages.
	
	Packet Format (video):
	[sequence_number:4][total_packets:4][packet_index:4][JPEG_data...]
	"""
	# Check if this is a fragmented video packet (at least 12 bytes for header)
	if packet.size() >= 12:
		# Try to parse as fragmented packet
		var sequence_number = _bytes_to_int(packet.slice(0, 4))
		var total_packets = _bytes_to_int(packet.slice(4, 8))
		var packet_index = _bytes_to_int(packet.slice(8, 12))
		
		# Validate header
		if sequence_number > 0 and total_packets > 0 and packet_index >= 0 and packet_index < total_packets:
			# Valid fragmented packet
			var packet_data = packet.slice(12)
			_handle_fragmented_packet(sequence_number, total_packets, packet_index, packet_data)
			return
	
	# If not a valid fragmented packet, try as text message or single-packet image
	if packet.size() < 100:  # Likely text message
		var data_string = packet.get_string_from_utf8()
		if data_string:
			_handle_received_data(data_string)
	else:
		# Try as single-packet JPEG (fallback)
		_try_display_image(packet)

func _handle_fragmented_packet(sequence_number: int, total_packets: int, packet_index: int, packet_data: PackedByteArray):
	"""Handle reassembly of fragmented video frames"""
	# Skip old frames
	if sequence_number < last_completed_sequence - 2:
		return
	
	# Initialize buffer for new frame
	if sequence_number not in frame_buffers:
		frame_buffers[sequence_number] = {
			"total_packets": total_packets,
			"received_packets": 0,
			"data_parts": {},
			"timestamp": Time.get_ticks_msec() / 1000.0
		}
	
	var frame_buffer = frame_buffers[sequence_number]
	
	# Add packet to frame buffer (if not already received)
	if packet_index not in frame_buffer.data_parts:
		frame_buffer.data_parts[packet_index] = packet_data
		frame_buffer.received_packets += 1
	
	# Check if frame is complete
	if frame_buffer.received_packets >= frame_buffer.total_packets:
		_assemble_and_display_frame(sequence_number)

func _assemble_and_display_frame(sequence_number: int):
	"""Assemble fragmented packets into complete frame and display"""
	if sequence_number not in frame_buffers:
		return
	
	var frame_buffer = frame_buffers[sequence_number]
	var frame_data = PackedByteArray()
	
	# Combine all packets in order
	for i in range(frame_buffer.total_packets):
		if i in frame_buffer.data_parts:
			frame_data.append_array(frame_buffer.data_parts[i])
		else:
			# Missing packet - cannot assemble
			print("⚠️  Frame %d missing packet %d" % [sequence_number, i])
			frame_buffers.erase(sequence_number)
			return
	
	# Clean up
	frame_buffers.erase(sequence_number)
	last_completed_sequence = sequence_number
	
	# Display the assembled frame
	_try_display_image(frame_data)

func _bytes_to_int(bytes: PackedByteArray) -> int:
	"""Convert 4 bytes to integer (big-endian)"""
	if bytes.size() != 4:
		return 0
	return (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3]

func _try_display_image(image_data: PackedByteArray):
	"""Try to load and display image from binary data"""
	var image = Image.new()
	var error = image.load_jpg_from_buffer(image_data)
	
	if error == OK:
		receiving_video = true
		placeholder_label.visible = false
		
		# Create texture from image
		current_texture = ImageTexture.create_from_image(image)
		video_rect.texture = current_texture
		
		# Update connection status
		connection_label.text = "📡 UDP Port: %d | Video: Active | FPS: %.1f" % [udp_port, Engine.get_frames_per_second()]
		
		# ✅ FACE DETECTION IN GODOT (not in Python!)
		if camera_connected and not login_successful:
			_detect_face_in_frame(image)
	else:
		# Try PNG if JPEG failed
		error = image.load_png_from_buffer(image_data)
		if error == OK:
			receiving_video = true
			placeholder_label.visible = false
			current_texture = ImageTexture.create_from_image(image)
			video_rect.texture = current_texture
			
			# ✅ FACE DETECTION IN GODOT
			if camera_connected and not login_successful:
				_detect_face_in_frame(image)

func _handle_received_data(data: String):
	print("Received text data: ", data)
	
	# Handle any text messages from Python (if needed)
	# For now, we don't expect any since Python just streams video
	if data.length() < 100:
		_update_status("📥 Data: %s" % data, Color.CYAN)

func _on_gesture_detected(gesture: String):
	# No longer needed - keeping for compatibility
	pass

func _enable_login():
	# No longer needed - login button is enabled after face detection completes
	pass

func _on_login_success():
	if is_transitioning:
		return
		
	login_successful = true
	is_processing_login = false
	
	_update_status("✅ Login Berhasil! Klik LOGIN untuk lanjut.", Color.GREEN)
	
	# Stop status pulse
	if status_tween:
		status_tween.kill()
	
	# ✅ ENABLE login button to proceed to next scene
	login_button.disabled = false
	login_button.text = "🚀 LANJUT"
	
	# Animate button to draw attention
	var pulse_tween = create_tween()
	pulse_tween.set_loops(3)
	pulse_tween.tween_property(login_button, "scale", Vector2(1.1, 1.1), 0.3).set_ease(Tween.EASE_OUT)
	pulse_tween.tween_property(login_button, "scale", Vector2.ONE, 0.3).set_ease(Tween.EASE_IN)

func _on_login_button_pressed():
	if is_transitioning or login_button.disabled:
		return
	
	# Button press feedback
	var press_tween = create_tween()
	press_tween.tween_property(login_button, "scale", Vector2(0.95, 0.95), 0.08).set_ease(Tween.EASE_OUT)
	press_tween.tween_property(login_button, "scale", Vector2.ONE, 0.15).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	
	# ✅ If login successful, proceed to next scene
	if login_successful:
		_proceed_to_next_scene()
	else:
		# Should not happen if button is properly disabled
		_update_status("⚠️ Login belum berhasil", Color.ORANGE)

func _on_retry_button_pressed():
	retry_button.visible = false
	connect_button.disabled = false
	connect_button.text = "📹 CONNECT CAMERA"
	camera_connected = false
	_update_status("📹 Click 'CONNECT CAMERA' to retry", Color.CYAN)

func _on_quit_button_pressed():
	if is_transitioning:
		return
	is_transitioning = true
	
	var exit_tween = create_tween()
	exit_tween.tween_property(self, "modulate:a", 0.0, 0.5).set_ease(Tween.EASE_IN)
	await exit_tween.finished
	
	# Return to Main_UI instead of quitting
	get_tree().change_scene_to_file("res://Scene/Main_UI.tscn")

# Hover effects
func _on_button_hover(button: Button):
	if is_transitioning or button.disabled:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(button, "scale", Vector2(1.05, 1.05), 0.15).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	button_tween.tween_property(button, "modulate", Color(1.1, 1.1, 1.1, 1.0), 0.15)

func _on_button_unhover(button: Button):
	if is_transitioning:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(button, "scale", Vector2.ONE, 0.2).set_ease(Tween.EASE_OUT)
	button_tween.tween_property(button, "modulate", Color.WHITE, 0.2)

func _exit_tree():
	if udp_socket:
		udp_socket.close()

func _detect_face_in_frame(image: Image):
	"""Detect face by analyzing the text and colors from MediaPipe output"""
	if is_processing_login:
		return
	
	# Get image data
	var width = image.get_width()
	var height = image.get_height()
	
	# Strategy 1: Look for bright GREEN text "FACE_DETECTED" in top-left corner
	# Strategy 2: Look for bright RED text "NO_FACE_DETECTED"
	# Strategy 3: Look for green MediaPipe bounding box lines
	
	var green_score = 0
	var red_score = 0
	
	# Check top-left corner (where text is drawn)
	# Sample area: 0-500 width, 0-60 height
	var text_width = min(500, width)
	var text_height = min(60, height)
	
	for y in range(10, text_height):
		for x in range(0, text_width):
			if x < width and y < height:
				var pixel = image.get_pixel(x, y)
				
				# Bright green (FACE_DETECTED text) - RGB(0, 255, 0)
				if pixel.g > 0.7 and pixel.r < 0.3 and pixel.b < 0.3:
					green_score += 1
				
				# Bright red (NO_FACE_DETECTED text) - RGB(255, 0, 0)
				if pixel.r > 0.7 and pixel.g < 0.3 and pixel.b < 0.3:
					red_score += 1
	
	# Also check for green bounding box lines (MediaPipe detection)
	var bbox_green = 0
	var sample_step = 15
	for y in range(text_height, height, sample_step):
		for x in range(0, width, sample_step):
			if x < width and y < height:
				var pixel = image.get_pixel(x, y)
				# Green lines from MediaPipe
				if pixel.g > 0.6 and pixel.g > pixel.r * 1.3 and pixel.g > pixel.b * 1.3:
					bbox_green += 1
	
	# Decision logic:
	# - If we see significant green text OR green bbox, face is detected
	# - If we see red text, no face
	# - Green text needs to be substantial (at least 50 pixels)
	var has_face = (green_score >= 50 or bbox_green >= 10) and red_score < green_score
	
	# Debug info (optional, remove in production)
	if face_detected_frames % 30 == 0:  # Print every 30 frames
		print("Detection scores - Green: %d, Red: %d, BBox: %d, Has Face: %s" % [green_score, red_score, bbox_green, has_face])
	
	# Update face detection counter
	if has_face:
		face_detected_frames += 1
		var progress = int((float(face_detected_frames) / float(required_frames)) * 100)
		_update_status("👤 Wajah Terdeteksi: %d%%" % progress, Color.YELLOW)
		
		# Enable login button at 50% progress
		if progress >= 50 and login_button.disabled and not login_successful:
			_update_status("👤 Wajah Terdeteksi: %d%% - Hampir selesai!" % progress, Color.CYAN)
		
		# Login successful after required frames
		if face_detected_frames >= required_frames:
			is_processing_login = true
			_on_login_success()
	else:
		# Reset counter if face not detected
		if face_detected_frames > 0:
			face_detected_frames = max(0, face_detected_frames - 3)  # Faster decay
			if face_detected_frames == 0:
				_update_status("📸 Silahkan tunjukkan wajah Anda ke kamera", Color.ORANGE)
		else:
			# Show instruction when no face detected at all
			if not login_successful and receiving_video:
				_update_status("📸 Silahkan tunjukkan wajah Anda ke kamera", Color.ORANGE)

func _proceed_to_next_scene():
	"""Transition to the next scene after successful login"""
	if is_transitioning:
		return
	
	is_transitioning = true
	_update_status("🚀 Loading...", Color.CYAN)
	
	# Transition animation
	await get_tree().create_timer(0.5).timeout
	
	var exit_tween = create_tween()
	exit_tween.set_parallel(true)
	exit_tween.tween_property(self, "modulate:a", 0.0, 0.6).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUART)
	
	await exit_tween.finished
	
	# Change to WorldEnv scene (the game)
	var result = get_tree().change_scene_to_file("res://Scene/WorldEnv.tscn")
	if result != OK:
		print("Failed to load WorldEnv scene")
		is_transitioning = false
