extends CanvasLayer
@onready var player: CharacterBody3D = get_parent().get_node("Player")
func _process(_delta: float) -> void:
	$Panel/Label.text = "LABORATORIO 3D / TAREA 1\nEstado: %s    |    Suelo: %s\nWASD / flechas: mover   Espacio: saltar\nRatón: cámara   Esc: liberar   Clic: capturar\nF1: límite 30 / 144 FPS   R: reiniciar\nFPS: %d    |    Límite: %d\nModelo provisional: pendiente Tripo / Meshy" % [player.State.keys()[player.state], player.is_on_floor(), Engine.get_frames_per_second(), Engine.max_fps]
