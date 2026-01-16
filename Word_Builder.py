"""
Word Builder Game
-----------------
A typing + reaction game built with pygame.
Catch falling letters with your mouse to build words before the timer runs out.
Choose from Easy, Medium, or Hard difficulties.
Author: Suyash Ranjan
"""

import pygame
import random
import sys
import time
import math

# ----------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------
pygame.init()

# Screen setup (fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Word Builder Game")

# Clock
clock = pygame.time.Clock()

# ----------------------------------------------------------------------
# Fonts & Colors
# ----------------------------------------------------------------------
FONT_SIZE = 32
FONT = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
HUD_FONT = pygame.font.SysFont("consolas", 40, bold=True)
BIG_FONT = pygame.font.SysFont("consolas", 80, bold=True)

WHITE = (255, 255, 255)
GREEN = (0, 255, 70)
RED = (255, 60, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)

# ----------------------------------------------------------------------
# Game Data
# ----------------------------------------------------------------------
TIME_LIMIT = 60  # Initial seconds

BONUS_TIME = {
    "easy": 5,     # seconds added per correct word
    "medium": 4,
    "hard": 3
}

# Load words from a file
def load_words(filename="Word_Builder_Wordlists.txt"):
    """The Wordlist file should contain one word per line. Words are case-insensitive. All words will be converted to uppercase."""
    try:
        with open(filename, "r") as f:
            words = [line.strip().upper() for line in f if line.strip()]
        if not words:
            raise ValueError("Word list is empty!")
        return words
    except FileNotFoundError:
        print("⚠️ Word_Builder_Wordlists.txt not found! Using default word list.")
        return ["PYTHON", "GAME", "MATRIX", "HACKER", "CODE", "CYBER", "AEREX", "RAIN"]

WORDS = load_words()

DIFFICULTY_SETTINGS = {
    "easy": {"min_speed": 1, "max_speed": 4, "count": 80},
    "medium": {"min_speed": 2, "max_speed": 6, "count": 120},
    "hard": {"min_speed": 3, "max_speed": 8, "count": 160},
}

# ----------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------
class FallingChar:
    """Represents a single falling character on the screen."""

    def __init__(self, x, y, char, speed):
        self.x = x
        self.y = y
        self.char = char
        self.speed = speed
        self.active = True

    def update(self):
        """Update position and reset if it moves off-screen."""
        if self.active:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.reset()

    def reset(self):
        """Reset position and assign a new random character."""
        self.y = random.randint(-50, -10)
        self.x = random.randint(0, SCREEN_WIDTH)
        self.char = chr(random.randint(65, 90))  # A–Z
        self.speed = random.uniform(min_speed, max_speed)
        self.active = True

    def draw(self):
        """Draw the character on the screen."""
        if self.active:
            text = FONT.render(self.char, True, GREEN)
            screen.blit(text, (self.x, self.y))

    def collide_with_mouse(self, mouse_pos):
        """Check if the mouse collides with the character."""
        if self.active:
            rect = FONT.render(self.char, True, GREEN).get_rect(topleft=(self.x, self.y))
            return rect.collidepoint(mouse_pos)
        return False


