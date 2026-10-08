from pathlib import Path
import json, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
C=canvas.Canvas(str(OUT/'informe-tarea-1.pdf'),pagesize=(595,842))
C.setTitle('Tarea 1 - Escena base 3D | Informe técnico provisional')
C.setAuthor('Proyecto individual - base con asistencia de Codex')
ink=HexColor('#183349'); teal=HexColor('#007F83'); muted=HexColor('#526575')
def page(n,title,subtitle):
    C.setFillColor(ink); C.rect(0,752,595,90,fill=1,stroke=0)
    C.setFillColor(HexColor('#61DBD2')); C.setFont('Helvetica-Bold',10); C.drawString(38,811,'PROYECTO I  /  GODOT 4.7.2  /  06 OCT 2026')
    C.setFillColor(white); C.setFont('Helvetica-Bold',22); C.drawString(38,781,title)
    C.setFillColor(muted); C.setFont('Helvetica',10); C.drawString(38,730,subtitle)
    C.setStrokeColor(HexColor('#DCE5EA')); C.line(38,42,557,42)
    C.setFillColor(muted); C.setFont('Helvetica',9); C.drawString(38,26,'Tarea 1 - Base técnica; integración del modelo IA pendiente')
    C.drawRightString(557,26,f'{n} / 5')
def heading(text,y):
    C.setFillColor(teal); C.setFont('Helvetica-Bold',14); C.drawString(38,y,text)
def para(text,y,width=519,size=11):
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    p=Paragraph(text,ParagraphStyle('body',fontName='Helvetica',fontSize=size,leading=size*1.45,textColor=ink))
    _,h=p.wrap(width,700); p.drawOn(C,38,y-h); return y-h-24
def picture(file,y,w=480):
    h=w*720/1280
    C.drawImage(str(ROOT/'docs/captures'/file),38,y-h,width=w,height=h)
    return y-h
def link(label,target,y):
    C.setFillColor(teal); C.setFont('Helvetica',11); C.drawString(38,y,label)
    C.linkURL(target,(38,y-3,550,y+13),relative=1,thickness=0)

page(1,'Escena base y alcance','Informe provisional de una base ejecutable. Autor: completar con nombre y matrícula.')
heading('Entorno y escenas editables',700)
y=para('Nivel de 32 × 32 m, suelo y obstáculos StaticBody3D con BoxShape3D. Dos paredes forman una esquina; bloques y escalón permiten ensayar colisiones y saltos. WorldEnvironment usa cielo procedural; DirectionalLight3D proyecta sombras. El nivel y el personaje se guardan como escenas visibles en el editor 3D.',678)
heading('Estructura del proyecto',y); y-=24
for line in ['Level (scenes/level.tscn)','  WorldEnvironment + Sun + suelo y obstáculos','  Player (scenes/player.tscn)','    CollisionShape3D: cápsula física de 1.8 m','    Visual > ModelWrapper: apariencia sustituible','    CameraPivot > SpringArm3D > Camera3D','  HUD: estado, controles y límite FPS']:
    C.setFont('Courier',11); C.setFillColor(ink); C.drawString(46,y,line); y-=20
y-=12
heading('Controles',y); y=para('WASD o flechas: desplazamiento relativo a cámara. Espacio: salto desde el suelo. Ratón: giro e inclinación. Esc: liberar ratón; clic: capturarlo. F1 alterna límites 30/144 FPS. R reinicia posición.',y-22)
heading('Archivos para revisión',y)
link('Proyecto completo local: ZIP portable', '../proyecto-i-base.zip',y-27)
link('Video local: demostración automatizada de 65 segundos','../../docs/demostracion.mp4',y-49)
para('Los enlaces locales funcionan conservando la estructura de carpetas. Enlaces públicos de repositorio y video: pendientes de publicación. El tutorial y la integración de un modelo IA siguen pendientes; este documento no afirma que la entrega esté completa.',y-66,size=10)
C.showPage()

