import pygame
import random
from settings import *
from collisions import *
from spritesheets import *

boss_hand_spritesheet = spritesheet("assets/boss/arm_projectile_glowing.png")
hand_attack_animations = \
	boss_hand_spritesheet.load_strip((0, 0, 100, 100), 3, (0, 0, 0)) + boss_hand_spritesheet.load_strip((0, 100, 100, 100), 3, (0, 0, 0))

hand_attack_animations = [scale_image(img, 0.5) for img in hand_attack_animations]

class BaseAttackHand:
	def __init__(self, gaurdian_rect, facing_right):
		self.rect = gaurdian_rect.copy()
		self.speed = 12 if facing_right else -12
		self.current_frame = 0
		self.image = hand_attack_animations[self.current_frame]
		self.state = 0
	
	def update(self):
		self.current_frame += 0.2
		if int(self.current_frame) > len(hand_attack_animations) - 1:
			self.current_frame = 0
		self.image = hand_attack_animations[int(self.current_frame)]

		if self.state == 0:
			self.rect.x += self.speed
			if self.rect.centerx < 0 or self.rect.centerx > SCALE_WIDTH:
				self.state = 2 
				self.rect.x += self.speed * 30
				self.speed = -self.speed * 1.8
				self.rect.y = random.randint(SCALE_HEIGHT - 95, SCALE_HEIGHT - 40)
		else:
			self.rect.x += self.speed
			if self.speed > 0 and self.rect.centerx > SCALE_WIDTH + 50:
				self.state = "done"
			elif self.speed < 0 and self.rect.centerx < -50:
				self.state = "done"
	
	def render(self, screen):
		image = self.image
		if self.speed < 5:
			image = pygame.transform.flip(self.image, True, False)
		screen.blit(image, (self.rect.centerx - self.image.get_width()/2, self.rect.centery - self.image.get_height()/2))

boss_spritesheet = spritesheet("assets/boss/spritesheet.png")

IDLE = "idle"
BASE_ATTACK = "base_attack"
SUPER_SMASH = "super_smash"
HELL_FIRE = "hell_fire"
TARGET_SHURIKEN = 3
BLAST_SHURIKEN = 4
COOLDOWN = "cooldown"

animations = {
	"idle": boss_spritesheet.load_strip((0, 0, 100, 100), 4, (0, 0, 0)),
	"base_attack": boss_spritesheet.load_strip((0, 200, 100, 100), 9, (0, 0, 0)),
	"super_smash": boss_spritesheet.load_strip((0, 300, 100, 100), 8, (0, 0, 0)),
	"cooldown": boss_spritesheet.load_strip((0, 600, 100, 100), 10, (0, 0, 0))
}

ATTACK_STAGES = {
	"1": [BASE_ATTACK, BASE_ATTACK, BASE_ATTACK, SUPER_SMASH],
	"2": [BASE_ATTACK, SUPER_SMASH, HELL_FIRE],
	"3": [SUPER_SMASH, HELL_FIRE, TARGET_SHURIKEN, BLAST_SHURIKEN],
}

animations["idle"] = [scale_image(img, 0.5) for img in animations["idle"]]
animations["base_attack"] = [scale_image(img, 0.5) for img in animations["base_attack"]]
animations["super_smash"] = [scale_image(img, 0.5) for img in animations["super_smash"]]
animations["cooldown"] = [scale_image(img, 0.5) for img in animations["cooldown"]]

