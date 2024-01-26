import colorama
import keyboard
import time

from random import randint
from os import system

class window () :
	def __init__ (self) :
		self.y = 10
		self.x = 10

	def create_appel (self, blocks) :
		free_bloks = []

		for x in range(self.x) :
			for y in range(self.y) :
				if (x, y) not in blocks :
					free_bloks.append((x, y))

		return free_bloks[randint(0, len(free_bloks) - 1)]

	def create_frame (self, blocks, apple, size_snake) :
		frame = ""
		system("cls")

		for y in range(self.y) :
			for x in range(self.x) :
				for block_position in blocks + apple :
					if block_position[0] == x and block_position[1] == y :
						if x == apple[0][0] and y == apple[0][1] :
								frame += "()"
						else :
								frame += "[]"
						break
				else :
					frame += "  "
			frame += "│"
			frame += "\n"
		frame += "──" * self.x
		frame += "┘"

		print(frame)
		print(f"{size_snake:*^{self.x * 2 + 1}}")

class snake_obj() :
	def __init__(self, x, y) :
		self.x = x
		self.y = y
		self.size = 1
		self.body = []
		self.direction = "right"

	def change_direction (self, param) :
		if self.direction == "left" and param != "right" :
			self.direction = param
		if self.direction == "right" and param != "left" :
			self.direction = param
		if self.direction == "up" and param != "down" :
			self.direction = param
		if self.direction == "down" and param != "up" :
			self.direction = param
		time.sleep(0.3)

	def check_apple (self, apple) :
		if self.x == apple[0][0] and self.y == apple[0][1] :
			self.size += 1
			return True

	def move (self, win) :
		if self.direction == "right" : self.x = self.x + 1
		elif self.direction == "left" : self.x = self.x - 1
		elif self.direction == "up" : self.y = self.y - 1
		elif self.direction == "down" : self.y = self.y + 1

		if self.x > win[0] - 1 : self.x = 0
		elif self.x < 0 : self.x = win[0] - 1
		elif self.y > win[1] - 1 : self.y = 0
		elif self.y < 0 : self.y = win[1] - 1

		self.body.append((self.x, self.y))
		if len(self.body) > self.size :
			self.body.pop(0)

def main () :
	win = window()
	snake = snake_obj(round(win.x / 5) + 0, round(win.y / 2))
	apple_pos = [win.create_appel(snake.body)]
	system(f"mode con lines={win.y + 3} cols={win.x * 2 + 1}")

	keyboard.add_hotkey("right", lambda: snake.change_direction("right"))
	keyboard.add_hotkey("left", lambda: snake.change_direction("left"))
	keyboard.add_hotkey("up", lambda: snake.change_direction("up"))
	keyboard.add_hotkey("down", lambda: snake.change_direction("down"))

	fps = time.time()
	speed = time.time()

	while True :
		if time.time() >= fps + 0.2 :
			fps = time.time()
			if (win.x * win.y) / 2 <= snake.size and snake.size <= 400 :
				win.x = win.x + 5
				win.y = win.y + 5
				system(f"mode con lines={win.y + 3} cols={win.x * 2 + 1}")

			win.create_frame(snake.body, apple = apple_pos, size_snake = snake.size)

		if time.time() >= speed + 0.3 :
			speed = time.time()
			snake.move((win.x, win.y))
			if (snake.x, snake.y) in snake.body[:-1] : break
			if snake.check_apple(apple_pos) : apple_pos = [win.create_appel(snake.body)]

	input("game over")

if __name__ == '__main__':
	main()