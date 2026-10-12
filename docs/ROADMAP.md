# AI Operations Assistant — Roadmap de aprendizaje profesional

## 1. Objetivo y forma de trabajo

Construir progresivamente un asistente de operaciones capaz de consultar clientes y tickets, buscar soluciones documentadas, proponer cambios y preparar comunicaciones. El proyecto debe servir para aprender AI Engineering implementando y para demostrar decisiones técnicas en una entrevista.

Este documento es el plan de desarrollo; no presupone que exista una aplicación, dependencias instaladas ni servicios funcionando. Partimos de un repositorio vacío. Los nombres de módulos y contratos son propuestas para implementar durante las fases, no componentes ya disponibles.

La dedicación de cada fase será aproximadamente **20% teoría y 80% práctica**. No hay una fecha fija de finalización: se avanza cuando pasan los criterios de salida. La teoría se limita a lo necesario para resolver el siguiente problema y explicar las decisiones.

Dinámica de mentoría:

1. Acordar el problema pequeño y sus criterios de aceptación.
2. Leer conceptos y documentación oficial de la tecnología de esa fase.
3. Vos implementás los ejercicios, con pistas y ejemplos acotados cuando los necesites.
4. Revisamos código, contratos, tests y decisiones como en una revisión profesional.
5. Corregís los hallazgos y registrás una breve retrospectiva y una decisión técnica.
6. Mostrás una demo reproducible y explicás lo que aprendiste antes de avanzar.

No generar de una vez toda la aplicación. No incorporar dependencias de fases futuras para resolver problemas que todavía no tenemos. La implementación inicial usa datos sintéticos y evita correo, pagos o clientes reales.

## 2. Producto y caso de referencia

Pedido de referencia:

> “Buscá el cliente 245, revisá sus tickets abiertos, fijate si existe una solución documentada y, si no hay solución, creá un ticket y prepará un correo.”

El comportamiento esperado distingue una consulta, una propuesta y una acción ejecutada. Preparar un correo crea un borrador; enviar requiere una autorización independiente. Si ya existe un ticket equivalente, el asistente debe proponer reutilizarlo y evitar duplicados. Una búsqueda sin resultados significa que no se encontró evidencia suficiente, no que sea imposible que exista una solución.

Escenarios que crecerán junto con el proyecto:

| Escenario | Resultado esperado |
| --- | --- |
| Cliente existente con solución documentada | Resumen con tickets relevantes, solución y referencia verificable. |
| Cliente existente sin evidencia suficiente | Propuesta de ticket, tratamiento explícito de duplicados y borrador de correo. |
| Cliente inexistente o identificador inválido | Error controlado o aclaración; no inventar datos ni ejecutar escrituras. |
| API externa caída o con timeout | Fallo acotado, resultado incompleto explícito y recuperación o escalamiento. |
| Acción sin permiso o sin aprobación | Denegación o propuesta pendiente; ninguna mutación. |
| Documento con instrucciones maliciosas | Tratarlo como contenido, mantener permisos y no revelar datos fuera de alcance. |

Inventario evolutivo de capacidades:

- Lectura: `get_customer`, `get_customer_tickets`, `search_knowledge_base`, `retrieve_internal_documentation` y consultas a APIs externas.
- Escritura: `create_ticket`, `update_ticket` y preparación de borradores.
- Acción sensible: `send_customer_email`; `refund_payment` y `delete_customer` se usarán como casos de política, inicialmente sin integración ejecutable.

## 3. Arquitectura que debe sobrevivir a los frameworks

La dependencia de ejecución será:

**Framework de agentes → Agent → Tool Adapter → Application Service → Repository / External API**

El dominio contiene entidades, reglas y errores del negocio. Los servicios de aplicación coordinan casos de uso mediante interfaces de repositorios y clientes externos. La infraestructura implementa esas interfaces. Los frameworks viven en el borde de orquestación y sus adaptadores traducen schemas, llamadas y resultados.

Responsabilidades:

| Capa | Responsabilidad | Ejemplo |
| --- | --- | --- |
| Dominio | Reglas independientes de LLMs y frameworks | Cuándo un ticket puede cambiar de estado. |
| Application Service | Ejecutar un caso de uso, exigir autorización y coordinar dependencias | Crear un ticket respetando permisos e idempotencia. |
| Repository / External API | Leer y persistir datos, integrar sistemas | Repositorio en memoria; más adelante PostgreSQL y API de soporte. |
| Tool Adapter | Validar entrada y traducir resultados/errores al contrato de la tool | Convertir `customer_id` en una llamada a `CustomerService`. |
| Agent | Elegir el siguiente paso permitido y generar una respuesta | Consultar tickets y seleccionar una búsqueda. |
| Framework | Proporcionar ejecución, composición o transporte | LangGraph, ADK o CrewAI. |

Reglas de diseño:

- Dominio y servicios no importan LangChain, LangGraph, ADK ni CrewAI.
- Las tools no contienen reglas de tickets, SQL ni lógica de envío de correo. Pueden validar y serializar contratos, sin duplicar reglas del servicio.
- El LLM propone acciones; la aplicación valida identidad, alcance, permisos y condiciones. Un prompt no es una barrera de autorización.
- La identidad y el tenant provienen de un contexto confiable, nunca de argumentos inventados por el modelo.
- Los adapters de diferentes frameworks deben pasar los mismos tests de contrato contra los mismos servicios.
- Un error de negocio no se convierte en una respuesta exitosa porque el agente logre narrarlo.
- Primero interfaces pequeñas, repositorios en memoria e inyección explícita de dependencias. Agregar abstracciones cuando exista una segunda necesidad concreta.

Una organización posible, para crear por etapas, es `src/ai_operations_assistant/{domain,application,infrastructure,tools,agents}` y `tests/{unit,contract,integration,evaluation}`. El frontend se agregará después. No crear carpetas vacías solo para completar un esquema.

