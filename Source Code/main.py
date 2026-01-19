# ============================================================================
# PONG GAME
# ============================================================================
# A classic Pong game reimagined with premium arcade aesthetics.
#
# Authors:          Amey Thakur & Mega Satish
# Date:             July 5, 2021
# License:          MIT License
# Repository:       https://github.com/Amey-Thakur/PONG-GAME
# Profiles:
#   - Amey Thakur:  https://github.com/Amey-Thakur
#   - Mega Satish:  https://github.com/msatmod
# ============================================================================
# title: AMEY & MEGA
# icon: icon.png

import pygame
import sys
import random
import asyncio
import math
import webbrowser

try:
    import platform
except ImportError:
    platform = None


# ============================================================================
# CONFIGURATION
# ============================================================================

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60

# Boundary Constants
TOP_BORDER    = 6
BOTTOM_BORDER = 714
LEFT_BORDER   = 6
RIGHT_BORDER  = 1274

# Color Palette
COLOR_BACKGROUND  = (20, 20, 20)
COLOR_BALL        = (240, 240, 240)
COLOR_PLAYER      = (0, 255, 127)
COLOR_OPPONENT    = (255, 69, 0)
COLOR_WHITE       = (255, 255, 255)
COLOR_BORDER      = (220, 220, 220)
COLOR_LINE        = (80, 80, 80)

# Game Physics
BALL_SPEED    = 7
PADDLE_SPEED  = 7
PADDLE_HEIGHT = 140
PADDLE_WIDTH  = 10
BALL_SIZE     = 30


# ============================================================================
# INITIALIZATION
# ============================================================================

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AMEY & MEGA')

# Fonts - Using clean sans-serif for Google Play aesthetic
game_font   = pygame.font.SysFont("segoeui", 32, bold=True)
author_font = pygame.font.SysFont("segoeui", 18, bold=True)
loading_font = pygame.font.SysFont("segoeui", 14, bold=True)

# Sound Effects
try:
    pong_sound  = pygame.mixer.Sound("sound/sfx_point.wav")
    score_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
except:
    pong_sound  = None
    score_sound = None

# Icon
try:
    icon_image = pygame.image.load("icon.png").convert_alpha()
    pygame.display.set_icon(icon_image)
except:
    icon_image = None


# ============================================================================
# GAME OBJECTS
# ============================================================================

ball = pygame.Rect(
    SCREEN_WIDTH / 2 - BALL_SIZE / 2,
    SCREEN_HEIGHT / 2 - BALL_SIZE / 2,
    BALL_SIZE,
    BALL_SIZE
)

player = pygame.Rect(
    RIGHT_BORDER - PADDLE_WIDTH - 5,
    (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

opponent = pygame.Rect(
    LEFT_BORDER + 5,
    (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)


# ============================================================================
# GAME STATE
# ============================================================================

ball_velocity     = [BALL_SPEED * random.choice((1, -1)), BALL_SPEED * random.choice((1, -1))]
player_velocity   = 0
player_score      = 0
opponent_score    = 0
score_time        = None
footer_rect       = pygame.Rect(0, 0, 0, 0)


# ============================================================================
# LOADING SCREEN
# ============================================================================

async def show_loading_screen():
    """Display premium Apple-style loading screen."""
    start_time = pygame.time.get_ticks()
    duration = 2500  # 2.5 seconds
    
    while True:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        
        if elapsed >= duration:
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        progress = min(elapsed / duration, 1.0)
        
        # Background
        screen.fill((5, 5, 5))
        
        # Icon with pulse effect
        if icon_image:
            pulse = 1.0 + 0.03 * math.sin(current_time * 0.006)
            size = int(120 * pulse)
            icon = pygame.transform.smoothscale(icon_image, (size, size))
            icon_rect = icon.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(icon, icon_rect)
        
        # Progress bar
        bar_width = 300
        bar_height = 4
        bar_x = (SCREEN_WIDTH - bar_width) / 2
        bar_y = SCREEN_HEIGHT / 2 + 40
        
        # Background bar
        pygame.draw.rect(screen, (34, 34, 34), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
        
        # Fill bar
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            pygame.draw.rect(screen, COLOR_WHITE, (bar_x, bar_y, fill_width, bar_height), border_radius=2)
        
        # Loading text
        text = loading_font.render("INITIALIZING PONG GAME...", True, (170, 170, 170))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, bar_y + 35))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)


# ============================================================================
# GAME LOGIC
# ============================================================================

def update_ball():
    """Update ball position and handle collisions."""
    global ball_velocity, player_score, opponent_score, score_time

    ball.x += ball_velocity[0]
    ball.y += ball_velocity[1]

    if ball.top <= TOP_BORDER:
        ball.top = TOP_BORDER
        ball_velocity[1] *= -1
        if pong_sound:
            pong_sound.play()

    if ball.bottom >= BOTTOM_BORDER:
        ball.bottom = BOTTOM_BORDER
        ball_velocity[1] *= -1
        if pong_sound:
            pong_sound.play()

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
        if score_sound:
            score_sound.play()

    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
        if score_sound:
            score_sound.play()

    if ball.colliderect(player) and ball_velocity[0] > 0:
        ball_velocity[0] *= -1
        if pong_sound:
            pong_sound.play()

    if ball.colliderect(opponent) and ball_velocity[0] < 0:
        ball_velocity[0] *= -1
        if pong_sound:
            pong_sound.play()


def update_player():
    """Update player paddle position."""
    player.y += player_velocity
    player.clamp_ip(pygame.Rect(0, TOP_BORDER, SCREEN_WIDTH, BOTTOM_BORDER - TOP_BORDER))


def update_opponent():
    """Update opponent (AI) paddle position."""
    if opponent.centery < ball.centery:
        opponent.y += PADDLE_SPEED
    elif opponent.centery > ball.centery:
        opponent.y -= PADDLE_SPEED

    opponent.clamp_ip(pygame.Rect(0, TOP_BORDER, SCREEN_WIDTH, BOTTOM_BORDER - TOP_BORDER))


def reset_ball():
    """Handle countdown and ball reset after scoring."""
    global ball_velocity, score_time

    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.centery = SCREEN_HEIGHT / 2
    opponent.centery = SCREEN_HEIGHT / 2

    elapsed = pygame.time.get_ticks() - score_time

    if elapsed < 700:
        countdown_text = "3"
    elif elapsed < 1400:
        countdown_text = "2"
    elif elapsed < 2100:
        countdown_text = "1"
    else:
        ball_velocity = [BALL_SPEED * random.choice((1, -1)), BALL_SPEED * random.choice((1, -1))]
        score_time = None
        return

    text_surface = game_font.render(countdown_text, True, COLOR_WHITE)
    screen.blit(text_surface, text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)))
    ball_velocity = [0, 0]


