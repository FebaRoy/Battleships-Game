# Battleships Game

This repository contains a Python implementation of the classic Battleships game. It allows two players to set up their boards, place ships, and take turns attacking each other’s ships until one player wins.

## Features

- **Customizable Board Size:** Players can select a board size between 2x2 and 9x9.
- **Ship Placement:** Players place ships of varying lengths on the board, with rules enforcing vertical/horizontal alignment and non-overlapping placements.
- **Turn-Based Gameplay:** Players take turns attacking each other’s ships, with real-time feedback on hits and misses.
- **Game Over Detection:** The game automatically detects when all of a player’s ships have been destroyed and announces the winner.
- **Error Handling:** Includes robust input validation, ensuring valid coordinates and correct ship placement.

## How to Play

1. **Setup Phase:**
   - Enter the desired board size and the sizes of the ships.
   - Players take turns placing their ships on the board, with real-time error checking.

2. **Turn-Taking Phase:**
   - Players alternate turns to enter attack coordinates.
   - The game provides feedback on whether the attack was a hit or miss and updates the board accordingly.

3. **Winning the Game:**
   - The game concludes when one player successfully hits and destroys all of their opponent's ships.

## Getting Started

### Prerequisites

- Python 3.12 installed on your machine.
- A Python IDE or text editor (e.g., PyCharm, VS Code).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/FebaRoy/Battleships-Game.git
   cd Battleships-Game

2. (Optional) Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`


###Running the Game
   - Open the project in your preferred Python IDE or text editor.
   - Run the a1.py file to start the game.
   - Follow the prompts in the terminal to play.

##Contributing
- Feel free to submit issues, fork the repository, and make pull requests. Contributions are welcome!

##Contact
- For any inquiries or questions, please contact febaroy7@gmail.com.
