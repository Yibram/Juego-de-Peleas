import pygame
from pygame import mixer
from peleador import Peleador

mixer.init()
pygame.init()

#crear la ventana del juego
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#Definir la frecuencia de los fotogramas
clock = pygame.time.Clock()
FPS = 60

#Definir colores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#Definir variables del juego
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#Definir variables de los peleadores
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Inicio de música del programa
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#Iniciar imagen de fondo (escenario)
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#Iniciar sprites de los personajes
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#Imagen de victoria
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#Definir el número de pasos en cada animación
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Definir fuente
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#Función para dibujar texto
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#Función para dibujar el fondo
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#Función para dibujar barras de salud de luchadores
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#Crear dos instancias de peleadores
peleador_1 = Peleador(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
peleador_2 = Peleador(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#Bucle del juego
run = True
while run:

  clock.tick(FPS)

  #Dibujar fondo
  draw_bg()

  #Mostrar estadísticas del jugador
  draw_health_bar(peleador_1.health, 20, 20)
  draw_health_bar(peleador_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

  #Actualizar cuenta regresiva
  if intro_count <= 0:
    #movimiento del los peleadores
    peleador_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, peleador_2, round_over)
    peleador_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, peleador_1, round_over)
  else:
    #Temporizador de conteo de pantalla
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #Actualizar el temporizador de conteo
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #actualizacion de los personajes
  peleador_1.update()
  peleador_2.update()

  # "Dibujar" o plantear los peleadores en la pantalla
  peleador_1.draw(screen)
  peleador_2.draw(screen)

  #Verificar la derrota del jugador
  if round_over == False:
    if peleador_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif peleador_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #Mostrar imagen de victoria
    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      peleador_1 = Peleador(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      peleador_2 = Peleador(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  #Controlador de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False


  #Actualizar pantalla
  pygame.display.update()

#Salir del juego
pygame.quit()