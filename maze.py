import tkinter as tk
import random
from tkinter import messagebox

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    path = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        path.append(current)

        if current == end:
            return path

        neighbors = get_neighbors(maze, current)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)

    return None

def get_neighbors(maze, position):
    neighbors = []
    x, y = position
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def generate_maze(size):
    maze = [[1] * size for _ in range(size)]
    start = (0, 0)
    end = (size - 1, size - 1)

    def carve_passages(cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 1:
                maze[nx - dx][ny - dy] = 0
                maze[nx][ny] = 0
                carve_passages(nx, ny)

    maze[start[0]][start[1]] = 0
    carve_passages(start[0], start[1])

    maze[end[0]][end[1]] = 0
    return maze, start, end

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=700, height=700, bg='white')
        self.canvas.pack()
        self.size = 31  # Increase the size for more complexity
        self.cell_size = 700 // self.size
        self.maze = None
        self.start = None
        self.end = None
        self.path = None
        self.current_position = None

        self.start_button = tk.Button(root, text="Find the Route", command=self.start_game, font=("Calibri", 24), fg="white", bg="gold", activebackground="white")
        self.start_button_window = self.canvas.create_window(350, 350, window=self.start_button)

        self.root.bind("<KeyPress>", self.handle_keypress)

        self.target_position = None
        self.move_speed = 10
        self.animation_speed = 0.02  # Adjust animation speed

        self.update()

    def start_game(self):
        self.canvas.delete(self.start_button_window)
        self.maze, self.start, self.end = generate_maze(self.size)
        self.path = dfs(self.maze, self.start, self.end)
        self.current_position = self.start
        self.target_position = self.start
        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        wall_thickness = self.cell_size * 0.001  # Adjust this value to change the thickness

        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size - wall_thickness
                y2 = y1 + self.cell_size - wall_thickness
                if self.maze[i][j] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='lightgrey', width=0)  # width=0 for no outline
                else:
                    self.canvas.create_rectangle(x1, y1, x2 + wall_thickness, y2 + wall_thickness, fill='lightgrey', outline='black', width=0)

        sx, sy = self.start
        ex, ey = self.end
        x1 = sy * self.cell_size
        y1 = sx * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='black')  # Start point

        x1 = ey * self.cell_size
        y1 = ex * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='black')  # End point

        cx, cy = self.current_position
        x1 = cy * self.cell_size + self.cell_size // 4
        y1 = cx * self.cell_size + self.cell_size // 4
        x2 = x1 + self.cell_size // 2
        y2 = y1 + self.cell_size // 2
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill='blue', outline='black')  # Player position
        

    def handle_keypress(self, event):
        if self.current_position is None:
            return

        cx, cy = self.current_position
        if event.keysym == "Up":
            nx, ny = int(cx - 1), int(cy)
        elif event.keysym == "Down":
            nx, ny = int(cx + 1), int(cy)
        elif event.keysym == "Left":
            nx, ny = int(cx), int(cy - 1)
        elif event.keysym == "Right":
            nx, ny = int(cx), int(cy + 1)
        else:
            return

        if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx][ny] == 0:
            self.target_position = (nx, ny)


    def update(self):
        if self.current_position and self.target_position and self.current_position != self.target_position:
            cx, cy = self.current_position
            tx, ty = self.target_position
            if cx < tx:
                cx += self.move_speed * self.animation_speed
            elif cx > tx:
                cx -= self.move_speed * self.animation_speed
            if cy < ty:
                cy += self.move_speed * self.animation_speed
            elif cy > ty:
                cy -= self.move_speed * self.animation_speed
            self.current_position = (round(cx, 2), round(cy, 2))
            self.canvas.coords(self.player, cy * self.cell_size + self.cell_size // 4, cx * self.cell_size + self.cell_size // 4, cy * self.cell_size + self.cell_size * 0.75, cx * self.cell_size + self.cell_size * 0.75)

            if self.current_position == self.end:
                self.show_congratulations()

        self.root.after(int(1000 / 60), self.update)


    def show_congratulations(self):
        messages = ["Congratulations!", "Genius!", "Well done!", "Amazing!"]
        messagebox.showinfo("Maze Game", random.choice(messages))
        self.current_position = None

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Hemu's Maze!")
    game = MazeGame(root)
    root.mainloop()
