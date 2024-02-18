def start_level1():

  import pygame
  import sys

  pygame.init()

  WHITE = (255, 255, 255)
  SCREEN_WIDTH = 420
  SCREEN_HEIGHT = 250

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Simple Pygame Game")

  platform_img = pygame.image.load("images_level_1/platform.png")  #

  background = pygame.image.load("images_level_1/background.png")
  background = pygame.transform.scale(background,
                                      (SCREEN_WIDTH, SCREEN_HEIGHT))

  player_image = pygame.image.load("images_level_1/player.png")
  player_image = pygame.transform.scale(
      player_image,
      (player_image.get_width() * 2, player_image.get_height() * 2))
  player_rect = player_image.get_rect()
  player_rect.topleft = (100, 50)

  heart_img = pygame.image.load("heart.png")
  portal_img = pygame.image.load("portal.png")

  #START FROM HERE!!!
  class Heart(pygame.sprite.Sprite):

    def __init__(self, x, y):
      super().__init__()

      self.image = heart_img
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

  class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, image_path):
      super().__init__()
      self.image = image_path
      self.image = pygame.transform.scale(self.image, (width, height))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

      self.hitbox = pygame.Rect(x, y, width, height)

    def draw(self, screen):
      screen.blit(self.image, (self.rect.x, self.rect.y))

    def collision_check(self, player_rect):
      return self.hitbox.colliderect(player_rect)

  # Основной игровой цикл

  clock = pygame.time.Clock()

  platforms = []

  def add_platform(x, y, x1, y2):
    platform = Platform(x, y, x1, y2, platform_img)
    platforms.append(platform)

  add_platform(10, 200, 175, 25)
  add_platform(200, 150, 175, 25)

  collide_check = False
  gravity = 5
  jump_speed = 15
  jumping = False
  running = True
  player_speed = 3

  ### MAIN GAME LOOP
  while running:
    # ITERATE OVER EVENTS
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    for plt in platforms:
      if plt.collision_check(player_rect):
        player_center = player_rect.center
        platform_center = plt.rect.center
        # растояние по горизонтали и вертикали
        dx = player_center[0] - platform_center[0]
        dy = player_center[1] - platform_center[1] - 100
        if abs(dx) <= abs(dy):
          if dy <= 0:
            collide_check = True
        break
    keys = pygame.key.get_pressed()

    # Движение вправо - d, влево - a
    if keys[pygame.K_d]:
      player_rect.x += player_speed
    elif keys[pygame.K_a]:
      player_rect.x -= player_speed

    # Прыжок
    if not jumping:
      # platform + space
      if keys[pygame.K_SPACE] and collide_check:
        jumping = True
        # since 0, 0 is upper left --> - gives up movement
        player_rect.y -= jump_speed
    # jump evry tick, then - speed = 0 --> no more jumping
    else:
      player_rect.y -= jump_speed
      jump_speed -= 1
      if jump_speed == 0:
        jumping = False
        jump_speed = 15

    if not collide_check and jump_speed >= 0:
      # Если игрок не стоит на платформе - gravity
      player_rect.y += gravity
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_rect)
    for plt in platforms:
      plt.draw(screen)
    pygame.display.flip()
    collide_check = False
    clock.tick(100)
