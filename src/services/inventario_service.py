from src.models.producto import Producto
from src.repositories.inventario_repository import InventarioRepository


class InventarioService:
    def __init__(self, repositorio: InventarioRepository):
        self._repositorio = repositorio

    def registrar_producto(self, producto: Producto) -> None:
        if self._repositorio.obtener(producto.id) is not None:
            raise ValueError("Ya existe un producto con ese ID.")
        self._repositorio.guardar(producto)

    def obtener_producto(self, producto_id: int) -> Producto:
        producto = self._repositorio.obtener(producto_id)
        if producto is None:
            raise LookupError("Producto no encontrado.")
        return producto

    def agregar_existencias(self, producto_id: int, cantidad: int) -> None:
        producto = self.obtener_producto(producto_id)
        producto.agregar_stock(cantidad)
        self._repositorio.guardar(producto)

    def listar_productos(self) -> list[Producto]:
        return self._repositorio.listar()