page(2,'Movimiento, física y cámara','El controlador conserva la lógica aunque se sustituya la apariencia.')
heading('Unidades y uso de delta',700)
y=para('La física se ejecuta a 60 Hz en _physics_process(delta). Se aplana la orientación de Camera3D al plano XZ; la dirección combina sus ejes derecho y posterior con Input.get_vector(). Se limita su longitud a 1 para evitar acelerar en diagonal.',678)
y=para('Velocidad objetivo: 5 m/s. Aceleración: 24 m/s²; move_toward usa aceleración × delta para cambiar velocidad. Gravedad: 20 m/s², aplicada a velocity.y con delta cuando no hay suelo. Salto: asignación de 7 m/s sólo con is_on_floor() y una pulsación nueva.',y)
y=para('<b>move_and_slide() integra velocity usando el paso de física.</b> No se multiplica la velocidad otra vez por delta. La gravedad convierte aceleración a cambio de velocidad, no directamente a posición. La posición y las colisiones se resuelven dentro de ese método.',y)
heading('Actualización visual independiente',y); y=para('_process(delta) suaviza solamente el giro de Visual con lerp_angle y factor 1 - exp(-12 × delta). El ratón aporta desplazamiento relativo: se multiplica por sensibilidad, sin delta. Ni el wrapper ni el modelo gobiernan el movimiento.',y-23)
heading('Seguimiento y obstáculos',y); y=para('CameraPivot es hijo del personaje y sigue su posición. SpringArm3D admite inclinación limitada entre -1.1 y 0.25 rad; su longitud nominal es 5 m. Usa SphereShape3D de radio 0.2 m, margen 0.15 m y máscara del entorno (capa 1). El personaje está en capa 2 y su RID se excluye.',y-23)
y=para('Las pruebas colocaron la cámara contra una pared: el brazo se redujo a 1.6211 m. En una esquina se ensayaron 72 ángulos sobre 360°, con dos pasos de física por ángulo; ningún rayo desde pivot hasta cámara atravesó el entorno. El modelo final debe volver a probarse visualmente.',y)
para('Referencia técnica: docs.godotengine.org/en/stable/classes/class_characterbody3d.html y class_springarm3d.html. No se utilizaron complementos de cámara.',y,size=9)
C.showPage()

page(3,'FSM: Idle, Walk y Jump','Las transiciones se deciden después de resolver el movimiento físico.')
heading('Transiciones explícitas',700)
for x,label in [(48,'IDLE'),(227,'WALK'),(406,'JUMP')]:
    C.setFillColor(teal); C.roundRect(x,609,140,48,8,fill=1,stroke=0)
    C.setFillColor(white); C.setFont('Helvetica-Bold',15); C.drawCentredString(x+70,627,label)
C.setStrokeColor(ink); C.setFillColor(ink)
C.line(189,646,225,646); C.line(225,646,218,650); C.line(225,646,218,642)
C.line(225,619,189,619); C.line(189,619,196,623); C.line(189,619,196,615)
C.setFont('Helvetica',8); C.drawString(191,668,'suelo + v > 0.1'); C.drawString(190,590,'suelo + v <= 0.1')
C.line(367,646,404,646); C.line(404,646,397,650); C.line(404,646,397,642)
C.setFont('Helvetica',8); C.drawString(370,668,'sin suelo')
C.line(404,619,368,619); C.line(368,619,375,623); C.line(368,619,375,615)
C.drawString(364,590,'suelo + v > 0.1')
C.line(95,609,95,564); C.line(95,564,460,564); C.line(460,564,460,609)
C.line(460,609,456,602); C.line(460,609,464,602)
C.drawString(246,570,'Idle -> Jump: sin suelo')
C.line(500,609,500,536); C.line(500,536,60,536); C.line(60,536,60,609)
C.line(60,609,56,602); C.line(60,609,64,602)
C.drawString(214,542,'Jump -> Idle: suelo + v <= 0.1')
y=para('Desde Idle o Walk: abandonar el suelo lleva a Jump. En Jump: aterrizar lleva a Walk si la velocidad horizontal supera 0.1 m/s; de lo contrario, Idle. No hay transición de salto adicional en el aire. Jump incluye ascenso y caída. El frenado puede mantener Walk unos pasos tras soltar controles.',512,size=10)
y=para('transition_to() evita eventos duplicados, guarda el estado anterior y emite state_changed. El HUD muestra estado y contacto con suelo; el registro imprime cada transición. No se requieren clips definitivos para evaluar esta FSM.',y)
heading('Captura 1 / Salto y rechazo de segundo impulso',y)
y=picture('02_jump.png',y-18,w=420)
para('Prueba real: vy = 7 m/s al despegar. Tras 12 pasos, 3 m/s; una segunda solicitud deja vy en 2.6667 m/s, resultado de la gravedad, sin renovar el salto. Después de aterrizar vuelve a Idle.',y-10,size=10)
C.showPage()

