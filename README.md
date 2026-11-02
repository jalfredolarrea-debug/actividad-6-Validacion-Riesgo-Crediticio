# Actividad 6 | Evaluación y validación de riesgo crediticio

**Gestión de Proyectos de Inteligencia Artificial · Ejercicio académico de clasificación**

Este repositorio documenta un ejercicio reproducible de evaluación y validación de modelos de clasificación sobre el conjunto público **South German Credit**. Se comparan un baseline, regresión logística y Random Forest, con validación cruzada, selección de umbral, análisis de incertidumbre, simulación A/B retrospectiva y evaluación final sobre datos reservados.

> **Dictamen:** **NO-GO para uso bancario real.** El candidato Random Forest (umbral 0.28) **no cumple simultáneamente** las tres metas de aceptación previamente definidas. Los costos son hipotéticos; las observaciones son históricas y no se acredita utilidad financiera, causalidad ni aptitud de despliegue.

## Objetivo y protocolo

- **Fuente:** [UCI Machine Learning Repository — South German Credit](https://archive.ics.uci.edu/dataset/573/south+german+credit+update) (1,000 observaciones; 20 predictores).
- **Clases:** en el archivo ASC original, `0 = crédito malo` y `1 = crédito bueno`; la variable modelada se recodifica explícitamente como `riesgo_alto = 1` para **crédito malo**, con 300 casos positivos y 700 negativos. La codificación y su contraste documental constan en el notebook.
- **Separación:** desarrollo de 800 casos y prueba independiente de 200, estratificada y con semilla 42.
- **Evaluación:** cinco folds estratificados; pipelines de preprocesamiento dentro de cada fold y predicciones *out-of-fold* (OOF) para seleccionar umbrales.
- **Metas predefinidas:** recall ≥ 0.75, especificidad ≥ 0.60 y ROC-AUC ≥ 0.70. Costos ilustrativos FN:FP de 5:1, **sin unidades monetarias reales**.
- **Modelo candidato:** Random Forest con umbral 0.28, congelado antes de evaluar el conjunto independiente. No se reoptimiza tras conocer el test.

## Resultados principales

| Indicador | Baseline | Regresión logística | Random Forest candidato |
|---|---:|---:|---:|
| Umbral | 0.50 | 0.21 | **0.28** |
| Exactitud (test) | 0.700 | 0.635 | 0.630 |
| Recall (test) | 0.000 | 0.733 | **0.783** |
| Especificidad (test) | 1.000 | 0.593 | **0.564** |
| Precisión (test) | 0.000 | 0.436 | 0.435 |
| F1 (test) | 0.000 | 0.547 | 0.560 |
| ROC-AUC (test) | 0.500 | 0.742 | **0.759** |
| Costo ilustrativo total | 300 | 137 | **126** |

**Matriz de confusión del candidato en test (n = 200):** TN 79, FP 61, FN 13, TP 47. El recall y el ROC-AUC cumplen las metas puntuales; la especificidad **no** cumple (0.564 < 0.60). La decisión documentada es **no aprobar su uso operativo**.

La diferencia exploratoria en ROC-AUC OOF entre Random Forest y regresión logística fue +0.013 (IC bootstrap 95%: −0.007 a +0.032). La simulación A/B retrospectiva obtuvo p = 0.6395: **no** demuestra una mejora estadísticamente significativa ni un efecto causal.

## Reproducibilidad

1. Abre [`Actividad_6_Notebook_Final.ipynb`](Actividad_6_Notebook_Final.ipynb) desde GitHub con Google Colab (o descárgalo y ábrelo en Colab).
2. Selecciona **Entorno de ejecución → Ejecutar todas**. No se necesitan datos privados: el notebook descarga el ZIP oficial de UCI; si falla la descarga, admite cargar manualmente ese mismo ZIP.
3. Revisa las verificaciones de las **Etapas 1 a 6** y los resultados producidos en `actividad6_resultados/`. La celda **6.6** permite descargar una copia ZIP de las evidencias desde Colab.
4. Compara la evaluación final con [`actividad6_resultados/etapa5_metricas_test_independiente.csv`](actividad6_resultados/etapa5_metricas_test_independiente.csv) y el dictamen con [`actividad6_resultados/etapa6_dictamen_final.json`](actividad6_resultados/etapa6_dictamen_final.json).

**Entorno utilizado:** Python 3.13 en Google Colab, Pandas 2.2.3 y scikit-learn 1.6.1. Los demás paquetes requeridos aparecen en [`requirements.txt`](requirements.txt). La ejecución necesita acceso a la fuente UCI o una copia auténtica de su ZIP original.

## Estructura

```text
Actividad_6_Notebook_Final.ipynb    # Notebook ejecutado, seis etapas
actividad6_resultados/              # CSV, JSON y PNG generados por Colab
README.md                           # Contexto, protocolo y resultados
requirements.txt                    # Dependencias del notebook y auditor
src/verificar_resultados.py         # Auditor independiente, no reentrena
docs/MAPA_RUBRICA.md                # Evidencia por criterio de evaluación
docs/REPRODUCIBILIDAD.md            # Reproducción, trazabilidad y limitaciones
```

El análisis experimental se encuentra en el notebook. Como control complementario, `src/verificar_resultados.py` recalcula las métricas finales y verifica el SHA-256 de las evidencias **sin reentrenar**; puede ejecutarse con `python src/verificar_resultados.py`. El conjunto fuente original se obtiene de UCI y **no se redistribuye** aquí.

## Tablero visual de Trello

[**Actividad 6 | Tablero Trello**](https://trello.com/b/EmbEfXPt) — cuatro listas, seis tarjetas de resultados y once imágenes de evidencia. El tablero es una representación visual de los resultados; **no reemplaza** los registros de cálculo de este repositorio.

## Alcance y límites

Este es un **ejercicio académico**, no una herramienta apta para evaluar solicitudes reales de crédito. La muestra es histórica y no representa necesariamente una cartera actual; no se comprobó desempeño temporal o externo, equidad, estabilidad, calibración ni costos observados. Los intervalos de confianza presentan incertidumbre relevante. El ajuste del umbral con OOF puede introducir optimismo. Cualquier nuevo modelo requiere un protocolo de validación independiente y controles adicionales, no una optimización sobre el test ya utilizado.

**Documentación adicional:** [mapa de rúbrica](docs/MAPA_RUBRICA.md) · [reproducibilidad y límites](docs/REPRODUCIBILIDAD.md).

**Referencia académica de codificación:** Grömping, U. (2019), documentación de South German Credit, Apéndice B (lectura de `SouthGermanCredit.asc`). En el informe existe una discrepancia textual sobre las etiquetas; el notebook deja documentada la correspondencia empleada conforme a la lectura del archivo y sus frecuencias.
