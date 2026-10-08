# Ficha provisional - NO es el modelo final de IA

Archivo: `scenes/model_wrapper.tscn`. Origen: primitivas nativas de Godot creadas por código con asistencia de Codex el 6 de octubre de 2026. Sin descarga de un activo de terceros. No se dispone de autorización docente como recurso sustituto.

Geometría: CapsuleMesh, SphereMesh y BoxMesh. Conteos obtenidos directamente del motor en `model_metrics.json`. Dos materiales, cero texturas, altura 1.8 m, escala raíz 1:1; frente local +Z. No tiene esqueleto, huesos, clips ni pesos. Las articulaciones del modelo final siguen pendientes.

Integración final: conservar el GLB original en `assets/models/`, instanciarlo dentro de ModelWrapper, retirar las tres primitivas y ajustar sólo transformación del importado. Registrar triángulos de cada superficie, materiales únicos, resolución de cada textura, dimensiones antes/después, licencia, herramienta y URL/ID. Importar una copia limpia para comprobar dependencias. Repetir pruebas y capturas con el recurso final.
