import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# ─── SOUND HELPER ────────────────────────────────────────────
def beep(freq=800, dur=60):
        pass

# ─── THEMES ──────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":          "#0f0f1a",
        "panel":       "#1a1a2e",
        "cell_bg":     "#16213e",
        "cell_hover":  "#0f3460",
        "cell_border": "#e94560",
        "x_color":     "#e94560",
        "o_color":     "#00d4ff",
        "win_bg":      "#2a0a40",
        "text":        "#ffffff",
        "subtext":     "#aaaacc",
        "btn_bg":      "#e94560",
        "btn_fg":      "#ffffff",
        "score_x":     "#e94560",
        "score_o":     "#00d4ff",
        "score_d":     "#f0a500",
        "status_bg":   "#1a1a2e",
    },
    "light": {
        "bg":          "#f0f4ff",
        "panel":       "#ffffff",
        "cell_bg":     "#e8eeff",
        "cell_hover":  "#cdd5ff",
        "cell_border": "#5c6bc0",
        "x_color":     "#e53935",
        "o_color":     "#1976d2",
        "win_bg":      "#fff9c4",
        "text":        "#1a1a2e",
        "subtext":     "#5c6bc0",
        "btn_bg":      "#5c6bc0",
        "btn_fg":      "#ffffff",
        "score_x":     "#e53935",
        "score_o":     "#1976d2",
        "score_d":     "#f57f17",
        "status_bg":   "#e8eeff",
    }
}

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],   # rows
    [0,3,6],[1,4,7],[2,5,8],   # cols
    [0,4,8],[2,4,6]            # diagonals
]

