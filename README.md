# Snake: Power-Up Edition

A customizable, feature-rich version of the classic Snake game built with Python and Pygame.

## Features
* **Power-Up Apples:** Three types of apples with different spawn rarities:
    * **Red:** +1 length
    * **Orange:** +3 length
    * **Purple:** +5 length
* **Adjustable Grid:** Choose between a 32x32 or a 64x64 board.
* **Wall Mechanics:** Select "Solid" (crash to lose) or "Wrap" (pass through) walls.
* **Save System:** Automatically remembers your menu settings for the next session.
* **Smooth Input:** Features an input queue system to prevent missed keystrokes.

## Controls
| Action | Key |
| :--- | :--- |
| **Movement** | W, A, S, D or Arrow Keys |
| **Menu Navigation** | Up/Down (Select), Left/Right (Adjust) |
| **Restart** | R (on Game Over) |
| **Return to Menu** | M (on Game Over) |

## Installation and Execution
1. Ensure you have [Python](https://www.python.org/) installed.
2. Install the required Pygame library:
   ```bash
   pip install pygame
