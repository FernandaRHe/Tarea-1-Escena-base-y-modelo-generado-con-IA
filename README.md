# Proyecto I - Tarea 1

Base técnica de escena 3D para Godot **4.7.2 stable**, probada el 6 de octubre de 2026 en Windows. Renderizador Compatibility; física GodotPhysics3D a 60 Hz. Sin complementos.

## Abrir y jugar

Importar `project.godot` en Godot 4.7.2 y pulsar F6 en `scenes/level.tscn` o F5. Las escenas de nivel, personaje y apariencia son archivos editables; los cuerpos y mallas se ven en el editor 3D. No se necesita Python para ejecutar el juego.

| Control | Acción |
| --- | --- |
| WASD / flechas | Movimiento relativo a la orientación horizontal de cámara |
| Espacio | Salto únicamente al estar en suelo |
| Ratón | Orbitar y ajustar inclinación |
| Esc / clic | Liberar / capturar ratón |
| F1 | Alternar límites 30 y 144 FPS |
| R | Regresar al inicio |

## Arquitectura

- `scenes/level.tscn`: suelo, seis obstáculos/paredes StaticBody3D con cajas de colisión, WorldEnvironment con ProceduralSkyMaterial, luz direccional con sombras y HUD.
- `scenes/player.tscn`: CharacterBody3D y CapsuleShape3D; Visual separado de CameraPivot > SpringArm3D > Camera3D.
- `scenes/model_wrapper.tscn`: apariencia provisional. Sustituir sus mallas por una instancia del GLB importado, conservando el controlador y la cápsula.
- `scripts/player.gd`: física, entrada y transiciones explícitas Idle/Walk/Jump; `_process` sólo suaviza el giro visual.
- `tests/acceptance.gd`: pruebas automáticas del controlador real, colisiones, FSM, referencia de cámara y límites de render.

La capa 1 contiene el entorno; la capa 2, el personaje. SpringArm usa sólo capa 1 y excluye el RID del personaje. Su esfera de radio 0.2 m y margen de 0.15 m protegen el volumen de cámara.

## Tiempo y FSM

Gravedad y aceleración se multiplican por delta de física porque son cambios de velocidad por segundo. Velocidad está en m/s: `move_and_slide()` integra internamente; no se multiplica otra vez por delta. El salto fija 7 m/s. Ratón usa desplazamiento relativo y no delta. El giro visual usa `1-exp(-12*delta)` para responder al tiempo de render sin modificar la física.

Tras `move_and_slide()`: si no hay suelo, Jump; con suelo y velocidad horizontal >0.1 m/s, Walk; con suelo y velocidad menor, Idle. Jump cubre ascenso y caída, incluso al abandonar una plataforma. Sólo cambios de estado emiten señal y registro. No se incorporan clips ni rig de Tarea 2.

## Reproducir pruebas

En PowerShell, sustituir la ruta del ejecutable por la propia:

```powershell
& 'C:/ruta/Godot_v4.7.2-stable_win64_console.exe' --headless --path . --script res://tests/acceptance.gd
& 'C:/ruta/Godot_v4.7.2-stable_win64_console.exe' --path . --script res://tests/acceptance.gd -- --capture
& 'C:/ruta/Godot_v4.7.2-stable_win64_console.exe' --headless --path . --script res://tools/inspect_model.gd
```

La primera ejecución valida física pero no compara render real. La segunda aplica límites reales de render, guarda cuatro capturas y resultados en `docs/test_results.json`. Cada medida recorre 120 pasos a 60 Hz (2 s simulados) desde reposo, sin obstáculos. Con aceleración, el resultado es 9.520004 m a ambos límites, no 10 m. Los límites son máximos, no una garantía de FPS alcanzados. Una pequeña diferencia en pruebas humanas puede venir de tiempos de entrada/redondeo de pasos; no del delta aplicado dos veces.

`tests/demo.gd` reproduce una demostración automatizada de 65 segundos. `docs/demostracion.mp4` es una grabación del motor, con entradas programadas, no una prueba de uso manual.

## Estado de entrega y autoría

**Esta base no es todavía una entrega completa.** El personaje visible es un robot hecho con primitivas de Godot por código. No fue generado con Tripo/Meshy ni se afirma que esté autorizado por el docente como recurso de práctica. Su uso permite probar el controlador mientras se obtiene el modelo final.

Pendientes: realizar el tutorial solicitado; generar/exportar el modelo en la herramienta elegida o recibir autorización para un recurso; incorporar el modelo final y su ficha; registrar prompt realmente ejecutado, herramienta, ajustes, fecha y procedencia; inspeccionar normales, materiales, escala y articulaciones; comparar variante/corrección o documentar tres verificaciones; actualizar las capturas y el video con ese recurso. Subir proyecto/video y añadir enlaces públicos al informe. Revisar y comprender el código antes de entregar individualmente; se documenta la asistencia de Codex en la bitácora.

`Prompts/` contiene propuesta y bitácora honesta; `docs/FICHA_MODELO.md` distingue inspección provisional de la pendiente. El informe PDF tiene cinco páginas y declara los pendientes.

La copia extraída del ZIP se importó sin caché y pasó también 14/14 comprobaciones con render. Detalles en `docs/VALIDACION_COPIA.md`.

## Fuentes

- https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html
- https://docs.godotengine.org/en/stable/classes/class_springarm3d.html
- https://docs.godotengine.org/en/stable/getting_started/first_3d_game/index.html

No se tuvo acceso a los documentos internos 02_Arquitectura_Entornos_y_Fisica ni a la guía docente Modelado y animación con IA; consultar esos materiales para ajustar requisitos específicos.