## 4. Orden y fundamentos transversales

Se conserva el orden solicitado: tool calling → loop → diseño de tools → LangChain → LangGraph → ADK → multiagentes ADK → CrewAI → Flows → RAG → state/memory → human-in-the-loop → MCP → A2A → evaluaciones → observabilidad → FastAPI → PostgreSQL → React → Docker/deployment.

Tres temas comienzan antes de su fase de profundización, por una razón técnica:

- **Structured outputs y testing desde la fase 1:** necesitamos verificar decisiones y contratos sin depender de comparar prosa.
- **Permisos y bloqueo de acciones sensibles desde la fase 3:** introducir escrituras sin una barrera determinista sería un diseño incorrecto. La fase 12 agrega aprobación, persistencia y reanudación completas.
- **Estado efímero y trazabilidad mínima desde el loop:** hay que correlacionar llamadas y evitar ciclos para depurarlo. Las fases 11 y 16 desarrollan persistencia, memoria y observabilidad de producción.

La búsqueda inicial será léxica sobre fixtures. RAG se incorpora en la fase 10 para aprender recuperación y grounding de manera independiente. Los frameworks se estudian uno por vez mediante experimentos equivalentes; no habrá tres implementaciones productivas permanentes.

### Contrato de tools

Cada tool debe documentar nombre claro, propósito, condiciones de uso, schema de entrada y salida, permisos, errores, efectos secundarios y política de timeout/reintento. Usar tipos explícitos y distinguir campos obligatorios de opcionales.

Contrato conceptual de resultado:

- Éxito: `status`, `data` y referencias de origen cuando corresponda.
- Error: `status`, `error.code`, mensaje seguro y `retryable` cuando sea relevante.
- El catálogo de errores distingue validación, no encontrado, permiso denegado, conflicto, timeout y dependencia no disponible.
- IDs de llamada y correlación van en metadata; no mezclar detalles del framework con entidades del dominio.

No exponer secretos, SQL, stack traces ni datos personales innecesarios al modelo. Describir qué hace la tool y cuándo usarla, sin instrucciones que permitan saltarse las políticas. Registrar límites de tamaño y paginación. Reintentar una lectura puede ser seguro; reintentar una escritura exige analizar idempotencia y un resultado ambiguo.

### Estrategia de testing

| Nivel | Qué valida | Cómo |
| --- | --- | --- |
| Unitario | Reglas, servicios, validación, políticas y transiciones | Fixtures pequeñas, reloj controlado y repositorios en memoria. |
| Contrato | Schemas de tools y equivalencia entre adapters | Mismas entradas válidas e inválidas; mismos resultados normalizados. |
| Orquestación determinista | Tool elegida, argumentos, límites, reintentos y efectos | Modelo/script de respuestas simulado y captura de llamadas reales al servicio. |
| Integración | SDK, API, almacenamiento y transporte | Dependencias reales o sandbox explícito con aislamiento. |
| Evaluación de agentes | Calidad de decisiones con modelos reales | Dataset versionado, repeticiones, métricas y costos. |

Verificar tools innecesarias, structured outputs válidos, escalamiento a humano y ausencia de efectos cuando se rechaza una acción. El texto final puede ser un criterio auxiliar; no será la única evidencia. Para resultados de lectura, comprobar datos y referencias; para escrituras, comprobar el estado persistido y el número de efectos.

Los tests rápidos no requieren credenciales. Separar claramente tests simulados de evaluaciones con LLM real. Temperatura baja y seed, cuando el proveedor la soporte, no garantizan determinismo. Registrar proveedor, modelo, configuración, prompts y versiones. Un test omitido por falta de credenciales no cuenta como aprobado.

### Evidencia de aprendizaje

Cada fase deja una demo, tests ejecutados, una explicación breve de arquitectura, errores encontrados y un ADR cuando haya una decisión significativa. El portfolio final debe incluir resultados medidos y limitaciones, además de capturas o videos. Las funcionalidades se consideran completas solo si se puede repetir la demostración.

## 5. Fases

### Fase 1 — Fundamentos de Tool Calling y outputs tipados

- **Objetivo técnico:** completar una interacción explícita con una sola tool de lectura, sin framework de agentes.
- **Conceptos:** mensajes, roles, schema JSON, tool request, ID de llamada, tool result, structured outputs y diferencia entre solicitar y ejecutar una función.
- **Funcionalidades:** fixture del cliente 245, servicio de consulta y adapter `get_customer`; inspección de una llamada propuesta por el modelo, ejecución local y respuesta basada en su resultado. Salida final con datos verificables y estado de la consulta.
- **Tecnologías:** Python, `venv`, `pytest`, Pydantic/JSON Schema y un SDK de proveedor elegido para esta fase. Fijar versiones tras comprobar compatibilidad; no instalar todos los frameworks.
- **Criterios de finalización:** la lógica de consulta funciona sin LLM; el adapter rechaza entradas inválidas; se muestra la secuencia mensaje → llamada → resultado → respuesta; se diferencia el modo simulado del proveedor real.
- **Tests esperados:** cliente existente/inexistente, ID inválido, resultado serializable, schema de salida y correspondencia del ID de tool call. Una prueba controlada verifica tool y argumentos; una demo real valida el protocolo si hay credenciales.
- **Riesgos o errores comunes:** ejecutar nombres arbitrarios, asumir que el modelo llamó a la función, inventar clientes o guardar claves en el repositorio.
- **Qué explicar en entrevista:** quién decide la llamada, quién la ejecuta y por qué un schema valida estructura pero no garantiza una decisión correcta.
- **Ejercicios que implementás vos:** construir la consulta del cliente 245; probar sus tres resultados principales; explicar y mostrar una interacción completa.

### Fase 2 — Agent loop explícito

