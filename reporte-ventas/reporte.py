"""Genera el reporte mensual de ventas de SNEAKER LAB en formato Markdown.

El script lee el archivo de ventas (datos/registros.csv por defecto), descarta
las filas danadas sin detener la ejecucion, calcula los totales generales y por
categoria, y escribe el informe en salida/reporte.md.

Si existen los modulos cargar.py (issue #22) y grafica.py (issue #21) en esta
misma carpeta, se usan automaticamente; si todavia no existen, el programa
funciona igual con su lector interno y omite la grafica.
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

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

# Columnas fijas del esquema. Las cuatro configurables se resuelven con config.
COLUMNAS_FIJAS = ["id", "producto", "medio_pago", "estado"]

MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def resolver_ruta(ruta, base=BASE_DIR):
    """Convierte una ruta relativa del config en una ruta absoluta."""
    ruta = Path(ruta)
    return ruta if ruta.is_absolute() else base / ruta


def resolver_columnas(config):
    """Devuelve el nombre real de las columnas configurables."""
    return {
        "fecha": config["columna_fecha"],
        "categoria": config["columna_categoria"],
        "cantidad": config["columna_cantidad"],
        "valor": config["columna_valor"],
    }


def formatear_pesos(valor):
    """Formatea un entero en pesos colombianos, por ejemplo $1.280.000."""
    return "$" + f"{int(valor):,}".replace(",", ".")


def formatear_entero(valor):
    """Formatea un entero con separador de miles."""
    return f"{int(valor):,}".replace(",", ".")


def formatear_porcentaje(valor):
    """Formatea un porcentaje con dos decimales y coma decimal."""
    return f"{valor:.2f} %".replace(".", ",")


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

    requeridas = ["id", "producto", "medio_pago", "estado"] + list(columnas.values())
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


def leer_registros_local(ruta, config):
    """Lee el CSV y separa los registros validos de las filas descartadas.

    Devuelve la tupla (registros, total_leidos, descartes), donde descartes es
    una lista de diccionarios con la linea y el motivo del descarte.
    """
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


def leer_con_cargar(config):
    """Intenta leer los registros con cargar.py (issue #22).

    Devuelve la misma tupla que leer_registros_local o None si el modulo no
    esta disponible o no cumple el contrato acordado.
    """
    try:
        import cargar
    except ImportError:
        return None

    try:
        resultado = cargar.leer_registros(config)
    except Exception as error:  # El lector interno sigue siendo el respaldo.
        print(
            f"Aviso: cargar.py fallo ({error}); se usa el lector interno.",
            file=sys.stderr,
        )
        return None

    if isinstance(resultado, tuple) and len(resultado) == 3:
        return resultado

    print(
        "Aviso: cargar.leer_registros no devolvio (registros, total, descartes); "
        "se usa el lector interno.",
        file=sys.stderr,
    )
    return None


def obtener_registros(ruta, config):
    """Lee los registros usando cargar.py si existe o el lector interno."""
    resultado = leer_con_cargar(config)
    if resultado is not None:
        return resultado
    return leer_registros_local(ruta, config)


def calcular_totales(registros):
    """Calcula el valor total, las unidades y los totales por categoria."""
    total = sum(
        registro["cantidad"] * registro["precio_unitario"] for registro in registros
    )
    unidades = sum(registro["cantidad"] for registro in registros)
    categorias = {}
    for registro in registros:
        datos = categorias.setdefault(
            registro["categoria"], {"unidades": 0, "valor": 0}
        )
        datos["unidades"] += registro["cantidad"]
        datos["valor"] += registro["cantidad"] * registro["precio_unitario"]

    for datos in categorias.values():
        datos["porcentaje"] = (datos["valor"] / total * 100) if total else 0.0

    ordenadas = dict(
        sorted(categorias.items(), key=lambda elemento: elemento[1]["valor"], reverse=True)
    )
    return {"total": total, "unidades": unidades, "categorias": ordenadas}


def describir_periodo(fechas):
    """Describe el periodo cubierto por las fechas de los registros."""
    if not fechas:
        return "sin datos"

    minimo = min(fechas)
    maximo = max(fechas)
    if (minimo.year, minimo.month) == (maximo.year, maximo.month):
        return f"{MESES[minimo.month - 1]} de {minimo.year}"
    if minimo.year == maximo.year:
        return (
            f"{MESES[minimo.month - 1]} a "
            f"{MESES[maximo.month - 1]} de {minimo.year}"
        )
    return (
        f"{MESES[minimo.month - 1]} de {minimo.year} a "
        f"{MESES[maximo.month - 1]} de {maximo.year}"
    )


def generar_grafica(categorias, valores, ruta_grafica):
    """Genera la grafica interactiva con grafica.py (issue #21) si existe."""
    try:
        import grafica
    except ImportError:
        print(
            "Aviso: grafica.py no esta disponible; se omite la grafica interactiva.",
            file=sys.stderr,
        )
        return False

    try:
        ruta_grafica.parent.mkdir(parents=True, exist_ok=True)
        grafica.crear_grafica(categorias, valores, str(ruta_grafica))
    except Exception as error:
        print(f"Aviso: no se pudo generar la grafica ({error}).", file=sys.stderr)
        return False

    return True


def generar_markdown(
    config,
    registros,
    totales,
    total_leidos,
    descartes,
    ruta_reporte,
    ruta_grafica,
    grafica_generada,
):
    """Construye el contenido del reporte en Markdown y lo guarda en disco."""
    descartadas = len(descartes)
    validas = len(registros)
    periodo = describir_periodo([registro["fecha"] for registro in registros])
    generado = datetime.now().strftime("%Y-%m-%d %H:%M")
    porcentaje_total = "100,00 %" if totales["total"] else "0,00 %"

    lineas = [
        f"# Reporte de ventas — {config['cliente']}",
        "",
        f"**Periodo:** {periodo}  ",
        f"**Generado:** {generado}",
        "",
        "## Resumen general",
        "",
        "| Métrica | Valor |",
        "| :--- | ---: |",
        f"| Filas leídas | {formatear_entero(total_leidos)} |",
        f"| Registros válidos | {formatear_entero(validas)} |",
        f"| Filas descartadas | {formatear_entero(descartadas)} |",
        f"| Unidades vendidas | {formatear_entero(totales['unidades'])} |",
        f"| Valor total vendido | {formatear_pesos(totales['total'])} |",
        "",
        "## Totales por categoría",
        "",
        "| Categoría | Unidades | Ventas | % del total |",
        "| :--- | ---: | ---: | ---: |",
    ]

    for categoria, datos in totales["categorias"].items():
        lineas.append(
            f"| {categoria} | {formatear_entero(datos['unidades'])} "
            f"| {formatear_pesos(datos['valor'])} "
            f"| {formatear_porcentaje(datos['porcentaje'])} |"
        )

    lineas.extend(
        [
            f"| **Total** | **{formatear_entero(totales['unidades'])}** "
            f"| **{formatear_pesos(totales['total'])}** | **{porcentaje_total}** |",
            "",
            "## Calidad de los datos",
            "",
            f"Coherencia: {validas} registros válidos + {descartadas} filas "
            f"descartadas = {total_leidos} filas leídas.",
            "",
        ]
    )

    if descartes:
        lineas.extend(
            [
                "| Línea del archivo | Motivo del descarte |",
                "| ---: | :--- |",
            ]
        )
        for descarte in descartes:
            lineas.append(f"| {descarte['linea']} | {descarte['motivo']} |")
        lineas.append("")
    else:
        lineas.extend(["No se encontraron filas dañadas.", ""])

    if grafica_generada:
        nombre_grafica = Path(ruta_grafica).name
        lineas.extend(
            [
                "## Gráfica interactiva",
                "",
                f"[Ver gráfica interactiva]({nombre_grafica})",
                "",
            ]
        )

    lineas.extend(
        [
            "---",
            "",
            "Reporte generado automáticamente por `reporte.py`.",
            "",
        ]
    )

    ruta_reporte.parent.mkdir(parents=True, exist_ok=True)
    ruta_reporte.write_text("\n".join(lineas), encoding="utf-8")


def construir_config(ruta_config=None):
    """Combina la configuracion por defecto con config.json si existe."""
    config = dict(DEFAULT_CONFIG)

    if ruta_config is None:
        ruta_config = BASE_DIR / "config.json"
    else:
        ruta_config = resolver_ruta(ruta_config)

    if ruta_config.is_file():
        with ruta_config.open("r", encoding="utf-8") as archivo:
            config.update(json.load(archivo))

    return config


def main(argv=None):
    analizador = argparse.ArgumentParser(
        description="Genera el reporte mensual de ventas de SNEAKER LAB."
    )
    analizador.add_argument(
        "--config",
        help="Ruta del archivo config.json (por defecto: config.json de la carpeta).",
    )
    analizador.add_argument(
        "--entrada",
        help="Ruta del CSV de entrada (sobrescribe la del config).",
    )
    analizador.add_argument(
        "--salida",
        help="Ruta del reporte Markdown (sobrescribe la del config).",
    )
    argumentos = analizador.parse_args(argv)

    try:
        config = construir_config(argumentos.config)
    except (OSError, ValueError) as error:
        print(f"Error: no se pudo leer la configuracion ({error}).", file=sys.stderr)
        return 1

    if argumentos.entrada:
        config["archivo_datos"] = argumentos.entrada
    if argumentos.salida:
        config["ruta_reporte"] = argumentos.salida

    ruta_datos = resolver_ruta(config["archivo_datos"])
    ruta_reporte = resolver_ruta(config["ruta_reporte"])
    ruta_grafica = resolver_ruta(config["ruta_grafica"])

    try:
        registros, total_leidos, descartes = obtener_registros(ruta_datos, config)
    except FileNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except (OSError, UnicodeDecodeError, csv.Error, ValueError) as error:
        print(f"Error al leer el archivo de datos: {error}", file=sys.stderr)
        return 1

    if len(registros) + len(descartes) != total_leidos:
        print(
            "Error: los conteos no son coherentes (validos + descartadas != leidas).",
            file=sys.stderr,
        )
        return 1

    totales = calcular_totales(registros)

    grafica_generada = False
    if registros:
        categorias = list(totales["categorias"])
        valores = [datos["valor"] for datos in totales["categorias"].values()]
        grafica_generada = generar_grafica(categorias, valores, ruta_grafica)

    generar_markdown(
        config,
        registros,
        totales,
        total_leidos,
        descartes,
        ruta_reporte,
        ruta_grafica,
        grafica_generada,
    )

    print(f"Archivo de datos: {ruta_datos}")
    print(f"Filas leidas: {total_leidos}")
    print(f"Registros validos: {len(registros)}")
    print(f"Filas descartadas: {len(descartes)}")
    print(f"Valor total: {formatear_pesos(totales['total'])}")
    print(f"Reporte generado: {ruta_reporte}")

    if not registros:
        print("Error: no hay registros validos para reportar.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