class Boss:
	def __init__(self, player, borders):
		self.player = player
		self.rect = pygame.Rect(SCALE_WIDTH/2 + 45, -50, 50, 50)
		self.borders = borders
		self.entered = False
		self.stage = 1

		self.state = IDLE
		self.action = animations[self.state]
		self.current_frame = 0
		self.image = self.action[self.current_frame]
		self.facing_right = False
		self.entered_time = 0
		self.message = None
		self.attacking = False
		self.done_attack = False
		self.attack_hand= None
		self.idle_move = False
		self.idle_new_x = 0
		self.last_walked = 0
		self.walk_wait_times = 200
		self.times_to_attack = 8
		self.smash_times = random.randint(10, 25)
		self.smashed_times = 0
		self.start_y = 50
		self.moving_to_cooldown = False
		self.cooling_down = False
		self.moving_back = False
		self.cooling_down_start = 0
		self.low_y = SCALE_HEIGHT - 100

		self.max_health = 1000
		self.health = self.max_health
		self.health_bar_length = SCALE_WIDTH / 2
		self.health_ratio = self.max_health / self.health_bar_length
	
	def update(self):
		self.action = animations[self.state]
		if self.moving_to_cooldown or self.cooling_down or self.moving_back:
			if self.moving_to_cooldown:
				if self.rect.y < self.low_y:
					self.rect.y += 3
					if abs(self.rect.y - self.low_y) < 10:
						self.rect.y = self.low_y
						self.moving_to_cooldown = False
						self.cooling_down = True
						self.cooling_down_start = pygame.time.get_ticks()
			elif self.cooling_down:
				if pygame.time.get_ticks() - self.cooling_down_start > 4000:
					self.cooling_down = False
					self.moving_to_cooldown = False
					self.moving_back = True
					self.state = IDLE
			elif self.moving_back:
				if self.rect.y > self.start_y:
					self.rect.y -= 3
					if abs(self.rect.y - self.start_y) < 10:
						self.rect.y = self.start_y
						self.moving_to_cooldown = False
						self.moving_back = False
			self.current_frame += 0.2
			if int(self.current_frame) > len(self.action) - 1:
				self.current_frame = 0
		elif self.attacking:
			if self.state == BASE_ATTACK:
				self.current_frame += 0.6
				if int(self.current_frame) > len(self.action) - 1:
					self.done_attack = True
					self.current_frame = len(self.action) - 1
				elif int(self.current_frame) > len(self.action) - 2 and self.attack_hand is None:
					self.attack_hand = BaseAttackHand(self.rect, self.facing_right)
					self.attacking = False
					self.times_to_attack -= 1
			elif self.state == SUPER_SMASH:
				if int(self.current_frame) < len(self.action) - 1 and not self.smashed_times >= self.smash_times:
					self.current_frame += 0.2
				elif self.smashed_times >= self.smash_times:
					if self.rect.y < self.start_y:
						self.rect.y += 25 * 0.15
						if self.current_frame > 0:
							self.current_frame -= 0.2
						
						if abs(self.rect.y - self.start_y) < 5:
							self.rect.y = self.start_y
							self.state = IDLE
							self.times_to_attack -= 1
							self.attacking = False
				else:
					self.rect.y += 28
					if self.rect.y > SCALE_HEIGHT + 100:
						self.rect.y = - 100
						self.rect.centerx = self.player.rect.centerx
						self.smashed_times += 1
						if self.smashed_times >= self.smash_times:
							self.rect.centerx = SCALE_WIDTH / 2
		else:
			self.current_frame += 0.09
			if int(self.current_frame) > len(self.action) - 1:
				self.current_frame = 0
				self.state = IDLE
		self.image = self.action[int(self.current_frame)]

		if self.attack_hand is not None and self.attack_hand.state == "done":
			self.attack_hand = None

		if self.state == IDLE and self.entered:
			if not self.idle_move:
				if pygame.time.get_ticks() - self.last_walked > self.walk_wait_times:
					if random.randint(0, 100) > 80:
						self.idle_move = True
						self.idle_new_x = random.randint(50, SCALE_WIDTH - 100)
						while abs(self.rect.x - self.idle_new_x) < 50:
							self.idle_new_x = random.randint(100, SCALE_WIDTH - 100)
						if self.idle_new_x > self.rect.x:
							self.facing_right = True
						else:
							self.facing_right = False
			else:
				self.rect.x += (self.idle_new_x - self.rect.x) * 0.04
				if abs(self.rect.x - self.idle_new_x) < 30:
					self.idle_new_x = 0
					self.idle_move = False
					self.last_walked = pygame.time.get_ticks()
					self.walk_wait_times = random.randint(200, 1200)
		
		if self.times_to_attack <= 0:
			self.times_to_attack = random.randint(10, 20)
			self.moving_to_cooldown = True
			self.state = COOLDOWN

		if not self.entered:
			if self.rect.y < SCALE_HEIGHT/2 - 100:
				self.rect.y += 2
			else:
				if self.entered_time == 0:
					self.entered_time = pygame.time.get_ticks()
					self.message = {
						"create_time": pygame.time.get_ticks(),
						"text": "HUMANS MUST DIE!!!!!",
						"multiline": False,
						"wait_time": 1500
					}
				else:
					if pygame.time.get_ticks() - self.entered_time > 500:
						self.entered = True
						self.state = BASE_ATTACK
						self.attacking = True
		
		if self.entered and not self.attacking and self.attack_hand is None and not self.moving_to_cooldown and not self.cooling_down and not self.moving_back:
			attack = random.choice(ATTACK_STAGES[str(self.stage)])
			if attack == BASE_ATTACK:
				self.state = BASE_ATTACK
				self.attacking = True
			elif attack == SUPER_SMASH:
				self.state = SUPER_SMASH
				self.attacking = True
				self.smashed_times = 0
				self.smash_times = random.randint(10, 25)
		
		if pygame.mouse.get_pressed()[0]:
			self.health -= 6

		if self.health > self.max_health * 2/3:
			self.stage = 1
		elif self.health > self.max_health * 2/3:
			self.stage = 2
		else:
			self.stage = 3

	
	def render(self, screen):		
		# pygame.draw.rect(screen, (0, 255, 0), self.rect)
		image = self.image
		if not self.facing_right:
			image = pygame.transform.flip(self.image, True, False)
		
		if self.state == SUPER_SMASH and int(self.current_frame) >= len(self.action) - 2:
			outline_mask(image, (self.rect.x - self.rect.width, self.rect.y - self.rect.width), screen)

		screen.blit(image, (self.rect.centerx - self.image.get_width()/2, self.rect.centery - self.image.get_height()/2))

		if self.message is not None:
			if pygame.time.get_ticks() - self.message["create_time"] > self.message["wait_time"]:
				self.message = None
			else:
				text = MESSAGE_TEXT_FONT.render(self.message["text"], False, (255, 255, 255))
				screen.blit(text, (self.rect.centerx - text.get_width()/2, self.rect.centery - 60))
		
		if self.message is None and self.entered:
			width = self.health / self.health_ratio
			pygame.draw.rect(screen, (255, 0, 0),(SCALE_WIDTH/2 - self.health_bar_length/2, 10, width, 15))
			pygame.draw.rect(screen, (0, 0, 0),(SCALE_WIDTH/2 - self.health_bar_length/2, 10, self.health_bar_length, 15), 2)
		
		if self.attack_hand is not None:
			self.attack_hand.update()
			self.attack_hand.render(screen)

