from multipledispatch import dispatch

class Board:
    
    # Define it for two integers
    @dispatch(int, int)
    def get_square_at(self, row: int, col: int):
        return f"Fetching via coordinates: {row}, {col}"

    # Define it for one string
    @dispatch(str)
    def get_square_at(self, square: str):
        return f"Fetching via notation: {square}"

# --- Usage ---
b = Board()
print(b.get_square_at(3, 5))   # automatically picks the 1st method
print(b.get_square_at("e4"))   # automatically picks the 2nd method