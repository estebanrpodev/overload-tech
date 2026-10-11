# Reglas de Trabajo de Overload Tech

Bienvenido al repositorio de **Overload Tech**. Para mantener un flujo de trabajo profesional, limpio y ordenado, todos los integrantes del equipo (**Esteban**, **Josué** y **Mateo**) debemos cumplir estrictamente con las siguientes normas de desarrollo.

---

## 👥 1. Estructura del Equipo
* **Líder de Proyecto:** Esteban
* **Desarrolladores:** Josué y Mateo

---

## 🌿 2. Flujo de Ramas y Protección de Main
1. **Rama `main` Protegida:** Queda prohibido realizar `git push` directamente a `main`.
2. **Creación de Ramas:** Antes de iniciar cualquier tarea, debes actualizar tu `main` local (`git pull`) y crear una rama propia partiendo del número del issue correspondiente.
   * **Formato de nombre de rama:** `<numero-issue>-<nombre-corto>`
   * **Ejemplo:** `2-reglas-contributing` o `3-perfil-mateo`

---

## 📝 3. Convención de Commits
Todos los mensajes de commit deben ser claros, en minúsculas y seguir la convención del tipo de cambio realizado:
* `docs:` Para cambios o adiciones en documentación (`README`, `CONTRIBUTING`, perfiles).
* `feat:` Para nuevas funcionalidades o estructuras iniciales.
* `fix:` Para correcciones de errores.
* `chore:` Para tareas de mantenimiento o pruebas.

**Ejemplo:** `docs: agrega reglas del equipo en CONTRIBUTING.md`

---

## 🔄 4. Revisiones en Cadena (Code Review)
Ningún cambio entra a `main` sin la aprobación de un compañero. La revisión se realiza en cadena cíclica:
* **Esteban** revisa a **Josué**.
* **Josué** revisa a **Mateo**.
* **Mateo** revisa a **Esteban**.

### Reglas para la revisión:
1. El autor abre el **Pull Request (PR)** hacia `main`.
2. En la descripción del PR DEBE escribir obligatoriamente: `Closes #NUMERO_ISSUE` (por ejemplo: `Closes #2`).
3. El revisor asignado entra a **Files changed**, analiza los cambios y **debe dejar al menos un comentario con sugerencia o mejora** usando el botón `+` sobre una línea.
4. El autor realiza las correcciones necesarias en su misma rama, vuelve a subir los cambios (`git push`), responde el comentario indicando lo modificado y da clic en **Resolve conversation**.
5. Una vez todo esté corregido, el revisor aprueba con **Review changes → Approve**.
6. El autor realiza el **Merge** de la Pull Request y elimina la rama remota en GitHub.
