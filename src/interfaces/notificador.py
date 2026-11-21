from abc import ABC, abstractmethod


class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> bool:
        """Envía una notificación y devuelve si tuvo éxito."""
        raise NotImplementedError
