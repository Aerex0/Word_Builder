# Word Builder Game

## Overview
Word Builder Game is a fast-paced typing and reaction game built with Pygame. Players catch falling letters with their mouse to build words before the timer runs out. The game offers three difficulty levels—Easy, Medium, or Hard—each with varying letter speeds and counts. Created by Suyash Ranjan (GitHub: [Aerex0](https://github.com/Aerex0)).

## Features
- **Dynamic Gameplay**: Catch falling letters to form words under a time limit.
- **Difficulty Levels**: Choose from Easy, Medium, or Hard modes with different speeds and letter counts.
- **Visual Effects**: Includes particle effects for letter captures and glowing word progress indicators.
- **Word List**: Loads words from `Word_Builder_Wordlists.txt`, filtered from `/usr/share/dict/wordlists-probable.txt` to include only words without numbers, or uses a default list if the file is missing.
- **Fullscreen Support**: Adapts to any screen resolution with a fullscreen display.

## Installation
1. **Prerequisites**:
   - Python 3.x
   - Pygame library (`pip install pygame`)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aerex0/word-builder-game.git
   cd word-builder-game
   ```

3. **Word List**:
   - The game uses `Word_Builder_Wordlists.txt`, generated from `/usr/share/dict/wordlists-probable.txt` and filtered to exclude words with numbers.
   - To create your own word list, ensure it contains one word per line (uppercase recommended).
   - If `Word_Builder_Wordlists.txt` is not provided, the game defaults to a built-in list: `PYTHON`, `GAME`, `MATRIX`, `HACKER`, `CODE`, `CYBER`, `NEON`, `RAIN`.

4. **Run the Game**:
   ```bash
   python word_builder_game.py
   ```

## How to Play
1. **Main Menu**:
   - Press `1` for Easy, `2` for Medium, or `3` for Hard to start the game.
2. **Gameplay**:
   - Letters fall from the top of the screen.
   - Click on letters with the mouse to collect them in the correct order to match the target word (displayed at the top).
   - Correct words increase your score and add bonus time based on difficulty:
     - Easy: +5 seconds
     - Medium: +3 seconds
     - Hard: +2 seconds
   - The game ends when the timer reaches zero.
3. **Game Over**:
   - View your final score and press `Enter` to return to the menu.
4. **Exit**:
   - Press `Esc` to quit the game at any time.

## Controls
- **Mouse Click**: Collect falling letters.
- **1, 2, 3**: Select difficulty in the menu.
- **Enter**: Return to the menu from the game over screen.
- **Esc**: Exit the game.

## File Structure
- `word_builder_game.py`: Main game script.
- `Word_Builder_Wordlists.txt` (optional): Custom word list file, filtered from `/usr/share/dict/wordlists-probable.txt` to exclude words with numbers.

## Dependencies
- Pygame: For rendering graphics and handling input.
- Python Standard Library: For file operations and random word selection.

## Notes
- The game runs in fullscreen mode and adapts to your screen resolution.
- Ensure `Word_Builder_Wordlists.txt` contains valid words (no numbers, uppercase preferred) to avoid gameplay issues.
- The game uses the Consolas font for rendering text; ensure it’s available on your system or a fallback font will be used.

## Author
Suyash Ranjan (GitHub: [Aerex0](https://github.com/Aerex0))

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.