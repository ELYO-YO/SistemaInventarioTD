import unittest
from unittest.mock import Mock
from src.models.producto import Producto
from src.models.pedido import Pedido
from src.repositories.inventario_repository import InventarioEnMemoria
from src.services.pedido_service import PedidoService


class NotificadorStub:
    """Stub: devuelve una respuesta fija sin llamar a un servicio real."""
    def __init__(self, resultado=True):
        self.resultado = resultado
        self.mensajes = []

    def enviar(self, mensaje):
        self.mensajes.append(mensaje)
        return self.resultado


class TestPedidoService(unittest.TestCase):
    def setUp(self):
        self.repo = InventarioEnMemoria()
        self.repo.guardar(Producto(1, "Laptop", 25000, 5))
        self.repo.guardar(Producto(2, "Mouse", 500, 10))
        self.notificador = NotificadorStub()
        self.service = PedidoService(self.repo, self.notificador)

    def test_procesar_pedido_y_calcular_total(self):
        pedido = Pedido(1, {1: 1, 2: 2})
        resultado = self.service.procesar_pedido(pedido)

        self.assertEqual(resultado.estado, "PROCESADO")
        self.assertEqual(resultado.total, 26000)
        self.assertEqual(self.repo.obtener(1).stock, 4)
        self.assertEqual(self.repo.obtener(2).stock, 8)
        self.assertEqual(len(self.notificador.mensajes), 1)

    def test_stock_insuficiente_no_modifica_inventario(self):
        pedido = Pedido(2, {1: 2, 2: 100})
        with self.assertRaises(ValueError):
            self.service.procesar_pedido(pedido)

        self.assertEqual(self.repo.obtener(1).stock, 5)
        self.assertEqual(self.repo.obtener(2).stock, 10)
        self.assertEqual(pedido.estado, "FALLIDO")

    def test_producto_inexistente(self):
        pedido = Pedido(3, {999: 1})
        with self.assertRaises(LookupError):
            self.service.procesar_pedido(pedido)
        self.assertEqual(pedido.estado, "FALLIDO")

    def test_mock_verifica_notificacion(self):
        notificador_mock = Mock()
        repo = InventarioEnMemoria()
        repo.guardar(Producto(1, "Tablet", 12000, 3))
        service = PedidoService(repo, notificador_mock)
        pedido = Pedido(4, {1: 1})

        service.procesar_pedido(pedido)

        notificador_mock.enviar.assert_called_once_with(
            "Pedido 4 procesado. Total: 12000.00"
        )

    def test_fallo_de_notificacion_no_cancela_pedido(self):
        notificador = Mock()
        notificador.enviar.side_effect = RuntimeError("Servicio no disponible")
        repo = InventarioEnMemoria()
        repo.guardar(Producto(1, "Tablet", 12000, 3))
        service = PedidoService(repo, notificador)
        pedido = Pedido(5, {1: 1})

        resultado = service.procesar_pedido(pedido)

        self.assertEqual(resultado.estado, "PROCESADO")
        self.assertEqual(repo.obtener(1).stock, 2)


if __name__ == "__main__":
    unittest.main()
