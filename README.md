# Ejercicio Práctico: TDD (Test-Driven Development) con Python

Este proyecto es un ejercicio práctico paso a paso para aprender y aplicar los principios de **Test-Driven Development (TDD)** desde cero.

## ¿Qué es TDD?

TDD es una metodología de desarrollo de software donde las pruebas automatizadas se escriben *antes* del código de producción. El ciclo básico consta de 3 fases:

1. 🔴 **Fase Roja (Red):** Escribir una prueba automatizada para una nueva funcionalidad. Como la funcionalidad no existe o está incompleta, la prueba **fallará**.
2. 🟢 **Fase Verde (Green):** Escribir el código mínimo y necesario para que la prueba pase con éxito.
3. 🔵 **Fase de Refactorización (Refactor):** Mejorar o reestructurar el código interno asegurándonos de no romper nada, ya que las pruebas nos respaldan (manteniéndolas en verde).

## Descripción del Proyecto

El objetivo de este ejercicio fue construir la lógica de un **Carrito de Compras Virtual**. 

### Funcionalidades implementadas y probadas:
*   **Creación del Carrito:** Validar que al iniciarse, el carrito está totalmente vacío.
*   **Validación de Stock disponible (Camino triste/Unhappy Path):** Prevenir que se agreguen al carrito más unidades de las que existen en stock, verificando que el sistema arroje un `ValueError` controlado.
*   **Agregar un producto (Camino feliz/Happy Path):** Validar que al agregar un producto con stock suficiente, este se guarde correctamente en el carrito.
*   **Vaciar el carrito:** Asegurar que se puedan eliminar todos los productos del carrito en una sola instrucción.

### Refactorización: De Funciones a POO (Programación Orientada a Objetos)

Una parte clave de este ejercicio fue la fase final de **Refactorización**:
1.  **Versión Inicial:** Se construyó la lógica de negocio utilizando un simple diccionario de Python y funciones sueltas (`create_cart`, `add_to_cart`, `clear_cart`).
2.  **Versión Final (Clase):** Siguiendo las reglas de TDD, primero se modificaron las pruebas para que esperaran una Clase (`Cart()`), provocando deliberadamente el fallo. Luego, se encapsuló toda la lógica dentro de una clase en `cart.py`, migrando el diccionario a un atributo interno (`self.items`).

Este proceso práctico demostró cómo las pruebas nos dan la tranquilidad de poder reestructurar profundamente el código sin miedo a romper la regla de negocio.

## Cómo ejecutar las pruebas

Este proyecto utiliza el veloz gestor **uv** y la librería **pytest**.

Para ejecutar las pruebas y validar el comportamiento del modelo, corre el siguiente comando en la raíz del proyecto:

```bash
uv run pytest test_cart.py
```

Al hacerlo, deberás ver un resultado exitoso (`4 passed`), confirmando que la lógica es robusta.
