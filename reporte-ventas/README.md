# Reporte de Ventas — SNEAKER LAB

Automatización del reporte mensual de ventas para **SNEAKER LAB**, una tienda de
sneakers y ropa urbana. El programa toma el archivo de ventas del mes, descarta
los registros dañados y entrega un resumen para la reunión de gerencia.

## El cliente y su problema

**Cliente:** SNEAKER LAB.

**Contacto:** Laura Restrepo, Gerente de Operaciones.

Cada mes Laura recibe el historial de ventas en un archivo de Excel/CSV que
preparan a mano varias personas de la tienda. El archivo suele traer filas
incompletas, precios escritos como texto o fechas con formatos distintos. Hoy
ella consolida esos datos manualmente para saber cuánto se vendió en total y
cuánto aportó cada categoría, lo que consume tiempo y permite que los errores
pasen desapercibidos.

**Lo que pidió Laura:** automatizar la lectura del archivo mensual, ignorar (y
contar) las filas inválidas sin que el programa se detenga, calcular el valor
total vendido y los totales por categoría, y generar un reporte en Markdown y
una gráfica interactiva para presentar en la reunión de gerencia.

## Alcance de esta entrega

Esta entrega incluye cuatro piezas:

- **`generar_datos.py`** (issue #19): genera el dataset de prueba con errores
  intencionales para validar la robustez del sistema.
- **`reporte.py`** (issue #20): lee el archivo mensual, descarta y cuenta las
  filas dañadas, calcula los totales y escribe `salida/reporte.md`.
- **`grafica.py`** (issue #21): genera la gráfica de barras interactiva en
  `salida/grafica.html` con Plotly.
- **`cargar.py` / `config.json`** (issue #22): permiten cambiar rutas, columnas
  y datos del cliente sin modificar el código Python.

## Configuración externa (`config.json`)

`cargar.py` permite cambiar rutas, columnas y datos del cliente sin tocar el
código. `reporte.py` importa `leer_registros(config)` automáticamente; si el
módulo no está disponible, usa su lector interno como respaldo.

Claves disponibles en `config.json`:

| Clave | Descripción | Valor por defecto |
| :--- | :--- | :--- |
| `cliente` | Nombre del cliente para el reporte. | `SNEAKER LAB` |
| `archivo_datos` | Ruta del CSV de entrada (relativa a `reporte-ventas/` o absoluta). | `datos/registros.csv` |
| `columna_categoria` | Columna con la categoría del producto. | `categoria` |
| `columna_valor` | Columna con el valor monetario unitario. | `precio_unitario` |
| `columna_cantidad` | Columna con las unidades vendidas. | `cantidad` |
| `columna_fecha` | Columna con la fecha de la venta (`AAAA-MM-DD`). | `fecha` |
| `ruta_reporte` | Ruta del reporte Markdown de salida. | `salida/reporte.md` |
| `ruta_grafica` | Ruta de la gráfica HTML de salida. | `salida/grafica.html` |

Por ejemplo, para usar `datos/ventas_octubre.csv` donde la categoría se llama
`tipo_producto`:

```json
{
  "archivo_datos": "datos/ventas_octubre.csv",
  "columna_categoria": "tipo_producto"
}
```

Después solo hay que ejecutar `python reporte.py`; no se modifica ninguna línea
de Python. Las columnas fijas `id`, `producto`, `medio_pago` y `estado` deben
seguir existiendo en el CSV.

## Datos generados

El script crea `datos/registros.csv` con **100 filas válidas + 6 filas dañadas**
(106 filas en total). Las columnas son:

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | Entero | Identificador consecutivo de la venta. |
| `fecha` | Texto (`AAAA-MM-DD`) | Fecha de la venta (septiembre de 2026). |
| `producto` | Texto | Nombre del producto vendido. |
| `categoria` | Texto | Categoría: Calzado, Ropa o Accesorios. |
| `cantidad` | Entero | Unidades vendidas. |
| `precio_unitario` | Entero | Precio en pesos colombianos (sin decimales). |
| `medio_pago` | Texto | Efectivo, tarjeta débito/crédito, transferencia o Nequi. |
| `estado` | Texto | Pagado, enviado, entregado, pendiente o cancelado. |

### Filas dañadas a propósito

| `id` | Error intencional |
| :--- | :--- |
| 101 | `cantidad` vacía. |
| 102 | `precio_unitario` vacío. |
| 103 | Texto (`dos`) en la columna numérica `cantidad`. |
| 104 | Texto (`mil doscientos`) en la columna numérica `precio_unitario`. |
| 105 | Fecha inválida: `31/02/2026` (el 31 de febrero no existe). |
| 106 | Fecha inválida: `2026-13-45` (mes y día fuera de rango). |

## Requisitos e instalación

**Requisito:** Python 3.10 o superior.

`generar_datos.py` y `reporte.py` usan solo la librería estándar, pero
`grafica.py` necesita **Plotly** y **pandas**. Instálalos en un entorno virtual:

```bash
cd reporte-ventas
python -m venv .venv
```

Activa el entorno (Windows):

```bash
.venv\Scripts\activate
```

Activa el entorno (macOS / Linux):

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el generador

**Requisito:** Python 3.10 o superior. El generador no necesita librerías
externas.

1. Abre una terminal y ubícate en la carpeta del proyecto:

   ```bash
   cd reporte-ventas
   ```

2. Ejecuta el generador:

   ```bash
   python generar_datos.py
   ```

3. Verifica que se haya creado el archivo `datos/registros.csv`.

Salida esperada:

```text
Archivo generado: .../reporte-ventas/datos/registros.csv
Filas totales: 106 (validas: 100, danadas: 6)
```

También puedes ejecutarlo desde la raíz del repositorio sin cambiar de carpeta,
ya que el script resuelve sus rutas a partir de su propia ubicación:

```bash
python reporte-ventas/generar_datos.py
```

Cada ejecución sobrescribe `datos/registros.csv`. El generador usa una semilla
fija (`random.seed(19)`) para que el contenido sea reproducible.

## Generar el reporte

`reporte.py` lee `datos/registros.csv`, descarta las filas inválidas sin
detenerse y escribe el informe en `salida/reporte.md`.

```bash
cd reporte-ventas
python reporte.py
```

También funciona desde la raíz del repositorio:

```bash
python reporte-ventas/reporte.py
```

Salida esperada:

```text
Archivo de datos: .../reporte-ventas/datos/registros.csv
Filas leidas: 106
Registros validos: 100
Filas descartadas: 6
Valor total: $56.745.000
Grafica generada: .../reporte-ventas/salida/grafica.html
Reporte generado: .../reporte-ventas/salida/reporte.md
```

Si las dependencias de `requirements.txt` no están instaladas, el programa
avisa, omite solo la gráfica y genera igualmente `salida/reporte.md`.

### Contenido del reporte

El archivo `salida/reporte.md` incluye:

- **Resumen general:** periodo, filas leídas, registros válidos, filas
  descartadas, unidades vendidas y valor total.
- **Totales por categoría:** unidades, ventas y porcentaje del total, ordenados
  de mayor a menor.
- **Calidad de los datos:** la verificación
  `válidas + descartadas = leídas` y el detalle de cada fila descartada con su
  motivo.
- **Gráfica interactiva:** enlace a `salida/grafica.html` cuando está disponible.

Con el dataset de ejemplo los totales son:

| Categoría | Unidades | Ventas | % del total |
| :--- | ---: | ---: | ---: |
| Calzado | 78 | $38.600.000 | 68,02 % |
| Ropa | 91 | $14.110.000 | 24,87 % |
| Accesorios | 80 | $4.035.000 | 7,11 % |
| **Total** | **249** | **$56.745.000** | **100,00 %** |

### Gráfica interactiva

`grafica.py` genera `salida/grafica.html` con `plotly.express`:

- Barras ordenadas de mayor a menor y con un color por categoría.
- Valor en pesos sobre cada barra (por ejemplo `$38.600.000`).
- Al pasar el cursor muestra categoría, ventas y porcentaje del total.
- Título con el cliente y subtítulo con el periodo del reporte.
- Estilo claro (`plotly_white`) y diseño responsivo.

El HTML es **autocontenido** (incluye Plotly dentro del archivo, ~4,6 MB), así
que se abre con doble clic en cualquier navegador **sin conexión a internet**.
El enlace también aparece al final de `salida/reporte.md`.

`reporte.py` llama a `crear_grafica(categorias, valores, ruta)` con los totales
ya calculados; si la gráfica falla, el reporte Markdown se genera igual.

### Opciones de línea de comandos

| Opción | Descripción |
| :--- | :--- |
| `--config RUTA` | Usa un `config.json` distinto al de la carpeta del proyecto. |
| `--entrada RUTA` | Sobrescribe el CSV de entrada definido en la configuración. |
| `--salida RUTA` | Sobrescribe la ruta del reporte Markdown. |

### Códigos de salida

| Código | Significado |
| :--- | :--- |
| `0` | Reporte generado correctamente. |
| `1` | Archivo inexistente, columnas obligatorias faltantes, configuración inválida o ningún registro válido. |

Las filas dañadas **no** detienen el programa: se descartan, se cuentan y se
listan en el reporte.

## Estructura del proyecto

```text
reporte-ventas/
├── datos/registros.csv   # archivo mensual (generado por generar_datos.py)
├── generar_datos.py      # dataset de prueba con errores intencionales (#19)
├── reporte.py            # procesamiento y reporte Markdown (#20)
├── grafica.py            # gráfica interactiva con Plotly (#21)
├── cargar.py             # configuración externa y lectura del CSV (#22)
├── config.json           # rutas, columnas y cliente configurables (#22)
├── requirements.txt      # dependencias de la gráfica (plotly, pandas)
└── salida/               # reporte.md y grafica.html (generados, no se versionan)
```

## Referencias

- Reglas del equipo, ramas, commits y Pull Requests: [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- Descripción general de la empresa y del repositorio: [`../README.md`](../README.md)