# ─── MAIN GAME ───────────────────────────────────────────────
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("❌⭕ Tic Tac Toe")
        self.root.resizable(False, False)

        self.theme_name  = "dark"
        self.T           = THEMES[self.theme_name]
        self.vs_ai       = False
        self.ai_symbol   = "O"

        # Player names
        self.names = {"X": "Player X", "O": "Player O"}

        # Scores
        self.score = {"X": 0, "O": 0, "D": 0}

        # Board state
        self.board   = [""] * 9
        self.current = "X"
        self.game_on = True

        self._build_ui()
        self._ask_names()

    # ── ASK PLAYER NAMES ─────────────────────────────────────
    def _ask_names(self):
        name_x = simpledialog.askstring(
            "Player Names", "Enter Player X name:",
            initialvalue="Player X", parent=self.root
        )
        if name_x and name_x.strip():
            self.names["X"] = name_x.strip()[:14]

        mode = messagebox.askyesno(
            "Game Mode", "Play vs AI (Computer)?", parent=self.root
        )
        self.vs_ai = mode

        if not self.vs_ai:
            name_o = simpledialog.askstring(
                "Player Names", "Enter Player O name:",
                initialvalue="Player O", parent=self.root
            )
            if name_o and name_o.strip():
                self.names["O"] = name_o.strip()[:14]
        else:
            self.names["O"] = "🤖 Computer"

        self._refresh_labels()
        self._update_status()

    # ── BUILD UI ─────────────────────────────────────────────
    def _build_ui(self):
        T = self.T
        self.root.configure(bg=T["bg"])

        # ── Top title ──
        self.title_lbl = tk.Label(
            self.root, text="❌  TIC TAC TOE  ⭕",
            font=("Segoe UI", 18, "bold"),
            bg=T["bg"], fg=T["text"], pady=10
        )
        self.title_lbl.pack(fill="x")

        # ── Score panel ──
        self.score_frame = tk.Frame(self.root, bg=T["panel"], pady=8, padx=10)
        self.score_frame.pack(fill="x", padx=16, pady=(0,8))

        self.score_labels = {}
        for sym, col_key, idx in [("X","score_x",0), ("D","score_d",1), ("O","score_o",2)]:
            f = tk.Frame(self.score_frame, bg=T["panel"])
            f.grid(row=0, column=idx, padx=18, pady=4, sticky="nsew")
            self.score_frame.columnconfigure(idx, weight=1)

            header = "DRAWS" if sym == "D" else self.names[sym]
            lbl_name = tk.Label(f, text=header,
                                font=("Segoe UI", 9, "bold"),
                                bg=T["panel"], fg=T[col_key])
            lbl_name.pack()

            lbl_num = tk.Label(f, text="0",
                               font=("Segoe UI", 26, "bold"),
                               bg=T["panel"], fg=T[col_key])
            lbl_num.pack()

            self.score_labels[sym] = {"name": lbl_name, "num": lbl_num}

        # ── Status bar ──
        self.status_var = tk.StringVar(value="")
        self.status_lbl = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 12, "bold"),
            bg=T["status_bg"], fg=T["text"],
            pady=7, padx=10
        )
        self.status_lbl.pack(fill="x", padx=16, pady=(0,6))

        # ── Grid ──
        self.grid_frame = tk.Frame(self.root, bg=T["cell_border"], padx=3, pady=3)
        self.grid_frame.pack(padx=20, pady=4)

        self.cells = []
        for i in range(9):
            btn = tk.Button(
                self.grid_frame,
                text="", font=("Segoe UI", 36, "bold"),
                width=3, height=1,
                bg=T["cell_bg"], fg=T["text"],
                activebackground=T["cell_hover"],
                relief="flat", bd=0,
                cursor="hand2",
                command=lambda idx=i: self._click(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: self._hover_on(b))
            btn.bind("<Leave>", lambda e, b=btn: self._hover_off(b))
            self.cells.append(btn)

        # ── Bottom buttons ──
        btn_frame = tk.Frame(self.root, bg=T["bg"], pady=10)
        btn_frame.pack(fill="x", padx=16)

        self.restart_btn = tk.Button(
            btn_frame, text="🔄 Restart",
            font=("Segoe UI", 10, "bold"),
            bg=T["btn_bg"], fg=T["btn_fg"],
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=self._restart_board
        )
        self.restart_btn.pack(side="left", padx=4)

        self.theme_btn = tk.Button(
            btn_frame, text="🌙 Dark Mode",
            font=("Segoe UI", 10, "bold"),
            bg=T["btn_bg"], fg=T["btn_fg"],
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="left", padx=4)

        self.mode_btn = tk.Button(
            btn_frame, text="🤖 vs AI",
            font=("Segoe UI", 10, "bold"),
            bg=T["btn_bg"], fg=T["btn_fg"],
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=self._toggle_mode
        )
        self.mode_btn.pack(side="left", padx=4)

        self.names_btn = tk.Button(
            btn_frame, text="✏️ Names",
            font=("Segoe UI", 10, "bold"),
            bg=T["btn_bg"], fg=T["btn_fg"],
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=self._change_names
        )
        self.names_btn.pack(side="left", padx=4)

        self.reset_score_btn = tk.Button(
            btn_frame, text="🗑 Reset Score",
            font=("Segoe UI", 10, "bold"),
            bg="#555577", fg=T["btn_fg"],
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=self._reset_scores
        )
        self.reset_score_btn.pack(side="right", padx=4)

    # ── HOVER EFFECTS ────────────────────────────────────────
    def _hover_on(self, btn):
        if btn["text"] == "" and self.game_on:
            btn.configure(bg=self.T["cell_hover"])

    def _hover_off(self, btn):
        if btn["text"] == "":
            btn.configure(bg=self.T["cell_bg"])

    # ── CELL CLICK ───────────────────────────────────────────
    def _click(self, idx):
        if not self.game_on or self.board[idx] != "":
            return
        if self.vs_ai and self.current == self.ai_symbol:
            return

        self._make_move(idx, self.current)

        if self.game_on and self.vs_ai and self.current == self.ai_symbol:
            self.root.after(400, self._ai_move)

    # ── MAKE MOVE ────────────────────────────────────────────
    def _make_move(self, idx, symbol):
        T = self.T
        self.board[idx] = symbol
        color = T["x_color"] if symbol == "X" else T["o_color"]
        self.cells[idx].configure(
            text=symbol,
            fg=color,
            bg=T["cell_bg"]
        )
        beep(900 if symbol == "X" else 1100, 50)

        winner_combo = self._check_winner()
        if winner_combo:
            self._highlight_win(winner_combo)
            self.score[symbol] += 1
            self._update_scores()
            beep(1400, 120)
            self.root.after(60, lambda: beep(1600, 120))
            self.root.after(120, lambda: beep(1800, 180))
            self.status_var.set(f"🎉 {self.names[symbol]} wins!")
            self.status_lbl.configure(fg=color)
            self.game_on = False
            return

        if "" not in self.board:
            self.score["D"] += 1
            self._update_scores()
            beep(400, 300)
            self.status_var.set("🤝 It's a Draw!")
            self.status_lbl.configure(fg=self.T["score_d"])
            self.game_on = False
            return

        # Switch player
        self.current = "O" if self.current == "X" else "X"
        self._update_status()

    # ── AI MOVE (minimax) ─────────────────────────────────────
    def _ai_move(self):
        if not self.game_on:
            return
        idx = self._best_move()
        self._make_move(idx, self.ai_symbol)

    def _best_move(self):
        # Try to win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai_symbol
                if self._check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        # Block opponent
        human = "X" if self.ai_symbol == "O" else "O"
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = human
                if self._check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        # Take center
        if self.board[4] == "":
            return 4
        # Take corners
        for i in [0, 2, 6, 8]:
            if self.board[i] == "":
                return i
        # Take any
        empties = [i for i in range(9) if self.board[i] == ""]
        return random.choice(empties)

    # ── WIN CHECK ────────────────────────────────────────────
    def _check_winner(self):
        for combo in WIN_COMBOS:
            a, b, c = combo
            if (self.board[a] != "" and
                    self.board[a] == self.board[b] == self.board[c]):
                return combo
        return None

    def _highlight_win(self, combo):
        T = self.T
        for idx in combo:
            self.cells[idx].configure(bg=T["win_bg"])

    # ── STATUS UPDATE ────────────────────────────────────────
    def _update_status(self):
        name = self.names[self.current]
        color = self.T["x_color"] if self.current == "X" else self.T["o_color"]
        self.status_var.set(f"{self.current}'s turn  →  {name}")
        self.status_lbl.configure(fg=color)

    # ── SCORE UPDATE ─────────────────────────────────────────
    def _update_scores(self):
        T = self.T
        for sym in ["X", "O", "D"]:
            key = "score_x" if sym == "X" else ("score_o" if sym == "O" else "score_d")
            self.score_labels[sym]["num"].configure(
                text=str(self.score[sym]), fg=T[key]
            )

    def _refresh_labels(self):
        T = self.T
        self.score_labels["X"]["name"].configure(text=self.names["X"])
        self.score_labels["O"]["name"].configure(text=self.names["O"])
        ai_label = "🤖 vs AI" if self.vs_ai else "👥 2 Player"
        if hasattr(self, "mode_btn"):
            self.mode_btn.configure(text=ai_label)

    # ── RESTART BOARD ────────────────────────────────────────
    def _restart_board(self):
        T = self.T
        self.board   = [""] * 9
        self.current = "X"
        self.game_on = True
        for btn in self.cells:
            btn.configure(text="", bg=T["cell_bg"], fg=T["text"])
        self._update_status()

    # ── RESET SCORES ─────────────────────────────────────────
    def _reset_scores(self):
        self.score = {"X": 0, "O": 0, "D": 0}
        self._update_scores()
        self._restart_board()

    # ── TOGGLE THEME ─────────────────────────────────────────
    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.T = THEMES[self.theme_name]
        lbl = "☀️ Light Mode" if self.theme_name == "dark" else "🌙 Dark Mode"
        self._rebuild_theme()
        self.theme_btn.configure(text=lbl)

    def _rebuild_theme(self):
        T = self.T
        self.root.configure(bg=T["bg"])
        self.title_lbl.configure(bg=T["bg"], fg=T["text"])
        self.score_frame.configure(bg=T["panel"])
        self.status_lbl.configure(bg=T["status_bg"])

        for sym, col_key in [("X","score_x"), ("O","score_o"), ("D","score_d")]:
            self.score_labels[sym]["name"].configure(bg=T["panel"], fg=T[col_key])
            self.score_labels[sym]["num"].configure(bg=T["panel"], fg=T[col_key])

        self.grid_frame.configure(bg=T["cell_border"])
        for i, btn in enumerate(self.cells):
            sym = self.board[i]
            if sym == "":
                btn.configure(bg=T["cell_bg"], fg=T["text"],
                              activebackground=T["cell_hover"])
            else:
                color = T["x_color"] if sym == "X" else T["o_color"]
                btn.configure(bg=T["cell_bg"], fg=color,
                              activebackground=T["cell_hover"])

        for b in [self.restart_btn, self.theme_btn, self.mode_btn, self.names_btn]:
            b.configure(bg=T["btn_bg"], fg=T["btn_fg"])

        # Re-highlight win cells if game over
        if not self.game_on:
            combo = self._check_winner()
            if combo:
                self._highlight_win(combo)

        self._update_status()

    # ── TOGGLE MODE ──────────────────────────────────────────
    def _toggle_mode(self):
        self.vs_ai = not self.vs_ai
        if self.vs_ai:
            self.names["O"] = "🤖 Computer"
        else:
            self.names["O"] = "Player O"
        self._refresh_labels()
        self._reset_scores()

    # ── CHANGE NAMES ─────────────────────────────────────────
    def _change_names(self):
        nx = simpledialog.askstring(
            "Rename", f"New name for X (current: {self.names['X']}):",
            initialvalue=self.names["X"], parent=self.root
        )
        if nx and nx.strip():
            self.names["X"] = nx.strip()[:14]

        if not self.vs_ai:
            no = simpledialog.askstring(
                "Rename", f"New name for O (current: {self.names['O']}):",
                initialvalue=self.names["O"], parent=self.root
            )
            if no and no.strip():
                self.names["O"] = no.strip()[:14]

        self._refresh_labels()
        self._update_scores()
        self._update_status()


# ─── ENTRY POINT ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x600")
    game = TicTacToe(root)
    root.mainloop()
