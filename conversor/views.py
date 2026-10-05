from django.http import JsonResponse
from django.shortcuts import render

from .conversiones import BASES, ErrorConversion, convertir


def _entero(valor, por_defecto):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return por_defecto


def index(request):
    return render(request, "conversor/index.html", {"bases": BASES.items()})


def api_convertir(request):
    texto = request.GET.get("valor", "")
    if len(texto) > 2000:
        return JsonResponse({"error": "El número es demasiado largo"}, status=400)
    try:
        datos = convertir(
            texto,
            base=_entero(request.GET.get("base"), 10),
            ancho=_entero(request.GET.get("ancho"), 8),
        )
    except ErrorConversion as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"datos": datos})
