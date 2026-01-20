# ============================================================================
# PONG GAME
# ============================================================================
# A classic Pong game reimagined with premium arcade aesthetics.
# Features progressive difficulty, smarter AI, and visual effects.
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
COLOR_PLAYER      = (0, 255, 127)      # Spring Green
COLOR_OPPONENT    = (255, 69, 0)       # Orange Red
COLOR_WHITE       = (255, 255, 255)
COLOR_BORDER      = (220, 220, 220)
COLOR_LINE        = (80, 80, 80)

# Game Physics - Progressive Difficulty
BALL_SPEED_START  = 4                  # Start slow for easy gameplay
BALL_SPEED_MAX    = 14                 # Maximum ball speed cap
BALL_SPEED_INC    = 0.3                # Speed increase per paddle hit
PLAYER_SPEED      = 7                  # Player paddle speed
AI_SPEED          = 7                  # AI matches player for fair play
PADDLE_HEIGHT     = 140
PADDLE_WIDTH      = 10
BALL_SIZE         = 30

# AI Behavior Settings - Natural Difficulty
AI_REACTION_ZONE      = SCREEN_WIDTH / 2   # AI only reacts when ball crosses center
AI_MISTAKE_START      = 0.04               # 4% mistake chance at game start
AI_MISTAKE_MIN        = 0.01               # 1% mistake at max skill
AI_SKILL_UP_POINTS    = 10                 # AI gets smarter every 10 total points


# ============================================================================
# INITIALIZATION
# ============================================================================

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AMEY & MEGA')

# Fonts
game_font    = pygame.font.SysFont("segoeui", 32, bold=True)
author_font  = pygame.font.SysFont("segoeui", 18, bold=True)
loading_font = pygame.font.SysFont("segoeui", 14, bold=True)

# Sound Effects - Using OGG format for browser compatibility
paddle_sound = None
goal_sound   = None
beep_sound   = None

def load_sounds():
    """Load sounds with fallback. Must be OGG for Pygbag browser support."""
    global paddle_sound, goal_sound, beep_sound
    
    try:
        paddle_sound = pygame.mixer.Sound("sound/paddle.ogg")
        paddle_sound.set_volume(0.4) # Lowered from 0.5
    except:
        pass
    
    try:
        goal_sound = pygame.mixer.Sound("sound/goal.ogg")
        goal_sound.set_volume(0.6) # Lowered from 0.7
    except:
        pass
    
    try:
        beep_sound = pygame.mixer.Sound("sound/countdown.ogg")
        beep_sound.set_volume(0.5)
    except:
        pass

load_sounds()

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

current_ball_speed = BALL_SPEED_START  # Tracks progressive speed
ball_velocity      = [0, 0]
player_velocity    = 0
player_score       = 0
opponent_score     = 0
score_time         = None
footer_rect        = pygame.Rect(0, 0, 0, 0)
rally_count        = 0                 # Count paddle hits in current rally

# Visual Effects State
ball_trail         = []                # Stores last N ball positions for trail
goal_flash         = 0                 # Frames remaining for goal flash effect
player_flash       = 0                 # Frames remaining for player paddle flash
opponent_flash     = 0                 # Frames remaining for opponent paddle flash
last_countdown     = 0                 # Track countdown number for beep sound
ai_mistake_timer   = 0                 # Frames remaining for AI to commit to mistake
goal_particles     = []                # Celebration particles on goal
player_score_glow  = 0                 # Frames for player score glow
opponent_score_glow = 0                # Frames for opponent score glow
border_flash_color = None              # Color for border flash (green/red)
border_flash_timer = 0                 # Frames remaining for border flash


# ============================================================================
# LOADING SCREEN
# ============================================================================

