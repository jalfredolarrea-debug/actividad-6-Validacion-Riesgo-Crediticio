"""Auditoria independiente de los artefactos exportados por Colab, sin reentrenar.

Ejecutar desde la raiz del repositorio: python src/verificar_resultados.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
RESULTADOS = ROOT / "actividad6_resultados"


def leer_csv(nombre: str):
    with (RESULTADOS / nombre).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def verificar_archivos() -> int:
    inventario = leer_csv("etapa6_inventario_archivos.csv")
    assert len(inventario) == 30, "El inventario debe contener 30 evidencias."
    for fila in inventario:
        nombre = fila["archivo"]
        assert Path(nombre).name == nombre, "Ruta insegura en inventario."
        archivo = RESULTADOS / nombre
        assert archivo.is_file(), f"Falta archivo: {nombre}"
        contenido = archivo.read_bytes()
        assert len(contenido) == int(fila["tamano_bytes"]), f"Tamano no coincide: {nombre}"
        assert hashlib.sha256(contenido).hexdigest() == fila["sha256"], f"SHA-256 no coincide: {nombre}"
    return len(inventario)


def verificar_test() -> dict:
    predicciones = leer_csv("etapa5_predicciones_prueba_reservada.csv")
    metricas = leer_csv("etapa5_metricas_test_independiente.csv")
    dictamen = json.loads((RESULTADOS / "etapa6_dictamen_final.json").read_text(encoding="utf-8"))
    assert len(predicciones) == 200
    assert len({f["indice_original"] for f in predicciones}) == 200
    assert [f["modelo"] for f in metricas] == ["Baseline (proporciones)", "Regresión logística", "Random Forest"]
    candidato = next(f for f in metricas if f["modelo"] == "Random Forest")
    assert dictamen["modelo"] == "Random Forest" and float(dictamen["umbral"]) == 0.28

    etiquetas = [int(f["riesgo_alto_real"]) for f in predicciones]
    probabilidades = [float(f["probabilidad_forest"]) for f in predicciones]
    estimadas = [int(f["prediccion_forest"]) for f in predicciones]
    assert all(pred == int(proba >= 0.28) for pred, proba in zip(estimadas, probabilidades)), "Umbral no coincide"
    TN = sum(y == 0 and p == 0 for y, p in zip(etiquetas, estimadas))
    FP = sum(y == 0 and p == 1 for y, p in zip(etiquetas, estimadas))
    FN = sum(y == 1 and p == 0 for y, p in zip(etiquetas, estimadas))
    TP = sum(y == 1 and p == 1 for y, p in zip(etiquetas, estimadas))
    for nombre, valor in (("TN", TN), ("FP", FP), ("FN", FN), ("TP", TP)):
        assert int(candidato[nombre]) == valor, f"Matriz inconsistente: {nombre}"
    calc = {
        "exactitud": (TP + TN) / len(etiquetas),
        "recall": TP / (TP + FN),
        "especificidad": TN / (TN + FP),
        "precision": TP / (TP + FP),
        "f1": 2 * TP / (2 * TP + FP + FN),
        "roc_auc": roc_auc_score(etiquetas, probabilidades),
        "costo_ponderado": 5 * FN + FP,
    }
    for nombre, valor in calc.items():
        assert abs(float(candidato[nombre]) - valor) < 1e-9, f"Tabla inconsistente: {nombre}"
        assert abs(float(dictamen["metricas"][nombre]) - valor) < 1e-9, f"Dictamen inconsistente: {nombre}"
    metas = dictamen["metas"]
    aprobado = all(calc[nombre] >= metas[nombre] for nombre in ("recall", "especificidad", "roc_auc"))
    assert aprobado is False and dictamen["cumplimiento_smart_puntual"] is False
    assert dictamen["despliegue_autorizado"] is False
    return {"TN": TN, "FP": FP, "FN": FN, "TP": TP, **calc}


if __name__ == "__main__":
    total = verificar_archivos()
    resumen = verificar_test()
    print(f"AUDITORIA CORRECTA: {total} archivos con SHA-256 verificado.")
    print(f"Test n=200 | TN={resumen['TN']} FP={resumen['FP']} FN={resumen['FN']} TP={resumen['TP']}")
    print(f"Recall={resumen['recall']:.3f} | Especificidad={resumen['especificidad']:.3f} | ROC-AUC={resumen['roc_auc']:.3f}")
    print("Dictamen consistente: NO-GO. No se reentreno ningun modelo.")
