# Detección de Colisiones en un Robot Agrónomo Utilizando XGBoost y ROS2
Este proyecto aborda la problemática de colisiones en un robot agrónomo que opera en entornos complejos. A partir de datos proporcionados por sensores como medición de corriente, rpm y señales diversas, se desarrolló una solución basada en Machine Learning para identificar y responder ante eventos de colisión en tiempo real.

Descripción del Proyecto
El enfoque principal consistió en el análisis de la corriente del motor del robot, utilizando técnicas de extracción de características para procesar los datos y entrenar un modelo de Machine Learning. Posteriormente, este modelo fue integrado en una simulación en ROS2 para realizar pruebas en tiempo real, desencadenando un protocolo de aborto en caso de detectar colisiones.

Detalles del Proyecto
Conjuntos de Datos

Mediciones de corriente (variable principal)
Velocidad en RPM
Señales de otros sensores
Preprocesamiento de Datos

Extracción de Características: A partir de las señales de corriente, se extrajeron características relevantes para identificar patrones asociados a colisiones.
División de Datos: Se separaron los datos en conjuntos de entrenamiento, validación y prueba.
Implementación del Modelo

Modelo de Machine Learning: Se utilizó XGBoost para entrenar un modelo capaz de clasificar eventos de colisión basándose en las características extraídas de la corriente.
Validación del Modelo: La precisión del modelo se evaluó con métricas como precisión, recall y F1-score para asegurar su efectividad en la detección de colisiones.
Simulación en ROS2

Se diseñó una simulación en ROS2 donde se probaron diferentes escenarios utilizando datos del conjunto de pruebas.
Protocolo de Aborto: En caso de detectar una colisión, el robot gatillaba un protocolo de emergencia que interrumpía su operación para evitar daños mayores.
Continuidad: Si no se detectaba colisión, la simulación continuaba hasta procesar todo el conjunto de datos.
Evaluación
Desempeño del Modelo: El modelo mostró una alta precisión en la detección de colisiones, identificando correctamente patrones asociados a estos eventos en los datos de prueba.
Visualización: Se generaron gráficos para analizar los datos crudos, las características extraídas y el desempeño del modelo.
Pruebas en Tiempo Real: La integración en ROS2 permitió validar el modelo en condiciones simuladas que replican el entorno del robot agrónomo.
Conclusiones y Próximos Pasos
El sistema desarrollado permite identificar colisiones en tiempo real, aumentando la seguridad y eficiencia del robot. Como próximos pasos, se podría optimizar el modelo mediante técnicas adicionales de extracción de características o probarlo en un entorno físico real para validar su desempeño fuera de la simulación.