class Particle:
    """Represents a small particle for explosion effect."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.color = color

    def update(self):
        """Move particle and decrease life."""
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        """Draw particle if still alive."""
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

# ----------------------------------------------------------------------
# Game Functions
# ----------------------------------------------------------------------
def start_game(difficulty):
    """Initialize game state based on difficulty."""
    global chars, current_word, progress_index, score, remaining_time
    global min_speed, max_speed, current_difficulty

    current_difficulty = difficulty
    settings = DIFFICULTY_SETTINGS[difficulty]
    min_speed, max_speed = settings["min_speed"], settings["max_speed"]

    # Generate falling characters
    chars = [
        FallingChar(
            random.randint(0, SCREEN_WIDTH),
            random.randint(-500, SCREEN_HEIGHT),
            chr(random.randint(65, 90)),
            random.uniform(min_speed, max_speed),
        )
        for _ in range(settings["count"])
    ]

    current_word = random.choice(WORDS)
    progress_index = 0
    score = 0
    remaining_time = TIME_LIMIT  # Initialize timer

def draw_menu():
    """Draw the main menu screen."""
    title = HUD_FONT.render("WORD BUILDER GAME", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

    options = ["1 - EASY", "2 - MEDIUM", "3 - HARD"]
    for i, text in enumerate(options):
        option = HUD_FONT.render(text, True, GREEN)
        screen.blit(option, (SCREEN_WIDTH // 2 - option.get_width() // 2, SCREEN_HEIGHT // 2 + i * 60))

def draw_game():
    """Draw active gameplay elements."""
    global final_score, state, remaining_time, chars, particles, current_word, progress_index, score

    # Timer
    if remaining_time <= 0:
        final_score = score
        state = "gameover"

    # Characters
    for c in chars:
        c.update()
        c.draw()

    # Particles
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)
        else:
            p.draw()

    # Glowing word progress
    for i, letter in enumerate(current_word):
        if i < progress_index:
            glow_intensity = int(128 + 127 * math.sin(pygame.time.get_ticks() / 200))
            glow_color = (glow_intensity, glow_intensity, 0)
            glow_surface = HUD_FONT.render(letter, True, glow_color)
        else:
            glow_surface = HUD_FONT.render(letter, True, (80, 80, 80))
        screen.blit(glow_surface, (50 + i * 50, 30))

    # HUD
    screen.blit(HUD_FONT.render(f"Score: {score}", True, WHITE), (50, 100))
    screen.blit(HUD_FONT.render(f"Time: {int(remaining_time)}", True, RED), (50, 150))

def draw_gameover():
    """Draw the game over screen."""
    over_text = BIG_FONT.render("GAME OVER", True, RED)
    score_text = HUD_FONT.render(f"Your Score: {final_score}", True, WHITE)
    restart_text = HUD_FONT.render("Press ENTER to return to Menu", True, GREEN)

    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

# ----------------------------------------------------------------------
# Main Game Loop
# ----------------------------------------------------------------------
state = "menu"
chars, particles = [], []
current_word, progress_index, score, final_score = "", 0, 0, 0
remaining_time = TIME_LIMIT
current_difficulty = "easy"
running = True

while running:
    dt = clock.tick(60) / 1000  # delta time in seconds
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    # Reduce remaining_time
    if state == "game":
        remaining_time -= dt

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Menu Input
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game("easy"); state = "game"
                elif event.key == pygame.K_2:
                    start_game("medium"); state = "game"
                elif event.key == pygame.K_3:
                    start_game("hard"); state = "game"

        # Game Input
        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for c in chars:
                    if c.collide_with_mouse(mouse_pos) and c.active:
                        c.active = False
                        for _ in range(20):
                            particles.append(Particle(c.x, c.y, GREEN))

                        # Word progress check
                        if c.char == current_word[progress_index]:
                            progress_index += 1
                            if progress_index == len(current_word):
                                score += 1
                                remaining_time += """
Word Builder Game
-----------------
A typing + reaction game built with pygame.
Catch falling letters with your mouse to build words before the timer runs out.
Choose from Easy, Medium, or Hard difficulties.
Author: Suyash Ranjan
"""

import pygame
import random
import sys
import time
import math

# ----------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------
pygame.init()

# Screen setup (fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Word Builder Game")

# Clock
clock = pygame.time.Clock()

# ----------------------------------------------------------------------
# Fonts & Colors
# ----------------------------------------------------------------------
FONT_SIZE = 32
FONT = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
HUD_FONT = pygame.font.SysFont("consolas", 40, bold=True)
BIG_FONT = pygame.font.SysFont("consolas", 80, bold=True)

WHITE = (255, 255, 255)
GREEN = (0, 255, 70)
RED = (255, 60, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)

# ----------------------------------------------------------------------
# Game Data
# ----------------------------------------------------------------------
TIME_LIMIT = 60  # Initial seconds

BONUS_TIME = {
    "easy": 5,     # seconds added per correct word
    "medium": 4,
    "hard": 3
}

# Load words from a file
def load_words(filename="Word_Builder_Wordlists.txt"):
    try:
        with open(filename, "r") as f:
            words = [line.strip().upper() for line in f if line.strip()]
        if not words:
            raise ValueError("Word list is empty!")
        return words
    except FileNotFoundError:
        print("⚠️ Word_Builder_Wordlists.txt not found! Using default word list.")
        return ["PYTHON", "GAME", "MATRIX", "HACKER", "CODE", "CYBER", "NEON", "RAIN"]

WORDS = load_words()

DIFFICULTY_SETTINGS = {
    "easy": {"min_speed": 1, "max_speed": 4, "count": 80},
    "medium": {"min_speed": 2, "max_speed": 6, "count": 120},
    "hard": {"min_speed": 3, "max_speed": 8, "count": 160},
}

# ----------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------
class FallingChar:
    """Represents a single falling character on the screen."""

    def __init__(self, x, y, char, speed):
        self.x = x
        self.y = y
        self.char = char
        self.speed = speed
        self.active = True

    def update(self):
        """Update position and reset if it moves off-screen."""
        if self.active:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.reset()

    def reset(self):
        """Reset position and assign a new random character."""
        self.y = random.randint(-50, -10)
        self.x = random.randint(0, SCREEN_WIDTH)
        self.char = chr(random.randint(65, 90))  # A–Z
        self.speed = random.uniform(min_speed, max_speed)
        self.active = True

    def draw(self):
        """Draw the character on the screen."""
        if self.active:
            text = FONT.render(self.char, True, GREEN)
            screen.blit(text, (self.x, self.y))

    def collide_with_mouse(self, mouse_pos):
        """Check if the mouse collides with the character."""
        if self.active:
            rect = FONT.render(self.char, True, GREEN).get_rect(topleft=(self.x, self.y))
            return rect.collidepoint(mouse_pos)
        return False


class Particle:
    """Represents a small particle for explosion effect."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.color = color

    def update(self):
        """Move particle and decrease life."""
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        """Draw particle if still alive."""
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

