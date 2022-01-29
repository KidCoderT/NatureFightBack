import pygame
from .settings import *
from .collisions import *
from .spritesheets import *

animations = {
	"idle": [
		pygame.image.load("assets/knight/idle/idle000.png").convert(),
		pygame.image.load("assets/knight/idle/idle001.png").convert(),
		pygame.image.load("assets/knight/idle/idle002.png").convert(),
		pygame.image.load("assets/knight/idle/idle003.png").convert(),
		pygame.image.load("assets/knight/idle/idle004.png").convert(),
		pygame.image.load("assets/knight/idle/idle005.png").convert(),
		pygame.image.load("assets/knight/idle/idle006.png").convert(),
		pygame.image.load("assets/knight/idle/idle007.png").convert(),
		pygame.image.load("assets/knight/idle/idle008.png").convert(),
		pygame.image.load("assets/knight/idle/idle009.png").convert()
	],
	"run": [
		pygame.image.load("assets/knight/run/run000.png").convert(),
		pygame.image.load("assets/knight/run/run001.png").convert(),
		pygame.image.load("assets/knight/run/run002.png").convert(),
		pygame.image.load("assets/knight/run/run003.png").convert(),
		pygame.image.load("assets/knight/run/run004.png").convert(),
		pygame.image.load("assets/knight/run/run005.png").convert(),
		pygame.image.load("assets/knight/run/run006.png").convert(),
		pygame.image.load("assets/knight/run/run007.png").convert(),
		pygame.image.load("assets/knight/run/run008.png").convert(),
		pygame.image.load("assets/knight/run/run009.png").convert()
	],
	"jump": pygame.image.load("assets/knight/jump/jump.png").convert(),
	"fall": pygame.image.load("assets/knight/fall/fall.png").convert(),
	"roll": [
		pygame.image.load("assets/knight/roll/roll000.png").convert(),
		pygame.image.load("assets/knight/roll/roll001.png").convert(),
		pygame.image.load("assets/knight/roll/roll002.png").convert(),
		pygame.image.load("assets/knight/roll/roll003.png").convert(),
		pygame.image.load("assets/knight/roll/roll004.png").convert(),
		pygame.image.load("assets/knight/roll/roll005.png").convert(),
		pygame.image.load("assets/knight/roll/roll006.png").convert(),
		pygame.image.load("assets/knight/roll/roll007.png").convert(),
		pygame.image.load("assets/knight/roll/roll008.png").convert(),
		pygame.image.load("assets/knight/roll/roll009.png").convert(),
		pygame.image.load("assets/knight/roll/roll010.png").convert(),
		pygame.image.load("assets/knight/roll/roll011.png").convert(),
		pygame.image.load("assets/knight/idle/idle000.png").convert()
	],
	"attack": [
		pygame.image.load("assets/knight/attack/attack000.png").convert(),
		pygame.image.load("assets/knight/attack/attack001.png").convert(),
		pygame.image.load("assets/knight/attack/attack002.png").convert(),
		pygame.image.load("assets/knight/attack/attack003.png").convert(),
	],
	"attackCombo": [
		pygame.image.load("assets/knight/attack/attack000.png").convert(),
		pygame.image.load("assets/knight/attack/attack001.png").convert(),
		pygame.image.load("assets/knight/attack/attack002.png").convert(),
		pygame.image.load("assets/knight/attack/attack003.png").convert(),
		pygame.image.load("assets/knight/attack2/attack000.png").convert(),
		pygame.image.load("assets/knight/attack2/attack001.png").convert(),
		pygame.image.load("assets/knight/attack2/attack002.png").convert(),
		pygame.image.load("assets/knight/attack2/attack003.png").convert(),
		pygame.image.load("assets/knight/attack2/attack004.png").convert(),
		pygame.image.load("assets/knight/attack2/attack005.png").convert(),
	],
}

