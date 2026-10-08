extends SceneTree
func _initialize() -> void:
	var model: Node3D = load("res://scenes/model_wrapper.tscn").instantiate()
	var rows: Array[Dictionary] = []
	var total := 0
	for child in model.get_children():
		if child is MeshInstance3D:
			var triangles: int = child.mesh.get_faces().size() / 3
			total += triangles
			rows.append({"node": child.name, "triangles": triangles, "surfaces": child.mesh.get_surface_count(), "scale": str(child.scale)})
	var file := FileAccess.open("res://docs/model_metrics.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "PROVISIONAL - not an AI model or authorized practice resource", "triangles": total, "materials": 2, "textures": 0, "height_m": 1.8, "skeleton": false, "parts": rows}, "\t"))
	print("Provisional mesh triangles: ", total)
	model.free()
	quit()
