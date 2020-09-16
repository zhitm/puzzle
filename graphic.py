import pygame
import sys
from random import randint
import os
from itertools import combinations
from load import load_img, load_img_from_dir, divide_img
pygame.init()
SCREEN_X = 1920
SCREEN_Y = 1080
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
screen.fill((100, 150, 200))

pzl_list = load_img_from_dir(os.getcwd()+"\\cat")
pzl_xy_to_pzl = dict()

for puzzle in pzl_list:
	pzl_xy_to_pzl.update({ (int(puzzle.pzl_x), int(puzzle.pzl_y)) : puzzle})
	puzzle.x = randint(250, SCREEN_X - 400)
	puzzle.y = randint(250, SCREEN_Y - 400)

pzl_width, pzl_height = pzl_list[0].size_x, pzl_list[0].size_y

def draw():
	for puzzle in pzl_list:
		screen.blit(puzzle.image, (puzzle.x - int(pzl_width / 2), puzzle.y - int(pzl_height / 2)))

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
	if pzl1.pzl_y == pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y
	if pzl1.pzl_x > pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x - pzl_width
	elif pzl1.pzl_x < pzl2.pzl_x:
		vector[0] = pzl1.x - pzl2.x + pzl_width
	if pzl1.pzl_y > pzl2.y:
		vector[1] = pzl1.y - pzl2.y - pzl_height
	elif pzl1.pzl_y < pzl2.pzl_y:
		vector[1] = pzl1.y - pzl2.y + pzl_height

	for pzl in pzl2.connected:
		if pzl!= pzl1:
			pzl.x += vector[0]
			pzl.y += vector[1]



def connect():
	for pzl, pzl1 in combinations(pzl_list, 2):
		if is_near(pzl, pzl1):
			if pzl not in pzl1.connected:
				for el in pzl.connected:
					if el not in pzl1.connected:
						pzl1.connected.append(el)
						if pzl not in el.connected:
							el.connected.append(pzl)
						if pzl1 not in el.connected:
							el.connected.append(pzl1)

				for el in pzl1.connected:
					if el not in pzl.connected:
						pzl.connected.append(el)
						if pzl1 not in el.connected:
							el.connected.append(pzl1)
						if pzl not in el.connected:
							el.connected.append(pzl)

				teleportation(pzl, pzl1)

def click(event):
	for puzzle in pzl_list:
		x, y = event.pos
		if abs(puzzle.x - x) < 50 and abs(puzzle.y - y) < 50:
			vector = [x - puzzle.x, y - puzzle.y]
			for pzl in puzzle.connected:
				pzl.x += vector[0]
				pzl.y += vector[1]
				connect()
			break

b1_is_clicked = False

while 1:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			b1_is_clicked = True
		elif event.type == pygame.MOUSEBUTTONUP:
			b1_is_clicked = False
		elif event.type == pygame.MOUSEMOTION:
			if b1_is_clicked:
				click(event)
		elif event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill((100, 150, 200))
	draw()
	pygame.display.update()

