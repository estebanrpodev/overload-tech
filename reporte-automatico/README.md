# Reporte Automático — Opción A

Script que lee un archivo de solicitudes (`data/solicitudes.csv`) y genera un resumen automático:
total de solicitudes, tipo más pedido y tiempo promedio de cierre. Está dirigido a equipos de
atención al cliente y dueños de negocio que hoy consolidan y cuentan sus solicitudes a mano.

## Opción elegida

**Opción A: Reporte Automático en Python.**

Se eligió porque resuelve el problema con herramientas simples y conocidas por el equipo
(Python estándar), sin dependencias externas y con una salida fácil de leer.

## Roles y responsabilidades

| Integrante | Usuario de GitHub | Rol | Responsabilidad |
| :--- | :--- | :--- | :--- |
| Esteban Montoya | `estebanrpodev` | Líder del proyecto | Define el alcance, coordina las entregas, gestiona issues, ramas y Pull Requests. |
| Josué Daniel Álvarez | `josuealvarez21` | Desarrollo | Implementa `reporte.py`, el resumen y el manejo de errores del script. |
| Luis Mateo Silva | `luismateo24` | Revisión | Revisa los Pull Requests, valida los datos de ejemplo y verifica los resultados. |

## Alcance y ruta de entregas

- **Kickoff:** repositorio creado, reglas del equipo (`CONTRIBUTING.md`), estructura de carpetas
  (`src/`, `docs/`, `equipo/`) y perfiles de los integrantes.
- **Encargo 2 — Resumen del reporte:** `reporte.py` lee `data/solicitudes.csv` y calcula el total
  de solicitudes, el tipo más pedido y el tiempo promedio de cierre (`dias_cierre`).
- **Encargo 3 — Datos de ejemplo:** `data/solicitudes.csv` con al menos 40 filas y su esquema
  documentado (ver la sección [Datos](#datos)).
- **Encargo 4 — Manejo de errores y configuración:** validación de datos inválidos (archivo
  inexistente, columnas faltantes, valores no numéricos, archivo vacío) y rutas/formato movidos a
  configuración. Con un CSV corrupto el script avisa el error y termina con código distinto de 0;
  con un CSV válido sigue funcionando.

## Datos

El script trabaja sobre `data/solicitudes.csv`, con las siguientes columnas:

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `fecha` | Texto (ISO `AAAA-MM-DD`) | Fecha en que se registró la solicitud. |
| `cliente` | Texto | Nombre del cliente que hizo la solicitud. |
| `tipo` | Texto | Categoría de la solicitud (por ejemplo, soporte, ventas, facturación). |
| `estado` | Texto | Estado actual de la solicitud (por ejemplo, abierta, cerrada). |
| `dias_cierre` | Número entero | Días que tardó en cerrarse la solicitud. |

Ejemplo:

```csv
fecha,cliente,tipo,estado,dias_cierre
2026-01-05,Acme S.A.,soporte,cerrada,3
2026-01-06,Globex,ventas,abierta,0
```

## Cómo ejecutar

1. Ubícate en la carpeta del proyecto:

   ```bash
   cd reporte-automatico
   ```

2. Ejecuta el script:

   ```bash
   python reporte.py
   ```

La salida esperada es un resumen con el **total** de solicitudes, el **tipo más pedido** y el
**tiempo promedio** de cierre.

## Referencias

- Reglas del equipo, ramas, commits y Pull Requests: [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- Descripción general de la empresa y del repositorio: [`../README.md`](../README.md)
