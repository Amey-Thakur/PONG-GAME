# title: AMEY & MEGA
# icon: icon.png
import pygame, sys, random, asyncio, math, webbrowser
try:
	import platform
except ImportError:
	platform = None

# Global Initialization
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AMEY & MEGA')

# Constants for Boundaries (Inner edges of 4px border starting at 2px)
TOP_BORD = 6
BOT_BORD = 714
LEFT_BORD = 6
RIGHT_BORD = 1274

# Assets
try:
	game_font = pygame.font.Font("freesansbold.ttf", 32)
	author_font = pygame.font.Font("freesansbold.ttf", 18)
except:
	game_font = pygame.font.Font(None, 32)
	author_font = pygame.font.Font(None, 18)

try:
	pong_sound = pygame.mixer.Sound("sound/sfx_point.wav")
	score_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
except:
	pong_sound = None
	score_sound = None

try:
	icon_orig = pygame.image.load("icon.png").convert_alpha()
	pygame.display.set_icon(icon_orig)
except:
	icon_orig = None

# Game Objects - Centered at Start
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(RIGHT_BORD - 15, (screen_height - 140)/2, 10, 140)
opponent = pygame.Rect(LEFT_BORD + 5, (screen_height - 140)/2, 10, 140)

# Colors
bg_color = (20, 20, 20)
ball_color = (240, 240, 240)
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
bg_rect = pygame.Rect(0, 0, 0, 0)

# Starfield
stars = []
for _ in range(100):
	stars.append([random.randint(0, screen_width), random.randint(0, screen_height), random.uniform(0.2, 1.5)])

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, player_kickback, opponent_kickback, player_glow, opponent_glow
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	# Wall Bounce (Clipped to inner borders)
	if ball.top <= TOP_BORD:
		ball.top = TOP_BORD
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1
	if ball.bottom >= BOT_BORD:
		ball.bottom = BOT_BORD
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	# Score Zones
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
		player_kickback = 15
		player_glow = 10
		ball_speed_x *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0: 
		if pong_sound: pygame.mixer.Sound.play(pong_sound)
		opponent_kickback = -15
		opponent_glow = 10
		ball_speed_x *= -1

def player_animation():
	global player_kickback
	player.y += player_speed
	# Clip to inner borders
	if player.top <= TOP_BORD: player.top = TOP_BORD
	if player.bottom >= BOT_BORD: player.bottom = BOT_BORD
	if player_kickback > 0: player_kickback -= 1

def opponent_animation():
	global opponent_kickback
	if opponent.top < ball.y: opponent.y += opponent_speed
	if opponent.bottom > ball.y: opponent.y -= opponent_speed
	# Clip to inner borders
	if opponent.top <= TOP_BORD: opponent.top = TOP_BORD
	if opponent.bottom >= BOT_BORD: opponent.bottom = BOT_BORD
	if opponent_kickback < 0: opponent_kickback += 1

def ball_start():
	global ball_speed_x, ball_speed_y, score_time
	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)

	if current_time - score_time < 700:
		num_text = game_font.render("3", True, white)
	elif current_time - score_time < 1400:
		num_text = game_font.render("2", True, white)
	elif current_time - score_time < 2100:
		num_text = game_font.render("1", True, white)
	else:
		ball_speed_y = 7 * random.choice((1, -1))
		ball_speed_x = 7 * random.choice((1, -1))
		score_time = None
		return

	num_rect = num_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
	screen.blit(num_text, num_rect)
	ball_speed_x, ball_speed_y = 0, 0

def draw_background():
	screen.fill(bg_color)
	for star in stars:
		star[1] += star[2]
		if star[1] > screen_height:
			star[1] = 0
			star[0] = random.randint(0, screen_width)
			star[2] = random.uniform(0.2, 1.5)
		color_val = int(star[2] * 80) + 40
		pygame.draw.circle(screen, (color_val, color_val, color_val), (int(star[0]), int(star[1])), max(1, int(star[2] * 1.2)))
	# Clean White Borders
	pygame.draw.rect(screen, (220, 220, 220), (2, 2, screen_width - 4, screen_height - 4), 4)

def draw_center_line():
	# Authentic Clipped Dashed Line
	segment_length = 15
	gap_length = 15
	line_color_ground = (80, 80, 80)
	for y in range(TOP_BORD, BOT_BORD, segment_length + gap_length):
		end_y = min(y + segment_length, BOT_BORD)
		pygame.draw.line(screen, line_color_ground, (screen_width/2, y), (screen_width/2, end_y), 2)

