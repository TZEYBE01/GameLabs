import pygame, sys, random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 250
PADDLE2_START_X = 780
PADDLE2_START_Y = 250
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

def load_sound( sound_name):
	try:
		sound = pygame.mixer.Sound(sound_name)
	except pygame.error, message:
		print "Cannot load sound: " + sound_name
		raise SystemExit, message
	return sound


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
# Oponnent paddle vertically centered on the left side
paddle2_rect = pygame.Rect((PADDLE2_START_X, PADDLE2_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# middle line
line_rect = pygame.Rect((392, 0), (16, 600))

#checks for rematch
rematch = False

# Scoring: 1 point if you hit the ball, 0 point if you miss the ball
score = 0
score2 = 0

#sounds
you_sound =load_sound("you.wav")
opponent_sound = load_sound("opponent.wav")

# Load the font for displaying the score
font = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 60)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT
			
			if paddle2_rect.top < 0:
				paddle_rect.top = 0
			elif paddle2_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	#update opponent paddle	
	if (ball_rect.top + 2*BALL_SPEED > paddle2_rect.bottom):
		paddle2_rect.top += BALL_SPEED -random.randint(0,1) #adding/subtracting random integers to the speed for imperfection
	elif (ball_rect.bottom - 2*BALL_SPEED < paddle2_rect.top):
		paddle2_rect.top -= BALL_SPEED +random.randint(0,1)
	else:
		paddle2_rect.top  += 0
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if  ball_rect.left <= 0:
		ball_rect.left = 392
		ball_rect.top =292
		
		pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.display.flip()
		score2 += 1
		score += 0
		pygame.time.delay(400)
		
	if ball_rect.right >= SCREEN_WIDTH:
		ball_rect.left = 392
		ball_rect.top =292
		
		pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.display.flip()
		score += 1
		score2 += 0
		pygame.time.delay(400)

	# Test if the ball is hit by the paddle; if yes reverse speed and play sound
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		you_sound.play()
		
	
		
	if paddle2_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		opponent_sound.play()
		
		
	
	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), paddle2_rect) # Opponent paddle
	pygame.draw.rect(screen, (255, 0, 0), line_rect) # Middle line
	
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text = font.render(str(score), True, (0, 0, 0))
	score2_text = font.render(str(score2), True, (0, 0, 0))
	youwon_text = font2.render("You won! Press space for rematch.", True, (0, 255, 0))
	opponentwon_text = font2.render("You lost! Press space for rematch.", True, (255,0, 0))
	
	screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
	screen.blit(score2_text, ((SCREEN_WIDTH *0.75) - font.size(str(score2))[0] / 2, 5)) # The score
	
	if (score == 11 or score2 == 11):
		screen.fill((255, 255, 255))
		score_text = font.render(str(score), True, (0, 0, 0))
		score2_text = font.render(str(score2), True, (0, 0, 0))
		screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
		screen.blit(score2_text, ((SCREEN_WIDTH *0.75) - font.size(str(score2))[0] / 2, 5)) # The score
	
		if score == 11:
			screen.blit(youwon_text, (50, 275)) # The message
		else:
			screen.blit(opponentwon_text, (50 , 275)) # The message
			
		while (not rematch) :
				pygame.display.flip()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit(0)
						pygame.quit()
					if pygame.key.get_pressed()[pygame.K_SPACE]: 
						rematch = True
					elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
						sys.exit(0)
						pygame.quit()
		if rematch:
			score = 0
			score2 = 0
			rematch = False
			
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
	
	
