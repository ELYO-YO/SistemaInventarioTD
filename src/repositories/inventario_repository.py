from abc import ABC, abstractmethod
from typing import Optional
from src.models.producto import Producto


class InventarioRepository(ABC):
    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        raise NotImplementedError

    @abstractmethod
    def obtener(self, producto_id: int) -> Optional[Producto]:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Producto]:
        raise NotImplementedError


class InventarioEnMemoria(InventarioRepository):
    """Implementación sencilla para ejecutar el proyecto sin una BD externa."""

    def __init__(self):
        self._productos: dict[int, Producto] = {}

    def guardar(self, producto: Producto) -> None:
        self._productos[producto.id] = producto

    def obtener(self, producto_id: int) -> Optional[Producto]:
        return self._productos.get(producto_id)

    def listar(self) -> list[Producto]:
        return list(self._productos.values())
