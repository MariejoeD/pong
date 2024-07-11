import tkinter as tk
import random


class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Game")
        self.root.resizable(False, False)

        # Set the screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = int(screen_width * 0.75)
        height = int(screen_height * 0.75)

        # Center the window on the screen
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.width = width
        self.height = height

        self.create_menu_screen()

    def create_menu_screen(self):
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.canvas.create_text(self.width // 2, self.height // 3, text="Pong Game", font=("Arial", 50), fill="white")
        self.canvas.create_text(self.width // 2, self.height // 2, text="1 Player", font=("Arial", 30), fill="white",
                                tags="one_player")
        self.canvas.create_text(self.width // 2, self.height // 2 + 50, text="2 Players", font=("Arial", 30),
                                fill="white", tags="two_players")

        self.canvas.tag_bind("one_player", "<Button-1>", lambda e: self.start_game(single_player=True))
        self.canvas.tag_bind("two_players", "<Button-1>", lambda e: self.start_game(single_player=False))

    def start_game(self, single_player):
        self.canvas.destroy()

        self.single_player = single_player
        self.score_left = 0
        self.score_right = 0
        self.paused = False

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Paddle settings
        self.paddle_width = 10
        self.paddle_height = 100
        self.paddle_speed = 20

        # Ball settings
        self.ball_size = 20
        self.ball_speed_x = 5
        self.ball_speed_y = 5

        # Create paddles and ball
        self.paddle_left = self.canvas.create_rectangle(10, self.height // 2 - self.paddle_height // 2, 20,
                                                        self.height // 2 + self.paddle_height // 2, fill="white")
        self.paddle_right = self.canvas.create_rectangle(self.width - 20, self.height // 2 - self.paddle_height // 2,
                                                         self.width - 10, self.height // 2 + self.paddle_height // 2,
                                                         fill="white")
        self.ball = self.canvas.create_oval(self.width // 2 - self.ball_size // 2,
                                            self.height // 2 - self.ball_size // 2,
                                            self.width // 2 + self.ball_size // 2,
                                            self.height // 2 + self.ball_size // 2, fill="white")

        # Score display
        self.score_display = self.canvas.create_text(self.width // 2, 30,
                                                     text=f"{self.score_left} - {self.score_right}", font=("Arial", 30),
                                                     fill="white")

        # Create buttons on canvas
        self.pause_button = tk.Button(self.canvas, text="Pause", command=self.toggle_pause)
        self.canvas.create_window(self.width // 2 - 50, self.height - 30, anchor="center", window=self.pause_button)

        self.give_up_button = tk.Button(self.canvas, text="Give Up", command=self.give_up)
        self.canvas.create_window(self.width // 2 + 50, self.height - 30, anchor="center", window=self.give_up_button)

        # Bind the keys
        self.root.bind("<w>", self.move_paddle_left_up)
        self.root.bind("<s>", self.move_paddle_left_down)
        if self.single_player:
            self.root.bind("<Up>", self.move_paddle_right_ai)
        else:
            self.root.bind("<Up>", self.move_paddle_right_up)
            self.root.bind("<Down>", self.move_paddle_right_down)

        # Start the game loop
        self.update_game()

    def move_paddle_left_up(self, event):
        self.canvas.move(self.paddle_left, 0, -self.paddle_speed)

    def move_paddle_left_down(self, event):
        self.canvas.move(self.paddle_left, 0, self.paddle_speed)

    def move_paddle_right_up(self, event):
        self.canvas.move(self.paddle_right, 0, -self.paddle_speed)

    def move_paddle_right_down(self, event):
        self.canvas.move(self.paddle_right, 0, self.paddle_speed)

    def move_paddle_right_ai(self, event=None):
        paddle_coords = self.canvas.coords(self.paddle_right)
        ball_coords = self.canvas.coords(self.ball)

        if ball_coords[1] < paddle_coords[1]:
            self.canvas.move(self.paddle_right, 0, -self.paddle_speed)
        elif ball_coords[3] > paddle_coords[3]:
            self.canvas.move(self.paddle_right, 0, self.paddle_speed)

    def update_game(self):
        if not self.paused:
            self.move_ball()
            if self.single_player:
                self.move_paddle_right_ai()
        self.root.after(30, self.update_game)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        ball_coords = self.canvas.coords(self.ball)

        # Ball collision with top and bottom walls
        if ball_coords[1] <= 0 or ball_coords[3] >= self.canvas.winfo_height():
            self.ball_speed_y = -self.ball_speed_y

        # Ball collision with paddles
        if self.canvas.coords(self.paddle_left)[2] >= ball_coords[0] and self.canvas.coords(self.paddle_left)[1] <= \
                ball_coords[3] and self.canvas.coords(self.paddle_left)[3] >= ball_coords[1]:
            self.ball_speed_x = -self.ball_speed_x
        if self.canvas.coords(self.paddle_right)[0] <= ball_coords[2] and self.canvas.coords(self.paddle_right)[1] <= \
                ball_coords[3] and self.canvas.coords(self.paddle_right)[3] >= ball_coords[1]:
            self.ball_speed_x = -self.ball_speed_x

        # Ball goes out of bounds
        if ball_coords[0] <= 0:
            self.score_right += 1
            self.update_score()
            self.reset_ball()
        if ball_coords[2] >= self.canvas.winfo_width():
            self.score_left += 1
            self.update_score()
            self.reset_ball()

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=f"{self.score_left} - {self.score_right}")

    def reset_ball(self):
        self.canvas.coords(self.ball, self.canvas.winfo_width() // 2 - self.ball_size // 2,
                           self.canvas.winfo_height() // 2 - self.ball_size // 2,
                           self.canvas.winfo_width() // 2 + self.ball_size // 2,
                           self.canvas.winfo_height() // 2 + self.ball_size // 2)
        self.ball_speed_x = random.choice([-5, 5])
        self.ball_speed_y = random.choice([-5, 5])

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")

    def give_up(self):
        self.canvas.destroy()
        self.pause_button.destroy()
        self.give_up_button.destroy()
        self.create_menu_screen()


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()