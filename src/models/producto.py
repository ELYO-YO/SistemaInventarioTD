from dataclasses import dataclass


@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("El ID debe ser mayor que cero.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    def agregar_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self.stock += cantidad

    def descontar_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad
