extends CharacterBody3D
## Physics owns velocity/collision/FSM; _process owns appearance only.
enum State { IDLE, WALK, JUMP }
signal state_changed(previous: State, current: State)
@export var speed: float = 5.0
@export var acceleration: float = 24.0
@export var jump_speed: float = 7.0
@export var gravity: float = 20.0
@export var mouse_sensitivity: float = 0.003
var state: State = State.IDLE
var test_mode: bool = false
var facing: float = 0.0
@onready var visual: Node3D = $Visual
@onready var pivot: Node3D = $CameraPivot
@onready var arm: SpringArm3D = $CameraPivot/SpringArm3D
@onready var camera: Camera3D = $CameraPivot/SpringArm3D/Camera3D

func _ready() -> void:
	arm.add_excluded_object(get_rid())
	if not test_mode:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		# Mouse displacement is already an amount, so no delta here.
		pivot.rotation.y -= event.relative.x * mouse_sensitivity
		arm.rotation.x = clampf(arm.rotation.x - event.relative.y * mouse_sensitivity, -1.1, 0.25)
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		if event.keycode == KEY_F1:
			Engine.max_fps = 30 if Engine.max_fps != 30 else 144
		if event.keycode == KEY_R:
			global_position = Vector3(0, 0.1, 5)
			velocity = Vector3.ZERO
	if event is InputEventMouseButton and event.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _physics_process(delta: float) -> void:
	if not test_mode:
		step(delta, Input.get_vector("move_left", "move_right", "move_forward", "move_back"), Input.is_action_just_pressed("jump"))

func step(delta: float, input_axis: Vector2, jump_requested: bool) -> void:
	# Flatten camera orientation: looking up/down never changes horizontal speed.
	var right := camera.global_basis.x
	var back := camera.global_basis.z
	right.y = 0.0
	back.y = 0.0
	var direction := right.normalized() * input_axis.x + back.normalized() * input_axis.y
	if direction.length_squared() > 1.0:
		direction = direction.normalized()
	velocity.x = move_toward(velocity.x, direction.x * speed, acceleration * delta)
	velocity.z = move_toward(velocity.z, direction.z * speed, acceleration * delta)
	if not is_on_floor():
		velocity.y -= gravity * delta
	elif jump_requested:
		velocity.y = jump_speed # impulse in m/s; no delta
	else:
		velocity.y = 0.0
	# move_and_slide integrates velocity using the physics timestep internally.
	move_and_slide()
	if direction.length_squared() > 0.001:
		facing = atan2(direction.x, direction.z)
	var next_state: State = State.JUMP
	if is_on_floor():
		next_state = State.WALK if Vector2(velocity.x, velocity.z).length() > 0.1 else State.IDLE
	transition_to(next_state)
	if global_position.y < -12.0:
		global_position = Vector3(0, 0.1, 5)
		velocity = Vector3.ZERO

func transition_to(next_state: State) -> void:
	if next_state == state:
		return
	var previous := state
	state = next_state
	state_changed.emit(previous, state)
	print("FSM: %s -> %s" % [State.keys()[previous], State.keys()[state]])

func _process(delta: float) -> void:
	visual.rotation.y = lerp_angle(visual.rotation.y, facing, 1.0 - exp(-12.0 * delta))
