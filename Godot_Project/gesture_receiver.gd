extends Node

# UDP Configuration
var udp := PacketPeerUDP.new()
var listen_port := 9999  # Port untuk menerima gesture dari Python
var is_listening := false

# Gesture state
var current_gesture := "NO_HAND"
var last_gesture_time := 0.0

# Reference to the object to control (e.g., drone)
@export var controlled_object: Node3D

# Movement settings
@export var move_speed := 5.0  # Speed of movement
@export var smooth_movement := true
@export var movement_scale := 1.0  # Scale for movement amount

# Debug
@export var show_debug := true

func _ready():
	print("🎮 Gesture Receiver Initialized")
	
	# Start listening for UDP gestures
	var err = udp.bind(listen_port)
	if err != OK:
		push_error("❌ Failed to bind UDP port %d: %s" % [listen_port, error_string(err)])
		is_listening = false
	else:
		print("✅ Listening for gestures on UDP port: ", listen_port)
		is_listening = true
	
	# Find controlled object if not set
	if not controlled_object:
		# Try to find the drone or any child with "Sketchfab_Scene" name
		controlled_object = get_node_or_null("../Sketchfab_Scene")
		if controlled_object:
			print("✅ Auto-detected controlled object: ", controlled_object.name)
		else:
			push_warning("⚠️ No controlled object set. Please assign in inspector.")

func _process(delta):
	if not is_listening:
		return
	
	# Check for incoming packets
	while udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var message = packet.get_string_from_utf8()
		
		# Parse JSON
		var json = JSON.new()
		var error = json.parse(message)
		
		if error == OK:
			var data = json.data
			if typeof(data) == TYPE_DICTIONARY and data.has("type") and data["type"] == "gesture":
				handle_gesture(data["gesture"])
		else:
			if show_debug:
				print("⚠️ Failed to parse JSON: ", message)

func handle_gesture(gesture: String):
	"""Handle incoming gesture and move the controlled object"""
	if not controlled_object:
		return
	
	current_gesture = gesture
	last_gesture_time = Time.get_ticks_msec() / 1000.0
	
	if show_debug and gesture != "CENTER" and gesture != "NO_HAND":
		print("👋 Gesture received: ", gesture)
	
	# Calculate movement vector based on gesture
	var movement := Vector3.ZERO
	
	match gesture:
		"UP":
			movement = Vector3(0, 0, -1) * move_speed * movement_scale
		"DOWN":
			movement = Vector3(0, 0, 1) * move_speed * movement_scale
		"LEFT":
			movement = Vector3(-1, 0, 0) * move_speed * movement_scale
		"RIGHT":
			movement = Vector3(1, 0, 0) * move_speed * movement_scale
		"CENTER", "NO_HAND":
			movement = Vector3.ZERO
	
	# Apply movement
	if movement != Vector3.ZERO:
		if smooth_movement:
			# Smooth movement using delta
			controlled_object.global_position += movement * get_process_delta_time()
		else:
			# Instant movement (step-based)
			controlled_object.global_position += movement * 0.1

func _notification(what):
	if what == NOTIFICATION_PREDELETE:
		# Cleanup UDP socket
		if udp:
			udp.close()
		print("👋 Gesture Receiver closed")

# Helper functions for external control
func get_current_gesture() -> String:
	return current_gesture

func set_controlled_object(obj: Node3D):
	controlled_object = obj
	print("✅ Controlled object set to: ", obj.name if obj else "null")

func set_move_speed(speed: float):
	move_speed = speed

func get_time_since_last_gesture() -> float:
	return (Time.get_ticks_msec() / 1000.0) - last_gesture_time