- **Objetivo técnico:** convertir la interacción manual en un loop pequeño y controlado.
- **Conceptos:** ciclo observar/decidir/actuar, historial efímero, condición de salida, presupuesto de pasos y manejo de fallos.
- **Funcionalidades:** registro cerrado de tools, `get_customer_tickets`, devolución de resultados al modelo, límite de pasos/tiempo y detección de repeticiones. Manejo explícito de varias llamadas propuestas; inicialmente ejecución secuencial.
- **Tecnologías:** Python, SDK de la fase 1, reloj y modelo simulados, `pytest`.
- **Criterios de finalización:** resuelve cliente + tickets, termina ante respuesta final o presupuesto agotado y nunca ejecuta una tool desconocida. Distingue finalización exitosa de terminación incompleta.
- **Tests esperados:** secuencia correcta y argumentos, tool desconocida, JSON inválido, repetición, timeout y agotamiento de pasos. Verificar que no aparecen llamadas adicionales después de terminar.
- **Riesgos o errores comunes:** loops infinitos, historial creciente sin límite, reintentos sin presupuesto y creer que una respuesta final implica que la tarea se cumplió.
- **Qué explicar en entrevista:** qué hace que este loop sea un agente y qué responsabilidades deben ser deterministas.
- **Ejercicios que implementás vos:** escribir el loop, agregar límites y reproducir un modelo que insiste en repetir la misma consulta.

### Fase 3 — Diseño profesional de tools y servicios

- **Objetivo técnico:** crear contratos reutilizables y separar lectura, escritura y acciones sensibles antes de ampliar capacidades.
- **Conceptos:** puertos/adapters, permisos, idempotencia, errores de negocio, paginación, límites y retries.
- **Funcionalidades:** catálogo de tools; búsqueda léxica `search_knowledge_base`; `create_ticket`, `update_ticket` y borrador de correo sobre datos sintéticos. Políticas deterministas bloquean acciones sensibles y escrituras no autorizadas.
- **Tecnologías:** Python, Pydantic, servicios de aplicación, repositorios en memoria y clientes externos simulados.
- **Criterios de finalización:** los servicios se invocan sin agente; adapters delgados; crear dos veces con la misma clave de idempotencia produce un solo ticket; una misma clave con distinto contenido da conflicto. El contexto de permisos no puede ser reemplazado por el modelo.
- **Tests esperados:** contrato de cada tool, estados inválidos de ticket, duplicados, permisos, timeout externo, errores normalizados, paginación y ausencia de mutaciones al denegar.
- **Riesgos o errores comunes:** reglas dentro de tools, aceptar `tenant_id` como autoridad del LLM, retries que duplican tickets y considerar “sin resultados” equivalente a “no existe solución”.
- **Qué explicar en entrevista:** cómo diseñar una tool usable por el modelo y segura para el negocio; cuándo una operación es idempotente.
- **Ejercicios que implementás vos:** refactorizar las consultas a servicios compartidos; implementar creación idempotente y escribir una ficha de contrato por tool.

### Fase 4 — LangChain como capa de integración

- **Objetivo técnico:** aprender sus modelos, mensajes y tools manteniendo el dominio existente.
- **Conceptos:** interfaces de modelos, bindings de tools, composición, structured outputs y traducción de mensajes.
- **Funcionalidades:** adapter LangChain para las mismas consultas y caso cliente + tickets + búsqueda; contrastar la integración con el loop manual.
- **Tecnologías:** LangChain, integración del proveedor seleccionado y contratos Python existentes.
- **Criterios de finalización:** mismas entradas y resultados de negocio; ningún import de LangChain en dominio/servicios; diferencias de errores y llamadas documentadas.
- **Tests esperados:** contratos compartidos, argumentos equivalentes, errores del proveedor y structured output inválido. Smoke de integración separado de los tests simulados.
- **Riesgos o errores comunes:** usar helpers sin entender el protocolo, depender de APIs obsoletas o incorporar memoria implícita no evaluada.
- **Qué explicar en entrevista:** qué trabajo elimina LangChain y qué responsabilidades siguen siendo tuyas.
- **Ejercicios que implementás vos:** escribir los adapters y comparar una traza con el loop de la fase 2.

### Fase 5 — LangGraph y workflows con estado

- **Objetivo técnico:** expresar explícitamente estados y transiciones del caso de referencia.
- **Conceptos:** nodos, edges, estado tipado, reducers, checkpoints y rutas de error.
- **Funcionalidades:** grafo consultar cliente → tickets → buscar solución → responder o proponer ticket/borrador. Checkpoint local de aprendizaje; todavía sin un sistema de memoria de usuarios.
- **Tecnologías:** LangGraph, servicios compartidos y checkpointer compatible con la versión elegida.
- **Criterios de finalización:** las rutas son visibles, el estado contiene solo lo necesario y una reanudación no repite una escritura ya registrada. Las propuestas no se confunden con efectos ejecutados.
- **Tests esperados:** transiciones con/sin solución, cliente inexistente, recuperación desde checkpoint, reducers y fallo durante una ejecución.
- **Riesgos o errores comunes:** confundir checkpoint con memoria semántica, estado gigante, efectos laterales dentro de reducers y duplicar acciones al reanudar.
- **Qué explicar en entrevista:** cuándo un grafo aporta control sobre un loop y cómo se representa una decisión recuperable.
- **Ejercicios que implementás vos:** dibujar el grafo, implementarlo y provocar un fallo para demostrar recuperación.

### Fase 6 — Google ADK con un solo agente

