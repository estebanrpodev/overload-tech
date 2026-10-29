"""Carga la configuracion externa y los registros de ventas de SNEAKER LAB.

El modulo permite cambiar rutas y columnas desde config.json sin modificar el
codigo Python. `leer_registros(config)` devuelve la misma tupla que espera
reporte.py: (registros validos, total de filas leidas, filas descartadas).
"""

import csv
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CONFIG = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "cliente": "SNEAKER LAB",
    "archivo_datos": "datos/registros.csv",
    "columna_categoria": "categoria",
    "columna_valor": "precio_unitario",
    "columna_cantidad": "cantidad",
    "columna_fecha": "fecha",
    "ruta_reporte": "salida/reporte.md",
    "ruta_grafica": "salida/grafica.html",
}

COLUMNAS_FIJAS = ["id", "producto", "medio_pago", "estado"]


def resolver_ruta(ruta, base=BASE_DIR):
    """Convierte una ruta relativa del config en una ruta absoluta."""
    ruta = Path(ruta)
    return ruta if ruta.is_absolute() else base / ruta


def cargar_config(ruta_config=None):
    """Lee config.json y devuelve la configuracion combinada con los valores por defecto."""
    ruta = ARCHIVO_CONFIG if ruta_config is None else resolver_ruta(ruta_config)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontro el archivo de configuracion: {ruta}")

    with ruta.open("r", encoding="utf-8-sig") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict):
        raise ValueError("El archivo de configuracion debe contener un objeto JSON.")

    config = dict(DEFAULT_CONFIG)
    config.update(datos)
    return config


def resolver_columnas(config):
    """Devuelve el nombre real de las columnas configurables."""
    return {
        "fecha": config.get("columna_fecha", DEFAULT_CONFIG["columna_fecha"]),
        "categoria": config.get(
            "columna_categoria", DEFAULT_CONFIG["columna_categoria"]
        ),
        "cantidad": config.get("columna_cantidad", DEFAULT_CONFIG["columna_cantidad"]),
        "valor": config.get("columna_valor", DEFAULT_CONFIG["columna_valor"]),
    }


def texto_campo(fila, campo):
    """Devuelve un campo de la fila como texto limpio (sin espacios extra)."""
    valor = fila.get(campo)
    return "" if valor is None else str(valor).strip()


def validar_fila(fila, columnas):
    """Valida y normaliza una fila del CSV.

    Devuelve un diccionario con los valores numericos convertidos o lanza
    ValueError con el motivo por el que la fila debe descartarse.
    """
    if fila is None or None in fila:
        raise ValueError("la fila tiene mas columnas que el encabezado")

    requeridas = COLUMNAS_FIJAS + list(columnas.values())
    for campo in requeridas:
        if texto_campo(fila, campo) == "":
            raise ValueError(f"campo '{campo}' vacío")

    cantidad_texto = texto_campo(fila, columnas["cantidad"])
    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        raise ValueError(f"cantidad no numérica ('{cantidad_texto}')") from None
    if cantidad <= 0:
        raise ValueError(f"cantidad no positiva ('{cantidad_texto}')")

    valor_texto = texto_campo(fila, columnas["valor"])
    try:
        precio_unitario = int(valor_texto)
    except ValueError:
        raise ValueError(f"precio no numérico ('{valor_texto}')") from None
    if precio_unitario <= 0:
        raise ValueError(f"precio no positivo ('{valor_texto}')")

    fecha_texto = texto_campo(fila, columnas["fecha"])
    try:
        fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"fecha inválida ('{fecha_texto}')") from None

    return {
        "id": texto_campo(fila, "id"),
        "fecha": fecha,
        "producto": texto_campo(fila, "producto"),
        "categoria": texto_campo(fila, columnas["categoria"]),
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "medio_pago": texto_campo(fila, "medio_pago"),
        "estado": texto_campo(fila, "estado"),
    }


def leer_registros(config):
    """Lee el CSV indicado en la configuracion y separa validos de descartados.

    Devuelve la tupla (registros, total_leidos, descartes). Las filas danadas se
    capturan una por una con try/except para no detener la lectura.
    """
    if not isinstance(config, dict):
        raise ValueError("La configuracion debe ser un diccionario.")

    ruta = resolver_ruta(
        config.get("archivo_datos", DEFAULT_CONFIG["archivo_datos"])
    )
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontro el archivo de datos: {ruta}")

    columnas = resolver_columnas(config)
    requeridas = COLUMNAS_FIJAS + list(columnas.values())
    registros = []
    descartes = []

    with ruta.open("r", newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        encabezado = lector.fieldnames or []
        faltantes = [campo for campo in requeridas if campo not in encabezado]
        if faltantes:
            raise ValueError(
                "Al archivo le faltan columnas obligatorias: "
                + ", ".join(faltantes)
            )

        for numero_linea, fila in enumerate(lector, start=2):
            try:
                registros.append(validar_fila(fila, columnas))
            except (ValueError, TypeError, KeyError) as error:
                descartes.append({"linea": numero_linea, "motivo": str(error)})

    total_leidos = len(registros) + len(descartes)
    return registros, total_leidos, descartes
