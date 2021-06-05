
"""

===============================================
			Space Invaders PyGame
===============================================

This game is based on the popular game "Space Invaders".
Written in Python 3 using PyGame.

- In-game controls:
	SPACE - Shoot laser
	A, Left-arrow 	- Move left
	D, right-arrow 	- Move right
	P 				- Pause game



	VERSIONS

	1.0.0 - 16 Mar 2020
		-First playable version of game.
		-One level, kill 25 invaders.
		-Shoot, move, and pause game

	1.0.1 - 17 Mar 2020
		-Set keys for moving left/right to A and D too.


	FUTURE DEVELOPMENT

	- Invaders shoot at random times
	- Invaders move left-right randomly
	- Special invaders harder to kill
	- Introduce levels. Each level is harder:
		--More invaders to kill
		--Invader move faster, shoot faster, etc

	- Killing invaders gives you credit to spend in store
		at the end of each level
	- Upgrades in store include:
		--Faster ship moving
		--Faster fire rate
		--New ship designs
		--More ship lives
"""


import pygame
from pygame.locals import *
import sys
import random



# ========== Colours ===========
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0, 255, 0)


# ========= Images ==========
BG = pygame.image.load('art/background.png')
INV = pygame.image.load('art/invader.png')
LASER = pygame.image.load('art/laser.png')
PLY = pygame.image.load('art/player.png')




# ============================== CLASSES ===========================

class Game:
	def __init__(self, screen_xy):
		self.status = 0
		# 0 - playing/default
		# 1 - player wins
		# 2 - player dead
		# 3 - quit game

		self.screen_xy = screen_xy
		self.clock = pygame.time.Clock()
		self.game_time = 0

		self.win_score = 25

		self.START_RUN = True	#While loop for start screen
		self.RUN = True			#While loop for main game loop
		self.END_RUN = True		#While loop for win/death end screen
		self.QUIT_ALL = False	#Bool for ending it all
		self.restart = True

		self.title_font = pygame.font.SysFont('verdana', 30, True)
		self.subtitle_font = pygame.font.SysFont('verdana', 14, True)

	def check_status(self, player, invader):

		# Fails game if player is dead
		if player.isdead == True:
			game.status = 2
			game.RUN = False
			return

		# Fails game if an invader went too far
		for i in range(0, len(invader)):
			if invader[i].y >= player.y:
				print('You loose!')
				game.status = 2
				game.RUN = False
				return

		# Wins the game if the player got the win score
		if player.score >= game.win_score:
			print('You win!')
			game.RUN = False
			game.status = 1
			return



class Invader:

	def __init__(self, x, laser_counter):
		self.x = x			# Initial = random.randint(10, 590)
		self.y = 20
		self.speed = 20
		self.size = (30, 37)
		self.isdead = False
		self.step_time = 0	#Tracks time between invader steps
		self.gap_time = 10000	# Step gap time (jumps each x miliseconds)
		self.laser_counter = laser_counter
		self.color = RED

	def draw_self(self, screen):
		if self.isdead == False:
			screen.blit(INV, (self.x, self.y))
			self.step_time += 100

	def step_forward(self):
		if self.isdead==False and self.step_time==self.gap_time:
			self.step_time = 0
			self.y += self.speed

	def randomize_gap(self):
		self.gap_time = int(random.uniform(500, 2000))



class new_invader_parameters():
	def __init__(self):
		self.gap = 20000		#Gap between new invaders in ms
		self.gap_factor = 0.999
			#Factor at which time gap is reduced after each new invader - increases difficulty
			#	At 1 the time gap doesn't change.
			#	At >1 the time gap increases
			#	At <1 the time gap decreases

		self.counter = self.gap #Time counter between invaders
		self.total_enemies = 0
		self.max_enemies = 25

	def new_invader(self, invader, game):

		if (self.counter >= self.gap) and self.total_enemies < game.win_score:
			
			test_inv = Invader(0, self.gap)

			min_x = 0
			max_x = int( game.screen_xy[0] - test_inv.size[0] )

			new_x = random.randint(min_x, max_x)
			invader.append( Invader(new_x, self.gap) )
			self.total_enemies += 1

			self.counter = 0
			self.gap *= self.gap_factor

		self.counter += 100



class Player:

	def __init__(self):
		self.x = 300
		self.y = 500
		self.speed = 2
		self.size = (25, 30)	# Length/width
		self.isdead = False
		self.color = BLUE
		self.score = 0
		self.laser_counter = 0
	
	def draw_self(self, screen):
		screen.blit(PLY, (self.x, self.y))

	def moving(self, keys):
			# Moves player left and right
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.x >= 0):
			self.x -= self.speed

		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.x+self.size[0] <= screen_xy[0]):
			self.x += self.speed	



