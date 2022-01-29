import pygame
from .settings import *

class spritesheet(object):
	def __init__(self, filename):
		self.sheet = pygame.image.load(filename).convert()
	
	def image_at(self, rectangle, colorkey = None):
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey == -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return scale_image(image, SCALE_AMOUNT)
	
	def images_at(self, rects, colorkey = None):
		return [self.image_at(rect, colorkey) for rect in rects]
		
	def load_strip(self, rect, image_count, colorkey = None):
		tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
				for x in range(image_count)]
		return self.images_at(tups, colorkey)

def get_strip(filename, rect, image_count, colorKey=None, scale = 1):
	sheet = spritesheet(filename)
	images = sheet.load_strip(rect, image_count, colorKey)
	
	for i in range(len(images)):
		images[i] = scale_image(images[i], scale)
	return images