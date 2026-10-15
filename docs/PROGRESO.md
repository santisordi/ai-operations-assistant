# Progreso y próxima tarea

Última actualización: 2026-10-15 (Argentina).

## Estado actual

- Fase: 1 — Fundamentos de Tool Calling y outputs tipados.
- Sprint: 1 — Una consulta de cliente y una tool real.
- Punto actual: `Customer`, contrato `CustomerRepository` y repositorio en memoria implementados; ejercicio de consulta todavía incompleto.
- Santiago movió la validación del ID antes de las asignaciones y creó `src/customer_repository.py` con `get_by_id`, retorno `Customer | None` y `NotImplementedError`.
- `InMemoryCustomerRepository.get_by_id` devuelve el cliente almacenado o `None`. Ejemplos protegidos con `if __name__ == "__main__":` en ambos módulos. `src/customer_service.py` tiene el constructor que recibe y guarda un `CustomerRepository`; falta implementar su consulta, definir el error de cliente inexistente, fijar dependencias y agregar tests.
- Python detectado en Mac: 3.12.1. Base inicial para ambos equipos: Python 3.12.

## Trabajo realizado

- Creación del repositorio y primer push a GitHub realizados por Santiago; autenticación SSH de la Mac funcionando.
- Roadmap existente en `docs/ROADMAP.md`, incorporado al conjunto de documentación a versionar sin modificar su contenido.
- Instrucciones de instalación y sincronización en `README.md`.
- Instrucciones de mentoría en `AGENTS.md` y exclusiones locales en `.gitignore`.
- Este registro permitirá continuar desde otra computadora o un chat nuevo.

## Verificaciones y pendientes

- Configuración de VS Code agregada en `.vscode/launch.json`: `Consultar cliente (módulo)` ejecuta `src.in_memory_customer_repository` desde la raíz con el intérprete seleccionado. Usar Run and Debug o Ctrl+F5; el botón Run Python File ejecuta un archivo suelto y no utiliza esta configuración. Pendiente comprobar el botón en el IDE del usuario.
- 2026-10-15: árbol de trabajo limpio al comenzar. Comprobación manual con `py -3.13 -`: atributos del cliente 245 correctos; rechazo de `0`, `-1`, `"245"`, `True`, `False`, `2.5` y `None`; importación de `CustomerRepository` correcta y método base lanza `NotImplementedError`. No es una suite de tests ni una verificación con Python 3.12. Importar `Customer` sigue imprimiendo el ejemplo.
- Se inspeccionó la copia real del proyecto, su rama `main` y el remoto de GitHub.
- Documentos presentes y enlaces locales verificados; `git diff --check` sin errores.
- Exclusiones verificadas con `git check-ignore`: entorno, archivos `.env`, secretos y cachés quedan fuera de Git.
- La publicación se confirma con el resultado de `git push` y la comparación del commit local con `main` en GitHub; este archivo no presupone ese resultado.
- No hay suite de tests implementada; se ejecutaron las comprobaciones manuales de `Customer` registradas abajo.
- Windows: checkout real inspeccionado en `main`, Git funcionando y `git pull --ff-only` indicó `Already up to date.` El commit `00abdb5` contiene `src/customer.py`.
- Windows: Python 3.13 disponible; `py -3.12 --version` indicó que no hay runtime compatible. No existe `.venv/Scripts/python.exe`. Instalar Python 3.12 y crear el entorno local queda pendiente.
- Comprobación manual en Windows: `py -3.13 src/customer.py` imprimió `245`, `Ana Demo` y `ana@example.com`. Esto verifica el ejemplo con 3.13; no reemplaza tests ni la ejecución pendiente con 3.12.
- Revisión de validación: comprobación manual por stdin con `py -3.13 -` aprobada. Se verificaron los atributos del cliente 245 y el rechazo con `ValueError` de `0`, `-1`, `"245"`, `True`, `False`, `2.5` y `None`. La condición funciona, pero todavía aparece después de las asignaciones. Al importar el módulo se ejecutan también los prints del ejemplo; separar el ejemplo cuando se incorporen otros módulos.
- Pendiente al existir código: ejecutar la misma consulta y los mismos tests en Mac y Windows.

