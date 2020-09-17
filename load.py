import os
from puzzle import Puzzle
from PIL import Image, ImageTk
import pygame
from pygame import image
def load_img(path):
	return Image.open(path)

def divide_img(img, x, y, folder_name):
	img_x, img_y = img.size
	path = os.getcwd()+"\\"+ folder_name
	try:
		os.mkdir(path)
	except:
		pass
	for i in range(x):
		for j in range(y):
			new_img = img.crop((i*img_x/x, j*img_y/y, (i+1)*img_x/x
								, (j+1)*img_y/y))
			new_img.save(path+"\\"+str(i)+"_"+str(j)+".jpg")

def load_img_from_dir(path):
	img_array = []
	for file in os.listdir(path):
		x = int(file.split("_")[0])
		y = int(file.split("_")[1].split(".")[0])
		img_array.append(Puzzle(pygame.image.load(path+"\\"+file).convert_alpha(), x,y))
	return img_array

if __name__ == "__main__":
	cat = load_img("cat.jpg")
	divide_img(cat, 4, 4, "cat")