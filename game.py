import pygame
import random
import math
import sys
import os
import time

# Iniciar pygame

def gameloop():
    
    global playerX, playerX_change, bulletX, bulletY, collision, bullet_state, score, in_game, actual_velc
    
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
    asset_background = resource_path("assets/images/AnimatedBackground/")
    img_bg_list = []
    # Recorre los archivos en el directorio y carga las imágenes
    for img in os.listdir(asset_background):
        if img.endswith((".gif")):
            complete_path = os.path.join(asset_background, img)
            image = pygame.image.load(complete_path)
            img_bg_list.append(image)

    asset_icon = resource_path("assets/images/enemigo1.png")
    icon = pygame.image.load(asset_icon)

    asset_sound = resource_path("assets/sounds/background_music3.mp3")
    pygame.mixer.music.load(asset_sound)

    asset_playerimg = resource_path("assets/images/nave.png")
    playerimg = pygame.image.load(asset_playerimg)

    asset_bulletimg = resource_path("assets/images/bullet.png")
    bulletimg = pygame.image.load(asset_bulletimg)

    asset_over_font = resource_path("assets/fonts/RAVIE.TTF")
    over_font = pygame.font.Font(asset_over_font, 64)

    asset_font = resource_path("assets/fonts/comicbd.ttf")
    font = pygame.font.Font(asset_font, 32)

    pause_text = font.render("Pause - Press 'P' to continue", True, (255, 255, 255))

    # Establecer título e icono de la ventana
    pygame.display.set_caption("Space Destroyer")
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
    speedIncrement = 1.0015

    for i in range(no_of_enemies):
        enemy1 = resource_path("assets/images/enemigo1.png")
        enemyimg.append(pygame.image.load(enemy1))

        enemy2 = resource_path("assets/images/enemigo2.png")
        enemyimg.append(pygame.image.load(enemy2))

        enemy3 = resource_path("assets/images/enemigo3.png")
        enemyimg.append(pygame.image.load(enemy3))

        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(0, 150))

        enemyX_change.append(speedIncrement)
        enemyY_change.append(20)

    # Inicializar variables para la bala
    bulletX = 0
    bulletY = 480
    bulletY_change = 26
    bullet_state = "ready"

    # Inicializar la puntuación en 0
    score = 0

    # Inicializar el indice de las imagenes
    index = 0

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

    actual_speed = 5
    seconds_for_increment = 20 
    init_time = time.time()
    time_img = 0.1
    pause = False

    in_game = True
    while in_game:
        actual_time = time.time()
        time_in_progress = actual_time - init_time
        if(actual_speed <= 20 and time_in_progress >= seconds_for_increment):
            actual_speed *= speedIncrement

        index = int(time_in_progress / time_img) % len(img_bg_list)

        # Manejar eventos
        screen.fill((0, 0, 0))
        screen.blit(img_bg_list[index], (0, 0))

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
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_UP:
                    playerX_change = 0
                if event.key == pygame.K_p:
                    pause = not pause

        if not pause:
            playerX += playerX_change
            if playerX <= -20:
                playerX = -20
            elif playerX >= 603:
                playerX = 603
        
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = actual_speed 
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -actual_speed
                    enemyY[i] += enemyY_change[i]

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

            # Si se alcanza el último fotograma, vuelve al primero
            if index >= len(img_bg_list):
                index = 0
        else:
            screen.blit(pause_text, (0,0))

        pygame.display.update()

        clock.tick(120)