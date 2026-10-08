from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
def write(name, text):
    p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
config='''config_version=5
[application]
config/name="Proyecto I - Laboratorio 3D"
run/main_scene="res://scenes/level.tscn"
config/features=PackedStringArray("4.7", "GL Compatibility")
config/icon="res://icon.svg"
[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
[physics]
common/physics_ticks_per_second=60
3d/physics_engine="GodotPhysics3D"
[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
environment/defaults/default_clear_color=Color(0.05, 0.08, 0.12, 1)
[input]
'''
for action, codes in {'move_left':[65,4194321],'move_right':[68,4194323],'move_forward':[87,4194320],'move_back':[83,4194322],'jump':[32]}.items():
    events=','.join('Object(InputEventKey,"physical_keycode":%d)'%c for c in codes)
    config+=f'{action}={{"deadzone":0.2,"events":[{events}]}}\n'
write('project.godot',config)
write('scenes/model_wrapper.tscn','''[gd_scene load_steps=6 format=3]
[sub_resource type="StandardMaterial3D" id="BodyMat"]
albedo_color = Color(0.08, 0.72, 0.7, 1)
roughness = 0.65
[sub_resource type="StandardMaterial3D" id="FaceMat"]
albedo_color = Color(0.03, 0.07, 0.11, 1)
[sub_resource type="CapsuleMesh" id="Body"]
material = SubResource("BodyMat")
radius = 0.32
height = 1.2
[sub_resource type="SphereMesh" id="Head"]
material = SubResource("BodyMat")
radius = 0.3
height = 0.6
[sub_resource type="BoxMesh" id="Face"]
material = SubResource("FaceMat")
size = Vector3(0.38, 0.12, 0.08)
[node name="ModelWrapper" type="Node3D"]
[node name="PlaceholderBody" type="MeshInstance3D" parent="."]
position = Vector3(0, 0.65, 0)
mesh = SubResource("Body")
[node name="PlaceholderHead" type="MeshInstance3D" parent="."]
position = Vector3(0, 1.5, 0)
mesh = SubResource("Head")
[node name="Visor" type="MeshInstance3D" parent="."]
position = Vector3(0, 1.52, 0.28)
mesh = SubResource("Face")
''')
write('scenes/player.tscn','''[gd_scene load_steps=5 format=3]
[ext_resource type="Script" path="res://scripts/player.gd" id="1"]
[ext_resource type="PackedScene" path="res://scenes/model_wrapper.tscn" id="2"]
[sub_resource type="CapsuleShape3D" id="Capsule"]
radius = 0.35
height = 1.8
[sub_resource type="SphereShape3D" id="CameraShape"]
radius = 0.2
[node name="Player" type="CharacterBody3D"]
collision_layer = 2
collision_mask = 1
floor_snap_length = 0.25
script = ExtResource("1")
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
position = Vector3(0, 0.9, 0)
shape = SubResource("Capsule")
[node name="Visual" type="Node3D" parent="."]
[node name="ModelWrapper" parent="Visual" instance=ExtResource("2")]
[node name="CameraPivot" type="Node3D" parent="."]
position = Vector3(0, 1.4, 0)
[node name="SpringArm3D" type="SpringArm3D" parent="CameraPivot"]
rotation = Vector3(-0.3, 0, 0)
spring_length = 5.0
margin = 0.15
collision_mask = 1
shape = SubResource("CameraShape")
[node name="Camera3D" type="Camera3D" parent="CameraPivot/SpringArm3D"]
current = true
fov = 65.0
near = 0.05
''')
boxes=[('Ground',(0,-0.5,0),(32,1,32),(0.19,0.26,0.31)),('NorthWall',(0,2,-10),(22,4,0.5),(0.32,0.4,0.51)),('WestWall',(-10,2,0),(0.5,4,20),(0.32,0.4,0.51)),('BlockA',(3,0.75,0),(2,1.5,2),(0.96,0.53,0.16)),('BlockB',(-3,1,0),(2,2,2),(0.96,0.53,0.16)),('Step',(3,0.25,3),(2,0.5,2),(0.8,0.65,0.3)),('Corner',(6,1.5,-5),(0.5,3,6),(0.42,0.49,0.61))]
scene='''[gd_scene load_steps=%d format=3]
[ext_resource type="PackedScene" path="res://scenes/player.tscn" id="1"]
[ext_resource type="Script" path="res://scripts/hud.gd" id="2"]
[sub_resource type="ProceduralSkyMaterial" id="SkyMat"]
sky_top_color = Color(0.12, 0.3, 0.52, 1)
sky_horizon_color = Color(0.7, 0.8, 0.86, 1)
[sub_resource type="Sky" id="Sky"]
sky_material = SubResource("SkyMat")
[sub_resource type="Environment" id="Env"]
background_mode = 2
sky = SubResource("Sky")
ambient_light_source = 3
ambient_light_color = Color(0.7, 0.8, 1, 1)
ambient_light_energy = 0.5
tonemap_mode = 2
'''%(6+len(boxes)*3)
for name,pos,size,color in boxes:
    v=', '.join(map(str,size)); c=', '.join(map(str,color))
    scene+=f'''[sub_resource type="StandardMaterial3D" id="{name}Mat"]
albedo_color = Color({c}, 1)
roughness = 0.85
[sub_resource type="BoxMesh" id="{name}Mesh"]
material = SubResource("{name}Mat")
size = Vector3({v})
[sub_resource type="BoxShape3D" id="{name}Shape"]
size = Vector3({v})
'''
scene+='''[node name="Level" type="Node3D"]
[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Env")
[node name="Sun" type="DirectionalLight3D" parent="."]
rotation = Vector3(-0.9, -0.55, 0)
light_energy = 0.8
shadow_enabled = true
[node name="Player" parent="." instance=ExtResource("1")]
position = Vector3(0, 0.1, 5)
'''
for name,pos,size,color in boxes:
    scene+=f'''[node name="{name}" type="StaticBody3D" parent="."]
position = Vector3({', '.join(map(str,pos))})
collision_layer = 1
collision_mask = 2
[node name="Mesh" type="MeshInstance3D" parent="{name}"]
mesh = SubResource("{name}Mesh")
[node name="Collision" type="CollisionShape3D" parent="{name}"]
shape = SubResource("{name}Shape")
'''
scene+='''[node name="HUD" type="CanvasLayer" parent="."]
script = ExtResource("2")
[node name="Panel" type="Panel" parent="HUD"]
offset_left = 20.0
offset_top = 20.0
offset_right = 590.0
offset_bottom = 260.0
[node name="Label" type="Label" parent="HUD/Panel"]
offset_left = 16.0
offset_top = 12.0
offset_right = 560.0
offset_bottom = 240.0
theme_override_font_sizes/font_size = 20
'''
write('scenes/level.tscn',scene)
print('Scenes and input map created.')
