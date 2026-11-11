from django.http import JsonResponse
from django.shortcuts import render

from .conversiones import BASES, ErrorConversion, convertir


ANCHOS_PERMITIDOS = {8, 16, 32, 64}


def _parametro_entero(request, nombre, por_defecto):
    valor = request.GET.get(nombre)
    if valor is None:
        return por_defecto
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ErrorConversion(f'El parámetro "{nombre}" debe ser un entero')


def index(request):
    return render(request, "conversor/index.html", {"bases": BASES.items()})


def api_convertir(request):
    if request.method != "GET":
        respuesta = JsonResponse({"error": "Método no permitido"}, status=405)
        respuesta["Allow"] = "GET"
        return respuesta

    texto = request.GET.get("valor", "")
    if len(texto) > 2000:
        return JsonResponse({"error": "El número es demasiado largo"}, status=400)

    try:
        if not texto.strip():
            raise ErrorConversion('El parámetro "valor" es obligatorio')
        base = _parametro_entero(request, "base", 10)
        ancho = _parametro_entero(request, "ancho", 8)
        if ancho not in ANCHOS_PERMITIDOS:
            raise ErrorConversion('El parámetro "ancho" debe ser 8, 16, 32 o 64')
        datos = convertir(
            texto,
            base=base,
            ancho=ancho,
        )
    except ErrorConversion as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"datos": datos})
