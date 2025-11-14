extends Control

@onready var btn_login = $BtnLogin
@onready var btn_exit = $BtnExit
@onready var sprite = $Sprite2D
@onready var color_rect2 = $ColorRect2
@onready var color_rect3 = $ColorRect3

var is_transitioning = false
var entrance_tween: Tween
var button_tween: Tween

func _ready():
	# Set initial states for animation
	modulate.a = 0.0
	btn_login.scale = Vector2.ZERO
	btn_login.modulate.a = 0.0
	btn_exit.scale = Vector2.ZERO
	btn_exit.modulate.a = 0.0
	# Keep background sprite as is - don't change it
	
	# Connect hover signals if not already connected
	if not btn_login.mouse_entered.is_connected(_on_btn_login_mouse_entered):
		btn_login.mouse_entered.connect(_on_btn_login_mouse_entered)
	if not btn_login.mouse_exited.is_connected(_on_btn_login_mouse_exited):
		btn_login.mouse_exited.connect(_on_btn_login_mouse_exited)
	if not btn_exit.mouse_entered.is_connected(_on_btn_exit_mouse_entered):
		btn_exit.mouse_entered.connect(_on_btn_exit_mouse_entered)
	if not btn_exit.mouse_exited.is_connected(_on_btn_exit_mouse_exited):
		btn_exit.mouse_exited.connect(_on_btn_exit_mouse_exited)
	
	# Small delay then start entrance animation
	await get_tree().process_frame
	animate_entrance()

func animate_entrance():
	# Kill any existing tweens
	if entrance_tween:
		entrance_tween.kill()
	
	entrance_tween = create_tween()
	entrance_tween.set_parallel(true)
	
	# Fade in the whole UI only (don't touch background sprite)
	entrance_tween.tween_property(self, "modulate:a", 1.0, 1.0).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	
	# Wait a bit then animate buttons
	await get_tree().create_timer(0.4).timeout
	
	# Animate buttons with staggered entrance
	var btn_entrance = create_tween()
	btn_entrance.set_parallel(false)
	
	# Login button first
	var login_tween = create_tween()
	login_tween.set_parallel(true)
	login_tween.tween_property(btn_login, "scale", Vector2.ONE, 0.8).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK).set_delay(0.0)
	login_tween.tween_property(btn_login, "modulate:a", 1.0, 0.6).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	
	await get_tree().create_timer(0.2).timeout
	
	# Exit button second
	var exit_tween = create_tween()
	exit_tween.set_parallel(true)
	exit_tween.tween_property(btn_exit, "scale", Vector2.ONE, 0.8).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	exit_tween.tween_property(btn_exit, "modulate:a", 1.0, 0.6).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)

func _on_BtnTryOn_pressed():
	if is_transitioning:
		return
	is_transitioning = true
	
	# Kill any existing tweens
	if button_tween:
		button_tween.kill()
	
	# Immediate button feedback with smooth scale
	var press_tween = create_tween()
	press_tween.set_parallel(true)
	press_tween.tween_property(btn_login, "scale", Vector2(0.95, 0.95), 0.08).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	press_tween.tween_property(btn_login, "modulate", Color(0.8, 0.8, 0.8, 1.0), 0.08)
	
	await press_tween.finished
	
	# Smooth exit animation
	var exit_tween = create_tween()
	exit_tween.set_parallel(true)
	
	# Fade out everything smoothly
	exit_tween.tween_property(self, "modulate:a", 0.0, 0.6).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUART)
	exit_tween.tween_property(btn_login, "scale", Vector2(0.8, 0.8), 0.6).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_BACK)
	exit_tween.tween_property(btn_exit, "scale", Vector2(0.8, 0.8), 0.6).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_BACK)
	
	await exit_tween.finished
	
	var result = get_tree().change_scene_to_file("res://Scene/Login.tscn")
	if result != OK:
		print("Scene Tidak Ada")
		is_transitioning = false

func _on_BtnExit_pressed():
	if is_transitioning:
		return
	is_transitioning = true
	
	# Kill any existing tweens
	if button_tween:
		button_tween.kill()
	
	# Immediate button feedback
	var press_tween = create_tween()
	press_tween.set_parallel(true)
	press_tween.tween_property(btn_exit, "scale", Vector2(0.95, 0.95), 0.08).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	press_tween.tween_property(btn_exit, "modulate", Color(0.8, 0.8, 0.8, 1.0), 0.08)
	
	await press_tween.finished
	
	# Smooth exit animation before quit
	var exit_tween = create_tween()
	exit_tween.set_parallel(true)
	exit_tween.tween_property(self, "modulate:a", 0.0, 0.6).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUART)
	
	await exit_tween.finished
	get_tree().quit()

# Smooth button hover effects
func _on_btn_login_mouse_entered():
	if is_transitioning:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(btn_login, "scale", Vector2(1.05, 1.05), 0.15).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	button_tween.tween_property(btn_login, "modulate", Color(1.1, 1.1, 1.1, 1.0), 0.15).set_ease(Tween.EASE_OUT)

func _on_btn_login_mouse_exited():
	if is_transitioning:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(btn_login, "scale", Vector2.ONE, 0.2).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	button_tween.tween_property(btn_login, "modulate", Color.WHITE, 0.2).set_ease(Tween.EASE_OUT)

func _on_btn_exit_mouse_entered():
	if is_transitioning:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(btn_exit, "scale", Vector2(1.05, 1.05), 0.15).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	button_tween.tween_property(btn_exit, "modulate", Color(1.1, 1.1, 1.1, 1.0), 0.15).set_ease(Tween.EASE_OUT)

func _on_btn_exit_mouse_exited():
	if is_transitioning:
		return
	if button_tween:
		button_tween.kill()
	button_tween = create_tween()
	button_tween.set_parallel(true)
	button_tween.tween_property(btn_exit, "scale", Vector2.ONE, 0.2).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUART)
	button_tween.tween_property(btn_exit, "modulate", Color.WHITE, 0.2).set_ease(Tween.EASE_OUT)
