# Progreso y próxima tarea

Última actualización: 2026-10-12 (Argentina).

## Estado actual

- Fase: 1 — Fundamentos de Tool Calling y outputs tipados.
- Sprint: 1 — Una consulta de cliente y una tool real.
- Punto actual: preparación del repositorio y continuidad entre Mac y Windows, antes del primer ejercicio Python.
- Último ejercicio de programación completado: ninguno todavía.
- Hay documentación; no hay aplicación, dependencias fijadas ni tests implementados.
- Python detectado en Mac: 3.12.1. Base inicial para ambos equipos: Python 3.12.

## Trabajo realizado

- Creación del repositorio y primer push a GitHub realizados por Santiago; autenticación SSH de la Mac funcionando.
- Roadmap existente en `docs/ROADMAP.md`, incorporado al conjunto de documentación a versionar sin modificar su contenido.
- Instrucciones de instalación y sincronización en `README.md`.
- Instrucciones de mentoría en `AGENTS.md` y exclusiones locales en `.gitignore`.
- Este registro permitirá continuar desde otra computadora o un chat nuevo.

## Verificaciones y pendientes

- Se inspeccionó la copia real del proyecto, su rama `main` y el remoto de GitHub.
- Documentos presentes y enlaces locales verificados; `git diff --check` sin errores.
- Exclusiones verificadas con `git check-ignore`: entorno, archivos `.env`, secretos y cachés quedan fuera de Git.
- La publicación se confirma con el resultado de `git push` y la comparación del commit local con `main` en GitHub; este archivo no presupone ese resultado.
- No se ejecutaron pruebas de la aplicación: todavía no existe código.
- Pendiente en Windows: instalar Git y Python 3.12, clonar, abrir la carpeta y comprobar los documentos y el entorno.
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

Comenzar explicando el contrato de `Customer` y la validación del ID, y dejar que Santiago escriba esa primera parte. Acordar los valores sintéticos del fixture y el contrato de errores durante el ejercicio. Revisar esta base antes de incorporar el adapter del LLM.

Entrega: código de contratos/servicio/repositorio, tests ejecutados y explicación corta de cada responsabilidad. Los criterios completos están en la sección Sprint 1 del roadmap.

## Historial de sesiones

- **2026-10-12:** repositorio conectado a GitHub y preparación de continuidad Mac/Windows. La implementación Python sigue pendiente; no se adelantó el ejercicio del alumno.

Al terminar cada sesión, actualizar estado, verificaciones, dudas y próxima tarea; agregar una entrada aquí antes del commit y push.
