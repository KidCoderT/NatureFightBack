import imp
import random
import pygame
from .settings import *

class leaf_particle:
	def __init__(self, leaves, scatter = False):
		self.image = scale_image(random.choice(leaves), 0.2)
		self.vel = [random.randint(-2, 2), random.randint(1, 2)]
		self.x, self.y = random.randint(50, SCALE_WIDTH - 50), -random.randint(-50, 100)
		self.image.set_alpha(200)
		if scatter:
			self.x, self.y = random.randint(50, SCALE_WIDTH - 50), -random.randint(50, SCALE_HEIGHT - 50)
	
	def update(self):
		self.x += self.vel[0] + random.uniform(-1.0, 1.0)
		self.y += self.vel[1] + random.uniform(-1.0, 1.0)

	def render(self, screen):
		screen.blit(self.image, (self.x, self.y))

