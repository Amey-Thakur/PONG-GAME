import pygame, sys, random, asyncio

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	# player score	
	if ball.left <= 0:
		if score_sound: pygame.mixer.Sound.play(score_sound)
		player_score += 1
		score_time = pygame.time.get_ticks()

	# opponent score	
	if ball.right >= screen_width:
		if score_sound: pygame.mixer.Sound.play(score_sound)
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	if ball.colliderect(player) and ball_speed_x > 0:
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0: 
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

def player_animation():
	player.y += player_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_animation():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def ball_start():
	global ball_speed_x, ball_speed_y, score_time

	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)

	if current_time - score_time < 700:
		number_three = game_font.render("3", False, white)
		screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
	elif current_time - score_time < 1400:
		number_two = game_font.render("2", False, white)
		screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
	elif current_time - score_time < 2100:
		number_one = game_font.render("1", False, white)
		screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0,0
	else:
		ball_speed_y = 7 * random.choice((1, -1))
		ball_speed_x = 7 * random.choice((1, -1))
		score_time = None

# Game Configurations & Constants
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global Rects
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Colors
bg_color = pygame.Color(0, 0, 0)
ball_color = (255, 255, 255)
line_color = (132, 132, 130)
player_color = (0, 255, 0)
opponent_color = (255, 0, 0)
white = (255, 255, 255)

# Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0
score_time = pygame.time.get_ticks() # Initialize with current time for startup delay

# Font Loading (Safe Pattern)
try:
	game_font = pygame.font.Font("freesansbold.ttf", 32)
except:
	game_font = pygame.font.Font(None, 32)

# Audio Loading (Safe Pattern)
try:
	pong_sound = pygame.mixer.Sound("sound/sfx_point.wav")
	score_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
except:
	pong_sound = None
	score_sound = None

async def main():
	global player_speed
	
	while True:
		#Handling input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					player_speed += 7
				if event.key == pygame.K_UP:
					player_speed -= 7
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					player_speed -= 7
				if event.key == pygame.K_UP:
					player_speed += 7

		# Logic
		ball_animation()
		player_animation()
		opponent_animation()
		
		# Visuals
		screen.fill(bg_color)
		pygame.draw.rect(screen, player_color, player)
		pygame.draw.rect(screen, opponent_color, opponent)
		pygame.draw.ellipse(screen, ball_color, ball)
		pygame.draw.aaline(screen, line_color, (screen_width/2,0), (screen_width/2, screen_height))

		if score_time:
			ball_start()

		# Score Display
		player_text = game_font.render(f"{player_score}", True, white)
		screen.blit(player_text, (660, 470))
		opponent_text = game_font.render(f"{opponent_score}", True, white)
		screen.blit(opponent_text, (600, 470))

		pygame.display.flip()
		clock.tick(60)
		await asyncio.sleep(0)

# Execution
if __name__ == "__main__":
	asyncio.run(main())

