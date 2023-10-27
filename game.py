import pygame
import random
import math
import sys
import os

#Iniciar pygame
pygame.init()

#Tamaño pantalla
screen_width = 800
screen_heigth = 600
screen = pygame.display.set_mode((screen_width, screen_heigth))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
#Cargar img fondo
asset_background = resource_path("assets/images/fondo_espacio_pixel.png")
background = pygame.image.load(asset_background)

#Cargar icono de ventana
asset_icon= resource_path("assets/images/enemigo1.png")
icon = pygame.image.load(asset_icon)

#Cargar sonido de fondo
asset_sound= resource_path("assets/sounds/background_music.mp3")
background_sound = pygame.mixer.music.load(asset_sound)

#Cargar img del jugador
asset_playerimg = resource_path("assets/images/nave.png")
playerimg = pygame.image.load(asset_playerimg)

#Cargar img bala
asset_bulletimg = resource_path("assets/images/bullet.png")
bulletimg = pygame.image.load(asset_bulletimg)

#Cargar fuente txt game over
asset_over_font = resource_path("assets/fonts/RAVIE.TTF")
over_font = pygame.font.Font(asset_over_font)

# Cargar txt de puntuación
asset_font = resource_path("assets/fonts/comicbd.ttf")
font = pygame.font.Font(asset_font)

# Establecer titulo de ventana
pygame.display.set_caption("Space Invader")

# Establecer icono de ventana
pygame.display.set_icon(icon)

# Sonido de fondo en bucle
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posicion inicial del jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# Lista para almacenar posiciones de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

# Inicialización de las var para las posiciones de los enemigos
for i in range(no_of_enemies):
    # Carga de la img del enemigo
    enemy1 = resource_path("assets/images/enemigo1.png")
    enemyimg.append(pygame.image.load(enemy1))

    """enemy2 = resource_path("assets/images/enemigo2.png")
    enemyimg.append(pygame.image.load(enemy2))"""

    # Posicion aleatoria
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

    # Velocidad enemigo
    enemyX_change.append(5)
    enemyY_change.append(20)

    # Inicialización de var para guardar la posicion de la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Puntuación en 0
    score = 0

    # Mostrar puntuación
    def show_score():
        score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))

    # Jugador en pantalla
    def player(x, y):
        screen.blit(playerimg, (x, y))

    # Enemigos en pantalla
    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))
    
    # Disparar bala
    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg, (x+16, y+10))

    # Colisión bala enemigo
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                             (math.pow(enemyY - bulletY, 2)))
        if distance < 27 :
            return True
        else:
            return False

    # Mostrar game over
    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center = (int(screen_width/2), int(screen_heigth/2)))
        screen.blit(over_text, text_rect)

    # Main
    def gameloop():
        # Declarar variables globales
        global score, playerX, playerX_change, bulletX, bulletY, collision, bullet_state

        in_game = True
        while(in_game):
            # Maneja eventos
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit()
                
                # Movimineto del jugador y el disparo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                    if event.key == pygame.K_UP:
                        playerX_change = 0

            # Actualiza la posicion del enemigo        
            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736
            
            #Bucle para cada enemigo
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]

                # Colisión entre enemigos y balas
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)
            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
            
            player(playerX, playerY)
            show_score()

            pygame.display.update()

            clock.tick(120)

gameloop()
                