## Dudas o decisiones pendientes

- No hay bloqueos para empezar el ejercicio local.
- Proveedor y modelo del LLM se elegirán cuando corresponda la integración; no hacen falta para esta tarea.
- Elegir y fijar las dependencias mínimas de testing durante el primer ejercicio, sin sumar frameworks futuros.

## Próxima tarea concreta

**Santiago implementa la consulta de cliente sin LLM ni framework**, con ayuda gradual del mentor.

1. Preparar un entorno Python local siguiendo el README.
2. Definir `Customer` con ID, nombre y email sintéticos y un ID válido como entero positivo estricto (rechazar también booleanos).
3. Definir una interfaz pequeña `CustomerRepository`, con resultado explícito para un cliente inexistente.
4. Implementar un repositorio en memoria con el cliente ficticio 245.
5. Implementar `CustomerService.get_customer`: validar antes de acceder al repositorio y delegar la consulta.
6. Probar cliente 245, cliente inexistente e ID inválido; un repositorio espía debe demostrar que un ID inválido no accede a datos.

Próximo ejercicio de Santiago: agregar `CustomerService.get_customer(customer_id)`, validar entero positivo estricto antes de consultar y devolver el resultado de `self.repository.get_by_id(customer_id)`. En este paso se conserva `Customer | None`; antes de aprobar la consulta completa se definirá el error de servicio `customer_not_found` y se probará que un ID inválido no accede al repositorio. Python 3.12 y el entorno local siguen pendientes; no incorporar todavía el adapter del LLM.

Entrega: código de contratos/servicio/repositorio, tests ejecutados y explicación corta de cada responsabilidad. Los criterios completos están en la sección Sprint 1 del roadmap.

## Historial de sesiones

- **2026-10-15 (constructor del servicio):** Santiago protegió ambas demos y creó el constructor de `CustomerService`. Comprobación manual con `py -3.13 -` aprobada: imports sin salida, servicio conserva el repositorio recibido, cliente 245 con datos esperados y 999 devuelve `None`. Pendiente método `get_customer`, contrato de no encontrado y tests del servicio. El usuario confirmó también salida sin duplicados desde VS Code. Sin commit ni push.
- **2026-10-15 (continuación):** repositorio en memoria revisado y demo con `py -3.13 -m src.in_memory_customer_repository` ejecutada correctamente por el mentor y por Santiago (salida compartida en el chat). Los prints duplicados se deben al ejemplo de `customer.py` ejecutado al importar. Configuración de VS Code creada y JSON validado; ejecución desde su botón aún no confirmada. Próximo ejercicio: proteger ambas demos antes de crear el servicio. Sin commit ni push en esta continuación.
- **2026-10-15:** revisados `Customer` corregido y contrato `CustomerRepository`; comprobaciones manuales aprobadas con Python 3.13. Repositorio en memoria propuesto como siguiente ejercicio, aún sin implementar. Se actualizó solo este documento; no se realizó commit ni push en esta sesión.
- **2026-10-13 (revisión de validación):** Santiago agregó el rechazo de IDs inválidos; comprobaciones manuales aprobadas con Python 3.13. Pendiente mover la validación antes de las asignaciones. No se modificó su código; cambios de código y progreso siguen locales, sin commit ni push.
- **2026-10-13:** retomado en Windows; clase `Customer` revisada y diferencia con el progreso anterior identificada. Checkout al día con el remoto; ejemplo ejecutado con Python 3.13. Pendientes: Python 3.12, entorno local, validación del ID y resto de la consulta. Esta actualización de progreso queda local, sin commit ni push.
- **2026-10-12:** repositorio conectado a GitHub y preparación de continuidad Mac/Windows. La implementación Python sigue pendiente; no se adelantó el ejercicio del alumno.

Al terminar cada sesión, actualizar estado, verificaciones, dudas y próxima tarea; agregar una entrada aquí antes del commit y push.
