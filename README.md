# Sistema de Gestión de Inventario con TDD

Proyecto académico desarrollado en Python para demostrar programación orientada a objetos, TDD, mocks, stubs y pruebas de regresión.

## Requisitos
- Python 3.10 o superior
- pip

## Instalación en Windows
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar todas las pruebas
```powershell
python -m unittest discover -s tests -v
```

También se puede utilizar:
```powershell
pytest -v
```

## Estructura
- `src/models`: entidades Producto y Pedido.
- `src/repositories`: contrato y repositorio en memoria.
- `src/services`: reglas de inventario y procesamiento de pedidos.
- `src/interfaces`: contrato del notificador.
- `tests`: pruebas unitarias, dobles de prueba y regresión.
- `.github/workflows`: integración continua con GitHub Actions.

## Dobles de prueba
- **Mock:** se usa `unittest.mock.Mock` para comprobar interacciones con el repositorio y el notificador.
- **Stub:** `NotificadorStub` devuelve una respuesta controlada para aislar el servicio del sistema externo.

## Ciclo TDD para documentar
1. RED: escribir primero una prueba y comprobar que falla por la funcionalidad aún no implementada.
2. GREEN: implementar el código mínimo para que pase.
3. REFACTOR: mejorar el diseño y ejecutar nuevamente todas las pruebas.

Las pruebas del repositorio muestran el estado final. Para demostrar el proceso TDD, conservar capturas reales de cada fase durante el desarrollo.

## Prueba de regresión
`tests/test_regresion.py` comprueba que el procesamiento de pedidos conserva el cálculo del total, el descuento de existencias y la validación completa antes de modificar el inventario.

## Alcance
El repositorio en memoria permite ejecutar el ejemplo sin configurar una base de datos. En una implementación real, se podría crear otro repositorio que implemente `InventarioRepository` y conectarlo a una base de datos sin cambiar los servicios.
