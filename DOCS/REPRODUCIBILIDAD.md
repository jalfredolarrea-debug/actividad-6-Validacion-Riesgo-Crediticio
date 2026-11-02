# Reproducción y controles de integridad

## Ejecución

1. Utilizar Google Colab con Python 3.13 y las bibliotecas requeridas.
2. Abrir el notebook del repositorio y ejecutar todas las celdas secuencialmente.
3. Permitir la descarga desde el repositorio público UCI. El ZIP se lee de forma automática, sin utilizar datos personales ni bancarios reales. Si la red impide la descarga, el notebook permite subir manualmente el ZIP oficial.
4. Verificar los mensajes `VERIFICACIÓN` de las seis etapas y los archivos de `actividad6_resultados/`.

## Fuente y definición de clases

Fuente primaria: `https://archive.ics.uci.edu/static/public/573/south+german+credit+update.zip`

SHA-256 registrado en la ejecución Colab del ZIP oficial: `0b40d40eb7321693d559e247a556f88a6cc8df8489c3cb2ae084db7592584551`.

El ZIP contiene `SouthGermanCredit.asc`. Conforme al código operativo del Apéndice B de Grömping (2019), el original contiene `0 = crédito malo` (300 casos) y `1 = crédito bueno` (700 casos). Se recodifica `riesgo_alto` como `1 = malo` y `0 = bueno` antes de modelar, y se comprueba la distribución esperada.

## Separación de datos

- Semilla: 42; estratificación 80/20 (desarrollo/test).
- El preprocesamiento se ajusta dentro de los pipelines, sin utilizar el conjunto de prueba.
- Validación cruzada: cinco folds estratificados sobre desarrollo.
- Umbrales elegidos con predicciones OOF en desarrollo. Candidato Random Forest, umbral 0.28, fijado antes de evaluar el test de 200 casos.
- No se emplea el test para reajustar umbral ni escoger otra versión después del resultado.

## Limitaciones estadísticas

- Las estimaciones de selección de umbral sobre OOF pueden ser optimistas.
- El bootstrap pareado de AUC y costos es exploratorio; IC que contienen cero **no prueban equivalencia**.
- La simulación A/B distribuye registros retrospectivos, no clientes reales; no establece causalidad, impacto operativo ni rentabilidad.
- La evaluación independiente se hizo una sola vez sobre 200 casos. Los intervalos son amplios y no sustituyen una validación externa, temporal o de equidad.
- El supuesto de costos FN:FP de 5:1 expresa **unidades ficticias**, no pérdidas monetarias.

## Entrega y archivos

- Los 31 archivos de `actividad6_resultados/` proceden del respaldo generado por Colab (30 evidencias más el inventario).
- El tablero [Trello](https://trello.com/b/EmbEfXPt) representa gráficamente los resultados.
- El reporte Word/PDF está pendiente de incorporación y no se declara entregado aquí.

## Comprobación independiente

En la raíz del repositorio, ejecutar `python src/verificar_resultados.py`. Comprueba el inventario SHA-256, la matriz de confusión, las métricas del conjunto de prueba, el umbral de 0.28 y el dictamen NO-GO, sin reentrenar modelos.