# ============================================================================
# RENDERING
# ============================================================================

def draw_background():
    """Render the game background."""
    screen.fill(COLOR_BACKGROUND)
    pygame.draw.rect(screen, COLOR_BORDER, (2, 2, SCREEN_WIDTH - 4, SCREEN_HEIGHT - 4), 4)


def draw_center_line():
    """Render the center dashed line."""
    segment = 15
    gap = 15
    for y in range(TOP_BORDER, BOTTOM_BORDER, segment + gap):
        end_y = min(y + segment, BOTTOM_BORDER)
        pygame.draw.line(screen, COLOR_LINE, (SCREEN_WIDTH / 2, y), (SCREEN_WIDTH / 2, end_y), 2)


def draw_paddles():
    """Render player and opponent paddles."""
    pygame.draw.rect(screen, COLOR_PLAYER, player, border_radius=2)
    pygame.draw.rect(screen, COLOR_OPPONENT, opponent, border_radius=2)


def draw_ball():
    """Render the ball."""
    pygame.draw.ellipse(screen, COLOR_BALL, ball)


def draw_scores():
    """Render the score display."""
    player_text = game_font.render(str(player_score), True, COLOR_PLAYER)
    opponent_text = game_font.render(str(opponent_score), True, COLOR_OPPONENT)

    screen.blit(player_text, player_text.get_rect(center=(SCREEN_WIDTH / 2 + 65, SCREEN_HEIGHT / 2)))
    screen.blit(opponent_text, opponent_text.get_rect(center=(SCREEN_WIDTH / 2 - 65, SCREEN_HEIGHT / 2)))


def draw_footer():
    """Render the authorship footer."""
    global footer_rect

    text = author_font.render("Designed & Developed by Amey & Mega", True, (180, 180, 180))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 35))

    footer_rect = text_rect.inflate(40, 15)
    pygame.draw.rect(screen, (30, 30, 30), footer_rect, border_radius=15)
    pygame.draw.rect(screen, (60, 60, 60), footer_rect, width=1, border_radius=15)
    screen.blit(text, text_rect)


# ============================================================================
# MAIN LOOP
# ============================================================================

async def main():
    """Main game entry point."""
    global player_velocity, score_time, footer_rect

    # Show loading screen first
    await show_loading_screen()

    # Initialize positions
    player.centery = SCREEN_HEIGHT / 2
    opponent.centery = SCREEN_HEIGHT / 2
    score_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if footer_rect.collidepoint(event.pos):
                    url = "https://github.com/Amey-Thakur/PONG-GAME"
                    if platform and hasattr(platform, 'window'):
                        platform.window.open(url, "_blank")
                    else:
                        webbrowser.open(url)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_velocity += PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_velocity -= PADDLE_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_velocity -= PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_velocity += PADDLE_SPEED

        update_ball()
        update_player()
        update_opponent()

        draw_background()
        draw_center_line()
        draw_paddles()
        draw_ball()

        if score_time:
            reset_ball()

        draw_scores()
        draw_footer()

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())