- **Objetivo técnico:** implementar el mismo caso con ADK sin sumar agentes todavía.
- **Conceptos:** agente, runner, sesión, eventos, tools y outputs estructurados según capacidades de la versión.
- **Funcionalidades:** un agente de operaciones con adapters ADK, sesiones aisladas y límites; reutilizar los mismos servicios y fixtures.
- **Tecnologías:** Google ADK y un modelo/proveedor compatible. Verificar la compatibilidad real de autenticación, tool calling y schemas antes de elegirlo.
- **Criterios de finalización:** el caso equivalente funciona con un agente; no hay datos compartidos accidentalmente entre sesiones; se documentan cambios del contrato y costo del SDK.
- **Tests esperados:** contratos de tools, aislamiento de sesión, eventos de llamada/resultado, fallo de dependencia y salida estructurada. Integración real cuando exista acceso.
- **Riesgos o errores comunes:** trasladar reglas al prompt, asumir compatibilidad entre todos los modelos y confundir sesión con identidad autenticada.
- **Qué explicar en entrevista:** qué ofrece ADK frente al loop y al grafo; cómo fluye una llamada desde el runner al servicio.
- **Ejercicios que implementás vos:** implementar el adapter ADK y reproducir los escenarios ya resueltos.

### Fase 7 — Sistemas multiagente con ADK

- **Objetivo técnico:** comprobar si dividir responsabilidades aporta valor frente al único agente de la fase 6.
- **Conceptos:** delegación, secuencias/paralelismo, límites de contexto, coordinación y fallos parciales.
- **Funcionalidades:** experimento acotado con análisis de soporte, recuperación documental y coordinación; mantener el baseline de un agente con varias tools.
- **Tecnologías:** primitivas multiagente disponibles en ADK, schemas compartidos y fixtures comunes.
- **Criterios de finalización:** antes de implementarlo existe una ficha por agente con responsabilidad, contexto, tools, inputs, outputs, comunicación y costo de complejidad; se comparan calidad, llamadas, tokens y latencia. Si no mejora, se conserva el agente único.
- **Tests esperados:** handoff tipado, permisos por agente, pérdida de un colaborador, mensajes incompletos, límites de delegación y decisiones contradictorias. Comprobar que no se repiten consultas sin motivo.
- **Riesgos o errores comunes:** roles decorativos, todos los agentes con todos los permisos, debates sin fin y coordinación más costosa que la tarea.
- **Qué explicar en entrevista:** cuándo evitar multiagentes y qué evidencia justificaría incorporarlos.
- **Ejercicios que implementás vos:** escribir las fichas y el diseño alternativo de un agente; medir ambas opciones y defender una decisión.

### Fase 8 — CrewAI: agentes, tasks y crews

- **Objetivo técnico:** comprender la orquestación basada en roles y tareas mediante otro experimento equivalente.
- **Conceptos:** agent, task, crew, procesos, contexto entre tareas y contratos de salida.
- **Funcionalidades:** caso de operaciones con el número mínimo de agentes; adapters CrewAI sobre los mismos servicios; salida normalizada para comparación.
- **Tecnologías:** CrewAI y proveedor compatible; contrato común de tools y dataset sintético.
- **Criterios de finalización:** no duplicar lógica de negocio ni agregar agentes para satisfacer una estética; documentar qué decisiones controla CrewAI y cuáles controla la aplicación.
- **Tests esperados:** inputs/outputs de tareas, schemas, selección/argumentos de tools, orden de tareas, permisos y errores propagados.
- **Riesgos o errores comunes:** resultados en prosa usados como API, contextos enormes, delegación implícita y configuración que oculta decisiones importantes.
- **Qué explicar en entrevista:** cuándo el modelo de tareas de CrewAI simplifica un problema y cuándo agrega incertidumbre.
- **Ejercicios que implementás vos:** implementar el caso equivalente y comparar su comportamiento con ADK.

### Fase 9 — CrewAI Flows y decisión de framework

- **Objetivo técnico:** distinguir un workflow explícito de una crew y elegir una base para las fases restantes.
- **Conceptos:** estado de Flow, eventos, routing, persistencia disponible y mezcla de pasos deterministas con tareas de agentes.
- **Funcionalidades:** Flow para cliente → tickets → búsqueda → propuesta/respuesta; ejecutar una crew solo donde sea útil. Comparación formal LangChain/LangGraph, ADK y CrewAI/Flows.
- **Tecnologías:** CrewAI Flows y los prototipos de fases 4–8, probados secuencialmente si las dependencias requieren entornos separados.
- **Criterios de finalización:** caso y dataset idénticos, misma lógica y política, configuración/modelo lo más comparable posible; ADR con un framework seleccionado. Los otros prototipos quedan como experimentos documentados, sin compromiso de soporte productivo permanente.
- **Tests esperados:** rutas del Flow, errores y recuperación; ejecutar el conjunto común de contratos y escenarios sobre cada candidato. Registrar diferencias no controlables de proveedor.
- **Riesgos o errores comunes:** elegir por popularidad, confundir workflow con autonomía o declarar un ganador universal con una demo pequeña.
- **Qué explicar en entrevista:** cuándo usar LangGraph, ADK o CrewAI; qué herramientas ofrecen para controlar estado y workflows; cómo exponen tools; cuándo basta un agente simple.
- **Ejercicios que implementás vos:** completar la matriz siguiente, registrar resultados y defender la selección para este producto.

Matriz a completar con evidencia, sin puntajes inventados:

| Criterio | LangChain / LangGraph | Google ADK | CrewAI / Flows |
| --- | --- | --- | --- |
| Binding, validación y errores de tools | Por medir | Por medir | Por medir |
| Control de transiciones y estado | Por medir | Por medir | Por medir |
| Persistencia, recuperación y aprobación | Por medir | Por medir | Por medir |
| Composición de agentes y comunicación | Por medir | Por medir | Por medir |
| Testing y facilidad de depuración | Por medir | Por medir | Por medir |
| Calidad, llamadas innecesarias, costo y latencia | Por medir | Por medir | Por medir |
| Acoplamiento y esfuerzo para mantener el caso | Por medir | Por medir | Por medir |

### Fase 10 — RAG con fuentes y evaluación de recuperación

