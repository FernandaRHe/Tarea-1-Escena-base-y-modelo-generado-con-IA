extends SceneTree
var player: CharacterBody3D
var tick_count := 0
var caption: Label
func _initialize() -> void:
	call_deferred("setup")
func setup() -> void:
	var level: Node3D = load("res://scenes/level.tscn").instantiate()
	player = level.get_node("Player")
	player.test_mode = true
	root.add_child(level)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	caption = Label.new()
	caption.position = Vector2(30, 640)
	caption.add_theme_font_size_override("font_size", 25)
	caption.add_theme_color_override("font_shadow_color", Color.BLACK)
	caption.add_theme_constant_override("shadow_offset_x", 2)
	caption.add_theme_constant_override("shadow_offset_y", 2)
	level.get_node("HUD").add_child(caption)
func reset_at(pos: Vector3, yaw := 0.0) -> void:
	player.global_position = pos
	player.velocity = Vector3.ZERO
	player.pivot.rotation.y = yaw
func _physics_process(delta: float) -> bool:
	if not is_instance_valid(player):
		return false
	tick_count += 1
	var t := float(tick_count) / 60.0
	var axis := Vector2.ZERO
	var jump := false
	if t < 8:
		caption.text = "01 / Escena editable: suelo, obstáculos, cielo y sombras. Idle."
	elif t < 18:
		caption.text = "02 / Walk y frenado: movimiento en el plano de la cámara."
		if t < 10 or (t > 13 and t < 15):
			axis = Vector2(0, -1) if t < 10 else Vector2(0, 1)
	elif t < 28:
		caption.text = "03 / Jump: salto desde el suelo; el segundo impulso se rechaza."
		jump = tick_count in [1110, 1125, 1350, 1365]
	elif t < 38:
		if tick_count == 1680:
			reset_at(Vector3(3, 0.1, 1.8))
		caption.text = "04 / Colisión: avance sostenido contra el bloque sin atravesarlo."
		if t > 29 and t < 36:
			axis = Vector2(0, -1)
	elif t < 50:
		if tick_count == 2280:
			reset_at(Vector3(-8, 0.1, -8))
		caption.text = "05 / Cámara: giro junto a paredes; SpringArm acorta la distancia."
		player.pivot.rotation.y = (t - 38) * TAU / 12
	elif t < 60:
		if tick_count == 3000:
			reset_at(Vector3(0, 0.1, 5), PI / 2)
		caption.text = "06 / Cámara a 90°: W mueve al personaje hacia la izquierda del mundo."
		if t > 51 and t < 52:
			axis = Vector2(0, -1)
	else:
		caption.text = "Base técnica verificada. Modelo IA y enlaces públicos pendientes."
	player.step(delta, axis, jump)
	if t >= 65:
		quit()
	return false
