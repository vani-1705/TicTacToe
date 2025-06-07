import tkinter as tk
from tkinter import messagebox

# Create main window
window = tk.Tk()
window.title("Tic Tac Toe")

current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]

def check_winner():
    # Check rows, columns and diagonals
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            return True
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return True
    return False

def is_draw():
    for row in buttons:
        for button in row:
            if button['text'] == "":
                return False
    return True

def on_click(row, col):
    global current_player

    if buttons[row][col]['text'] == "":
        buttons[row][col]['text'] = current_player
        if check_winner():
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_board()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            current_player = "O" if current_player == "X" else "X"

def reset_board():
    global current_player
    current_player = "X"
    for row in buttons:
        for button in row:
            button['text'] = ""

# Create 3x3 grid of buttons
for i in range(3):
    for j in range(3):
        button = tk.Button(window, text="", font=('consolas', 40), width=5, height=2,
                           command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j)
        buttons[i][j] = button

window.mainloop()