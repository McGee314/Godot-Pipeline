extends CharacterBody3D

# Drone movement parameters
@export var fly_speed: float = 5.0
@export var down_speed: float = 3.0
@export var horizontal_speed: float = 8.0
@export var horizontal_speed_boost: float = 50.0 # Speed when holding Shift
@export var acceleration: float = 7.0
@export var deceleration: float = 7.0
@export var rotation_speed: float = 2.5

# Minimum height to allow horizontal movement
@export var min_flight_height: float = 1.0

# Gravity
@export var gravity: float = 9.8
@export var hover_force: float = 10.0

# State
var is_flying: bool = false
var current_height: float = 0.0
var target_velocity: Vector3 = Vector3.ZERO

func _ready():
	# Initialize position
	current_height = global_position.y

func _physics_process(delta: float):
	# Check current height
	current_height = global_position.y
	
	# Handle vertical movement
	if Input.is_action_pressed("Up"):
		velocity.y = fly_speed
		is_flying = true
	elif Input.is_action_pressed("Down"):
		velocity.y = -down_speed
	else:
		# Apply slight gravity when not pressing up
		if is_flying:
			velocity.y = -gravity * 0.3 * delta
		else:
			velocity.y = -gravity * delta
	
	# Check if drone is high enough to fly
	if current_height >= min_flight_height:
		is_flying = true
	else:
		is_flying = false
	
	# Handle rotation
	if Input.is_action_pressed("Rotate_Left"):
		rotation.y += rotation_speed * delta
	if Input.is_action_pressed("Rotate_Right"):
		rotation.y -= rotation_speed * delta
	
	# Handle horizontal movement only if flying
	var input_dir := Vector3.ZERO
	
	if is_flying:
		# Get input direction
		if Input.is_action_pressed("Forward"):
			input_dir.x += 1  # Inverted
		if Input.is_action_pressed("Backward"):
			input_dir.x -= 1  # Inverted
		if Input.is_action_pressed("Left"):
			input_dir.z -= 1  # Inverted
		if Input.is_action_pressed("Right"):
			input_dir.z += 1  # Inverted
		
		# Normalize input direction
		if input_dir.length() > 0:
			input_dir = input_dir.normalized()
	
	# Transform input direction to drone's local space (relative to rotation)
	var direction := transform.basis * input_dir
	direction.y = 0  # Keep movement horizontal
	
	# Check if boost is active
	var current_speed := horizontal_speed
	if Input.is_action_pressed("Faster"):
		current_speed = horizontal_speed_boost
	
	# Apply acceleration/deceleration
	if direction.length() > 0 and is_flying:
		target_velocity.x = direction.x * current_speed
		target_velocity.z = direction.z * current_speed
	else:
		target_velocity.x = 0
		target_velocity.z = 0
	
	# Smoothly interpolate to target velocity
	if target_velocity.length() > 0:
		velocity.x = lerp(velocity.x, target_velocity.x, acceleration * delta)
		velocity.z = lerp(velocity.z, target_velocity.z, acceleration * delta)
	else:
		velocity.x = lerp(velocity.x, 0.0, deceleration * delta)
		velocity.z = lerp(velocity.z, 0.0, deceleration * delta)
	
	# Apply movement
	move_and_slide()
	
	# Prevent drone from going below ground
	if global_position.y < 0:
		global_position.y = 0
		velocity.y = 0

func _process(_delta: float):
	# Optional: Add visual feedback for flight status
	if is_flying:
		# Drone is ready to move
		pass
	else:
		# Drone needs to gain altitude
		pass
