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

Este primer ticket implementa únicamente el **generador del dataset de prueba**
(`generar_datos.py`), que simula el archivo mensual recibido por la Gerente de
Operaciones, incluyendo errores intencionales para probar la robustez del
sistema. Los scripts de reporte (`reporte.py`), gráfica (`grafica.py`) y
configuración (`cargar.py` / `config.json`) se abordan en tickets posteriores.

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

## Cómo ejecutar

**Requisito:** Python 3.10 o superior. No se necesitan librerías externas.

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

## Referencias

- Reglas del equipo, ramas, commits y Pull Requests: [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- Descripción general de la empresa y del repositorio: [`../README.md`](../README.md)
