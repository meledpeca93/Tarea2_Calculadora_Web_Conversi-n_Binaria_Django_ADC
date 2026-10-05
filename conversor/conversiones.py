DIGITOS = "0123456789ABCDEF"
BASES = {2: "Binario", 8: "Octal", 10: "Decimal", 16: "Hexadecimal"}
PREFIJOS = {2: "0b", 8: "0o", 16: "0x"}


class ErrorConversion(ValueError):
    pass


def validar_base(base):
    if base not in BASES:
        raise ErrorConversion("La base debe ser 2, 8, 10 o 16")


def parsear(texto, base):
    validar_base(base)
    texto = "".join(texto.split()).replace("_", "")
    if not texto:
        return None
    negativo = texto[0] == "-"
    if texto[0] in "+-":
        texto = texto[1:]
    prefijo = PREFIJOS.get(base)
    if prefijo and texto.lower().startswith(prefijo):
        texto = texto[2:]
    if not texto:
        raise ErrorConversion("Número incompleto")
    valor = 0
    for ch in texto.upper():
        d = DIGITOS.find(ch)
        if d < 0 or d >= base:
            validos = " ".join(DIGITOS[:base])
            raise ErrorConversion(f'El dígito "{ch}" no es válido en base {base} (usa: {validos})')
        valor = valor * base + d
    return -valor if negativo else valor


def a_base(valor, base):
    validar_base(base)
    if valor == 0:
        return "0"
    signo, n, out = ("-" if valor < 0 else ""), abs(valor), []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITOS[r])
    return signo + "".join(reversed(out))


def agrupar(texto, n, sep=" "):
    signo = "-" if texto.startswith("-") else ""
    texto = texto.lstrip("-")
    texto = texto.zfill(-(-len(texto) // n) * n)
    return signo + sep.join(texto[i:i + n] for i in range(0, len(texto), n))


def con_prefijo(valor, base):
    return ("-" if valor < 0 else "") + PREFIJOS[base] + a_base(abs(valor), base)


def ancho_minimo(valor):
    bits = ((-valor - 1).bit_length() + 1) if valor < 0 else valor.bit_length()
    bits = max(bits, 1)
    for w in (8, 16, 32, 64, 128):
        if bits <= w:
            return w
    return -(-bits // 8) * 8


def convertir(texto, base=10, ancho=8):
    valor = parsear(texto, base)
    if valor is None:
        return None
    ancho = max(ancho, ancho_minimo(valor))
    sin_signo = valor % (1 << ancho)
    con_signo = sin_signo - (1 << ancho) if sin_signo >> (ancho - 1) else sin_signo
    absoluto = abs(valor)
    bits_necesarios = max(absoluto.bit_length(), 1)
    binario, decimal, hexa = a_base(valor, 2), str(valor), a_base(valor, 16)
    bits = format(sin_signo, f"0{ancho}b")

    return {
        "valor": decimal,
        "base": base,
        "resultados": [
            {"nombre": "Binario", "etiqueta": "base 2", "valor": binario,
             "pista": "Agrupado: " + agrupar(binario, 4), "color": "#7c5cff"},
            {"nombre": "Octal", "etiqueta": "base 8", "valor": a_base(valor, 8),
             "pista": "Prefijo: " + con_prefijo(valor, 8), "color": "#ff9f43"},
            {"nombre": "Decimal", "etiqueta": "base 10", "valor": decimal,
             "pista": "Con separadores: " + f"{valor:,}".replace(",", "."), "color": "#2ee59d"},
            {"nombre": "Hexadecimal", "etiqueta": "base 16", "valor": hexa,
             "pista": "Prefijo: " + con_prefijo(valor, 16) + " · Bytes: " + agrupar(hexa, 2),
             "color": "#00d4ff"},
        ],
        "bits": {
            "ancho": ancho,
            "cadena": bits,
            "unos": bits.count("1"),
            "complemento_a_2": valor < 0,
        },
        "info": [
            ["Signo", "Negativo" if valor < 0 else "Cero" if valor == 0 else "Positivo"],
            ["Par / Impar", "Par" if valor % 2 == 0 else "Impar"],
            ["Bits necesarios", bits_necesarios],
            ["Bytes necesarios", -(-bits_necesarios // 8)],
            ["Dígitos decimales", len(str(absoluto))],
            ["¿Potencia de 2?",
             f"Sí (2^{absoluto.bit_length() - 1})" if absoluto and absoluto & (absoluto - 1) == 0 else "No"],
            [f"Como entero con signo ({ancho}b)", str(con_signo)],
            [f"Sin signo ({ancho}b)", str(sin_signo)],
        ],
    }
