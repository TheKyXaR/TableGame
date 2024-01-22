import os
import keyboard
import time
from random import randint

class figure :  # це сука клас єбучий 
	def __init__ (self, x, y, form, angle, all_blocks) :  # головний метод класу (типу всяка інфа нахуй яку я зберігаю)
		self.x = x
		self.y = y
		self.form = form  # 1, 2, 3, 4, 5, 6, 7
		self.angle = angle  # 1, 2, 3, 4
		self.all_blocks = all_blocks

		# далі всі форми (іди нахуй Святослав це норм код)
		self.forms = {
			(1, 1): [(0, 0), (-1, 0), (1, 0), (2, 0)],
			(1, 2): [(0, 0), (0, -1), (0, 1), (0, 2)],
			(1, 3): [(0, 0), (-1, 0), (-2, 0), (1, 0)],
			(1, 4): [(0, 0), (0, -1), (0, -2), (0, 1)],
			(2, 1): [(0, 0), (1, 0), (0, 1), (1, 1)],
			(2, 2): [(0, 0), (1, 0), (0, 1), (1, 1)],
			(2, 3): [(0, 0), (1, 0), (0, 1), (1, 1)],
			(2, 4): [(0, 0), (1, 0), (0, 1), (1, 1)],
			(3, 1): [(0, 0), (-1, 0), (0, 1), (1, 1)],
			(3, 2): [(0, 0), (0, -1), (-1, 0), (-1, 1)],
			(3, 3): [(0, 0), (-1, 0), (0, 1), (1, 1)],
			(3, 4): [(0, 0), (0, -1), (-1, 0), (-1, 1)],
			(4, 1): [(0, 0), (1, 0), (0, 1), (-1, 1)],
			(4, 2): [(0, 0), (-1, -1), (-1, 0), (0, 1)],
			(4, 3): [(0, 0), (1, 0), (0, 1), (-1, 1)],
			(4, 4): [(0, 0), (-1, -1), (-1, 0), (0, 1)],
			(5, 1): [(0, 0), (-1, 0), (-1, 1), (1, 0)],
			(5, 2): [(0, 0), (0, -1), (-1, -1), (0, 1)],
			(5, 3): [(0, 0), (-1, 0), (1, 0), (1, -1)],
			(5, 4): [(0, 0), (0, -1), (0, 1), (1, 1)],
			(6, 1): [(0, 0), (-1, 0), (1, 1), (1, 0)],
			(6, 2): [(0, 0), (0, -1), (0, 1), (-1, 1)],
			(6, 3): [(0, 0), (-1, 0), (-1, -1), (1, 0)],
			(6, 4): [(0, 0), (0, -1), (0, 1), (1, -1)],
			(7, 1): [(0, 0), (-1, 0), (0, -1), (1, 0)],
			(7, 2): [(0, 0), (0, -1), (0, 1), (1, 0)],
			(7, 3): [(0, 0), (-1, 0), (0, 1), (1, 0)],
			(7, 4): [(0, 0), (0, -1), (0, 1), (-1, 0)],
		}

	def create_form (self, command) :  # тут короче взагалі піздєц сам робререшся
			if command == "create" :
				self.figure_form = [(block[0] + self.x, block[1] + self.y) for block in self.forms[(self.form, self.angle)]]
			else :
				for x in [(block[0] + command[0], block[1] + command[1]) for block in self.forms[(self.form, command[2])]] :
					if x in self.all_blocks or x[1] > 19 :  # if fall + rotate valid
						return False
					if x[0] < 0 or x[0] > 9 :  # if move x + rotate valid
						return False
				else :
					return True

	def rotate (self) :  # ця золупа вміє крутити фігуру коли це можливо
		if self.create_form((self.x, self.y, self.angle + 1 if self.angle < 4 else 1)) :
			self.angle = self.angle + 1 if self.angle < 4 else 1
			self.create_form("create")

	def move_x (self, param) :  # ця золупа вміє переміщати фігуру по осі Х коли це можливо
		if self.create_form((self.x + param, self.y, self.angle)) :
			self.x = self.x + param
			self.create_form("create")

	def fall (self):  # тут кокоче якщо фігура перемістилась то воно видає ТРУ нахуй (потім поймеш для чого)
		if self.create_form((self.x, self.y + 1, self.angle)) :
			self.y = self.y + 1
			self.create_form("create")
			return True
		else :
			return False

