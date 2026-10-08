# Comparación y verificaciones

No existe aún una variante de IA ni una corrección de su malla. No se inventan defectos ni resultados antes/después.

Tres verificaciones realizadas sobre el provisional, que deben repetirse y documentarse sobre el modelo final:

1. Escala: robot de 1.8 m de alto, raíz con escala (1,1,1), pies a nivel del suelo. Cápsula independiente de 1.8 m. El modelo no cambia el volumen físico.
2. Materiales: dos StandardMaterial3D incluidos en la escena (turquesa y visor oscuro); sin texturas externas. Capturas del viewport muestran ambos. Repetir desde copia limpia.
3. Separación: mallas bajo Visual/ModelWrapper; cámara bajo CameraPivot y colisión bajo Player. El modelo no contiene scripts de movimiento. Se verificó que cambiar yaw de cámara mantiene referencia de movimiento.

Pendientes sobre el recurso importado: normales y caras invertidas, agujeros y geometría flotante, material/texturas, orientación, escala, uniones de articulaciones y aptitud para el rig de Tarea 2. Registrar vista frontal, lateral y posterior. Si se corrige la escala en el wrapper, conservar exportación original y documentar factor aplicado; no inventar una modificación de topología.
