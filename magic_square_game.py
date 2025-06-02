import streamlit as st
import json
import random
from models import Square
from ops import sum_op, product_op

class MagicSquareGame:
    def __init__(self):
        self.load_problems()
        
    def load_problems(self) -> None:
        with open('data/problems_and_solutions.json', 'r') as f:
            self.problems = json.load(f)
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'current_square' not in st.session_state:
            self.start_new_game()
        if 'selected_cells' not in st.session_state:
            st.session_state.selected_cells = set()
        if 'moves' not in st.session_state:
            st.session_state.moves = 0
        if 'show_solution_hint' not in st.session_state:
            st.session_state.show_solution_hint = False
        if 'gave_up' not in st.session_state:
            st.session_state.gave_up = False
    
    def start_new_game(self):
        """Start a new game with a random problem"""
        problem = random.choice(self.problems)
        st.session_state.current_square = Square.from_dict(problem['square'])
        st.session_state.solution = set(tuple(cell) for cell in problem['solution'])
        st.session_state.selected_cells = set()
        st.session_state.moves = 0
        st.session_state.show_solution_hint = False
        st.session_state.game_solved = False
        st.session_state.gave_up = False
    
    def toggle_cell(self, row: int, col: int):
        """Toggle cell selection"""
        cell = (row, col)
        if cell in st.session_state.selected_cells:
            st.session_state.selected_cells.remove(cell)
        else:
            st.session_state.selected_cells.add(cell)
        
        st.session_state.moves += 1
        st.session_state.show_solution_hint = False
        
        # Check if game is solved
        if st.session_state.selected_cells == st.session_state.solution:
            st.session_state.game_solved = True
        else:
            st.session_state.game_solved = False
    
    def calculate_current_values(self) -> tuple[list[int], list[int]]:
        """Calculate current row and column values"""
        current_row_values = []
        current_col_values = []
        
        for i in range(5):
            # Calculate row values
            row_numbers = [
                st.session_state.current_square.get_number((i, j)) 
                for j in range(5)
                if (i, j) in st.session_state.selected_cells
            ]
            if row_numbers:
                row_value = st.session_state.current_square.op(row_numbers)
            else:
                row_value = 1 if st.session_state.current_square.op == product_op else 0
            current_row_values.append(row_value)
            
            # Calculate column values  
            col_numbers = [st.session_state.current_square.get_number((j, i)) 
                          for j in range(5) if (j, i) in st.session_state.selected_cells]
            if col_numbers:
                col_value = st.session_state.current_square.op(col_numbers)
            else:
                col_value = 1 if st.session_state.current_square.op == product_op else 0
            current_col_values.append(col_value)
        
        return current_row_values, current_col_values
    
    def render_game(self):
        """Render the complete game interface"""
        self.initialize_session_state()
        
        # Compact header with title and controls in one row
        title_col, controls_col = st.columns([2, 3])
        
        with title_col:
            st.title("Magic Square")
            operation = "Sum" if st.session_state.current_square.op == sum_op else "Product"
            st.markdown(f"**{operation} Game** • Moves: **{st.session_state.moves}** • Optimal: **{len(st.session_state.solution)}**")
        
        with controls_col:
            # Control buttons in a compact row
            new_game_button, give_up_button, reset_button = st.columns(3)
            with new_game_button:
                if st.button("🎮 New", use_container_width=True):
                    self.start_new_game()
                    st.rerun()
            with give_up_button:
                if st.button("🏳️ Give Up", use_container_width=True):
                    st.session_state.selected_cells = st.session_state.solution.copy()
                    st.session_state.game_solved = True
                    st.session_state.show_solution_hint = False
                    st.session_state.gave_up = True
                    st.rerun()
            with reset_button:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.selected_cells = set()
                    st.session_state.moves = 0
                    st.session_state.game_solved = False
                    st.session_state.show_solution_hint = False
                    st.session_state.gave_up = False
                    st.rerun()
            
            # Status indicator
            if st.session_state.game_solved:
                if st.session_state.gave_up:
                    st.warning("🏳️ You gave up! Better luck next time (loser) 😏")
                else:
                    moves_msg = f"🎉 Solved in {st.session_state.moves} moves!"
                    optimal_moves = len(st.session_state.solution)
                    if st.session_state.moves == optimal_moves:
                        st.success(f"{moves_msg} Perfect! ⭐")
                    elif st.session_state.moves <= optimal_moves + 2:
                        st.info(f"{moves_msg} Excellent! 👏")
                    else:
                        st.warning(f"{moves_msg} Good job! 💪")
        
        # Game board
        self.render_game_board()
    
    def render_game_board(self):
        """Render the game board with targets and grid"""
        current_row_values, current_col_values = self.calculate_current_values()
        
        # Column headers (targets) - align with grid below
        header_cols = st.columns([1, 1, 1, 1, 1, 0.8])  # 5 grid columns + 1 for row targets
        for j in range(5):
            with header_cols[j]:
                target = st.session_state.current_square.get_column(j).target
                current = current_col_values[j]
                
                if current == target:
                    st.success(f"**{target}**")
                elif current != (1 if st.session_state.current_square.op == product_op else 0):
                    st.error(f"**{target}**")
                else:
                    st.info(f"**{target}**")
        
        # Header for row targets column
        with header_cols[5]:
            st.markdown("**Rows**")
        
        # Grid rows
        for i in range(5):
            row_cols = st.columns([1, 1, 1, 1, 1, 0.8])  # Match header layout exactly
            
            # Grid cells
            for j in range(5):
                with row_cols[j]:
                    number = st.session_state.current_square.get_number((i, j))
                    cell_key = f"cell_{i}_{j}"
                    
                    # Determine button styling
                    is_selected = (i, j) in st.session_state.selected_cells
                    
                    if is_selected:
                        button_type = "primary"  # Green selected
                        label = f"**{number}**"
                    else:
                        button_type = "secondary"  # Default
                        label = str(number)
                    
                    if st.button(label, key=cell_key, use_container_width=True, type=button_type):
                        self.toggle_cell(i, j)
                        st.rerun()
            
            # Row target
            with row_cols[5]:
                target = st.session_state.current_square.get_row(i).target
                current = current_row_values[i]
                
                if current == target:
                    st.success(f"**{target}**")
                elif current != (1 if st.session_state.current_square.op == product_op else 0):
                    st.error(f"**{target}**")
                else:
                    st.info(f"**{target}**")
        
        # Compact instructions
        with st.expander("📋 How to Play", expanded=False):
            st.markdown("""
            **Goal:** Select numbers so each row and column matches its target.
            • **Sum:** Selected numbers add up to target • **Product:** Selected numbers multiply to target
            • Green = achieved target • Red = wrong • Blue = no selection yet
            """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Magic Square Game",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    /* Hide Streamlit header */
    header[data-testid="stHeader"] {
        height: 0px;
        display: none;
    }
    
    .stButton > button {
        height: 45px;
        font-size: 16px;
        font-weight: bold;
        margin: 2px 0;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 5px;
        border-radius: 5px;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }
    .element-container {
        margin: 0.25rem 0;
    }
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0rem !important;
    }
    .stExpander {
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    game = MagicSquareGame()
    game.render_game()

if __name__ == "__main__":
    main() 