async def show_loading_screen():
    """Display premium Apple-style loading screen."""
    start_time = pygame.time.get_ticks()
    duration = 2500
    
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
        screen.fill((5, 5, 5))
        
        # Pulsing icon
        if icon_image:
            pulse = 1.0 + 0.03 * math.sin(current_time * 0.006)
            size = int(120 * pulse)
            icon = pygame.transform.smoothscale(icon_image, (size, size))
            icon_rect = icon.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(icon, icon_rect)
        
        # Progress bar
        bar_width, bar_height = 300, 4
        bar_x = (SCREEN_WIDTH - bar_width) / 2
        bar_y = SCREEN_HEIGHT / 2 + 40
        pygame.draw.rect(screen, (34, 34, 34), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            pygame.draw.rect(screen, COLOR_WHITE, (bar_x, bar_y, fill_width, bar_height), border_radius=2)
        
        # Loading text
        text = loading_font.render("INITIALIZING PONG GAME...", True, (170, 170, 170))
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH / 2, bar_y + 35)))
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)


# ============================================================================
# GAME LOGIC
# ============================================================================

def update_ball():
    """
    Update ball position and handle collisions.
    Implements progressive difficulty - ball speeds up with each paddle hit.
    """
    global ball_velocity, player_score, opponent_score, score_time
    global current_ball_speed, rally_count, goal_flash
    global player_flash, opponent_flash, goal_particles
    global player_score_glow, opponent_score_glow
    global border_flash_color, border_flash_timer

    ball.x += ball_velocity[0]
    ball.y += ball_velocity[1]

    # Store position for trail effect (last 8 positions)
    ball_trail.append((ball.centerx, ball.centery))
    if len(ball_trail) > 8:
        ball_trail.pop(0)

    # Wall collisions (top/bottom) - no sound, just visual bounce
    if ball.top <= TOP_BORDER:
        ball.top = TOP_BORDER
        ball_velocity[1] *= -1

    if ball.bottom >= BOTTOM_BORDER:
        ball.bottom = BOTTOM_BORDER
        ball_velocity[1] *= -1

    # Scoring (left/right edges)
    if ball.left <= 0:
        player_score += 1
        player_score_glow = 20
        border_flash_color = 'player'
        border_flash_timer = 20
        score_time = pygame.time.get_ticks()
        goal_flash = 15
        rally_count = 0
        current_ball_speed = BALL_SPEED_START
        for _ in range(12):
            goal_particles.append({
                'x': SCREEN_WIDTH / 4, 'y': SCREEN_HEIGHT / 2,
                'vx': random.uniform(-3, 3), 'vy': random.uniform(-4, 2),
                'life': random.randint(20, 40), 'color': COLOR_PLAYER
            })
        if goal_sound:
            goal_sound.play()

    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        opponent_score_glow = 20
        border_flash_color = 'opponent'
        border_flash_timer = 20
        score_time = pygame.time.get_ticks()
        goal_flash = 15
        rally_count = 0
        current_ball_speed = BALL_SPEED_START
        for _ in range(12):
            goal_particles.append({
                'x': 3 * SCREEN_WIDTH / 4, 'y': SCREEN_HEIGHT / 2,
                'vx': random.uniform(-3, 3), 'vy': random.uniform(-4, 2),
                'life': random.randint(20, 40), 'color': COLOR_OPPONENT
            })
        if goal_sound:
            goal_sound.play()

    # Paddle collisions with speed increase
    if ball.colliderect(player) and ball_velocity[0] > 0:
        # Increase ball speed (progressive difficulty)
        rally_count += 1
        current_ball_speed = min(current_ball_speed + BALL_SPEED_INC, BALL_SPEED_MAX)
        
        # Update velocity with new speed, preserve direction
        direction_x = -1  # Reverse horizontal
        direction_y = 1 if ball_velocity[1] > 0 else -1
        ball_velocity[0] = current_ball_speed * direction_x
        ball_velocity[1] = current_ball_speed * direction_y
        
        player_flash = 8  # Visual feedback
        if paddle_sound:
            paddle_sound.play()

    if ball.colliderect(opponent) and ball_velocity[0] < 0:
        rally_count += 1
        current_ball_speed = min(current_ball_speed + BALL_SPEED_INC, BALL_SPEED_MAX)
        
        direction_x = 1
        direction_y = 1 if ball_velocity[1] > 0 else -1
        ball_velocity[0] = current_ball_speed * direction_x
        ball_velocity[1] = current_ball_speed * direction_y
        
        opponent_flash = 8
        if paddle_sound:
            paddle_sound.play()


