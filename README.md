# Proyecto Final — Automation Testing

Framework de automatización de pruebas **UI** (SauceDemo) y **API** (ReqRes) desarrollado con **Python**, **Pytest**, **Selenium** y **Requests**.

**Autor:** Luis Malave  
**Repositorio:** [proyecto-final-automation-testing-luis-malave](https://github.com/LuisAdonais/proyecto-final-automation-testing-luis-malave)

---

## Estructura del proyecto

```
proyecto-final-automation-testing-luis-malave/
├── pages/              # Page Object Model (UI)
├── tests/
│   ├── ui/             # Pruebas SauceDemo
│   └── api/            # Pruebas ReqRes
├── data/               # Datos externos JSON
├── utils/              # Logger y helpers
├── reports/            # Reporte HTML y log de ejecución
├── screenshots/        # Capturas en fallos UI
├── scripts/            # Scripts de ejecución
├── conftest.py         # Fixtures y hooks globales
├── pytest.ini          # Configuración de Pytest
└── requirements.txt    # Dependencias
```

---

## Requisitos

- Python 3.11 o superior
- Firefox instalado (para pruebas UI)
- Cuenta en [ReqRes](https://reqres.in/) con API key (para pruebas API)

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/LuisAdonais/proyecto-final-automation-testing-luis-malave.git
cd proyecto-final-automation-testing-luis-malave

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env   # Windows
# cp .env.example .env       # Linux / macOS
```

Editar `.env` y agregar tu API key de ReqRes:

```
REQRES_API_KEY=tu_api_key_aqui
```

---

## Ejecución de pruebas

```bash
# Suite completa
pytest

# Solo UI
pytest tests/ui/
pytest -m ui

# Solo API
pytest tests/api/
pytest -m api

# Un test individual
pytest tests/ui/test_saucedemo.py::test_tc_ui_04_agregar_producto_al_carrito -v
```

También puedes usar el script:

```powershell
.\scripts\ejecutar_suite.ps1
```

---

## Reportes y evidencias

| Artefacto | Ubicación |
|-----------|-----------|
| Reporte HTML | `reports/reporte.html` |
| Log de ejecución | `reports/ejecucion.log` |
| Screenshots (fallos UI) | `screenshots/failure_*.png` |

Los screenshots se incrustan automáticamente en el reporte HTML cuando falla un test UI.

---

## Ramas de desarrollo

El proyecto se desarrolló con ramas por funcionalidad, fusionadas a `main`:

| Rama | Contenido |
|------|-----------|
| `feature/project-structure` | Estructura base, Page Objects, datos JSON, tests UI |
| `feature/api-tests` | Pruebas API contra ReqRes |
| `feature/reports-logging` | Logging, reporte HTML y screenshots |
| `feature/github-actions` | Pipeline CI/CD en GitHub Actions |
| `feature/stability-cleanup` | Waits explícitos, legibilidad y estabilidad |
| `feature/readme` | Documentación del proyecto |

Flujo de trabajo:

```bash
git checkout -b feature/nueva-funcionalidad
# ... desarrollar y commitear ...
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

---

## CI/CD (GitHub Actions)

El workflow `.github/workflows/tests.yml` ejecuta en cada push/PR a `main`:

- **api-tests** — pruebas API con secret `REQRES_API_KEY`
- **ui-tests** — pruebas UI con Firefox headless

Configurar el secret en: **Settings → Secrets and variables → Actions → New repository secret**

---

## Casos de prueba

### UI (SauceDemo) — 9 ejecuciones

| ID | Descripción |
|----|-------------|
| TC_UI_01 | Login parametrizado (positivo y negativo) |
| TC_UI_02 | Navegación al catálogo |
| TC_UI_03 | Filtro por precio |
| TC_UI_04 | Agregar producto al carrito |
| TC_UI_05 | Remover producto del carrito |
| TC_UI_06 | Checkout completo exitoso |
| TC_UI_07 | Checkout sin datos obligatorios |

### API (ReqRes) — 5 tests

| ID | Descripción |
|----|-------------|
| TC_API_01 | GET usuario existente |
| TC_API_02 | POST crear usuario |
| TC_API_03 | DELETE usuario |
| TC_API_04 | GET usuario no encontrado (negativo) |
| TC_API_05 | Encadenamiento demostrativo |

---

## Tecnologías

- **Selenium WebDriver** + WebDriverWait
- **Pytest** + pytest-html
- **Requests**
- **Page Object Model**
- **Git / GitHub**
