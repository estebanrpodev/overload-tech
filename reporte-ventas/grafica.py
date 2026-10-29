"""Genera la grafica interactiva del reporte de ventas de SNEAKER LAB.

Usa plotly.express para construir un grafico de barras con los totales por
categoria y lo guarda como un archivo HTML autocontenido (funciona sin
conexion a internet). Las dependencias estan en requirements.txt.
"""

from pathlib import Path

import plotly.express as px

CLIENTE_POR_DEFECTO = "SNEAKER LAB"
PERIODO_POR_DEFECTO = "Reporte mensual"

# Colores representativos de la marca por categoria.
COLORES_CATEGORIA = {
    "Calzado": "#111827",
    "Ropa": "#F97316",
    "Accesorios": "#0EA5E9",
}

# Colores de respaldo para categorias nuevas.
COLORES_RESPALDO = ["#6B7280", "#8B5CF6", "#14B8A6", "#DC2626", "#CA8A04"]

COLOR_TEXTO = "#1F2937"
COLOR_GRILLA = "#E5E7EB"


def formatear_pesos(valor):
    """Formatea un entero en pesos colombianos, por ejemplo $1.280.000."""
    return "$" + f"{int(valor):,}".replace(",", ".")


def formatear_porcentaje(valor):
    """Formatea un porcentaje con dos decimales y coma decimal."""
    return f"{valor:.2f} %".replace(".", ",")


def _calcular_paso(valor_maximo, cantidad_divisiones=5):
    """Calcula un paso "redondo" para las marcas del eje vertical."""
    if valor_maximo <= 0:
        return 1

    bruto = valor_maximo / cantidad_divisiones
    magnitud = 10 ** max(0, len(str(int(bruto))) - 1)
    for factor in (1, 2, 2.5, 5, 10):
        paso = factor * magnitud
        if paso >= bruto:
            return int(paso)
    return int(magnitud * 10)


def _marcas_eje(valor_maximo, cantidad_divisiones=5):
    """Genera los valores y etiquetas del eje vertical en formato de pesos."""
    paso = _calcular_paso(valor_maximo, cantidad_divisiones)
    valores = list(range(0, int(valor_maximo) + paso, paso))
    return valores, [formatear_pesos(valor) for valor in valores]


def _colores_por_categoria(categorias):
    """Asigna un color de marca a cada categoria, con respaldo para nuevas."""
    colores = {}
    respaldo = 0
    for categoria in categorias:
        if categoria in COLORES_CATEGORIA:
            colores[categoria] = COLORES_CATEGORIA[categoria]
        else:
            colores[categoria] = COLORES_RESPALDO[respaldo % len(COLORES_RESPALDO)]
            respaldo += 1
    return colores


def _normalizar(categorias, valores):
    """Valida, agrupa y ordena los datos de mayor a menor."""
    if len(categorias) != len(valores):
        raise ValueError("las categorias y los valores deben tener el mismo tamano")
    if not categorias:
        raise ValueError("no hay categorias para graficar")

    acumulado = {}
    for categoria, valor in zip(categorias, valores):
        nombre = str(categoria).strip()
        if not nombre:
            raise ValueError("hay una categoria vacia")
        try:
            numero = int(valor)
        except (TypeError, ValueError):
            raise ValueError(
                f"el valor de '{nombre}' no es numerico ('{valor}')"
            ) from None
        if numero < 0:
            raise ValueError(f"el valor de '{nombre}' es negativo")
        acumulado[nombre] = acumulado.get(nombre, 0) + numero

    pares = sorted(acumulado.items(), key=lambda par: par[1], reverse=True)
    if sum(valor for _, valor in pares) <= 0:
        raise ValueError("el valor total debe ser mayor que cero para graficar")
    return pares


def _construir_figura(categorias, valores, cliente=None, periodo=None):
    """Construye la figura de barras con el estilo y los datos del reporte."""
    pares = _normalizar(categorias, valores)
    nombres = [categoria for categoria, _ in pares]
    montos = [valor for _, valor in pares]
    total = sum(montos)

    etiquetas = [formatear_pesos(valor) for valor in montos]
    porcentajes = [formatear_porcentaje(valor / total * 100) for valor in montos]

    figura = px.bar(
        x=nombres,
        y=montos,
        color=nombres,
        color_discrete_map=_colores_por_categoria(nombres),
        text=etiquetas,
        custom_data=[etiquetas, porcentajes],
    )

    figura.update_traces(
        textposition="outside",
        textfont=dict(size=14, color=COLOR_TEXTO),
        cliponaxis=False,
        width=0.55,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Ventas: %{customdata[0]}<br>"
            "Participación: %{customdata[1]}"
            "<extra></extra>"
        ),
    )

    titulo = f"<b>{cliente or CLIENTE_POR_DEFECTO}</b>"
    subtitulo = f"Ventas por categoría · {periodo or PERIODO_POR_DEFECTO}"

    valores_eje, etiquetas_eje = _marcas_eje(max(montos))
    figura.update_layout(
        template="plotly_white",
        title=dict(
            text=f"{titulo}<br><sup>{subtitulo}</sup>",
            x=0.02,
            xanchor="left",
            font=dict(size=22, color=COLOR_TEXTO),
        ),
        xaxis=dict(title="", showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(
            title="Ventas (COP)",
            tickvals=valores_eje,
            ticktext=etiquetas_eje,
            showgrid=True,
            gridcolor=COLOR_GRILLA,
            zeroline=False,
        ),
        showlegend=False,
        bargap=0.35,
        height=540,
        margin=dict(l=100, r=40, t=115, b=60),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif", size=14, color=COLOR_TEXTO),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=COLOR_GRILLA,
            font=dict(size=13, color=COLOR_TEXTO),
        ),
    )
    return figura


def crear_grafica(categorias, valores, ruta, cliente=None, periodo=None):
    """Crea la grafica de barras interactiva y la guarda en un archivo HTML.

    Parametros:
        categorias: nombres de las categorias.
        valores: total vendido por cada categoria (mismo orden y tamano).
        ruta: ruta del archivo HTML de salida.
        cliente: nombre del cliente para el titulo.
        periodo: texto del periodo para el subtitulo.

    Devuelve la ruta (Path) del archivo generado.
    """
    figura = _construir_figura(categorias, valores, cliente, periodo)

    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    figura.write_html(
        str(ruta),
        include_plotlyjs=True,
        full_html=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        },
    )
    return ruta