- **Objetivo técnico:** recuperar documentación pertinente y generar respuestas sustentadas en evidencia.
- **Conceptos:** ingestión, chunking, embeddings, búsqueda léxica/vectorial/híbrida, top-k, reranking, grounding y abstención.
- **Funcionalidades:** colección pequeña de documentos sintéticos, metadatos de acceso y versión; búsqueda con fuentes; `retrieve_internal_documentation` por ID autorizado; respuesta que cite fragmentos verificables.
- **Tecnologías:** framework seleccionado, modelo de embeddings y un índice local. Elegir una solución simple; PostgreSQL/pgvector se evalúa en la fase 18 si aporta valor.
- **Criterios de finalización:** fuentes trazables, documentos inaccesibles filtrados antes de entrar al contexto, reingestión sin duplicados y abstención sin evidencia suficiente. Comparar con la búsqueda léxica inicial.
- **Tests esperados:** documentos esperados en top-k, citas válidas, pregunta sin respuesta, permisos, documentos desactualizados y prompt injection dentro del contenido. Separar métricas del retriever de las del generador.
- **Riesgos o errores comunes:** creer que similitud significa veracidad, filtrar permisos después de generar, citar documentos no recuperados y medir RAG solo por prosa convincente.
- **Qué explicar en entrevista:** diferencia entre RAG y fine-tuning; cómo chunking y recuperación afectan calidad; por qué una cita no prueba por sí sola la respuesta.
- **Ejercicios que implementás vos:** crear un pequeño corpus con preguntas etiquetadas y analizar tres fallos de recuperación.

### Fase 11 — State, sesiones y Memory

- **Objetivo técnico:** persistir conversaciones y ejecuciones sin mezclar usuarios ni recordar información sin control.
- **Conceptos:** estado de ejecución, historial conversacional, memoria de largo plazo, checkpoints, TTL y resumen.
- **Funcionalidades:** `conversation_id`, sesiones vinculadas a identidad, recuperación tras reinicio y memoria opt-in de preferencias pertinentes. Inicialmente almacenamiento local compatible; migración al repositorio persistente en fase 18.
- **Tecnologías:** mecanismo de persistencia del framework seleccionado, interfaces de almacenamiento y reloj controlado.
- **Criterios de finalización:** separación explícita de estado/memoria; aislamiento por usuario/tenant; caducidad y eliminación verificables; el resumen conserva decisiones necesarias sin convertir contenido del usuario en instrucciones confiables.
- **Tests esperados:** reanudación, TTL, eliminación, contaminación entre conversaciones, memoria desactualizada y dos procesos que intentan avanzar una ejecución.
- **Riesgos o errores comunes:** recordar todo, tratar un resumen como fuente de verdad y usar memoria para evadir permisos de acceso.
- **Qué explicar en entrevista:** qué persistir, durante cuánto tiempo y cómo impedir que una memoria errónea contamine decisiones futuras.
- **Ejercicios que implementás vos:** diseñar la política de memoria y demostrar que dos clientes no comparten datos.

### Fase 12 — Human-in-the-loop y permisos de ejecución

- **Objetivo técnico:** pausar, aprobar, rechazar y reanudar acciones mediante decisiones verificables.
- **Conceptos:** mínimo privilegio, aprobación vinculada a una acción, expiración, revocación, auditoría y control de concurrencia.
- **Funcionalidades:** propuesta con argumentos inmutables, diff visible cuando corresponda y estado pendiente; aprobación por un actor autorizado, rechazo y escalamiento. La ejecución revalida permisos y estado, no solo el hecho de haber recibido una aprobación.
- **Tecnologías:** interrupción/reanudación del framework, servicio de políticas, registro persistente de aprobaciones e interfaz CLI inicial.
- **Criterios de finalización:** aprobar una propuesta no autoriza cambios posteriores en sus argumentos; no se ejecuta dos veces; rechazo/caducidad/revocación bloquean efectos; un cambio de estado relevante exige nueva evaluación.
- **Tests esperados:** aprobación válida, actor equivocado, argumentos alterados, rechazo, expiración, replay, permisos revocados y fallo ambiguo después de ejecutar el efecto.
- **Riesgos o errores comunes:** usar “sí” en el chat como identidad, autorización global, aprobación sin payload concreto y confiar en el estado recordado por el agente.
- **Qué explicar en entrevista:** cuándo permitir ejecución directa, cuándo pedir aprobación y cuándo prohibir; cómo evitar duplicados después de reanudar.
- **Ejercicios que implementás vos:** implementar una aprobación de ticket y demostrar el bloqueo de un envío de correo modificado después de aprobarse.

Política inicial del producto, ajustable mediante un ADR:

| Acción | Ejecución directa | Aprobación | Prohibición |
| --- | --- | --- | --- |
| `get_customer`, `get_customer_tickets`, `search_knowledge_base`, `retrieve_internal_documentation` / búsqueda documental | Con permiso de lectura y alcance correcto | Si la consulta excede el alcance habitual | Sin autorización o acceso a otro tenant. |
| Preparar borrador de correo | Con permiso, sin envío | Si incorpora información restringida que requiere revisión | Si pretende revelar datos no autorizados. |
| `create_ticket`, `update_ticket` | Solo política explícita para cambios de bajo riesgo; inicialmente modo propuesta | Por defecto, mostrando la mutación concreta | Sin permiso, transición inválida o recurso fuera de alcance. |
| `send_customer_email` / envío de email | Deshabilitada en el aprendizaje inicial | Actor autorizado revisa destinatario, asunto y cuerpo exactos, dentro de una política habilitada | Sin aprobación vigente, destinatario indebido o integración real no habilitada. |
| `refund_payment`, `delete_customer` | Nunca en el alcance inicial | Solo en una ampliación separada con controles específicos | Siempre en el alcance inicial; se evalúa la denegación sin ejecutar. |

