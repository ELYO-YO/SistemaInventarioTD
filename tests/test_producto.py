import unittest
from src.models.producto import Producto


class TestProducto(unittest.TestCase):
    def test_crear_producto_correctamente(self):
        producto = Producto(1, "Laptop", 25000, 10)
        self.assertEqual(producto.nombre, "Laptop")
        self.assertEqual(producto.precio, 25000)
        self.assertEqual(producto.stock, 10)

    def test_no_acepta_precio_negativo(self):
        with self.assertRaises(ValueError):
            Producto(2, "Mouse", -100, 5)

    def test_no_acepta_stock_negativo(self):
        with self.assertRaises(ValueError):
            Producto(3, "Teclado", 1500, -5)

    def test_agregar_stock(self):
        producto = Producto(1, "Laptop", 25000, 4)
        producto.agregar_stock(3)
        self.assertEqual(producto.stock, 7)

    def test_descontar_stock(self):
        producto = Producto(1, "Laptop", 25000, 4)
        producto.descontar_stock(2)
        self.assertEqual(producto.stock, 2)

    def test_no_permite_descontar_mas_del_disponible(self):
        producto = Producto(1, "Laptop", 25000, 2)
        with self.assertRaises(ValueError):
            producto.descontar_stock(3)


if __name__ == "__main__":
    unittest.main()
