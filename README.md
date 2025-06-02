# Magic Square Game

A web-based implementation of the Magic Square puzzle game where players need to select numbers to match target sums or products for each row and column.

## Game Description

The Magic Square game presents a 5x5 grid of numbers with target values for each row and column. Players must:

1. Click on numbers to select/deselect them (selected numbers appear in green)
2. Make sure the selected numbers in each row match the row's target (sum or product)
3. Make sure the selected numbers in each column match the column's target (sum or product)
4. Complete the puzzle in as few moves as possible

## Features

- **Modern UI**: Clean, responsive design with beautiful animations
- **Real-time Feedback**: Target values change color to indicate correct/incorrect status
- **Solution Hints**: Option to show the optimal solution
- **Move Tracking**: Displays current moves vs optimal moves
- **Victory Screen**: Celebration when puzzle is solved
- **Random Puzzles**: Loads random puzzles from pre-generated set

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- streamlit

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run magic_square_game.py
   ```

4. **Open your web browser** and go to:
   ```
   http://localhost:8501
   ```

## How to Play

1. **Start a new game** by clicking the "New Game" button
2. **Observe the targets** - numbers on the right show row targets, numbers at the bottom show column targets
3. **Click on cells** to select/deselect them - selected cells turn green
4. **Monitor feedback** - target cells turn green when correct, red when incorrect
5. **Complete the puzzle** by making all targets correct
6. **Use hints** if needed by clicking "Show Solution"

## Game Rules

- **Sum puzzles**: Selected numbers in each row/column must add up to the target
- **Product puzzles**: Selected numbers in each row/column must multiply to the target
- **Optimal play**: Try to solve in the minimum number of moves shown
- **Visual feedback**: Target cells provide instant feedback on correctness
