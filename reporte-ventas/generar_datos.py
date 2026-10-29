"""Genera el dataset de prueba de SNEAKER LAB con errores intencionales.

El script crea datos/registros.csv con el historial mensual de ventas que
recibe la Gerente de Operaciones. Usa unicamente la libreria estandar.
"""

import csv
import random
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA_SALIDA = BASE_DIR / "datos" / "registros.csv"

FILAS_VALIDAS = 100
SEMILLA = 19
ANIO = 2026
MES = 9

COLUMNAS = [
    "id",
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "medio_pago",
    "estado",
]

CATALOGO = {
    "Calzado": [
        ("Air Max 90", (320000, 520000)),
        ("Air Force 1", (300000, 480000)),
        ("Jordan 1 Retro", (450000, 780000)),
        ("Ultraboost 22", (380000, 650000)),
        ("Forum Low", (280000, 420000)),
        ("Samba OG", (300000, 460000)),
        ("Chuck Taylor", (180000, 290000)),
        ("Gel-Kayano 14", (400000, 620000)),
    ],
    "Ropa": [
        ("Hoodie Oversize", (120000, 220000)),
        ("Camiseta Boxy", (60000, 120000)),
        ("Jogger Cargo", (110000, 190000)),
        ("Chaqueta Cortavientos", (150000, 280000)),
        ("Sudadera Crewneck", (100000, 180000)),
        ("Pantaloneta Deportiva", (70000, 130000)),
    ],
    "Accesorios": [
        ("Gorra Snapback", (45000, 90000)),
        ("Gym Sack", (35000, 70000)),
        ("Medias Deportivas", (18000, 40000)),
        ("Canguro", (50000, 110000)),
        ("Botella Termica", (40000, 85000)),
        ("Cordones Reflective", (15000, 35000)),
    ],
}

MEDIOS_PAGO = ["efectivo", "tarjeta debito", "tarjeta credito", "transferencia", "nequi"]
ESTADOS = ["pagado", "pagado", "pagado", "enviado", "entregado", "pendiente", "cancelado"]


def fecha_aleatoria():
    dia = random.randint(1, 28)
    return datetime(ANIO, MES, dia).strftime("%Y-%m-%d")


def fila_valida(identificador):
    categoria = random.choice(list(CATALOGO))
    producto, (precio_min, precio_max) = random.choice(CATALOGO[categoria])
    return {
        "id": identificador,
        "fecha": fecha_aleatoria(),
        "producto": producto,
        "categoria": categoria,
        "cantidad": random.randint(1, 4),
        "precio_unitario": random.randrange(precio_min, precio_max + 1, 10000),
        "medio_pago": random.choice(MEDIOS_PAGO),
        "estado": random.choice(ESTADOS),
    }


def filas_danadas(primer_id):
    base = {
        "producto": "Jordan 1 Retro",
        "categoria": "Calzado",
        "cantidad": 1,
        "precio_unitario": 520000,
        "medio_pago": "tarjeta credito",
        "estado": "pagado",
    }

    danadas = [
        # Cantidad vacia.
        {**base, "id": primer_id, "fecha": "2026-09-03", "cantidad": ""},
        # Precio unitario vacio.
        {**base, "id": primer_id + 1, "fecha": "2026-09-07", "precio_unitario": ""},
        # Texto en una columna numerica (cantidad).
        {**base, "id": primer_id + 2, "fecha": "2026-09-11", "cantidad": "dos"},
        # Texto en una columna numerica (precio).
        {**base, "id": primer_id + 3, "fecha": "2026-09-14", "precio_unitario": "mil doscientos"},
        # Fecha imposible (31 de febrero).
        {**base, "id": primer_id + 4, "fecha": "31/02/2026"},
        # Fecha con formato invalido y mes fuera de rango.
        {**base, "id": primer_id + 5, "fecha": "2026-13-45"},
    ]
    return danadas


def generar_filas():
    filas = [fila_valida(i) for i in range(1, FILAS_VALIDAS + 1)]
    filas.extend(filas_danadas(FILAS_VALIDAS + 1))
    return filas


def guardar_csv(filas, ruta):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    random.seed(SEMILLA)
    filas = generar_filas()
    guardar_csv(filas, RUTA_SALIDA)
    danadas = len(filas_danadas(FILAS_VALIDAS + 1))
    print(f"Archivo generado: {RUTA_SALIDA}")
    print(f"Filas totales: {len(filas)} (validas: {len(filas) - danadas}, danadas: {danadas})")


if __name__ == "__main__":
    main()
