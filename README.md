# Stickman Drop: Neo‑Tetris Arcade

Juego arcade inspirado en Tetris, pero con un giro revolucionario:

- Eres un **stickman** que debe moverse y saltar para sobrevivir.
- Los bloques caen automáticamente desde arriba.
- Pierdes cuando un bloque te aplasta.
- Incluye **música dramática tecno** en bucle.
- Tiene **contador de puntos**, **niveles** y **aumento progresivo de velocidad**.
- Agrega retos dinámicos como lluvia intensa y bloques gigantes.

## Requisitos

- Python 3.10+
- Pygame 2.0+

Instalación:

```bash
pip install pygame
```

## Ejecutar

```bash
python tetris.py
```

## Controles

- **A / Flecha Izquierda**: mover a la izquierda
- **D / Flecha Derecha**: mover a la derecha
- **Espacio / W / Flecha Arriba**: saltar
- **R**: reiniciar al perder

## Mecánicas arcade

- Cada ~10 segundos sube el nivel.
- Al subir de nivel, los bloques caen más rápido y aparecen con mayor frecuencia.
- La puntuación sube por tiempo de supervivencia y por esquivar bloques.
- Desafíos rotativos según nivel (reflejos, lluvia tecno, bloques gigantes).