def update_player():
    """Update player paddle position. Supports Keyboard AND Mouse Drag."""
    # Mouse Interaction: If left click is held, paddle follows mouse
    if pygame.mouse.get_pressed()[0]:
        mouse_y = pygame.mouse.get_pos()[1]
        player.centery = mouse_y
    else:
        # Keyboard Interaction
        player.y += player_velocity
        
    player.clamp_ip(pygame.Rect(0, TOP_BORDER, SCREEN_WIDTH, BOTTOM_BORDER - TOP_BORDER))


def update_opponent():
    """
    Update opponent (AI) paddle position.
    
    AI Behavior:
    - Matches player speed for fair play
    - Starts dumb and gets smarter over time
    - Mistakes persist for multiple frames to avoid jitter
    """
    global ai_mistake_timer
    
    # Only react when ball is approaching (crosses center line)
    if ball.centerx > AI_REACTION_ZONE:
        return  # Ball is on player's side, AI rests
    
    # If in mistake mode, continue the mistake
    if ai_mistake_timer > 0:
        ai_mistake_timer -= 1
        # Move away from ball (wrong direction)
        if opponent.centery < ball.centery:
            opponent.y -= AI_SPEED * 0.5  # Slower mistake movement
        else:
            opponent.y += AI_SPEED * 0.5
    else:
        # Check if we should start a new mistake
        total_points = player_score + opponent_score
        skill_level = min(total_points / AI_SKILL_UP_POINTS, 1.0)
        current_mistake_chance = AI_MISTAKE_START - (AI_MISTAKE_START - AI_MISTAKE_MIN) * skill_level
        
        if random.random() < current_mistake_chance * 0.05:  # Very rare mistakes
            ai_mistake_timer = random.randint(8, 15)  # Short mistake duration
        else:
            # Normal tracking behavior (smooth)
            if opponent.centery < ball.centery - 5:  # Dead zone to prevent jitter
                opponent.y += AI_SPEED
            elif opponent.centery > ball.centery + 5:
                opponent.y -= AI_SPEED
    
    opponent.clamp_ip(pygame.Rect(0, TOP_BORDER, SCREEN_WIDTH, BOTTOM_BORDER - TOP_BORDER))


def reset_ball():
    """Handle countdown and ball reset after scoring."""
    global ball_velocity, score_time, current_ball_speed, last_countdown

    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.centery = SCREEN_HEIGHT / 2
    opponent.centery = SCREEN_HEIGHT / 2
    ball_trail.clear()

    elapsed = pygame.time.get_ticks() - score_time

    if elapsed < 1000:
        countdown_num = 3
        countdown_text = "3"
    elif elapsed < 2000:
        countdown_num = 2
        countdown_text = "2"
    elif elapsed < 3000:
        countdown_num = 1
        countdown_text = "1"
    else:
        # Start with slow speed
        current_ball_speed = BALL_SPEED_START
        ball_velocity = [
            current_ball_speed * random.choice((1, -1)),
            current_ball_speed * random.choice((1, -1))
        ]
        score_time = None
        last_countdown = 0
        return

    # Play beep when countdown number changes
    if countdown_num != last_countdown:
        last_countdown = countdown_num
        if beep_sound:
            # Play at MAX volume for all counts to ensure it's audible
            beep_sound.set_volume(1.0)
            beep_sound.play()

    text_surface = game_font.render(countdown_text, True, COLOR_WHITE)
    screen.blit(text_surface, text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)))
    ball_velocity = [0, 0]


# ============================================================================
# RENDERING
# ============================================================================

