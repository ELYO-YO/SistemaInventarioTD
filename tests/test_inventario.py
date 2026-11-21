import unittest
from unittest.mock import Mock
from src.models.producto import Producto
from src.repositories.inventario_repository import InventarioEnMemoria
from src.services.inventario_service import InventarioService


class TestInventarioService(unittest.TestCase):
    def setUp(self):
        self.repo = InventarioEnMemoria()
        self.service = InventarioService(self.repo)

    def test_registrar_y_consultar_producto(self):
        producto = Producto(1, "Monitor", 8000, 5)
        self.service.registrar_producto(producto)
        encontrado = self.service.obtener_producto(1)
        self.assertEqual(encontrado.nombre, "Monitor")

    def test_no_registra_id_duplicado(self):
        self.service.registrar_producto(Producto(1, "Monitor", 8000, 5))
        with self.assertRaises(ValueError):
            self.service.registrar_producto(Producto(1, "Teclado", 1500, 8))

    def test_producto_inexistente(self):
        with self.assertRaises(LookupError):
            self.service.obtener_producto(99)

    def test_agregar_existencias(self):
        self.service.registrar_producto(Producto(1, "Monitor", 8000, 5))
        self.service.agregar_existencias(1, 4)
        self.assertEqual(self.service.obtener_producto(1).stock, 9)

    def test_mock_verifica_que_se_guarde_producto(self):
        repo_mock = Mock()
        repo_mock.obtener.return_value = None
        service = InventarioService(repo_mock)
        producto = Producto(10, "Mouse", 500, 12)

        service.registrar_producto(producto)

        repo_mock.obtener.assert_called_once_with(10)
        repo_mock.guardar.assert_called_once_with(producto)


if __name__ == "__main__":
    unittest.main()
