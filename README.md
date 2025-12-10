# Proyecto final – Patrones de Diseño


## Autores

- Dominic Robayo – 20241020072  
- Julián Valencia – 20241020048


## Descripción General del Juego

Este proyecto consiste en un videojuego 2D desarrollado con **Pygame**, inspirado en juegos de evasión tipo *The World’s Hardest Game*.  
El jugador controla un personaje que debe desplazarse a través de distintos niveles llenos de obstáculos (paredes) y enemigos móviles. El objetivo es llegar a la meta sin chocar con ningún enemigo ni con las paredes.  

Cada nivel incrementa su dificultad mediante:
- Mayor cantidad de obstáculos.
- Diseño tipo laberinto.
- Enemigos con distintos tipos de movimiento.
- Incremento de velocidad y complejidad de recorridos.

El juego cuenta con:
- Sistema de reinicio de nivel al colisionar.
- Avance automático entre niveles.
- Reinicio completo del juego al finalizar el último nivel.
- Enemigos con animación por sprites.

---

## Patrones de Diseño Utilizados

### 1. **State (Comportamiento)**

**Dónde se aplica:**  
En el sistema de movimiento de los enemigos.

**Cómo funciona:**  
Cada enemigo posee un objeto de estado que define su comportamiento de movimiento. Existen varios estados:
- Patrulla lineal
- Movimiento senoidal
- Patrulla rápida
- Movimiento en trayectoria cuadrada

**Por qué se usa:**  
Permite cambiar el comportamiento del enemigo sin modificar la clase principal del enemigo. Cada tipo de movimiento está completamente separado, lo que facilita la extensión del sistema con nuevos comportamientos.

---

### 2. **Command (Comportamiento)**

**Dónde se aplica:**  
En el control de movimientos del jugador y el reinicio del nivel.

**Cómo funciona:**  
Cada acción del jugador se encapsula como un comando:
- Movimiento del jugador.
- Reinicio de estado.

Cada comando puede ejecutarse y deshacerse.

**Por qué se usa:**  
Permite almacenar un historial de acciones y aplicar fácilmente funciones como deshacer movimientos o reiniciar el estado del jugador sin acoplar la lógica directamente al control del teclado.

---

### 3. **Memento (Comportamiento)**

**Dónde se aplica:**  
En la gestión del estado del jugador al morir o reiniciar el nivel.

**Cómo funciona:**  
Se guarda una copia del estado inicial del jugador al comenzar un nivel (posición, nivel actual, etc.). Cuando el jugador colisiona con un enemigo o una pared, se restaura ese estado guardado.

**Por qué se usa:**  
Permite restaurar el estado del jugador sin violar el principio de encapsulación, evitando accesos directos a los atributos internos desde otras clases.

---

### 4. **Facade (Estructural)**

**Dónde se aplica:**  
En la clase que centraliza la ejecución del juego.

**Cómo funciona:**  
Se utiliza una fachada para simplificar la interacción entre el sistema principal, el jugador, los niveles, los enemigos y los comandos.

**Por qué se usa:**  
Reduce el acoplamiento entre los distintos módulos del sistema y ofrece una interfaz más sencilla para iniciar y ejecutar el juego.

---

### 5. **Strategy (Comportamiento)**

**Dónde se aplica:**  
En la asignación de comportamientos de movimiento a los enemigos.

**Cómo funciona:**  
Cada enemigo recibe una estrategia de movimiento al crearse. Esta estrategia puede cambiarse sin modificar la estructura del enemigo.

**Por qué se usa:**  
Permite intercambiar dinámicamente los algoritmos de movimiento sin afectar el resto del sistema, favoreciendo la reutilización y extensión.

---

## Patrones No Utilizados y Justificación

### Singleton
No se usa porque el juego no requiere una única instancia global estricta para ninguna clase crítica. Forzar este patrón limitaría la escalabilidad y reutilización.


### Factory Method
No se aplica de forma explícita, ya que los enemigos y niveles se crean de forma directa. Su implementación sería útil si los niveles se generaran dinámicamente.

### Builder
No es necesario debido a que los niveles y enemigos no tienen estructuras de construcción complejas por partes independientes.

### Decorator
No se utiliza ya que no se requiere agregar funcionalidades dinámicas sobre enemigos o jugador sin modificar su estructura base.

---