def draw_background():
    """Render the game background with goal flash and border color effect."""
    global goal_flash, border_flash_timer
    
    # Goal flash creates a brief bright pulse
    if goal_flash > 0:
        flash_intensity = int(30 * (goal_flash / 15))
        bg_color = (20 + flash_intensity, 20 + flash_intensity, 20 + flash_intensity)
        goal_flash -= 1
    else:
        bg_color = COLOR_BACKGROUND
    
    screen.fill(bg_color)
    
    # Border flashes green (player win) or red (opponent win)
    if border_flash_timer > 0:
        alpha = border_flash_timer / 20
        if border_flash_color == 'player':
            border_color = (int(COLOR_PLAYER[0] * alpha + COLOR_BORDER[0] * (1 - alpha)),
                            int(COLOR_PLAYER[1] * alpha + COLOR_BORDER[1] * (1 - alpha)),
                            int(COLOR_PLAYER[2] * alpha + COLOR_BORDER[2] * (1 - alpha)))
        else:
            border_color = (int(COLOR_OPPONENT[0] * alpha + COLOR_BORDER[0] * (1 - alpha)),
                            int(COLOR_OPPONENT[1] * alpha + COLOR_BORDER[1] * (1 - alpha)),
                            int(COLOR_OPPONENT[2] * alpha + COLOR_BORDER[2] * (1 - alpha)))
        border_flash_timer -= 1
    else:
        border_color = COLOR_BORDER
    
    pygame.draw.rect(screen, border_color, (2, 2, SCREEN_WIDTH - 4, SCREEN_HEIGHT - 4), 4)


def draw_center_line():
    """Render the center dashed line."""
    segment, gap = 15, 15
    for y in range(TOP_BORDER, BOTTOM_BORDER, segment + gap):
        end_y = min(y + segment, BOTTOM_BORDER)
        pygame.draw.line(screen, COLOR_LINE, (SCREEN_WIDTH / 2, y), (SCREEN_WIDTH / 2, end_y), 2)


def draw_goal_particles():
    """Render and update celebration particles on goal."""
    for particle in goal_particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.15  # Gravity
        particle['life'] -= 1
        
        if particle['life'] <= 0:
            goal_particles.remove(particle)
        else:
            alpha = int(255 * (particle['life'] / 40))
            size = max(2, int(6 * (particle['life'] / 40)))
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(surf, color, (size, size), size)
            screen.blit(surf, (particle['x'] - size, particle['y'] - size))


def draw_ball_trail():
    """Render smooth glow trail behind the ball."""
    if len(ball_trail) < 2:
        return
    
    # Draw glowing trail using connected circles with fade
    for i in range(len(ball_trail) - 1):
        progress = (i + 1) / len(ball_trail)
        alpha = int(40 * progress)  # Subtle glow
        radius = int(BALL_SIZE / 2 * progress * 0.6)
        
        if radius > 1:
            glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 255, alpha), (radius * 2, radius * 2), radius)
            pos = ball_trail[i]
            screen.blit(glow_surface, (pos[0] - radius * 2, pos[1] - radius * 2))


def draw_paddles():
    """Render player and opponent paddles with flash effects."""
    global player_flash, opponent_flash
    
    # Player paddle with flash
    if player_flash > 0:
        flash_color = (min(255, COLOR_PLAYER[0] + 100), 
                       min(255, COLOR_PLAYER[1] + 100), 
                       min(255, COLOR_PLAYER[2] + 100))
        pygame.draw.rect(screen, flash_color, player, border_radius=2)
        player_flash -= 1
    else:
        pygame.draw.rect(screen, COLOR_PLAYER, player, border_radius=2)
    
    # Opponent paddle with flash
    if opponent_flash > 0:
        flash_color = (min(255, COLOR_OPPONENT[0] + 100), 
                       min(255, COLOR_OPPONENT[1] + 100), 
                       min(255, COLOR_OPPONENT[2] + 100))
        pygame.draw.rect(screen, flash_color, opponent, border_radius=2)
        opponent_flash -= 1
    else:
        pygame.draw.rect(screen, COLOR_OPPONENT, opponent, border_radius=2)


