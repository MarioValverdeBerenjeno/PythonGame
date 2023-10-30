import pygame
import random
import math
import sys
import os
import multiprocessing

# Inicializa pygame
pygame.init()

# Tamaño de pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar imágenes, sonidos y fuentes
asset_background = resource_path("assets/images/fondo_espacio_pixel.png")
background = pygame.image.load(asset_background)

asset_icon = resource_path("assets/images/enemigo1.png")
icon = pygame.image.load(asset_icon)

asset_sound = resource_path("assets/sounds/background_music.mp3")
pygame.mixer.music.load(asset_sound)

asset_playerimg = resource_path("assets/images/nave.png")
playerimg = pygame.image.load(asset_playerimg)

asset_bulletimg = resource_path("assets/images/bullet.png")
bulletimg = pygame.image.load(asset_bulletimg)

asset_over_font = resource_path("assets/fonts/RAVIE.TTF")
over_font = pygame.font.Font(asset_over_font, 64)

asset_font = resource_path("assets/fonts/comicbd.ttf")
font = pygame.font.Font(asset_font, 32)

# Establecer título e icono de la ventana
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# Reproducir música de fondo en bucle
pygame.mixer.music.play(-1)

# Crear un reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posición inicial del jugador
playerX = 250
playerY = 470
playerX_change = 0

# Número de enemigos y listas para almacenar sus posiciones
no_of_enemies = 10
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(no_of_enemies):
    enemy1 = resource_path("assets/images/enemigo1.png")
    enemyimg.append(pygame.image.load(enemy1))

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))

    enemyX_change.append(5)
    enemyY_change.append(20)

# Inicializar variables para la bala
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Inicializar la puntuación en 0
score = 0

# Mostrar puntuación
def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

# Dibujar al jugador en la pantalla
def player(x, y):
    screen.blit(playerimg, (x, y))

# Dibujar a los enemigos en la pantalla
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Disparar una bala
def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# Comprobar colisión entre enemigos y balas
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Mostrar "Game Over"
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(over_text, text_rect)


# Función para manejar la lógica del juego en un proceso secundario
def game_logic(queue):
    # Inicializa tus variables de juego aquí
    playerX = 250
    playerY = 470
    playerX_change = 0
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"
    score = 0
    in_game = True

    # Lista de enemigos
    no_of_enemies = 10
    enemyX = [random.randint(0, 736) for _ in range(no_of_enemies)]
    enemyY = [random.randint(0, 150) for _ in range(no_of_enemies)]
    enemyX_change = [5 for _ in range(no_of_enemies)]
    enemyY_change = [20 for _ in range(no_of_enemies)]

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX + 80
                        bullet_state = "fire"
                if event.key == pygame.K_UP:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= -20:
            playerX = -20
        elif playerX >= 603:
            playerX = 603
        
        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                in_game = False
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            distance = math.hypot(enemyX[i] - bulletX, enemyY[i] - bulletY)
            if distance < 27:
                bulletY = 454
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)

        if bulletY < 0:
            bulletY = 454
            bullet_state = "ready"
        if bullet_state == "fire":
            bulletY -= bulletY_change

        queue.put((playerX, score, enemyX, enemyY, in_game, bullet_state))

# Función para manejar la representación gráfica del juego en un proceso secundario
def game_graphics(queue):
    pygame.init()
    pygame.mixer.init()

    # Configurar Pygame y crear la ventana
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("assets/images/enemigo1.png")
    pygame.display.set_icon(icon)

    # Inicializar otras variables de juego aquí
    # ...

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        playerX, score, enemyX, enemyY, in_game, bullet_state = queue.get()

        screen.fill((0, 0, 0))
        background = pygame.image.load("assets/images/fondo_espacio_pixel.png")
        screen.blit(background, (0, 0))

        for i in range(10):
            screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))

        player(playerX, playerY)
        show_score()

        if not in_game:
            game_over_text()

        if bullet_state == "fire":
            screen.blit(bulletimg, (bulletX, bulletY))
            
        pygame.display.update()

def gameloop():
    queue = multiprocessing.Queue()
    game_logic(queue)
    game_graphics(queue)
    clock.tick(5)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    gameloop()