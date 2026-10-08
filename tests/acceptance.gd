extends SceneTree
var player: CharacterBody3D
var results: Array[Dictionary] = []
var level: Node3D
var capture := false

func _initialize() -> void:
	call_deferred("run")

func check(label: String, passed: bool, detail: String) -> void:
	results.append({"test": label, "passed": passed, "detail": detail})
	print("%s: %s | %s" % ["PASS" if passed else "FAIL", label, detail])

func tick(axis := Vector2.ZERO, jump := false) -> void:
	await physics_frame
	player.step(1.0 / 60.0, axis, jump)

func settle(pos: Vector3) -> void:
	player.global_position = pos
	player.velocity = Vector3.ZERO
	player.pivot.rotation.y = 0.0
	for i in 30:
		await tick()

func screenshot(name: String) -> void:
	if not capture:
		return
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://docs/captures/%s.png" % name)

func run() -> void:
	capture = "--capture" in OS.get_cmdline_user_args()
	DirAccess.make_dir_recursive_absolute("res://docs/captures")
	level = load("res://scenes/level.tscn").instantiate()
	player = level.get_node("Player")
	player.test_mode = true
	root.add_child(level)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await settle(Vector3(0, 0.1, 5))
	check("Suelo e Idle", player.is_on_floor() and player.state == player.State.IDLE, str(player.global_position))
	await screenshot("01_idle")
	await tick(Vector2.ZERO, true)
	check("Jump al despegar", player.state == player.State.JUMP and player.velocity.y > 0, str(player.velocity.y))
	for i in 12:
		await tick()
	await screenshot("02_jump")
	var before := player.velocity.y
	await tick(Vector2.ZERO, true)
	check("Sin doble salto", player.velocity.y < before, "vy antes %.4f / después %.4f" % [before, player.velocity.y])
	for i in 80:
		await tick()
	check("Aterrizaje a Idle", player.is_on_floor() and player.state == player.State.IDLE, str(player.global_position))
	await settle(Vector3(0, 0.1, 5))
	for i in 20:
		await tick(Vector2(0, -1))
	check("Walk", player.state == player.State.WALK, str(player.global_position))
	await screenshot("03_walk")
	for i in 30:
		await tick()
	check("Walk a Idle", player.state == player.State.IDLE, str(player.velocity))
	var distances: Array[float] = []
	for cap in [30, 144]:
		Engine.max_fps = cap
		await settle(Vector3(0, 0.1, 8))
		var start := player.global_position
		for i in 120:
			await tick(Vector2(0, -1))
		distances.append(start.distance_to(player.global_position))
		check("Desplazamiento %d FPS" % cap, absf(distances[-1] - 9.52) < 0.15, "120 ticks (2 s): %.6f m" % distances[-1])
	check("Comparación 30/144", absf(distances[0] - distances[1]) < 0.01, "Diferencia %.8f m" % absf(distances[0] - distances[1]))
	await settle(Vector3(0, 0.1, 5))
	player.pivot.rotation.y = PI / 2.0
	await process_frame
	var start := player.global_position
	for i in 30:
		await tick(Vector2(0, -1))
	var change := player.global_position - start
	check("Movimiento relativo a cámara 90 grados", change.x < -1.5 and absf(change.z) < 0.05, str(change))
	await settle(Vector3(3, 0.1, 1.8))
	for i in 150:
		await tick(Vector2(0, -1))
	check("Colisión con bloque", player.global_position.z > 1.3 and player.global_position.z < 1.5, str(player.global_position))
	await settle(Vector3(-8, 0.1, -8))
	for i in 150:
		await tick(Vector2(-1, -1).normalized())
	check("Esquina sin atravesar paredes", player.global_position.x > -9.5 and player.global_position.z > -9.5, str(player.global_position))
	await settle(Vector3(0, 0.1, -8))
	player.pivot.rotation.y = PI
	for i in 10:
		await tick()
	check("SpringArm ante pared", player.arm.get_hit_length() < 2.0 and player.arm.get_hit_length() > 0.0, "Longitud %.4f m" % player.arm.get_hit_length())
	await screenshot("04_camera_wall")
	# Sweep around a corner. Check every segment from pivot to camera against world.
	await settle(Vector3(-8, 0.1, -8))
	var clear := true
	for i in 72:
		player.pivot.rotation.y = TAU * float(i) / 72.0
		await tick()
		await tick()
		var ray := PhysicsRayQueryParameters3D.create(player.pivot.global_position, player.camera.global_position, 1)
		if not player.get_world_3d().direct_space_state.intersect_ray(ray).is_empty():
			clear = false
	check("Giro 360 grados junto a esquina", clear, "72 ángulos, rayos pivot-cámara sin intersección")
	var file := FileAccess.open("res://docs/test_results.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info().string, "physics_hz": 60, "rendered": capture, "results": results}, "\t"))
	var failed := results.any(func(item): return not item.passed)
	quit(1 if failed else 0)
