# title: AMEY & MEGA
# icon: icon.png
import pygame, sys, random, asyncio, math

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, player_kickback, opponent_kickback, player_glow, opponent_glow
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	# Boundary Collisions
	if ball.top <= 0 or ball.bottom >= screen_height:
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	# Score Tracking
	if ball.left <= 0:
		if score_sound: pygame.mixer.Sound.play(score_sound)
		player_score += 1
		score_time = pygame.time.get_ticks()

	if ball.right >= screen_width:
		if score_sound: pygame.mixer.Sound.play(score_sound)
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	# Paddle Collisions
	if ball.colliderect(player) and ball_speed_x > 0:
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		player_kickback = 15  # Trigger animation
		player_glow = 10      # Trigger glow
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0: 
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		opponent_kickback = -15 # Trigger animation
		opponent_glow = 10       # Trigger glow
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

def player_animation():
	global player_kickback
	player.y += player_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height
	
	# Smoothly return paddle to original X position
	if player_kickback > 0:
		player_kickback -= 1

def opponent_animation():
	global opponent_kickback
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height
		
	# Smoothly return paddle to original X position
	if opponent_kickback < 0:
		opponent_kickback += 1

def ball_start():
	global ball_speed_x, ball_speed_y, score_time

	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)

	if current_time - score_time < 700:
		number_three = game_font.render("3", True, white)
		screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
	elif current_time - score_time < 1400:
		number_two = game_font.render("2", True, white)
		screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
	elif current_time - score_time < 2100:
		number_one = game_font.render("1", True, white)
		screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0,0
	else:
		ball_speed_y = 7 * random.choice((1, -1))
		ball_speed_x = 7 * random.choice((1, -1))
		score_time = None


def draw_background():
	screen.fill(bg_color)
	
	for star in stars:
		# Move star
		star[1] += star[2]
		if star[1] > screen_height:
			star[1] = 0
			star[0] = random.randint(0, screen_width)
			star[2] = random.uniform(0.2, 1.5)
		
		# Determine color based on speed (depth)
		color_val = int(star[2] * 80) + 40
		color = (color_val, color_val, color_val)
		
		# Draw star
		pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), max(1, int(star[2] * 1.2)))

async def loading_screen():
	try:
		icon_orig = pygame.image.load("icon.png").convert_alpha()
	except:
		icon_orig = None

	start_time = pygame.time.get_ticks()
	while True:
		current_time = pygame.time.get_ticks()
		elapsed = current_time - start_time
		if elapsed > 3500: break # Increased slightly for better feel

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.fill(bg_color)
		
		# Draw Background Grid even in loading for consistency
		draw_background()

		if icon_orig:
			# Pulse effect
			pulse = 1.0 + 0.05 * math.sin(current_time * 0.005)
			icon = pygame.transform.smoothscale(icon_orig, (int(300 * pulse), int(300 * pulse)))
			icon_rect = icon.get_rect(center=(screen_width/2, screen_height/2 - 50))
			screen.blit(icon, icon_rect)
		
		# Progress bar
		bar_width = 460
		bar_height = 6
		bar_x = screen_width/2 - bar_width/2
		bar_y = screen_height/2 + 180
		
		progress = min(elapsed / 3000, 1.0)
		
		# Draw background bar (glass look)
		pygame.draw.rect(screen, (40, 40, 40), (bar_x-2, bar_y-2, bar_width+4, bar_height+4), border_radius=10)
		# Draw progress
		pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width * progress, bar_height), border_radius=10)
		
		# Loading Text
		load_text = author_font.render("INITIALIZING PONG GAME...", True, (220, 220, 220))
		load_rect = load_text.get_rect(center=(screen_width/2, bar_y + 40))
		screen.blit(load_text, load_rect)

		pygame.display.flip()
		await asyncio.sleep(0)
		clock.tick(60)

# System Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AMEY & MEGA')

# Initialize Stars for Parallax Starfield
stars = []
for _ in range(100):
	# [x, y, speed, depth/brightness]
	stars.append([random.randint(0, screen_width), random.randint(0, screen_height), random.uniform(0.2, 1.5)])

try:
	pygame.display.set_icon(pygame.image.load("icon.png"))
except:
	pass

# Objects & Positioning
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Colors
bg_color = (20, 20, 20)  # Deep charcoal
accent_color = (40, 40, 40)
ball_color = (240, 240, 240)
line_color = (60, 60, 60)
player_color = (0, 255, 127) # Spring Green
opponent_color = (255, 69, 0) # Orange Red
white = (255, 255, 255)

# Game State
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0
player_kickback = 0
opponent_kickback = 0
player_glow = 0
opponent_glow = 0
score_time = None

# Font Assets
try:
	game_font = pygame.font.Font("freesansbold.ttf", 32)
	author_font = pygame.font.Font("freesansbold.ttf", 18)
except:
	game_font = pygame.font.Font(None, 32)
	author_font = pygame.font.Font(None, 18)

# Audio Assets
try:
	pong_sound = pygame.mixer.Sound("sound/sfx_point.wav")
	score_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
except:
	pong_sound = None
	score_sound = None

async def main():
	global player_speed, player_glow, opponent_glow, score_time
	
	await loading_screen()
	score_time = pygame.time.get_ticks()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN: player_speed += 7
				if event.key == pygame.K_UP: player_speed -= 7
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN: player_speed -= 7
				if event.key == pygame.K_UP: player_speed += 7

		# Logic Update
		ball_animation()
		player_animation()
		opponent_animation()
		
		# Rendering
		draw_background()
		
		# Render Paddles with Kickback Animation & Glow
		if player_glow > 0:
			# Subtle outer glow rect (larger and transparent) - simulated with multiple outlines
			glow_rect = pygame.Rect(player.x + player_kickback - 5, player.y - 5, player.width + 10, player.height + 10)
			pygame.draw.rect(screen, (50, 150, 80), glow_rect, border_radius=5)
			player_glow -= 1

		pygame.draw.rect(screen, player_color, (player.x + player_kickback, player.y, player.width, player.height), border_radius=2)
		
		if opponent_glow > 0:
			glow_rect = pygame.Rect(opponent.x + opponent_kickback - 5, opponent.y - 5, opponent.width + 10, opponent.height + 10)
			pygame.draw.rect(screen, (150, 50, 50), glow_rect, border_radius=5)
			opponent_glow -= 1

		pygame.draw.rect(screen, opponent_color, (opponent.x + opponent_kickback, opponent.y, opponent.width, opponent.height), border_radius=2)
		
		pygame.draw.ellipse(screen, ball_color, ball)
		pygame.draw.aaline(screen, line_color, (screen_width/2,0), (screen_width/2, screen_height))

		if score_time:
			ball_start()

		# HUD - Scores
		player_text = game_font.render(f"{player_score}", True, white)
		screen.blit(player_text, (660, 470))
		opponent_text = game_font.render(f"{opponent_score}", True, white)
		screen.blit(opponent_text, (600, 470))

		# Footer - Authorship
		author_text = author_font.render("Designed & Developed by AMEY & MEGA", True, (100, 100, 100))
		screen.blit(author_text, (screen_width/2 - 165, screen_height - 30))

		pygame.display.flip()
		clock.tick(60)
		await asyncio.sleep(0)

if __name__ == "__main__":
	asyncio.run(main())

