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
- API JSON: `GET /api/convertir/?valor=FF&base=16&ancho=8`
- Tests: `python manage.py test`

### API de conversión

`GET /api/convertir/` recibe estos parámetros:

| Parámetro | Requerido | Valores | Predeterminado |
|---|---|---|---|
| `valor` | Sí | Número en la base indicada; admite prefijos y guiones bajos | — |
| `base` | No | `2`, `8`, `10` o `16` | `10` |
| `ancho` | No | `8`, `16`, `32` o `64` bits | `8` |

Una conversión válida responde con HTTP `200` y un objeto `datos` que contiene
`valor`, `base`, `resultados`, `bits` e `info`. Por ejemplo, los errores usan:

```json
{
  "error": "La base debe ser 2, 8, 10 o 16"
}
```

Las entradas inválidas responden con HTTP `400` y `{"error": "..."}`. Los métodos
distintos de GET responden con HTTP `405`, el encabezado `Allow: GET` y el mismo
formato JSON de error. Los números de más de 2000 caracteres se rechazan.
