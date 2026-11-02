# Actividad 6 — Guía de carga en Trello

Tablero propuesto: Evaluación y validación | Riesgo crediticio
Crear seis tarjetas con las siguientes descripciones y adjuntar las imágenes indicadas.
Entregar el enlace al tablero o capturas en PDF. Esta guía no sustituye el tablero real.

## 01 · Problema, datos y objetivo SMART

1,000 registros; 700 créditos buenos y 300 malos. Clase positiva = crédito malo. Criterios: recall ≥ 0.75, especificidad ≥ 0.60, ROC-AUC ≥ 0.70.
Imagen para adjuntar: `etapa1_distribucion_clases.png`

## 02 · Validación cruzada y comparación de modelos

Cinco folds estratificados sobre desarrollo (800 observaciones). Baseline, regresión logística y Random Forest. No se usa el test en la selección.
Imagen para adjuntar: `etapa2_comparacion_roc_auc_cv.png`

## 03 · Umbral, ROC y matrices de confusión

Random Forest con umbral 0.28 seleccionado en desarrollo OOF. Distinguir optimización retrospectiva de validación independiente.
Imagen para adjuntar: `etapa3_matriz_seleccionado.png`

## 04 · Significancia y A/B simulado

Prueba A/B retrospectiva, dos grupos de 400; p=0.6395. No hay evidencia de diferencia significativa ni efecto causal demostrado.
Imagen para adjuntar: `etapa4_ab_costos_medios.png`

## 05 · Resultado independiente y decisión

Random Forest, umbral 0.28: recall=0.783, especificidad=0.564, ROC-AUC=0.759. No cumple todas las metas. Decisión: no aprobar despliegue.
Imagen para adjuntar: `etapa6_tablero_ejecutivo.png`

## 06 · Evidencias, limitaciones y siguientes pasos

Falta representatividad contemporánea, validación temporal/externa, análisis de sesgos y costos observables. Mantener revisión humana obligatoria.
Imagen para adjuntar: `etapa6_metas_vs_intervalos.png`

## Nota metodológica
El test independiente se consultó en Etapa 5 con modelos y umbrales fijados previamente.
La especificidad del candidato no alcanzó el mínimo originalmente establecido.
La prueba A/B es una simulación retrospectiva y no un experimento de negocio en producción.
Las unidades de costo son hipotéticas; no representan pesos ni pérdidas observadas.
