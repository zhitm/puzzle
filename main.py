from tkinter import *
from random import randint
import os
from itertools import combinations
from puzzle import Puzzle
from load import load_img, load_img_from_dir, divide_img
from PIL import Image, ImageTk
x = 1920
y = 1080
root = Tk()
pzl_list = load_img_from_dir(os.getcwd()+"\\cat")
pzl_width, pzl_height = pzl_list[0].image.size
pzl_xy_to_pzl = dict()

for puzzle in pzl_list:
	pzl_xy_to_pzl.update({ (int(puzzle.pzl_x), int(puzzle.pzl_y)) : puzzle})
	puzzle.x = randint(250, x - 400)
	puzzle.y = randint(250, y - 400)
	puzzle.label.place(x = puzzle.x - int(pzl_width/2), y = puzzle.y - int(pzl_height/2))

def check():
	(x, y) = max(pzl_xy_to_pzl.keys())

	for j in range(y):
		for i in range(x-1):
			pzl1 = pzl_xy_to_pzl[i, j]
			pzl2 = pzl_xy_to_pzl[i+1, j]
			if not (pzl2.x - pzl1.x > pzl_width-10 and  pzl2.x - pzl1.x < pzl_width + 10 and abs(pzl2.y - pzl1.y) < 10):
				print("false")
				return False
	for i in range(y - 1):
		pzl1 = pzl_xy_to_pzl[0, j]
		pzl2 = pzl_xy_to_pzl[0, j+1]
		if not (pzl2.y - pzl1.y > pzl_height - 10 and  pzl2.y - pzl1.y < pzl_height + 10 and abs(pzl2.x - pzl1.x) < 10):
			print("false")
			return False
	print("true")
	return True
def is_near(pzl1, pzl2):
	px1 = pzl1.pzl_x
	px2 = pzl2.pzl_x
	py1 = pzl1.pzl_y
	py2 = pzl2.pzl_y
	dx = 10
	dy = 10
	if ((px1-px2) == 0 or (py1-py2) == 0) and (abs(px1-px2) == 1 or abs(py1-py2) == 1):
		if px1 == px2:
			if not abs(pzl1.x - pzl2.x) < dx:
				return False
		if py1 == py2:
			if not abs(pzl1.y - pzl2.y) < dy:
				return False
		if px1 < px2:
			if not(pzl2.x - pzl1.x > pzl_width-dx and pzl2.x - pzl1.x < pzl_width + dx):
				return False
		if px1 > px2:
			if not(pzl1.x - pzl2.x > pzl_width-dx and pzl1.x - pzl2.x < pzl_width + dx):
				return False
		if py1 > py2:
			if not(pzl1.y - pzl2.y > pzl_height-dy and pzl1.y - pzl2.y < pzl_height+ dy):
				return False
		if py1 < py2:
			if not(pzl2.y - pzl1.y > pzl_height-dy and pzl2.y - pzl1.y < pzl_height+ dy):
				return False
		return True
def teleportation(pzl1, pzl2):
	vector = [0,0]
	if pzl1.pzl_x == pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x
		print(1, "x=")

	if pzl1.pzl_y == pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y
		print(2, "y=")
	if pzl1.pzl_x > pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x - pzl_width
		print(3, "x>")
	elif pzl1.pzl_x < pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x + pzl_width
		print(4, "x<")
	if pzl1.pzl_y > pzl2.y:
		vector[1] = pzl1.y - pzl2.y - pzl_height
		print(5, "y>")
	elif pzl1.pzl_y < pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y + pzl_height
		print(6, "y<")
	print("-----------------------------------------------------")

	for pzl in pzl2.connected:
		if pzl!= pzl1:
			pzl.x += vector[0]
			pzl.y += vector[1]
			pzl.label.place(x=pzl.x - int(pzl_width / 2), y=pzl.y - int(pzl_height / 2))

def connect():
#	(x, y) = max(pzl_xy_to_pzl.keys())
	for pzl, pzl1 in combinations(pzl_list, 2):
		if is_near(pzl, pzl1):
			for el in pzl.connected:
				if el not in pzl1.connected:
					pzl1.connected.append(el)
			for el in pzl1.connected:
				if el not in pzl.connected:
					pzl.connected.append(el)
			teleportation(pzl, pzl1)


def click(event):
	for puzzle in pzl_list:
		abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
		abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
		if abs(puzzle.x - abs_coord_x ) < 50 and abs(puzzle.y - abs_coord_y) < 50:
			vector = [abs_coord_x - puzzle.x, abs_coord_y - puzzle.y]
			for pzl in puzzle.connected:
				pzl.x += vector[0]
				pzl.y += vector[1]
				pzl.label.place(x = pzl.x - int(pzl_width/2), y = pzl.y - int(pzl_height/2))
				connect()
			break
root.bind('<B1-Motion>', click)
btn = Button(text = "check puzzle", command = check)
btn.pack()
root.mainloop()
