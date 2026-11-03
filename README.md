# UTN PROG4 TP1 - Backend FastAPI

API REST desarrollada con **FastAPI** y **Pydantic** para la cátedra de Programación 4. Implementa un sistema de gestión en memoria (ABM de Usuarios y Productos) con arquitectura basada en rutas, tipado estricto y validación automática de datos.

> **Importante:** Los datos se almacenan en memoria volátil. El estado se reinicia cada vez que el servidor recarga (Hot Reload) al guardar un archivo.

## 🚀 Tecnologías
- **Python 3.11** (Entorno de ejecución base)
- **FastAPI 0.141** (Framework Web asíncrono para routing y API REST)
- **Pydantic 2** (Validación estricta de esquemas de datos y serialización)
- **Uvicorn** (Servidor ASGI de alto rendimiento)
- **Pyright & Pycodestyle** (Herramientas de linting PEP 8 y chequeo estático de tipos)

## 🏗️ Arquitectura
El proyecto sigue una estructura modular para separar responsabilidades y facilitar su escalabilidad:
- `main.py (Entrypoint)`: Punto de entrada de la aplicación. Inicializa la instancia de FastAPI y orquesta la inyección de los diferentes enrutadores mediante `app.include_router`.
- `models/ (Data Layer & Schemas)`: Centraliza las clases de Pydantic (`BaseModel`). Define el contrato estricto de entrada y salida de la API (Request/Response), actuando como escudo validador antes de que los datos toquen la lógica de negocio.
- `routers/ (Controllers)`: Aísla la lógica de las rutas HTTP (`@router.get`, `@router.post`, etc.) agrupadas por entidad. Actualmente también gestiona el estado en memoria (`list[User]`) como fuente de verdad temporal.
- `In-Memory Persistence (Pattern)`: Implementación de almacenamiento efímero usando listas nativas de Python (List Comprehensions y Mutaciones). Ideal para el cumplimiento de la consigna actual sin dependencias externas de bases de datos.
- `Fail-Fast Validation (Pattern)`: Aprovechamiento del motor de Pydantic para rechazar requests malformadas automáticamente (422 Unprocessable Entity) sin necesidad de escribir validaciones manuales (`if/else`) en los endpoints.

## ⚙️ Instalación y Entorno

**1. Clonar el repositorio**
```bash
git clone https://github.com/FefeSaenz/utn-prog4-tp1-fastapi.git
cd utn-prog4-tp1-fastapi
```

**2. Crear y activar el entorno virtual**
```bash
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

**3. Instalar las dependencias**
```bash
pip install -r requirements.txt
```

## 🚀 Levantar la Aplicación
Con el entorno virtual activado, iniciar el servidor en modo desarrollo (con recarga automática):
```bash
fastapi dev main.py
```
La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

## 📖 Documentación Interactiva (Swagger)
FastAPI autogenera la interfaz visual de pruebas basándose en los tipos de Pydantic y las firmas de las funciones. Para usarla:
1. Con la aplicación levantada, abre **http://127.0.0.1:8000/docs** en tu navegador.
2. Despliega el endpoint que deseas probar.
3. Presiona **Try it out**.
4. Completa los parámetros de consulta (query params) o el cuerpo de la petición (JSON body).
5. Presiona **Execute** y evalúa los códigos HTTP de respuesta.

## 📌 Endpoints de Usuarios

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| `GET` | `/user` | Lista usuarios. Query param opcional `is_active` (`true`/`false`) para filtrar por estado. | 200 |
| `POST` | `/user` | Crea un usuario (`id`, `name`, `is_active` opcional, por defecto `true`). | 201, 409 si el id ya existe, 422 |
| `PUT` | `/user/{id}` | Reemplaza los datos del usuario (`name`, `is_active` opcional). El id no va en el body: se toma de la URL. | 200, 404 si no existe, 422 |
| `DELETE` | `/user/{id}` | Elimina un usuario. | 200, 404 si no existe |

Ejemplo de body para `PUT /user/1`:
```json
{ "name": "juan actualizado", "is_active": false }
```

## 🔍 Lint y chequeo de tipos
El proyecto incluye configuración local para dos herramientas:
- **`setup.cfg`**: configuración de pycodestyle (chequeo de estilo PEP 8). Define `max-line-length = 130` y excluye `.venv` y `__pycache__` del análisis.
- **`pyrightconfig.json`**: configuración de pyright (chequeo de tipos). Apunta al entorno virtual local (`.venv`) para resolver las dependencias instaladas y excluye `.venv` y `__pycache__`.

`pyright` ya está incluido en `requirements.txt`. `pycodestyle` no, así que hay que instalarlo aparte.
Con el entorno virtual activado, correr:
```bash
pip install pycodestyle
python -m pycodestyle .
pyright
```

## ✅ Logros y Avances

**Parte 1: Usuarios**
- [x] ~~Alta y listado~~ (Implementación de HTTP 201 Created y protección 409 Conflict contra IDs duplicados).
- [x] ~~Eliminar por id~~ (Implementación de HTTP 404 Not Found para IDs inexistentes).
- [x] ~~Filtrar por estado~~ (Inyección de query param opcional `is_active` procesado vía List Comprehension).
- [x] ~~Modificar~~ (Endpoint `PUT /user/{id}` que reemplaza integralmente el registro; el id se toma de la URL y responde HTTP 404 Not Found si no existe).

**Entrega**
- [x] ~~README con instrucciones de uso y arquitectura detallada.~~

## 🛠️ Próximos Pasos

**Parte 2: Productos**
- [ ] **Crear modelo base:** Estructurar `models/products.py` con atributos propios de negocio.
- [ ] **Crear (POST):** Endpoint de alta con validación de existencia previa.
- [ ] **Listar (GET):** Retornar el catálogo completo en memoria.
- [ ] **Obtener por id (GET):** Búsqueda puntual mediante Path Parameter.
- [ ] **Modificar (PUT):** Actualización de propiedades del producto.
- [ ] **Eliminar (DELETE):** Baja del catálogo.
- [ ] **Buscar o filtrar (GET):** Implementar query params para refinar la búsqueda del listado principal.