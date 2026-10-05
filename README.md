# Conversor Numérico (Django)

Convierte números entre binario, octal, decimal y hexadecimal. Incluye visualizador de bits interactivo (complemento a 2).

## Ejecutar en localhost

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Abre http://127.0.0.1:8000

- Lógica de conversión: `conversor/conversiones.py`
- API JSON: `GET /api/convertir/?valor=FF&base=16`
- Tests: `python manage.py test`
