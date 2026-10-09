# Reglas de trabajo del equipo - Overload Tech

## 1. Convención de nombres para ramas

Usaremos el **número del issue** seguido de una breve descripción en **kebab-case**.

**Formato:**
```text
<NÚMERO-ISSUE>-descripcion-corta
```

**Ejemplos:**
- `2-reglas-del-equipo`
- `4-estructura-carpetas`
- `5-archivos-perfil-integrantes`
- `1-actualizar-readme`

## 2. Convención para escribir commits

Seguiremos el estándar **Conventional Commits** para mantener un historial claro.

| Tipo | Cuándo usar |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de errores |
| `docs:` | Cambios en documentación |
| `style:` | Cambios de formato (espacios, indentación) sin alterar lógica |
| `refactor:` | Reestructuración de código sin añadir/corregir funcionalidad |
| `test:` | Añadir o modificar pruebas |
| `chore:` | Tareas menores, configuración o limpieza |

**Ejemplos:**
- `docs: agrega archivo CONTRIBUTING.md con reglas del equipo`
- `docs: crea perfiles de los integrantes en equipo/`
- `chore: añade .gitignore y estructura inicial`

## 3. Regla de revisión en cadena

Para garantizar una revisión cruzada entre todos los integrantes, seguiremos este orden:

1. **josuealvarez21** revisa los Pull Requests de **luismateo24**
2. **luismateo24** revisa los Pull Requests de **estebanrpodev**
3. **estebanrpodev** revisa los Pull Requests de **josuealvarez21**

## 4. Requisitos obligatorios para aprobar un Pull Request

Antes de hacer **merge** a `main`, todo Pull Request debe cumplir los siguientes requisitos:

- [ ] **Vinculado al issue:** Incluir `Closes #N` o `Resolves #N` en la descripción.
- [ ] **Título claro:** Debe describir brevemente el cambio realizado.
- [ ] **Descripción completa:** Explicar qué se hizo, por qué y qué archivos se modificaron.
- [ ] **Nombre de rama correcto:** Seguir la convención definida en el punto 1.
- [ ] **Commits con convención correcta:** Usar el formato Conventional Commits.
- [ ] **Sin archivos innecesarios:** Solo subir lo estrictamente relacionado al issue.
- [ ] **Sin conflictos:** Actualizar con `main` y resolver conflictos si existen.
- [ ] **Aprobación del revisor:** Contar con al menos **1 aprobación** del revisor correspondiente según la revisión en cadena.
- [ ] **Coherente con el repositorio:** Respetar estructura, nombres, estilo y patrones existentes.