Una aprobación no transforma una operación prohibida en permitida. Los permisos se aplican en servicios/adapters externos además de orientar al agente.

### Fase 13 — MCP: interoperabilidad de tools

- **Objetivo técnico:** exponer capacidades existentes como tools MCP y consumirlas desde un cliente separado.
- **Conceptos:** cliente/servidor, descubrimiento, schemas, transporte, resources frente a tools y frontera de confianza.
- **Funcionalidades:** servidor con consultas y búsqueda documental sobre servicios existentes; cliente agente; escritura primero solo en sandbox y con la política de aprobación existente.
- **Tecnologías:** SDK MCP compatible, transporte local para empezar y transporte HTTP soportado para el experimento remoto.
- **Criterios de finalización:** no duplicar lógica; contratos preservados; identidad/alcance explícitos; una desconexión produce un error controlado. La autenticación depende del transporte y no se presume por usar MCP.
- **Tests esperados:** listado y schema de tools, invocación válida/inválida, error remoto, límites, desconexión y acceso sin permisos. No aceptar instrucciones de un servidor como política interna.
- **Riesgos o errores comunes:** creer que MCP resuelve autorización, confiar ciegamente en servidores o reintentar efectos remotos ambiguos.
- **Qué explicar en entrevista:** qué estandariza MCP y qué sigue siendo responsabilidad de la aplicación.
- **Ejercicios que implementás vos:** exponer dos tools y ejecutar los mismos tests de contrato por llamada local y MCP.

### Fase 14 — A2A: colaboración entre agentes separados

- **Objetivo técnico:** estudiar la delegación entre servicios de agentes con un caso que justifique una frontera independiente.
- **Conceptos:** capacidades publicadas, agent card, tareas, estados, mensajes, artifacts, cancelación y autenticación entre servicios.
- **Funcionalidades:** servicio de consulta documental delegado por el asistente de operaciones; contrato tipado de solicitud/resultado y límites. Comparar contra una tool local/MCP y contra el multiagente interno.
- **Tecnologías:** SDK A2A y versión del protocolo fijados después de verificar documentación; dos procesos locales y datos sintéticos.
- **Criterios de finalización:** responsabilidad, contexto, tools, inputs, outputs, comunicación y costo del agente remoto documentados; identidad y permisos separados; beneficio o costo de la frontera medido.
- **Tests esperados:** descubrimiento, estados de tarea, cancelación, timeout, fallo parcial, respuesta incompatible, request duplicado y acceso no autorizado.
- **Riesgos o errores comunes:** usar A2A para cualquier función, asumir que los permisos del llamador se heredan y confundir artifacts con instrucciones confiables.
- **Qué explicar en entrevista:** MCP conecta herramientas y datos; A2A permite colaboración entre agentes. Cuándo un proceso remoto agrega más costo que valor.
- **Ejercicios que implementás vos:** construir la demo de dos servicios y un ADR que justifique mantenerla o dejarla como experimento.

### Fase 15 — Evaluaciones y regresiones de agentes

- **Objetivo técnico:** convertir los escenarios acumulados en un benchmark reproducible para decidir cambios.
- **Conceptos:** dataset, ground truth, métricas, variabilidad, evaluadores deterministas y jueces LLM con límites.
- **Funcionalidades:** casos versionados positivos, negativos y adversariales; reporte de tools, argumentos, efectos, decisiones, escalamiento, calidad de fuentes, costo y latencia. Comparar cambios de prompt/modelo contra un baseline.
- **Tecnologías:** `pytest`, runner de evaluación Python, fixtures JSON y proveedor real en un job separado con presupuesto.
- **Criterios de finalización:** al menos 30 casos con categorías explícitas; criterios esperados por caso; múltiples ejecuciones de casos estocásticos; reporte de errores y no solo promedio. Umbrales de regresión definidos antes de evaluar un cambio.
- **Tests esperados:** el evaluador detecta a propósito tool incorrecta, argumentos incorrectos, llamada innecesaria, output inválido, escritura no aprobada y escalamiento omitido. Ejecuciones simuladas no se reportan como evaluación del modelo real.
- **Riesgos o errores comunes:** adaptar el dataset a los ejemplos que pasan, usar un juez LLM como único árbitro, confundir validez sintáctica con éxito y omitir costos de reintentos.
- **Qué explicar en entrevista:** cómo evaluar un agente sin comparar texto exacto, qué medir y cómo distinguir variación del modelo de una regresión.
- **Ejercicios que implementás vos:** etiquetar el dataset, escribir evaluadores de decisiones y diagnosticar los cinco peores resultados.

### Fase 16 — Observabilidad y tracing

- **Objetivo técnico:** explicar una ejecución de punta a punta y detectar fallos operativos sin registrar secretos.
- **Conceptos:** logs estructurados, spans, correlación, métricas, contexto distribuido, sampling y redacción.
- **Funcionalidades:** trazas conversation → ejecución → agente → modelo → tool → servicio → dependencia. Registrar `conversation_id`, agente, modelo, tool calls, argumentos/resultados redactados, tokens de entrada/salida, latency, errores, retries y decisiones de aprobación.
- **Tecnologías:** logging estructurado y OpenTelemetry o integración de tracing compatible. Elegir un backend local/simple antes de incorporar SaaS.
- **Criterios de finalización:** reconstruir una consulta, una escritura aprobada y un fallo remoto; correlacionar MCP/A2A cuando sigan en alcance. Diferenciar tokens reales reportados por el proveedor de estimaciones o datos no disponibles.
- **Tests esperados:** propagación de IDs, spans de error, trazas durante reanudación y redacción de datos personales, tokens y correos. Verificar acceso/retención de trazas.
- **Riesgos o errores comunes:** registrar prompts completos con datos privados, IDs incoherentes, métricas sin denominador y un sistema de tracing que se vuelve requisito para responder.
- **Qué explicar en entrevista:** cómo encontrar una tool lenta, una llamada duplicada o una fuga de contexto mediante evidencia.
- **Ejercicios que implementás vos:** instrumentar el caso principal y analizar una ejecución fallida usando únicamente su traza.