def draw_ball():
    """Render the ball."""
    pygame.draw.ellipse(screen, COLOR_BALL, ball)


def draw_scores():
    """Render the score display with glow effect."""
    global player_score_glow, opponent_score_glow
    
    # Player score with glow
    if player_score_glow > 0:
        glow_intensity = int(100 * (player_score_glow / 20))
        glow_color = (min(255, COLOR_PLAYER[0] + glow_intensity),
                      min(255, COLOR_PLAYER[1] + glow_intensity),
                      min(255, COLOR_PLAYER[2] + glow_intensity))
        player_score_glow -= 1
    else:
        glow_color = COLOR_PLAYER
    player_text = game_font.render(str(player_score), True, glow_color)
    screen.blit(player_text, player_text.get_rect(center=(SCREEN_WIDTH / 2 + 65, SCREEN_HEIGHT / 2)))
    
    # Opponent score with glow
    if opponent_score_glow > 0:
        glow_intensity = int(100 * (opponent_score_glow / 20))
        glow_color = (min(255, COLOR_OPPONENT[0] + glow_intensity),
                      min(255, COLOR_OPPONENT[1] + glow_intensity),
                      min(255, COLOR_OPPONENT[2] + glow_intensity))
        opponent_score_glow -= 1
    else:
        glow_color = COLOR_OPPONENT
    opponent_text = game_font.render(str(opponent_score), True, glow_color)
    screen.blit(opponent_text, opponent_text.get_rect(center=(SCREEN_WIDTH / 2 - 65, SCREEN_HEIGHT / 2)))


def draw_rally_counter():
    """Display rally count on left, speed on right of center line."""
    if rally_count > 0:
        # Rally on left side of center line
        rally_text = loading_font.render(f"Rally: {rally_count}", True, (100, 100, 100))
        screen.blit(rally_text, rally_text.get_rect(midright=(SCREEN_WIDTH / 2 - 20, 30)))
        
        # Speed on right side of center line
        speed_text = loading_font.render(f"Speed: {current_ball_speed:.1f}", True, (100, 100, 100))
        screen.blit(speed_text, speed_text.get_rect(midleft=(SCREEN_WIDTH / 2 + 20, 30)))


def draw_footer():
    """Render the authorship footer with score-based color flash."""
    global footer_rect
    
    # Footer text flashes with score color
    if border_flash_timer > 0:
        alpha = border_flash_timer / 20
        if border_flash_color == 'player':
            text_color = (int(COLOR_PLAYER[0] * alpha + 180 * (1 - alpha)),
                          int(COLOR_PLAYER[1] * alpha + 180 * (1 - alpha)),
                          int(COLOR_PLAYER[2] * alpha + 180 * (1 - alpha)))
        else:
            text_color = (int(COLOR_OPPONENT[0] * alpha + 180 * (1 - alpha)),
                          int(COLOR_OPPONENT[1] * alpha + 180 * (1 - alpha)),
                          int(COLOR_OPPONENT[2] * alpha + 180 * (1 - alpha)))
    else:
        text_color = (180, 180, 180)
    
    text = author_font.render("Designed & Developed by Amey & Mega", True, text_color)
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
    global player_velocity, score_time, footer_rect, current_ball_speed

    await show_loading_screen()

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
                    player_velocity += PLAYER_SPEED
                if event.key == pygame.K_UP:
                    player_velocity -= PLAYER_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_velocity -= PLAYER_SPEED
                if event.key == pygame.K_UP:
                    player_velocity += PLAYER_SPEED

        update_ball()
        update_player()
        update_opponent()

        draw_background()
        draw_center_line()
        draw_ball_trail()
        draw_paddles()
        
        if score_time:
            reset_ball()

        draw_scores()
        draw_rally_counter()
        draw_footer()
        draw_goal_particles()
        draw_ball()  # Ball drawn last to be on top of footer

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())
