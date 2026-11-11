from django.test import TestCase

from .conversiones import ErrorConversion, convertir, parsear


class ConversionesTests(TestCase):
    def test_parsear(self):
        self.assertEqual(parsear("FF", 16), 255)
        self.assertEqual(parsear("0b1010", 2), 10)
        self.assertEqual(parsear("-777", 8), -511)
        with self.assertRaises(ErrorConversion):
            parsear("102", 2)

    def test_convertir(self):
        d = convertir("255")
        valores = {r["nombre"]: r["valor"] for r in d["resultados"]}
        self.assertEqual(valores["Binario"], "11111111")
        self.assertEqual(valores["Hexadecimal"], "FF")
        self.assertEqual(len(valores), 4)
        self.assertEqual(d["bits"]["cadena"], "11111111")

    def test_negativo_complemento_a_2(self):
        d = convertir("-128")
        self.assertEqual(d["bits"]["ancho"], 8)
        self.assertEqual(d["bits"]["cadena"], "10000000")

    def test_api_exitoso(self):
        r = self.client.get("/api/convertir/", {"valor": "DEADBEEF", "base": 16})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(set(r.json()), {"datos"})
        self.assertEqual(r.json()["datos"]["valor"], "3735928559")

    def test_api_rechaza_valores_y_parametros_invalidos(self):
        casos = [
            ({}, "valor"),
            ({"valor": "   "}, "valor"),
            ({"valor": "10", "base": "abc"}, "base"),
            ({"valor": "10", "base": 36}, "base"),
            ({"valor": "10", "ancho": "abc"}, "ancho"),
            ({"valor": "10", "ancho": 1000000000}, "ancho"),
            ({"valor": "Z", "base": 10}, "dígito"),
        ]
        for parametros, mensaje in casos:
            with self.subTest(parametros=parametros):
                respuesta = self.client.get("/api/convertir/", parametros)
                self.assertEqual(respuesta.status_code, 400)
                self.assertEqual(set(respuesta.json()), {"error"})
                self.assertIn(mensaje, respuesta.json()["error"])

    def test_api_rechaza_numeros_demasiado_largos(self):
        respuesta = self.client.get("/api/convertir/", {"valor": "1" * 2001})
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(respuesta.json(), {"error": "El número es demasiado largo"})

    def test_api_solo_acepta_get(self):
        respuesta = self.client.post("/api/convertir/", {"valor": "10"})
        self.assertEqual(respuesta.status_code, 405)
        self.assertEqual(respuesta.json(), {"error": "Método no permitido"})
        self.assertEqual(respuesta["Allow"], "GET")

    def test_api_ancho_valido(self):
        respuesta = self.client.get(
            "/api/convertir/", {"valor": "1", "ancho": 16}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["datos"]["bits"]["ancho"], 16)