### Fase 17 — Backend Python con FastAPI

- **Objetivo técnico:** ofrecer una API estable para conversaciones, ejecuciones y aprobaciones.
- **Conceptos:** HTTP, schemas, dependency injection, autenticación, autorización, trabajo en background y cancelación.
- **Funcionalidades:** crear conversación/ejecución, consultar su estado/resultados y aprobar/rechazar propuestas. Errores HTTP consistentes; identidad confiable en la entrada; streaming opcional después del flujo básico.
- **Tecnologías:** FastAPI, Pydantic, Uvicorn y HTTPX/TestClient. Para desarrollo, identidad simulada explícita; antes de deployment, mecanismo de autenticación real o acceso privado documentado.
- **Criterios de finalización:** servicios reutilizados sin lógica en handlers; no bloquear el event loop con SDKs síncronos; tareas largas tienen estados, límites y una estrategia de ejecución documentada. Reinicios no deben presentarse como éxitos de tareas perdidas.
- **Tests esperados:** ciclo API completo, validación, autenticación, aislamiento, aprobación por tercero, idempotencia y error de dependencia. Una petición funcional demuestra más que un healthcheck.
- **Riesgos o errores comunes:** exponer claves al cliente, confiar en IDs enviados como identidad, asumir durabilidad de background tasks y permitir acceso sin controles por tener una demo.
- **Qué explicar en entrevista:** diferencia entre orquestar una tarea y servir HTTP; cómo propagar identidad hasta un servicio.
- **Ejercicios que implementás vos:** implementar endpoints mínimos y un test API que recorra una propuesta y su rechazo.

### Fase 18 — PostgreSQL y persistencia durable

- **Objetivo técnico:** persistir clientes, tickets, conversaciones, ejecuciones y aprobaciones con integridad.
- **Conceptos:** modelo relacional, migraciones, índices, transacciones, restricciones, locks y control de versiones.
- **Funcionalidades:** adapters PostgreSQL, migraciones y seed sintético repetible; claves únicas de idempotencia, versionado de tickets y persistencia de ejecuciones. Evaluar pgvector solo si mejora el caso RAG.
- **Tecnologías:** PostgreSQL, SQLAlchemy/Alembic o driver elegido mediante ADR. Base local/servicio disponible; Docker será la distribución estándar en fase 20, no un requisito asumido aquí.
- **Criterios de finalización:** contratos del repositorio pasan con memoria y PostgreSQL; datos sobreviven reinicio; aislamiento y restricciones se verifican; ejecutar seed dos veces no duplica datos.
- **Tests esperados:** migración desde base vacía, transacciones, concurrencia en aprobación/tickets, idempotencia, aislamiento por tenant y recuperación. Probar restauración con datos sintéticos.
- **Riesgos o errores comunes:** mantener una transacción abierta durante una llamada al LLM, SQL en tools y prometer atomicidad entre la DB y un email externo. Estudiar outbox/deduplicación para efectos externos cuando se necesiten.
- **Qué explicar en entrevista:** qué garantiza una transacción y por qué un servicio externo impide asumir “exactly once”.
- **Ejercicios que implementás vos:** implementar los adapters y reproducir dos intentos concurrentes de crear el mismo ticket.

### Fase 19 — Frontend React para operar con confianza

- **Objetivo técnico:** permitir que una persona comprenda, revise y controle las acciones del asistente.
- **Conceptos:** estado de UI, contratos API, accesibilidad, loading/error y consistencia con el backend.
- **Funcionalidades:** conversación, tickets y fuentes; estados de ejecución; propuestas con destinatario/diff/payload; botones de aprobar/rechazar solo cuando corresponda. Mostrar borrador y enviado como estados diferentes.
- **Tecnologías:** React, TypeScript, Vite y cliente HTTP tipado. Elegir herramientas de tests de componentes y Playwright para un flujo real.
- **Criterios de finalización:** UI no trata una aprobación local como ejecución confirmada; estados y errores son comprensibles; no expone claves ni decide permisos finales. Evitar renderizar HTML no confiable de documentos/modelos.
- **Tests esperados:** lectura con fuentes, rechazo sin efectos, aprobación y resultado, fallo de red, doble clic, propuesta expirada y accesibilidad básica.
- **Riesgos o errores comunes:** interfaz de chat que oculta acciones, mutaciones optimistas peligrosas y confiar en que ocultar un botón protege el backend.
- **Qué explicar en entrevista:** cómo diseñar human-in-the-loop para que una persona entienda exactamente qué autoriza.
- **Ejercicios que implementás vos:** construir la pantalla de revisión de un ticket y probarla con una propuesta obsoleta.

### Fase 20 — Docker, deployment y portfolio reproducible

- **Objetivo técnico:** empaquetar y desplegar una demo reproducible con límites operativos claros.
- **Conceptos:** imágenes, servicios, configuración por entorno, secrets, health/readiness, CI y rollback.
- **Funcionalidades:** imágenes backend/frontend, entorno local con PostgreSQL, migraciones explícitas, jobs de tests/build, smoke funcional y deployment privado o sandbox. Acciones externas reales permanecen deshabilitadas salvo habilitación independiente.
- **Tecnologías:** Docker/Compose, CI del repositorio y un destino de deployment elegido según recursos y costo. Verificar disponibilidad del runtime; no asumir que el entorno cloud permite Docker anidado.
- **Criterios de finalización:** instalación desde checkout limpio, arranque documentado, operación funcional cliente 245, rechazo sin efectos, persistencia tras reinicio y procedimiento de rollback/restauración. Autenticación, TLS y manejo seguro de secretos definidos para el destino.
- **Tests esperados:** builds, migraciones, smoke end-to-end, readiness de dependencias, reinicio, límites de recursos y revisión de que las imágenes no contienen credenciales.
- **Riesgos o errores comunes:** tags/versiones flotantes, secretos en imágenes, publicar datos reales, asumir que un puerto abierto demuestra funcionamiento y permitir gasto de LLM sin límites.
- **Qué explicar en entrevista:** cómo desplegar, observar y recuperar el sistema; qué decisiones harías distintas con más tráfico o requisitos regulatorios.
- **Ejercicios que implementás vos:** desplegar la demo, ejecutar el runbook y preparar un recorrido de portfolio que incluya un fallo y su diagnóstico.

