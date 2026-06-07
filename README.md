# 🌴 Turismo RD – Plataforma de Reservas y Ofertas Turísticas

> Plataforma web fullstack para gestionar ofertas turísticas y reservas en la República Dominicana.  
> Construida con **Reflex** (frontend/backend Python) + **FastAPI** (API REST) + **MySQL** (base de datos).

---

## 📸 Vistas del Proyecto

| Inicio | Descripción | Reservas |
|---|---|---|
| Hero + buscador + ofertas | Galería + itinerario + precio | Formulario multi-paso + resumen |

---

## 🏗️ Arquitectura

```
turismo-app/
├── turismo_app/              # App Reflex (frontend + estado)
│   ├── pages/
│   │   ├── index.py          # Página de Inicio
│   │   ├── descripcion.py    # Página de Descripción
│   │   └── reservas.py       # Página de Reservas
│   ├── components/
│   │   └── __init__.py       # Navbar, Footer, Cards, estilos
│   ├── state.py              # Estado global + cliente API
│   └── turismo_app.py        # Punto de entrada Reflex
├── api/
│   └── main.py               # API REST FastAPI + modelos SQLAlchemy
├── database/
│   └── setup.sql             # Script de inicialización MySQL
├── pyproject.toml            # Dependencias Poetry
├── rxconfig.py               # Configuración Reflex
├── render.yaml               # Despliegue en Render
├── .env.example              # Variables de entorno de ejemplo
└── README.md
```

---

## ⚙️ Requisitos

- Python **3.11+**
- [Poetry](https://python-poetry.org/docs/#installation) `pip install poetry`
- MySQL **8.0+** (local o en la nube)
- Node.js **18+** (requerido por Reflex internamente)

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/turismo-app.git
cd turismo-app
```

### 2. Instalar dependencias con Poetry

```bash
poetry install
poetry shell          # Activa el entorno virtual
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus credenciales de MySQL
```

### 4. Inicializar la base de datos MySQL

```bash
mysql -u root -p < database/setup.sql
```

### 5. Ejecutar la API (terminal 1)

```bash
uvicorn api.main:app --reload --port 8000
# → Documentación interactiva: http://localhost:8000/docs
```

### 6. Ejecutar el frontend Reflex (terminal 2)

```bash
reflex run
# → http://localhost:3000
```

---

## 🔌 API REST – Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/ofertas` | Listar todas las ofertas (soporta filtros: `?destino=&precio_max=`) |
| `GET` | `/ofertas/{id}` | Obtener una oferta por ID |
| `POST` | `/reservas` | Crear una nueva reserva |
| `GET` | `/reservas` | Listar reservas (filtro opcional: `?email=`) |
| `GET` | `/reservas/{id}` | Ver detalle de una reserva |
| `DELETE` | `/reservas/{id}` | Cancelar una reserva |

### Ejemplo: Crear reserva

```bash
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/json" \
  -d '{
    "oferta_id": 1,
    "nombre_cliente": "Juan Pérez",
    "email_cliente": "juan@email.com",
    "telefono_cliente": "+1 809 555 1234",
    "cantidad_personas": 2,
    "fecha_viaje": "2025-03-15",
    "metodo_pago": "tarjeta"
  }'
```

---

## 🌿 GitFlow – Estructura de Ramas

```
main          ← producción estable
develop       ← integración
├── feature/pagina-inicio
├── feature/pagina-descripcion
├── feature/pagina-reservas
├── feature/api-ofertas
├── feature/api-reservas
└── feature/deploy-render
```

Comandos básicos:

```bash
git checkout -b feature/nueva-funcionalidad develop
# ... commits ...
git checkout develop && git merge --no-ff feature/nueva-funcionalidad
```

---

## ☁️ Despliegue en Render

1. Sube el proyecto a GitHub
2. Ve a [render.com](https://render.com) → **New → Blueprint**
3. Conecta tu repositorio (detectará `render.yaml` automáticamente)
4. Configura las variables de entorno de MySQL en el dashboard
5. ¡Deploy automático en cada push a `main`!

### Variables de entorno en Render

| Variable | Descripción |
|----------|-------------|
| `DB_HOST` | Host MySQL (ej: `db.render.com`) |
| `DB_USER` | Usuario MySQL |
| `DB_PASSWORD` | Contraseña MySQL |
| `DB_NAME` | Nombre de la base de datos |

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 📦 Tecnologías

| Capa | Tecnología |
|------|-----------|
| Frontend | [Reflex](https://reflex.dev) (Python → React) |
| API | [FastAPI](https://fastapi.tiangolo.com) |
| ORM | [SQLAlchemy 2.0](https://sqlalchemy.org) |
| Base de datos | MySQL 8 + PyMySQL |
| Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Gestor de paquetes | [Poetry](https://python-poetry.org) |
| Despliegue | [Render](https://render.com) |
| Control de versiones | Git + GitFlow |

---

## 👥 Créditos

Proyecto desarrollado por Miguel Angel Vargas – Desarrollo Web.

### 🔗 Enlaces útiles

- [Reflex Docs](https://reflex.dev/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Poetry Docs](https://python-poetry.org/docs)
- [Render Docs](https://render.com/docs)
- [GitFlow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

---

> Hecho con ❤️ y ☕ en la República Dominicana 🇩🇴