def create_frame (fall_figure, score = 0) :  # Тут просто створення кадра
	os.system("cls")
	frame = ""
	for y in range(20) :
		for x in range(10) :
			for block in fall_figure.figure_form + fall_figure.all_blocks :  #хуярим фігуру палкою
				if block[0] == x and block[1] == y :
					frame += "[]"
					break
			else :
				frame += "  "
		else :
			frame += "|"
		frame += "\n"
	else :
		frame += "--" * 10
	print(frame)
	print(f"{score:*^21}") 

def check_lose (all_blocks) :  # ця хуйня перевіряє чи ши ше не вмер ДИБІЛ  
	for x in all_blocks :
		if x[1] <= 0 :
			return True 

def check_lines (all_blocks) :  # а ця хуйня нахуй стирає всі заповнені лінії 
	new_array = [x[1] for x in all_blocks]
	del_line_index = [x for x in range(20) if new_array.count(x) == 10]
	if not bool(del_line_index) : return (all_blocks, len(del_line_index))
	del_line = []
	[[del_line.append((x, y)) for x in range(10)] for y in del_line_index]
	del_line = [x for x in all_blocks if x not in del_line]
	del_line = [(x[0], x[1] + len(del_line_index)) if x[1] < min(del_line_index) else x for x in del_line]
	return (del_line, len(del_line_index))

def main () :  # це типу початок роботи (ага на заводі блять)
	  # тут типу блок з перемінними
	score = 0
	all_blocks = []
	fall_figure = figure(4, 0, randint(1, 7), 1, all_blocks)
	fall_figure.create_form("create")

	fps = time.time()
	fall_figure_time = time.time()

	  # а тут блок Петра Ппорошенка 
	keyboard.add_hotkey("left", lambda: fall_figure.move_x(-1))
	keyboard.add_hotkey('right', lambda: fall_figure.move_x(1))
	keyboard.add_hotkey('up', lambda: fall_figure.rotate())

	while True :  # а тут вже натурі початок роботи на заводі
		if keyboard.is_pressed('down') : fall_figure_time_plus = 0.1  # якщо кнопка в низ блять іди нахуй довго пояснювати
		else : fall_figure_time_plus = 0.5

		if time.time() >= fps + 0.2 :  # ци типу як millis на ардуїно 
			  # тут ми просто виводимо на екран всякі штуки
			fps = time.time()
			lines = check_lines(fall_figure.all_blocks)

			fall_figure.all_blocks = lines[0]
			all_blocks = fall_figure.all_blocksS
			if lines[1] == 1 : score += 100
			elif lines[1] == 2 : score += 200
			elif lines[1] == 3 : score += 700
			elif lines[1] == 4 : score += 1500

			create_frame(fall_figure, score)
			if check_lose(fall_figure.all_blocks) :
				break

		if time.time() >= fall_figure_time + fall_figure_time_plus :  # ци типу як millis на ардуїно (да да другий раз)
			  # тут логіка вдарення об якусь хуйню
			  # да да тут якраз використовується те що золупа fall видає ТРУ
			fall_figure_time = time.time()
			if not fall_figure.fall() :
				all_blocks += fall_figure.figure_form
				  # тут просто пізда
				fall_figure = figure(5, 0, randint(1, 7), 1, all_blocks)
				fall_figure.create_form("create")

if __name__ == '__main__':  # а це щоб ніякий далбайоб не використовував мій код як бібліотеку нахуй
	main()  # це кривий стартер
input("game over")

# смерть блять

"""  життя після смерті
[][][][]

[][]
[][]

[][]
	[][]

	[][]
[][]


[][][]
[]

[][][]
		[]

	[]
[][][]
"""