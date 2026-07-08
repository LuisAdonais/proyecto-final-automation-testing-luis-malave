# scripts/ejecutar_suite.ps1
# Comandos de verificacion del framework (EPIC 08 - Ticket 33).

python -m pytest
python -m pytest tests/ui/
python -m pytest tests/api/
python -m pytest -m api
python -m pytest -m ui
