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

    def test_api(self):
        r = self.client.get("/api/convertir/", {"valor": "DEADBEEF", "base": 16})
        self.assertEqual(r.json()["datos"]["valor"], "3735928559")
        r = self.client.get("/api/convertir/", {"valor": "Z", "base": 10})
        self.assertEqual(r.status_code, 400)
        r = self.client.get("/api/convertir/", {"valor": "10", "base": 36})
        self.assertEqual(r.status_code, 400)