class Projectile:

	def __init__(self, x, y, ptype):
		self.ptype = ptype
			# 0 for player laser
			# 1 for invader laser
		self.x = x
		self.y = y
		self.speed = 3
		self.size = (3,8)
		self.color = BLACK
		self.isdead = False

	def draw_self(self, screen):
		screen.blit(LASER, (self.x, self.y))

	def moving(self):
		if self.ptype == 0:
			self.y -= self.speed

		else:
			self.y += self.speed

		# Delete projectile if out of bounds of screen
		if self.y>=screen_xy[1] or self.y<=0:
			self.isdead = True

	def impact(self, target):

		check_impact = False

		x_hit = False
		y_hit = False

		if (self.x + self.size[0] > target.x and self.x < target.x + target.size[0]):
			x_hit = True

		if (self.y + self.size[1] > target.y and self.y < target.y + target.size[1]):
			y_hit = True

		if x_hit==True and y_hit==True:
			check_impact = True
			target.isdead = True
			self.isdead = True
			return True

		else:
			return False



class new_projectile_parameters():

	def __init__(self, gap):
		self.gap = gap
		self.counter = self.gap

	def new_projectile(self, proj, shooter, ptype, game):
		if shooter.laser_counter >= self.gap:
			proj.append( Projectile(shooter.x + shooter.size[0]/2, shooter.y + shooter.size[1]/2, ptype) )
			shooter.laser_counter = 0




# ============================== FUNCTIONS =========================



def initialise():
	
	pygame.init()

	# Screen sizes
	screen_xy = (600, 600)

	screen = pygame.display.set_mode(screen_xy)
	pygame.display.set_caption("Space Invaders")

	return screen_xy, screen



def redraw_screen(player, invader, player_laser, inv_laser):
	
	#screen.fill(BLACK)
	screen.blit(BG, (0,0))

	# Drawing player
	player.draw_self(screen)

	# Drawing invaders
	for c, inv in enumerate(invader):
		inv.step_forward()
		inv.draw_self(screen)

	# Drawing player lasers
	if len(player_laser) > 0:
		for c, lsr in enumerate(player_laser):
			lsr.draw_self(screen)

	# Drawing invader lasers
	if len(inv_laser) > 0:
		for c, lsr in enumerate(inv_laser):
			lsr.draw_self(screen)


	myfont = pygame.font.SysFont("monospace", 16)
	text = myfont.render("SCORE: "+str(player.score)+"/25", 1, WHITE)
	screen.blit(text, [10,10])


	pygame.display.update()

	

	

def deleting_dead(dead):
	
	if len(dead) > 0:
		for i in range(len(dead), 0, -1):
			if dead[i-1].isdead == True:
				dead.pop(i-1)



# Pauses the game when P is pressed,
# and draws pause menu to continue (SPACE)
# or quit game (Q).

def pause_game(game):

	paused = True
	continue_game = True

	titlefont = pygame.font.SysFont('verdana', 30, True)
	startfont = pygame.font.SysFont('verdana', 14, True)
	
	while paused:

		pausetext = titlefont.render('GAME PAUSED', 1, (255,165,0))
		y = screen_xy[0]/2 - pausetext.get_width()/2
		screen.blit(pausetext, (y, 150))

		pausespace = startfont.render('Press SPACE to continue', 1, (255,165,0))
		y = screen_xy[0]/2 - pausespace.get_width()/2
		screen.blit(pausespace, (y, 300))

		pausequit = startfont.render('Press Q to exit', 1, (255,165,0))
		y = screen_xy[0]/2 - pausequit.get_width()/2
		screen.blit(pausequit, (y, 350))

		pygame.display.update()


		for event in pygame.event.get():
			if event.type == KEYDOWN:

				if event.key == K_SPACE:
					paused = False

				elif event.key == K_q:
					continue_game = False
					paused = False
					game.status = 3

	game.RUN = continue_game


def blit_title(screen, game, message, color):

	titletext = game.title_font.render(message, 1, color)
	y = game.screen_xy[0]/2 - titletext.get_width()/2
	screen.blit(titletext, (y, 150))



# ============================== GAME-LOOP FUNCTIONS =========================