## 6. Cierre del proyecto y alcance del portfolio

La versión de portfolio debe mostrar el caso de referencia completo con datos sintéticos, fuentes verificables y aprobación explícita para las mutaciones definidas. Debe incluir arquitectura, ADR de framework, tests de contrato, evaluaciones, trazas redactadas y una guía reproducible de ejecución.

La demostración final incluye: consulta exitosa, ausencia de solución, ticket duplicado evitado, propuesta rechazada sin efectos, acción aprobada una sola vez, dependencia caída y aislamiento entre usuarios. Debe declarar qué acciones son simuladas y qué integraciones son reales.

Fuera del alcance inicial: pagos reales, eliminación de clientes reales, tres backends de agentes productivos, conectores empresariales sin permisos, soporte multitenant a escala y autonomía sin límites. Cada ampliación requiere un objetivo, tests y una decisión técnica propios.

Un buen relato de entrevista conecta un problema con alternativas, decisión, implementación, evidencia y límites. No alcanza con enumerar frameworks.

## 7. Sprint 1 — Una consulta de cliente y una tool real

### Definición

**Meta:** comprender y demostrar una interacción de tool calling para consultar el cliente 245, con lógica de aplicación independiente del proveedor. El sprint cubre una parte acotada de la fase 1; no incluye loop autónomo, escrituras, RAG ni framework de agentes.

Cadencia sugerida: cinco sesiones ajustables a tu disponibilidad. Mantener aproximadamente 20% de lectura/discusión y 80% de implementación/tests. No dar por terminado el sprint únicamente porque haya transcurrido una semana.

1. Contratos, entorno Python mínimo y consulta de cliente sin LLM.
2. Tests de servicio y adapter, errores y schema de tool.
3. Interacción simulada: solicitud, ejecución y devolución del resultado.
4. Una integración de proveedor y demo real, si existe acceso configurado.
5. Revisión, correcciones, demo reproducible y explicación técnica.

### Entregables del Sprint 1

- Proyecto Python mínimo con instrucciones de instalación y ejecución, versiones fijadas mediante el mecanismo elegido y `pytest`.
- Entidad/contrato `Customer` con campos mínimos: ID, nombre y email sintéticos; interfaz `CustomerRepository`, implementación en memoria y `CustomerService.get_customer`.
- Fixture determinista para el cliente 245 y comportamiento definido para cliente inexistente e ID inválido.
- Adapter `get_customer` con descripción útil, schema tipado y resultado estructurado. Ninguna escritura ni llamada a un sistema de clientes real.
- Una demostración controlada del protocolo con proveedor simulado y una integración SDK separada. La respuesta final debe usar los datos efectivamente devueltos por la tool.
- Tests unitarios y de contrato ejecutados; una captura/traza redactada que muestre tool, argumentos, ID de llamada y resultado.
- Nota breve sobre separación de capas, errores encontrados y limitaciones. No guardar claves ni dumps del entorno.

### Criterios de aceptación

1. La consulta del cliente 245 devuelve exactamente el fixture esperado; se puede ejecutar sin SDK, red ni credenciales.
2. Un ID inválido se rechaza antes de consultar el repositorio. Un ID válido inexistente genera un resultado `customer_not_found` definido, sin datos inventados.
3. El adapter no contiene el dataset ni lógica de acceso; delega en el servicio y produce JSON conforme al schema.
4. La prueba controlada exige `get_customer` con `customer_id=245`, ejecuta el servicio y asocia el resultado al ID correcto de la llamada. Un nombre desconocido no se ejecuta.
5. Tests rápidos reproducibles pasan en un entorno limpio. La explicación demuestra por qué solicitar una tool y ejecutarla son pasos diferentes.
6. Una demo con el proveedor real completa mensaje → tool call → resultado → respuesta con structured output válido. Documentar modelo y configuración; no exigir que todas las respuestas en lenguaje natural sean idénticas.
7. Si faltan credenciales, quedan completos los entregables locales y se informa **integración real pendiente**. No declarar terminado el criterio 6 ni pedir claves por chat: configurar el valor por el mecanismo seguro disponible.
8. La revisión confirma independencia del dominio, ausencia de secretos y ninguna acción de escritura.

### Primera tarea que deberías implementar vos

**Implementá la consulta de cliente sin LLM ni framework.**

1. Definí el contrato mínimo de `Customer` y qué significa un `customer_id` válido; para el primer caso, un entero positivo estricto.
2. Definí una interfaz pequeña `CustomerRepository` para consultar por ID, con resultado explícito cuando no existe.
3. Implementá un repositorio en memoria con el cliente sintético 245.
4. Implementá `CustomerService.get_customer`, que valida el ID y delega la consulta. Mantené el servicio separado de la implementación en memoria.
5. Escribí tests para cliente 245, cliente inexistente e ID inválido. Incluí un repositorio espía para demostrar que una entrada inválida no dispara acceso a datos.

**Entrega para la primera revisión:** código de esos contratos/servicio/repositorio, tests ejecutados y una explicación corta de dónde vive cada responsabilidad. Todavía no implementes el adapter del LLM: primero revisamos esta base y después conectamos la tool.
