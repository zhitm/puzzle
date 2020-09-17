import pygame
import sys
from random import randint
import os
from itertools import combinations
from load import load_img, load_img_from_dir, divide_img
import easygui
image = easygui.fileopenbox(filetypes=["*.jpg"])
folder_name = image.split("\\")[-1].split(".")[0]

x_divide = int(easygui.enterbox("Enter width of puzzle:"))
y_divide = int(easygui.enterbox("Enter height of puzzle:"))

divide_img(load_img(image), x_divide, y_divide, folder_name)

pygame.init()

SCREEN_X = 1920
SCREEN_Y = 1080
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.FULLSCREEN)
screen.fill((100, 150, 200))

path_to_puzzle = image.split(".")[0]
pzl_list = load_img_from_dir(path_to_puzzle)
pzl_xy_to_pzl = dict()

global moved_puzzle
moved_puzzle = None

for puzzle in pzl_list:
	pzl_xy_to_pzl.update({ (int(puzzle.pzl_x), int(puzzle.pzl_y)) : puzzle})
	puzzle.x = randint(250, SCREEN_X - 400)
	puzzle.y = randint(250, SCREEN_Y - 400)

pzl_width, pzl_height = pzl_list[0].size_x, pzl_list[0].size_y

list_of_union = []
def draw():
	for puzzle in pzl_list[::-1]:
		screen.blit(puzzle.image, (puzzle.x - int(pzl_width / 2), puzzle.y - int(pzl_height / 2)))

def is_near(pzl1, pzl2):
	px1 = pzl1.pzl_x
	px2 = pzl2.pzl_x
	py1 = pzl1.pzl_y
	py2 = pzl2.pzl_y
	dx = 5
	dy = 5
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
	vector = [0, 0]
	if pzl1.pzl_x == pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x
	if pzl1.pzl_y == pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y
	if pzl1.pzl_x > pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x - pzl_width
	elif pzl1.pzl_x < pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x + pzl_width
	if pzl1.pzl_y > pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y - pzl_height
	elif pzl1.pzl_y < pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y + pzl_height

	for pzl in pzl2.connected:
		if pzl != pzl1:
			pzl.x += vector[0]
			pzl.y += vector[1]

def unite_list(list1, list2):
	union = []
	for el in list1:
		if el not in union:
			union.append(el)
	for el in list2:
		if el not in union:
			union.append(el)
	return union

def connect():
	for A, B in combinations(pzl_list, 2):
		if is_near(A, B):
			if [A, B] not in list_of_union:
				teleportation(A, B)
				list_of_union.append([A, B])
				list_of_union.append([B, A])
			union = unite_list(A.connected, B.connected)
			A.connected = union
			B.connected = union
			for el in A.connected:
				el.connected = union
			for el in B.connected:
				el.connected = union

def clear_folder(path_to_folder):
	files = os.listdir(path_to_folder)
	for file in files:
		os.remove(path_to_folder+"\\"+file)

def are_you_win():
	(x, y) = max(pzl_xy_to_pzl.keys())
	pzl = pzl_list[0]
	if len(pzl.connected) == (x+1)*(y+1):
		easygui.msgbox("YOU WIN", "you win", "ok", "ball.jpg")
		return True
	return False


def push_to_the_top_of_array(pzl):
	pzl_list.remove(pzl)
	pzl_list.insert(0, pzl)

def move_segment(puzzle, vector):
	for pzl in puzzle.connected:
		pzl.x += vector[0]
		pzl.y += vector[1]
		push_to_the_top_of_array(pzl)
	push_to_the_top_of_array(puzzle)

def click(event):
	global moved_puzzle
	x, y = event.pos
	if moved_puzzle == None:
		for puzzle in pzl_list:
			if abs(puzzle.x - x) <= puzzle.size_x/2 and abs(puzzle.y - y) <= puzzle.size_y/2:
				vector = [x - puzzle.x, y - puzzle.y]
				move_segment(puzzle, vector)
				moved_puzzle = puzzle
				connect()
				break
	else:
		vector = [x - moved_puzzle.x, y - moved_puzzle.y]
		move_segment(moved_puzzle, vector)
		connect()


def quit():
	clear_folder(os.getcwd() + "\\" + folder_name)
	pygame.quit()
	sys.exit()

b1_is_clicked = False
game_is_not_over = True
while game_is_not_over:
	events = pygame.event.get()
	if are_you_win():
		game_is_not_over = False
		clear_folder(os.getcwd() + "\\" + folder_name)
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			b1_is_clicked = True
		elif event.type == pygame.MOUSEBUTTONUP:
			b1_is_clicked = False
			moved_puzzle = None
		elif event.type == pygame.MOUSEMOTION:
			if b1_is_clicked:
				click(event)
		elif event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()

	screen.fill((100, 150, 200))
	draw()
	pygame.display.update()