def start_menu(screen, game):

	screen_xy = game.screen_xy


	while game.START_RUN:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				START_RUN = False
				QUIT_ALL = True

		screen.blit(BG, (0,0))

		title_text = game.title_font.render('SPACE INVADERS', 1, (255,165,0))
		y = screen_xy[0]/2 - title_text.get_width()/2
		screen.blit(title_text, (y, 150))

		start_text = game.subtitle_font.render('Press SPACE to start', 1, WHITE)
		y = screen_xy[0]/2 - start_text.get_width()/2
		screen.blit(start_text, (y, 300))

		quit_text = game.subtitle_font.render('Press Q to quit', 1, WHITE)
		y = screen_xy[0]/2 - quit_text.get_width()/2
		screen.blit(quit_text, (y, 350))

		pygame.display.update()


		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE]:
			game.START_RUN = False

		elif keys[pygame.K_q]:
			game.START_RUN = False
			game.RUN = False
			game.END_RUN = False



def game_loop(screen, game, player, 
				invader, invader_param, 
				player_laser, player_laser_param, 
				inv_laser, inv_laser_param):

	while game.RUN:

		# ========== SAFE QUIT ==============

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.RUN = False
				game.QUIT_ALL = True

		if not(game.RUN):
			break

		if game.QUIT_ALL == True:
			break


		# ========== UPDATE TIMES ==============
		game.game_time += 100
		game.clock.tick(100)

		# ========== NEW INVADER ==============
		invader_param.new_invader(invader, game)

		# ========== KEY TRACKING ==============
		keys = pygame.key.get_pressed() 
		player.moving(keys)

		#========== PAUSE GAME ==============
		if keys[pygame.K_p]:
			pause_game(game)

		#========== PLAYER LASER SHOOTING ==============
		if keys[pygame.K_SPACE]:
			player_laser_param.new_projectile(player_laser, player, 0, game)
		player.laser_counter += 10

		# ========== INVADER LASER SHOOTING ==============
		if len(invader) > 0:
			for c, inv in enumerate(invader):
				inv_laser_param.new_projectile(inv_laser, inv, 1, game)
				inv.laser_counter += 10

		# ========== PROJECTILE DYNAMICS ==============
		if len(player_laser) > 0:
			for c, lsr in enumerate(player_laser):
				lsr.moving()
				for i, inv in enumerate(invader):
					if lsr.impact(inv):
						player.score += 1

		if len(inv_laser) > 0:
			for c, lsr in enumerate(inv_laser):
				lsr.moving()
				lsr.impact(player)

		# ===================== DELETING DEAD OBJECTS ====================
		deleting_dead(invader)
		deleting_dead(player_laser)
		deleting_dead(inv_laser)

		# ===================== LOOSE / WIN CONDITIONS =====================
		game.check_status(player, invader)

		# ========== Redraw Screen ============
		redraw_screen(player, invader, player_laser, inv_laser)


def end_loop(screem, game):
	while game.END_RUN:

		# Check end bools
		for event in pygame.event.get():
			if event.type == pygame.quit:
				game.END_RUN = False

		if game.QUIT_ALL == True:
			break

		# Reset screen
		screen.blit(BG, (0,0))

		# End Message
		if game.status == 1:
			blit_title(screen, game, 'YOU WIN', GREEN)

		elif game.status == 2:
			blit_title(screen, game, 'YOU DIED', RED)

		else:
			game.restart = False
			return game.restart

		# Play Again or Quit messages
		contdtext = game.subtitle_font.render('Press SPACE to play again', 1, WHITE)
		y = screen_xy[0]/2 - contdtext.get_width()/2
		screen.blit(contdtext, (y, 300))

		quittext = game.subtitle_font.render('Press Q to quit', 1, WHITE)
		y = screen_xy[0]/2 - quittext.get_width()/2
		screen.blit(quittext, (y, 350))

		pygame.display.update()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			game.END_RUN = False
			game.restart = True
			return game.restart

		elif keys[pygame.K_q]:
			game.END_RUN = False
			game.restart = False
			return game.restart


def reset_params(game, player, 
					invader, invader_param, 
					player_laser, player_laser_param, 
					inv_laser, inv_laser_param):
	
	screen_xy = game.screen_xy
	game = Game(screen_xy)

	player = Player()

	invader = []
	invader_param = new_invader_parameters()

	player_laser = []
	player_laser_param = new_projectile_parameters(500)

	inv_laser = []
	inv_laser_param = new_projectile_parameters(1000)

	

# ========================= MAIN LOOP ================================

restart = True

while restart:

	# Initialising parameters
	screen_xy, screen = initialise()
	game = Game(screen_xy)
	player = Player()
	invader = []
	invader_param = new_invader_parameters()
	player_laser = []
	player_laser_param = new_projectile_parameters(500)
	inv_laser = []
	inv_laser_param = new_projectile_parameters(1000)

	start_menu(screen, game)		
	
	game_loop(screen, game, player, 
			invader, invader_param, 
			player_laser, player_laser_param, 
			inv_laser, inv_laser_param)

	restart = end_loop(screen, game)

pygame.quit()