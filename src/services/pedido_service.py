from src.models.pedido import Pedido
from src.repositories.inventario_repository import InventarioRepository
from src.interfaces.notificador import Notificador


class PedidoService:
    def __init__(self, repositorio: InventarioRepository, notificador: Notificador):
        self._repositorio = repositorio
        self._notificador = notificador

    def procesar_pedido(self, pedido: Pedido) -> Pedido:
        """Valida, calcula y descuenta stock. Si falla, no deja descuentos parciales."""
        productos = []
        total = 0.0

        # Primera fase: validar todo antes de modificar el inventario.
        for producto_id, cantidad in pedido.items.items():
            producto = self._repositorio.obtener(producto_id)
            if producto is None:
                pedido.marcar_fallido()
                raise LookupError(f"No existe el producto con ID {producto_id}.")
            if cantidad <= 0:
                pedido.marcar_fallido()
                raise ValueError("La cantidad debe ser mayor que cero.")
            if producto.stock < cantidad:
                pedido.marcar_fallido()
                raise ValueError(f"Stock insuficiente para {producto.nombre}.")
            productos.append((producto, cantidad))
            total += producto.precio * cantidad

        # Segunda fase: aplicar los cambios después de validar todos los artículos.
        for producto, cantidad in productos:
            producto.descontar_stock(cantidad)
            self._repositorio.guardar(producto)

        pedido.marcar_procesado(total)
        try:
            self._notificador.enviar(
                f"Pedido {pedido.id} procesado. Total: {pedido.total:.2f}"
            )
        except Exception:
            # El pedido ya quedó registrado; un fallo de notificación no revierte la venta.
            pass

        return pedido
