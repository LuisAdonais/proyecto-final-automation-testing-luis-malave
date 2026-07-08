# Proyecto Final — Automation Testing

**Curso:** Talento Tech  
**Autor:** Luis Malave  
**Repositorio:** [proyecto-final-automation-testing-luis-malave](https://github.com/LuisAdonais/proyecto-final-automation-testing-luis-malave)

---

## Propósito del proyecto

Framework de automatización de pruebas **UI** (SauceDemo) y **API** (ReqRes) desarrollado con **Python**, **Pytest**, **Selenium** y **Requests**.

El objetivo es demostrar un framework completo y mantenible que:

- Automatice flujos reales de una aplicación web con **Page Object Model**
- Valide endpoints REST con distintos métodos HTTP
- Genere reportes visuales y logs para facilitar la depuración
- Sea fácil de extender con nuevos casos de prueba

---

## Tecnologías

- **Python** — lenguaje principal
- **Pytest** + **pytest-html** — ejecución y reportes
- **Selenium WebDriver** + WebDriverWait — pruebas UI
- **Requests** — pruebas API
- **Page Object Model** — organización del código
- **Git / GitHub** — control de versiones y CI/CD

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

### Cómo interpretar los reportes

**Reporte HTML (`reports/reporte.html`)**

1. Abrir el archivo en el navegador después de ejecutar `pytest`.
2. Revisar el resumen superior: cantidad de tests **Passed**, **Failed** y **Skipped**.
3. En la tabla de resultados, cada fila muestra:
   - **Nombre del test**
   - **Estado** (verde = pasó, rojo = falló)
   - **Duración** en segundos
4. Si un test UI falló, el reporte incluye la **captura de pantalla incrustada** al final de la fila del test.

**Log de ejecución (`reports/ejecucion.log`)**

- Registra inicio/fin de cada test, apertura/cierre del navegador y códigos HTTP de las pruebas API.
- Útil para depurar: buscar el nombre del test que falló y revisar los mensajes anteriores al error.

**Screenshots (`screenshots/`)**

- Se generan solo cuando falla un test UI.
- Nombre descriptivo: `failure_{nombre_test}_{fecha_hora}.png`

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

El workflow **Automation Testing CI** (`.github/workflows/tests.yml`) se ejecuta en:

- Push a `main`
- Pull request hacia `main`
- Ejecución manual (`workflow_dispatch`)

Pasos que realiza:

1. Checkout del código
2. Configuración de Python 3.12 y Firefox
3. Instalación de dependencias
4. Ejecución de `pytest` (suite completa UI + API)
5. Subida de `reports/` y `screenshots/` como artefacto **`reportes-automation-testing`**

Configurar el secret en: **Settings → Secrets and variables → Actions → New repository secret**

Nombre del secret: `REQRES_API_KEY`

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