# ----------------------------------------------------------------------
# Game Functions
# ----------------------------------------------------------------------
def start_game(difficulty):
    """Initialize game state based on difficulty."""
    global chars, current_word, progress_index, score, remaining_time
    global min_speed, max_speed, current_difficulty

    current_difficulty = difficulty
    settings = DIFFICULTY_SETTINGS[difficulty]
    min_speed, max_speed = settings["min_speed"], settings["max_speed"]

    # Generate falling characters
    chars = [
        FallingChar(
            random.randint(0, SCREEN_WIDTH),
            random.randint(-500, SCREEN_HEIGHT),
            chr(random.randint(65, 90)),
            random.uniform(min_speed, max_speed),
        )
        for _ in range(settings["count"])
    ]

    current_word = random.choice(WORDS)
    progress_index = 0
    score = 0
    remaining_time = TIME_LIMIT  # Initialize timer

def draw_menu():
    """Draw the main menu screen."""
    title = HUD_FONT.render("WORD BUILDER GAME", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

    options = ["1 - EASY", "2 - MEDIUM", "3 - HARD"]
    for i, text in enumerate(options):
        option = HUD_FONT.render(text, True, GREEN)
        screen.blit(option, (SCREEN_WIDTH // 2 - option.get_width() // 2, SCREEN_HEIGHT // 2 + i * 60))

def draw_game():
    """Draw active gameplay elements."""
    global final_score, state, remaining_time, chars, particles, current_word, progress_index, score

    # Timer
    if remaining_time <= 0:
        final_score = score
        state = "gameover"

    # Characters
    for c in chars:
        c.update()
        c.draw()

    # Particles
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)
        else:
            p.draw()

    # Glowing word progress
    for i, letter in enumerate(current_word):
        if i < progress_index:
            glow_intensity = int(128 + 127 * math.sin(pygame.time.get_ticks() / 200))
            glow_color = (glow_intensity, glow_intensity, 0)
            glow_surface = HUD_FONT.render(letter, True, glow_color)
        else:
            glow_surface = HUD_FONT.render(letter, True, (80, 80, 80))
        screen.blit(glow_surface, (50 + i * 50, 30))

    # HUD
    screen.blit(HUD_FONT.render(f"Score: {score}", True, WHITE), (50, 100))
    screen.blit(HUD_FONT.render(f"Time: {int(remaining_time)}", True, RED), (50, 150))

def draw_gameover():
    """Draw the game over screen."""
    over_text = BIG_FONT.render("GAME OVER", True, RED)
    score_text = HUD_FONT.render(f"Your Score: {final_score}", True, WHITE)
    restart_text = HUD_FONT.render("Press ENTER to return to Menu", True, GREEN)

    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

# ----------------------------------------------------------------------
# Main Game Loop
# ----------------------------------------------------------------------
state = "menu"
chars, particles = [], []
current_word, progress_index, score, final_score = "", 0, 0, 0
remaining_time = TIME_LIMIT
current_difficulty = "easy"
running = True

while running:
    dt = clock.tick(60) / 1000  # delta time in seconds
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    # Reduce remaining_time
    if state == "game":
        remaining_time -= dt

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Menu Input
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game("easy"); state = "game"
                elif event.key == pygame.K_2:
                    start_game("medium"); state = "game"
                elif event.key == pygame.K_3:
                    start_game("hard"); state = "game"

        # Game Input
        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for c in chars:
                    if c.collide_with_mouse(mouse_pos) and c.active:
                        c.active = False
                        for _ in range(20):
                            particles.append(Particle(c.x, c.y, GREEN))

                        # Word progress check
                        if c.char == current_word[progress_index]:
                            progress_index += 1
                            if progress_index == len(current_word):
                                score += 1
                                remaining_time += (BONUS_TIME[current_difficulty]*len(current_word))  # ADD BONUS TIME
                                current_word = random.choice(WORDS)
                                progress_index = 0

        # Game Over Input
        elif state == "gameover":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                state = "menu"

    # State Drawing
    if state == "menu":
        draw_menu()
    elif state == "game":
        draw_game()
    elif state == "gameover":
        draw_gameover()

    pygame.display.flip()

pygame.quit()
sys.exit()  # ADD BONUS TIME