class Player():
	jump_height = -12
	move_speed = 8

	def __init__(self, borders):
		self.move_right = False
		self.move_left = False

		self.y_momentum = 0
		self.air_timer = 0

		self.rect = pygame.Rect(30, SCALE_HEIGHT - 100, animations["idle"][0].get_width()/4, animations["idle"][0].get_height() / 2)
		self.borders = borders

		self.action = animations["idle"]
		self.current_frame = 0
		self.image = self.action[self.current_frame]
		self.facing_right = True
		self.attack_box = pygame.Rect(30 + animations["idle"][0].get_width()/4, SCALE_HEIGHT - 100, animations["idle"][0].get_width()/4, animations["idle"][0].get_height() / 2)

		self.attacking = False
		self.attack_timer = 0
		self.rolling = False
 	
	def update(self):
		if not self.attacking and not self.rolling:
			movement = [0, 0]
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				movement[0] += self.move_speed
				self.facing_right = True
			if keys[pygame.K_LEFT] or keys[pygame.K_a]:
				movement[0] -= self.move_speed
				self.facing_right = False
			
			movement[1] += self.y_momentum
			self.y_momentum += 1.1

			if self.y_momentum > 30:
				self.y_momentum = 30
			
			self.rect, collisions = move(self.rect, movement, self.borders)
			self.attack_box.x = self.rect.x + (animations["idle"][0].get_width()/4 if self.facing_right else -animations["idle"][0].get_width()/4)
			self.attack_box.y = self.rect.y
			
			if collisions['bottom']:
				self.air_timer = 0
			else:
				self.air_timer += 1
			
			if movement[0] == 0:
				self.action = animations["idle"]
			else:
				self.action = animations["run"]
			self.current_frame += 0.3 if self.action == animations["idle"] else 0.6
			if self.current_frame > len(self.action) - 1:
				self.current_frame = 0
			self.image = self.action[int(self.current_frame)]

			if self.y_momentum < 0:
				self.image = animations["jump"]
			elif self.y_momentum > 1 and not collisions['bottom']:
				self.image = animations["fall"]
		elif self.rolling:
			self.y_momentum += 2.4

			if self.y_momentum > 30:
				self.y_momentum = 30
			
			self.rect, collisions = move(self.rect, [self.move_speed*1.5 if self.facing_right else -self.move_speed*1.5, self.y_momentum], self.borders)
			self.attack_box.x = self.rect.x + (animations["idle"][0].get_width()/4 if self.facing_right else -animations["idle"][0].get_width()/4)
			self.attack_box.y = self.rect.y

			self.current_frame += 0.9
			if int(self.current_frame) > len(self.action) - 1:
				self.current_frame = 0
				self.rolling = False
			self.image = self.action[int(self.current_frame)]
		else:
			self.current_frame += 0.3 if self.action == animations["idle"] else 0.6
			if self.current_frame > len(self.action) - 1:
				self.current_frame = 0
				self.attacking = False
			self.image = self.action[int(self.current_frame)]
	
	def attack(self):
		if not self.rolling:
			if not self.attacking:
				self.attacking = True
				self.current_frame = 0
				self.action = animations["attack"]
				self.attack_timer = pygame.time.get_ticks()
			else:
				if pygame.time.get_ticks() - self.attack_timer < 300 and self.y_momentum :
					self.action = animations["attackCombo"]
	
	def roll(self):
		if not self.rolling and not self.attacking:
			self.rolling = True
			self.current_frame = 0
			self.action = animations["roll"]

	def render(self, screen):
		image = self.image
		# pygame.draw.rect(screen, (0, 0, 0), self.attack_box)
		if not self.facing_right:
			image = pygame.transform.flip(image, True, False)
			screen.blit(image, (self.rect.x - animations["idle"][0].get_width()/3 - 10, self.rect.y - 40))
		else:
			screen.blit(image, (self.rect.x - animations["idle"][0].get_width()/3, self.rect.y - 40))

