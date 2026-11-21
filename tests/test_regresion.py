import unittest
from src.models.producto import Producto
from src.models.pedido import Pedido
from src.repositories.inventario_repository import InventarioEnMemoria
from src.services.pedido_service import PedidoService


class NotificadorStub:
    def enviar(self, mensaje):
        return True


class TestRegresion(unittest.TestCase):
    def test_regresion_pedido_con_varios_productos(self):
        """Regresión: se mantiene el cálculo y descuento correcto tras cambios."""
        repo = InventarioEnMemoria()
        repo.guardar(Producto(1, "Cuaderno", 100, 20))
        repo.guardar(Producto(2, "Lapiz", 25, 30))
        service = PedidoService(repo, NotificadorStub())

        pedido = Pedido(20, {1: 3, 2: 4})
        resultado = service.procesar_pedido(pedido)

        self.assertEqual(resultado.total, 400)
        self.assertEqual(resultado.estado, "PROCESADO")
        self.assertEqual(repo.obtener(1).stock, 17)
        self.assertEqual(repo.obtener(2).stock, 26)

    def test_regresion_no_hay_cambios_parciales_si_falla_validacion(self):
        repo = InventarioEnMemoria()
        repo.guardar(Producto(1, "Cuaderno", 100, 20))
        repo.guardar(Producto(2, "Lapiz", 25, 2))
        service = PedidoService(repo, NotificadorStub())

        pedido = Pedido(21, {1: 3, 2: 5})
        with self.assertRaises(ValueError):
            service.procesar_pedido(pedido)

        self.assertEqual(repo.obtener(1).stock, 20)
        self.assertEqual(repo.obtener(2).stock, 2)


if __name__ == "__main__":
    unittest.main()
