



import pygame
from sys import exit
from random import randint, choice


class Ship(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.keys = pygame.key.get_pressed()
		ship_surf1 = pygame.image.load('images/ship1.png').convert_alpha()
		ship_surf1 =  pygame.transform.rotozoom(ship_surf1, 180, 1)
		ship_surf2 = pygame.image.load('images/ship2.png').convert_alpha()
		ship_surf2 =  pygame.transform.rotozoom(ship_surf2, 180, 1)
		ship_surf3 = pygame.image.load('images/ship3.png').convert_alpha()
		ship_surf3 =  pygame.transform.rotozoom(ship_surf3, 180, 1)
		self.ship_index = 0
		self.ship_fly = [ship_surf1, ship_surf2, ship_surf3]
		self.image = self.ship_fly[self.ship_index]
		self.rect = self.image.get_rect(midbottom = (300,750))
		self.momentum = 0
		self.gun_cool = 0
		# this is the value I need to get out. it updates every cycle on line 74
		self.hitbox = pygame.Rect(self.rect.x + 27, self.rect.y + 18, self.rect.width-47, self.rect.height - 70)
		self.shoot_sound = pygame.mixer.Sound('soundfx/laserpew.ogg')
		self.shoot_sound.set_volume(0.2)
	# cycle the ship animation
	def ship_animation(self):
		self.ship_index += .2
		if self.ship_index >= len(self.ship_fly):
			self.ship_index = 0
		self.image = self.ship_fly[int(self.ship_index)]
		
		
	# adjusts total momentum
	def player_input(self):
		# tracks player inputs
		if keys[pygame.K_a] and self.rect.x >= -10:
			self.momentum -= 0.15
		elif keys[pygame.K_d] and self.rect.x <= 600:
			self.momentum += 0.15
		# coast slow down	
		elif self.momentum < 0.05 and self.momentum > -0.05:
			self.momentum = 0
		elif self.momentum < 0:
			self.momentum += 0.1
		elif self.momentum > 0:
			self.momentum -= 0.1	
		# stops overspeed
		if self.momentum > 6:
			self.momentum = 6
		elif self.momentum < -6:
			self.momentum = -6
			
	# it shoots what els would it do?	
	def shoot(self):
		if keys[pygame.K_SPACE] and self.gun_cool == 0:
			projectile_group.add(Projectile(self.rect))
			self.shoot_sound.play()
			self.gun_cool = 20
		else:
			if self.gun_cool > 0:
				self.gun_cool -= 1
		
		
	# updates the position of the ship based on the momentum
	def ship_movement(self):
		# check for edge of screen
		if self.rect.left < -50:
			self.rect.left = -50
			self.momentum = 0
		if self.rect.right > 650:
			self.rect.right = 650
			self.momentum = 0
			
		# updates the ship position
		# the hitbox updates here
		self.hitbox = pygame.Rect(self.rect.x + 27, self.rect.y + 18, self.rect.width-47, self.rect.height - 70)
		self.rect.x = self.rect.x + int(self.momentum)
		
		#draws the ship hitbox
		#pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
	

#	def get_hitbox(self):
#		return self.hitboxS
	
	# the function called in the main loop		
	def update(self):
		self.ship_animation()
		self.player_input()
		self.ship_movement()
		self.shoot()
#===========================================================================


class enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		duck_surf = pygame.image.load('images/parrot.png').convert_alpha()
		duck_surf1 =  pygame.transform.rotozoom(duck_surf, 0, 2)
		duck_surf2 =  pygame.transform.rotozoom(duck_surf, 350, 2)
		duck_surf3 =  pygame.transform.rotozoom(duck_surf, 10, 2)
		self.duck_walk = [duck_surf1, duck_surf2, duck_surf1, duck_surf3]
		self.walk_index = 0
		self.image = self.duck_walk[self.walk_index]
		self.rect = self.image.get_rect(midbottom = (randint(0,600),0))
		#self.hitbox = pygame.Rect.(self.rect.x + 0, self.rect.y + 0, self.rect.width - 0, self.rect.height - 0)
		self.health = 2
		self.explode_sound = pygame.mixer.Sound('soundfx/hit01.wav')
		self.explode_sound.set_volume(0.2)
		
	
	
	def duck_animation(self):
		self.walk_index += .1
		if self.walk_index >= len(self.duck_walk):
			self.walk_index = 0
		
		#pygame.draw.rect(screen, (255,0,0), self.rect, 2)
		self.image = self.duck_walk[int(self.walk_index)]
			
	# eliminates the enemies and increases the score as required		
	def destroy(self):
		global score
		if self.rect.y >= 800:
			self.kill()	
			

		for enemy in pygame.sprite.groupcollide(enemy_group, projectile_group, False, True):
			enemy.health -= 1
			pygame.mixer.Sound.play(self.explode_sound)
			if enemy.health < 1:
				score += 2
				enemy.kill()
		
	def get_hitbox(self):
		return self.hitbox
		
	def update(self):
		self.duck_animation()
		self.rect.y += 6
		self.destroy()

#================================================================================

class Projectile(pygame.sprite.Sprite):
	def __init__(self, rect):
		super().__init__()

		projectile1_surf = pygame.image.load('images/projectile1.png').convert_alpha()
		self.projectile1_surf1 = pygame.transform.rotozoom(projectile1_surf, 0, 2)
		self.image = self.projectile1_surf1
		self.rect = self.image.get_rect(midtop = (rect.x + 53, 620))
		
	def movement(self):
		self.image = self.projectile1_surf1
	
	def destroy(self):
		if self.rect.bottom <= 0:
			self.kill()	
	
	def update(self):
		self.rect.y -= 6
		self.movement()
		self.destroy()
#=============================================================================

# keeps the score updated
def display_score(score):
	score_surf= score_font.render("SCORE: " + str(score), False, (255,255,255))
	if game_active:
		score_rect = score_surf.get_rect(topleft = (20, 20))
		screen.blit(score_surf, (score_rect))
	else:
		score_rect = score_surf.get_rect(midtop = (300, 200))
		screen.blit(score_surf, (score_rect))
	return score


# checks for collisions between the ship and enemies
def collision_sprite():
	for enemy in enemy_group:
		if ship.sprite.hitbox.colliderect(enemy.rect):
			enemy_group.empty()
			projectile_group.empty()
			return False
	else: return True




# initial settings
pygame.mixer.pre_init(44100, -16, 2, 64)
pygame.mixer.init()
pygame.init()

music = pygame.mixer.Sound('soundfx/2010_June_HypnoticChill_17.ogg')
music.set_volume(0.3)
music.play()

screen = pygame.display.set_mode((600,800))
pygame.display.set_caption('Space Slalom')
clock = pygame.time.Clock()
score = 0
score_font = pygame.font.Font(None, 40)
game_active = False

# controls on start screen
controls_surf= score_font.render("s  to start    a / d to move spacebar to shoot", False, (255,255,255))
controls_rect = controls_surf.get_rect(midtop = (300, 300))

#import background
game_background = pygame.image.load('images/space_background.png').convert()
space_rect = game_background.get_rect(topleft = (0,0))

# groups
ship = pygame.sprite.GroupSingle()
ship.add(Ship())
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

#timers
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 300)


# main game loop
while True:
	
	for event in pygame.event.get():
		keys = pygame.key.get_pressed()
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
			
		if game_active:
		
			if event.type == enemy_timer:
				enemy_group.add(enemy())
				

		else:
			
			if keys[pygame.K_s]:
				game_active = True
				score = 0
	if game_active:
		
		screen.blit(game_background,(space_rect))
		
		display_score(score)
		
		projectile_group.draw(screen)
		projectile_group.update()
		
		ship.draw(screen)
		ship.update()
		
		enemy_group.draw(screen)
		enemy_group.update()
		

		# to check for collision
		game_active = collision_sprite()
		
	# title screen
	else:
		screen.fill((50,50,50))
		screen.blit(controls_surf, (controls_rect))
		display_score(score)
	
	
	pygame.display.update()
	clock.tick(60)
	

	
	
	
