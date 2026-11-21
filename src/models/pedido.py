from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Pedido:
    id: int
    items: Dict[int, int]
    total: float = 0.0
    estado: str = "PENDIENTE"

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("El ID del pedido debe ser mayor que cero.")
        if not self.items:
            raise ValueError("El pedido debe contener al menos un producto.")
        for producto_id, cantidad in self.items.items():
            if producto_id <= 0 or cantidad <= 0:
                raise ValueError("Los productos y cantidades deben ser positivos.")

    def marcar_procesado(self, total: float) -> None:
        self.total = total
        self.estado = "PROCESADO"

    def marcar_fallido(self) -> None:
        self.estado = "FALLIDO"
