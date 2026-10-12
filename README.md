# AI Operations Assistant

Proyecto de aprendizaje de AI Engineering: construir progresivamente un asistente que consulte clientes y tickets, busque soluciones y prepare propuestas de acciones. Se trabaja con datos sintéticos y ejercicios pequeños, implementados por Santiago con acompañamiento y revisión.

## Dónde retomar

1. Leer [el progreso y la próxima tarea](docs/PROGRESO.md).
2. Consultar [el roadmap](docs/ROADMAP.md) para el objetivo y los criterios de aceptación.
3. Usar [las instrucciones de mentoría](AGENTS.md) al continuar en otro chat.

Actualmente hay documentación; todavía no hay aplicación, dependencias ni tests implementados.

## Primera vez en Windows

1. Instalar [Git for Windows](https://gitforwindows.org/) con Git Credential Manager y Python **3.12** desde [Python](https://www.python.org/downloads/). Esta es la versión base inicial, coherente con la Mac; las dependencias se elegirán en el primer ejercicio.
2. Abrir PowerShell en la carpeta donde quieras guardar tus proyectos y ejecutar:

```powershell
git clone https://github.com/santisordi/ai-operations-assistant.git
cd ai-operations-assistant
git switch main
git --version
py -3.12 --version
```

Git Credential Manager permite iniciar sesión en GitHub desde el navegador cuando haga falta autenticarse. No hace falta crear un token manual para este flujo. Ver [la guía de GitHub](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git).

3. Abrir **esa carpeta clonada** como proyecto en tu editor o asistente. No crear otro repositorio ni repetir `git init`.
4. Configurar la identidad de tus commits una vez dentro del repositorio, reemplazando el email por uno verificado en GitHub o el email privado que aparece en GitHub → Settings → Emails:

```powershell
git config user.name "Santiago Sordi"
git config user.email "TU_EMAIL_DE_GITHUB"
```

## Primera vez en Mac

La copia existente está en `~/Documents/Programacion/ai-operations-assistant` y ya usa SSH correctamente:

```bash
cd ~/Documents/Programacion/ai-operations-assistant
git switch main
git --version
python3 --version
```

Para una Mac nueva, instalar Git y Python 3.12 y clonar por HTTPS:

```bash
git clone https://github.com/santisordi/ai-operations-assistant.git
cd ai-operations-assistant
```

Para autenticación HTTPS, seguir la guía de GitHub enlazada arriba. Si usás SSH, configurar una clave propia de esa computadora. Windows puede usar HTTPS y la Mac SSH: ambos acceden al mismo repositorio. Cada máquina conserva sus credenciales localmente.

## Entorno Python local

Crear el entorno una sola vez por computadora, cuando empecemos el primer ejercicio. No copiar `.venv` entre sistemas ni subirlo a Git.

En Mac, comprobar que `python3 --version` indica 3.12 y ejecutar:

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

En Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

Si PowerShell bloquea la activación, podés usar el intérprete directamente sin cambiar la configuración del sistema:

```powershell
.\.venv\Scripts\python.exe --version
```

Cuando existan dependencias y tests, sus comandos de instalación y ejecución se documentarán aquí con versiones fijadas. Por ahora no hay paquetes que instalar ni una aplicación que ejecutar. En sesiones posteriores solo activá el entorno existente. Ver [documentación de venv](https://docs.python.org/3.12/library/venv.html).

## Al empezar cada sesión

Trabajar en una computadora por vez. Dentro de la carpeta del proyecto:

```bash
git status
git switch main
git pull --ff-only
```

Si `git status` muestra cambios pendientes de una sesión anterior, revisarlos y guardarlos antes de traer cambios. `--ff-only` evita una mezcla automática cuando las dos copias hayan avanzado por separado.

Leer `docs/PROGRESO.md` y abrir el proyecto desde esta misma carpeta. Para un chat nuevo, podés decir:

> Leé AGENTS.md, docs/PROGRESO.md y docs/ROADMAP.md. Quiero continuar con la próxima tarea en modo mentoría: yo implemento y vos me explicás y revisás.

Git sincroniza archivos y el progreso escrito; no sincroniza el historial del chat, paquetes instalados, entornos ni credenciales.

## Al terminar o cambiar de computadora

1. Actualizar `docs/PROGRESO.md`: qué hiciste, qué verificaste, dudas y próximo paso. Un ejercicio incompleto también se puede guardar indicando qué falta.
2. Revisar los archivos antes de guardarlos:

```bash
git status
git diff
git add .
git diff --cached
git commit -m "Guardar avance y próxima tarea"
git push
```

3. Confirmar que el push terminó correctamente y `git status` no muestra cambios pendientes. Recién entonces continuar en la otra computadora con `git pull --ff-only`.

Si no hay cambios, no hace falta crear un commit. Si no hay conexión, el commit queda local: no retomar en la otra PC hasta subirlo y descargarlo allí.

## Si aparecen conflictos o se rechaza el push

No usar `git push --force` ni descartar archivos. Guardar primero el trabajo local en un commit y consultar:

```bash
git fetch origin
git log --oneline --graph --all -10
```

Pedir ayuda mostrando el error y revisar ambos avances. Cuando corresponda integrarlos, usar `git merge origin/main`, resolver los archivos conservando las aportaciones válidas y revisar que no queden marcas de conflicto. Después ejecutar las verificaciones disponibles, guardar la resolución y subirla. Si necesitás cancelar una mezcla en curso, `git merge --abort` vuelve al estado anterior al merge; empezá siempre con tu trabajo guardado.

## Archivos que quedan en cada computadora

`.gitignore` excluye entornos, cachés y secretos habituales. No guardar claves, tokens o contraseñas en código, documentación o commits. Configurar las credenciales del proveedor localmente cuando lleguemos a la integración real. Un futuro `.env.example` podrá incluir nombres de variables y valores ficticios.

## Comprobación en Windows

Después de clonar, confirmar que están `README.md`, `AGENTS.md`, `docs/ROADMAP.md` y `docs/PROGRESO.md`, que la rama es `main` y que se entiende la próxima tarea. La descarga y ejecución en Windows quedan pendientes de comprobar en esa PC. Cuando exista la consulta Python, ejecutaremos los mismos casos y tests en ambos sistemas.
