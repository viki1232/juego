import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH = 600
HEIGHT = 450
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Viaje Espacial")

# Colores
WHITE = (255, 255, 255)

# Cargar imágenes
space = pygame.image.load("images/space.jpg")
ship1 = pygame.image.load("images/ship1.png")
ship2 = pygame.image.load("images/ship2.png")
ship3 = pygame.image.load("images/ship3.png")
enemy_img = pygame.image.load("images/enemy.png")
meteor_img = pygame.image.load("images/meteor.png")
missile_img = pygame.image.load("images/missiles.png")
planet_imgs = [pygame.image.load(f"images/plan{i}.png") for i in range(1, 4)]
planet_speed = 1 
# Variables del juego
ship = ship1  # Empezamos con la nave 1
ship_rect = ship.get_rect(center=(WIDTH // 2, HEIGHT - 50))
enemies = []
meteors = []
balas = []
score = 0
mode = 'menu'

# Función para crear enemigos
def new_enemy():
    x = random.randint(0, WIDTH - enemy_img.get_width())
    y = random.randint(-450, -50)
    enemy_rect = enemy_img.get_rect(topleft=(x, y))
    speed = random.randint(2, 8)
    enemies.append([enemy_img, enemy_rect, speed])

# Función para crear meteoritos
def new_meteor():
    x = random.randint(0, WIDTH - meteor_img.get_width())
    y = random.randint(-450, -50)
    meteor_rect = meteor_img.get_rect(topleft=(x, y))
    speed = random.randint(2, 10)
    meteors.append([meteor_img, meteor_rect, speed])

# Mover los enemigos
def move_enemies():
    global enemies
    for i in range(len(enemies)-1, -1, -1):
        enemy_img, enemy_rect, speed = enemies[i]
        enemy_rect.y += speed
        if enemy_rect.y > HEIGHT:
            enemies.pop(i)
            new_enemy()

# Mover meteoritos
def move_meteors():
    global meteors
    for i in range(len(meteors)-1, -1, -1):
        meteor_img, meteor_rect, speed = meteors[i]
        meteor_rect.y += speed
        if meteor_rect.y > HEIGHT:
            meteors.pop(i)
            new_meteor()

# Colisiones entre balas y enemigos
def collisions():
    global score, mode
    for i in range(len(enemies)-1, -1, -1):
        enemy_img, enemy_rect, _ = enemies[i]
        if ship_rect.colliderect(enemy_rect):  # Si la nave toca un enemigo
            mode = 'end'  # Fin del juego
        for j in range(len(balas)-1, -1, -1):
            bala, bala_rect = balas[j]
            if bala_rect.colliderect(enemy_rect):
                enemies.pop(i)  # Eliminar enemigo
                balas.pop(j)  # Eliminar bala
                score += 1  # Aumentar puntaje
                new_enemy()  # Crear un nuevo enemigo
                break

# Dibujar los objetos
def draw():
    screen.blit(space, (0, 0))  # Fondo
    if mode == 'game':
        for planet_img in planet_imgs:
            screen.blit(planet_img, (random.randint(0, WIDTH), random.randint(-600, -50)))
            planet_speed=1
        for enemy_img, enemy_rect, _ in enemies:
            screen.blit(enemy_img, enemy_rect)
        for meteor_img, meteor_rect, _ in meteors:
            screen.blit(meteor_img, meteor_rect)
        for bala, bala_rect in balas:
            screen.blit(bala, bala_rect)
        screen.blit(ship, ship_rect)  # Dibujar la nave
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Mostrar puntaje
    elif mode == 'end':
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    elif mode == 'menu':
        screen.blit(space, (0, 0))  # Fondo
        font = pygame.font.SysFont(None, 36)
        text = font.render("Escoge tu nave", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
        screen.blit(ship1, (100, 200))  # Nave 1
        screen.blit(ship2, (300, 200))  # Nave 2
        screen.blit(ship3, (500, 200))  # Nave 3

# Detectar clic en las naves del menú
def on_mouse_down(pos):
    global mode, ship, ship_rect
    if mode == "menu":
        if 100 <= pos[0] <= 200 and 200 <= pos[1] <= 300:  # Clic en nave 1
            ship = ship1
            ship_rect = ship.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            mode = "game"
        elif 300 <= pos[0] <= 400 and 200 <= pos[1] <= 300:  # Clic en nave 2
            ship = ship2
            ship_rect = ship.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            mode = "game"
        elif 500 <= pos[0] <= 600 and 200 <= pos[1] <= 300:  # Clic en nave 3
            ship = ship3
            ship_rect = ship.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            mode = "game"

# Mover la nave con el ratón
def on_mouse_move(pos):
    global ship_rect
    ship_rect.centerx = pos[0]
    if ship_rect.centerx < 0:
        ship_rect.centerx = 0
    elif ship_rect.centerx > WIDTH:
        ship_rect.centerx = WIDTH

# Disparar misiles
def shoot_missile():
    missile = missile_img
    missile_rect = missile.get_rect(center=ship_rect.center)
    balas.append([missile, missile_rect])
def reset_game():
    global score, enemies, meteors, balas, planets, mode, ship, ship_rect
    # Restablecer el puntaje y los objetos del juego
    score = 0
    enemies = []
    meteors = []
    balas = []
    planets = []
    mode = 'menu'  # Volver al menú
    # Seleccionar la nave por defecto (nave 1)
    ship = ship1
    ship_rect = ship.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    # Crear algunos enemigos, meteoritos y planetas al reiniciar
    new_enemy()
    new_meteor()
    
# Bcle principal
def game_loop():
    global mode, score, enemies, meteors, balas
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))  # Limpiar pantalla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_down(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                on_mouse_move(event.pos)  # Mover la nave con el ratón
            elif event.type == pygame.KEYDOWN:
                if mode == 'end' and event.key == pygame.K_RETURN:  # Reiniciar solo en modo 'end'
                    reset_game()
                elif mode == 'game' and event.key == pygame.K_SPACE:  # Disparar con la tecla ESPACIO
                    shoot_missile()
        if mode == "game":
            move_enemies()
            move_meteors()
            collisions()
            for bala, bala_rect in balas:
                bala_rect.y -= 10  # Mover misiles hacia arriba
                if bala_rect.y < 0:
                    balas.remove([bala, bala_rect])  # Eliminar bala si sale de la pantalla
        






        draw()
        pygame.display.update()
        clock.tick(FPS)

# Iniciar juego
new_enemy()
new_meteor()
game_loop()

# Cerrar Pygame
pygame.quit()
