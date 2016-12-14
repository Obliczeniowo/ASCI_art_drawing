import tkinter as tk
from tkinter import filedialog as fd

class Application:
	def __init__(self):
		self.window = tk.Tk();
		self.window.title("obliczeniowo.com.pl/?id=571")
		self.buttons = [];
		
		signs = " ~!@#$%^&*()-+=|_\{}[];:'\",<.>?/"
		self.buttonset = tk.StringVar()
		self.buttonset.set("=")
		x = 0
		self.colors = []
		self.colorset = tk.StringVar()
		self.colorset.set("#ffffff")
		
		self.colors_t = {"#a50000": 31, "#00a100": 32, "#aa5500": 33, "#0000a8": 34, "#aa00aa": 35, "#00aaaa": 36, "#aaaaaa": 37, "#ff514a": 91, "#54ff55": 92, "#fcff55": 93, "#5455ff": 94, "#fc55ff": 95, "#54ffff": 96, "#ffffff": 97}
		
		self.width = 80
		self.height = 50
		
		self.sign_width = 10
		self.sign_height = 15
		
		for i in self.colors_t:
			self.colors += [tk.Radiobutton(self.window, text=" ", indicatoron = 0, variable = self.colorset, value = i, background = i, selectcolor = i)];
			
			self.colors[-1].place(x = x, y = 20, width = 20, height = 20)
			x += 20
		x = 0
		for i in signs:
			self.buttons += [tk.Radiobutton(self.window, text=i, indicatoron = 0, variable = self.buttonset, value = i)];
			
			self.buttons[-1].place(x = x, y = 0, width = 20, height = 20)
			x += 20
		
		self.menu = tk.Menu(self.window) # tworzenie menu
		
		cascade = tk.Menu(self.menu, tearoff = 0)
		self.menu.add_cascade(label="Program", menu = cascade)
		
		cascade.add_command(label = "Otwórz", command = self.openfile)
		cascade.add_command(label = "Zapisz", command = self.savefile)
		cascade.add_command(label = "Zapisz z kolorami jako py", command = self.savefileascolorspy)
		cascade.add_command(label = "Odczyt z kolorami z pliku py", command = self.openfileascolorspy)
		
		self.window.config(menu = self.menu)
		
		self.xscrollbar = tk.Scrollbar(self.window, orient = tk.HORIZONTAL)
				
		self.yscrollbar = tk.Scrollbar(self.window)
				
		self.canvas = tk.Canvas(self.window, background = "#000000", scrollregion = (0,0,self.width * self.sign_width, self.height * self.sign_height), xscrollcommand = self.xscrollbar.set, yscrollcommand = self.yscrollbar.set)
		self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S+tk.E+tk.W)
		self.canvas.place(in_ = self.window, x = 0, y = 40, relwidth = 1., relheight = 1., height = -60, width = -20)
		
		self.yscrollbar.place(in_ = self.canvas, rely = 0, relx = 1., relheight = 1.)
		self.xscrollbar.place(in_ = self.canvas, relx = 0, rely = 1., relwidth = 1.)
		
		self.xscrollbar.config(command = self.canvas.xview)
		self.yscrollbar.config(command = self.canvas.yview)

		for y in range(self.height):
			for x in range(self.width):
				self.canvas.create_text(x * self.sign_width, y * self.sign_height, text = " ", anchor = tk.NE, fill = self.colorset.get())
		
		self.canvas.bind("<B1-Motion>", self.mouse_move_lb)
		self.canvas.bind("<Button-1>", self.mouse_move_lb)
		self.canvas.bind("<B3-Motion>", self.mouse_move_rb)
		self.canvas.bind("<Button-3>", self.mouse_move_rb)
		
		self.window.mainloop()
		
	def mouse_move_lb(self, event):
		item = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
		self.canvas.itemconfig(item, text = self.buttonset.get(), fill = self.colorset.get())
		
	def mouse_move_rb(self, event):
		item = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
		self.canvas.itemconfig(item, text = " ", fill = self.colorset.get())
		
	def openfile(self):
		filename = fd.askopenfilename(filetypes=[("Plik tekstowy","*.txt")]) # wywołanie okna dialogowego open file
		
		if filename:
			with open(filename, "r", -1, "utf-8") as file:
				lines = file.readlines()
				for y in range(self.height):
					for x in range(self.width):
						item = self.canvas.find_closest((x - 0.5) * self.sign_width, (y - 0.5) * self.sign_height)
						self.canvas.itemconfig(item, text = lines[y][x], fill = self.collorset.get())
	def savefile(self):
		filename = fd.asksaveasfilename(filetypes=[("Plik tekstowy","*.txt")], defaultextension = "*.txt") # wywołanie okna dialogowego save file
		
		if filename:
			with open(filename, "w", -1, "utf-8") as file:
				for y in range(self.height):
					for x in range(self.width):
						item = self.canvas.find_closest((x - 0.5) * self.sign_width, (y - 0.5) * self.sign_height)
						item_config = self.canvas.itemconfig(item)
						file.write(item_config['text'][4])
					file.write('\n')

	def savefileascolorspy(self):
		filename = fd.asksaveasfilename(filetypes=[("Plik pythona","*.py")], defaultextension = "*.txt") # wywołanie okna dialogowego save file
		
		if filename:
			with open(filename, "w", -1, "utf-8") as file:
				file.write("print(\"\"\"\n")
				for y in range(self.height):
					for x in range(self.width):
						item = self.canvas.find_closest((x - 0.5) * self.sign_width, (y - 0.5) * self.sign_height)
						item_config = self.canvas.itemconfig(item)
						file.write("\\033[{color}m{text}".format(color = self.colors_t[item_config['fill'][4]], text = item_config['text'][4] if item_config['text'][4] != "\\" else "\\\\"))
					file.write('\n')
				file.write('""")')
	def findColor(self, value):
		value = int(value)
		for color, cid in self.colors_t.items():
			if value == cid:
				return color
		return "#ffffff"
	def openfileascolorspy(self):
		filename = fd.askopenfilename(filetypes=[("Plik pythona","*.py")]) # wywołanie okna dialogowego open file
		
		if filename:
			with open(filename, "r", -1, "utf-8") as file:
				lines = file.readlines()
				del(lines[0])
				del(lines[-1])
				for i in range(len(lines)):
					lines[i] = lines[i].split("\\033[")
					del(lines[i][0])
				for y in range(self.height):
					for x in range(self.width):
						item = self.canvas.find_closest((x - 0.5) * self.sign_width, (y - 0.5) * self.sign_height)
						self.canvas.itemconfig(item, text = lines[y][x].split("m",1)[1][0], fill = self.findColor(lines[y][x].split("m",1)[0]))

apl = Application()