async def main():
	global player_speed, player_glow, opponent_glow, score_time, bg_rect, player_kickback, opponent_kickback
	
	# Initial Paddle Center
	player.centery = screen_height/2
	opponent.centery = screen_height/2

	# Loading Screen (Robust 3-second sequence)
	start_ticks = pygame.time.get_ticks()
	while pygame.time.get_ticks() - start_ticks < 3000:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		elapsed = pygame.time.get_ticks() - start_ticks
		progress = min(elapsed / 2500, 1.0)
		
		draw_background()
		if icon_orig:
			pulse = 1.0 + 0.05 * math.sin(pygame.time.get_ticks() * 0.005)
			icon = pygame.transform.scale(icon_orig, (int(300 * pulse), int(300 * pulse)))
			screen.blit(icon, icon.get_rect(centerx=screen_width/2, bottom=screen_height/2 + 80))
		
		bar_width, bar_height = 460, 6
		bar_x, bar_y = screen_width/2 - bar_width/2, screen_height/2 + 100
		pygame.draw.rect(screen, (40, 40, 40), (bar_x-2, bar_y-2, bar_width+4, bar_height+4), border_radius=10)
		pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width * progress, bar_height), border_radius=10)
		
		lt = author_font.render("INITIALIZING PONG GAME...", True, (220, 220, 220))
		screen.blit(lt, lt.get_rect(center=(screen_width/2, bar_y + 40)))
		
		pygame.display.flip()
		await asyncio.sleep(0)
		clock.tick(60)

	score_time = pygame.time.get_ticks()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if bg_rect.collidepoint(event.pos):
					github_url = "https://github.com/Amey-Thakur/PONG-GAME"
					if platform and hasattr(platform, 'window'): platform.window.open(github_url, "_blank")
					else: webbrowser.open(github_url)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN: player_speed += 7
				if event.key == pygame.K_UP: player_speed -= 7
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN: player_speed -= 7
				if event.key == pygame.K_UP: player_speed += 7

		# Update Logic
		ball_animation()
		player_animation()
		opponent_animation()
		
		# Rendering - Correct Layering
		draw_background()
		draw_center_line() # Draw this early so objects are ON TOP
		
		# Draw Paddles
		if player_glow > 0:
			glow = pygame.Rect(player.x + player_kickback - 5, player.y - 5, player.width + 10, player.height + 10)
			pygame.draw.rect(screen, (50, 150, 80), glow, border_radius=5)
			player_glow -= 1
		pygame.draw.rect(screen, player_color, (player.x + player_kickback, player.y, player.width, player.height), border_radius=2)
		
		if opponent_glow > 0:
			glow = pygame.Rect(opponent.x + opponent_kickback - 5, opponent.y - 5, opponent.width + 10, opponent.height + 10)
			pygame.draw.rect(screen, (150, 50, 50), glow, border_radius=5)
			opponent_glow -= 1
		pygame.draw.rect(screen, opponent_color, (opponent.x + opponent_kickback, opponent.y, opponent.width, opponent.height), border_radius=2)
		
		# Draw Ball
		pygame.draw.ellipse(screen, ball_color, ball)

		# Wait Timer / Countdown
		if score_time: ball_start()

		# HUD - Scores
		pt = game_font.render(f"{player_score}", True, white)
		screen.blit(pt, pt.get_rect(center=(screen_width/2 + 65, screen_height/2)))
		ot = game_font.render(f"{opponent_score}", True, white)
		screen.blit(ot, ot.get_rect(center=(screen_width/2 - 65, screen_height/2)))

		# Footer
		at = author_font.render("Designed & Developed by Amey & Mega", True, (180, 180, 180))
		tr = at.get_rect(center=(screen_width/2, screen_height - 35))
		bg_rect = tr.inflate(40, 15)
		pygame.draw.rect(screen, (30, 30, 30), bg_rect, border_radius=15)
		pygame.draw.rect(screen, (60, 60, 60), bg_rect, width=1, border_radius=15)
		screen.blit(at, tr)

		pygame.display.flip()
		await asyncio.sleep(0)
		clock.tick(60)

if __name__ == "__main__":
	asyncio.run(main())