page(4,'Capturas de funcionamiento','Imágenes del viewport de Godot; corresponden a la batería automática.')
heading('Captura 2 / Idle y contacto con suelo',699)
y=picture('01_idle.png',681,w=450)
y=para('Suelo verdadero, velocidad horizontal nula y estado Idle. Apariencia turquesa provisional y sombras direccionales visibles.',y-8,size=10)
heading('Captura 3 / Movimiento y estado Walk',y)
y=picture('03_walk.png',y-18,w=450)
para('Tras 20 pasos de avance: posición Z = 3.813333 m y estado Walk. Al frenar durante 30 pasos vuelve a Idle. Captura adicional de pared en docs/captures/04_camera_wall.png.',y-8,size=10)
C.showPage()

page(5,'Pruebas y trazabilidad del modelo','14 comprobaciones automáticas aprobadas; el recurso final IA sigue pendiente.')
heading('Resumen de aceptación',700)
y=para('Suelo y Idle; Jump al despegar; rechazo de doble salto; aterrizaje; Walk y regreso a Idle; desplazamiento a dos límites de render; comparación entre límites; referencia de cámara a 90°; bloque; esquina; brazo contra pared y giro completo junto a esquina. Evidencia: docs/test_results.json.',678)
heading('Comparación de tiempo',y)
C.setFillColor(HexColor('#EDF5F5')); C.rect(38,y-94,519,70,fill=1,stroke=0)
C.setFillColor(ink); C.setFont('Helvetica-Bold',11)
C.drawString(50,y-43,'Límite de render'); C.drawString(245,y-43,'Física'); C.drawString(370,y-43,'Desplazamiento')
C.setFont('Helvetica',11)
for row,(cap,dist) in enumerate([('30 FPS','9.520004 m'),('144 FPS','9.520004 m')]):
    yy=y-64-row*18; C.drawString(50,yy,cap); C.drawString(245,yy,'120 pasos / 2 s'); C.drawString(370,yy,dist)
y=para('Diferencia: 0 m. Se usa el mismo controlador, desde reposo y sin obstáculos. La aceleración explica recorrer menos de 10 m. Son límites de render, no garantía de FPS alcanzados. En un ensayo humano influyen instante de pulsación y número de pasos. Física de 60 Hz independiente del render.',y-106,size=10)
heading('Ficha provisional y procedencia',y)
metrics=json.loads((ROOT/'docs/model_metrics.json').read_text())
y=para(f'Robot con tres primitivas Godot: {metrics["triangles"]:,} triángulos, 2 materiales, 0 texturas, altura 1.8 m, escala (1,1,1), frente +Z. Sin rig ni clips. Escala y materiales visibles; apariencia separada de lógica. No es un modelo generado en Tripo/Meshy ni un recurso de práctica autorizado.',y-23)
heading('Registro honesto y pendientes',y)
y=para('Prompts contiene una propuesta no ejecutada, bitácora y tres verificaciones del provisional. No se inventaron herramienta, ajustes, generación, defectos o correcciones de IA. Se documenta asistencia de Codex en la base técnica. Revisar código y realizar el tutorial antes de la entrega individual.',y-23,size=10)
y=para('Falta obtener el GLB final, conservar original, registrar prompt exacto realmente usado y procedencia/licencia; revisar malla, normales, materiales, escala y articulaciones; comparar variante/corrección o tres verificaciones del modelo final. Repetir importación en copia limpia y actualizar video/informe. Publicar enlaces de proyecto y video.',y,size=10)
para('La copia portable se comprueba sin caché .godot. Esa validación sólo cubre los recursos actuales; no verifica un modelo IA que aún no se ha incorporado.',y,size=9)
C.save()
print(OUT/'informe-tarea-1.pdf')
