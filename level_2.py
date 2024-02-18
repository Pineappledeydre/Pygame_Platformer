def start_level2():
  import pygame
  import sys

  # Инициализация Pygame
  pygame.init()

  # Определение цветов
  WHITE = (255, 255, 255)

  # Определение размеров экрана
  SCREEN_WIDTH = 420
  SCREEN_HEIGHT = 250
  # Создание игрового окна
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Простая игра на Pygame - level 2")

  # Загрузка изображения платформы
  platform_img = pygame.image.load("images_level_2/platform2.png")

  # Загрузка изображения фона, где название - путь
  background = pygame.image.load("images_level_2/background2.jpg")
  # Подгон под экран
  background = pygame.transform.scale(background,
                                      (SCREEN_WIDTH, SCREEN_HEIGHT))

  # Загрузка изображения игрока
  player_image = pygame.image.load("images_level_2/player2.png")
  # *2 height and width
  player_image = pygame.transform.scale(
      player_image, (player_image.get_width(), player_image.get_height()))
  # создаем хитбокс
  player_rect = player_image.get_rect()
  """
  Это новые координаты, куда будет   перемещен верхний левый угол прямоугольника. В данном случае, это (x=100, y=50)
  """
  player_rect.topleft = (100, 50)

  class Platform(pygame.sprite.Sprite):
    # конструктор класса, инициализирует объект Platform с параметрами,
    def __init__(self, x, y, width, height, image_path):
      #способ  метод конструктора ( __init__) родительского класса внутри подкласса
      super().__init__()

      # Загрузка изображения платформы
      self.image = image_path
      # Преобразование изображения
      self.image = pygame.transform.scale(self.image, (width, height))
      # Получение прямоугольника изображения для обработки столкновений
      self.rect = self.image.get_rect()
      # Установка координат для отображения изображения
      self.rect.x = x
      self.rect.y = y

      # Установка хитбокса (прямоугольника для обработки столкновений)
      self.hitbox = pygame.Rect(x, y, width, height)

    def draw(self, screen):
      # Отображение изображения на экране - bit block transfr
      screen.blit(self.image, (self.rect.x, self.rect.y))
      """
          to check for collisions between two rectangles, specifically between the hitbox of the current object (an instance of the class) and the player's rectangle (player_rect).
          """

    def collision_check(self, player_rect):
      return self.hitbox.colliderect(player_rect)

  # Основной игровой цикл
  """
  Если поезд двигается слишком быстро, может быть трудно увидеть детали, а если слишком медленно, становится скучно. Наши волшебные часы помогают нам установить правильную скорость для нашей игры.
  """
  clock = pygame.time.Clock()

  ############ РАССТАНОВКА ПЛАТФОРМ ###############

  platforms = []
  """
  создать новый экземпляр класса «Платформа» с заданными параметрами и добавить его в список платформ.
  """

  def add_platform(x, y, x1, y2):
    platform = Platform(x, y, x1, y2, platform_img)
    platforms.append(platform)

  add_platform(20, 100, 175, 25)
  add_platform(240, 140, 175, 25)

  ############ РАССТАНОВКА ПЛАТФОРМ ###############

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

    # Проверка столкновения с платформой - ДЛЯ КАЖДОЙ ПЛАТФОРМЫ
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

    if not collide_check and jump_speed >= 0:  # Если игрок не стоит на платформе - gravity
      player_rect.y += gravity

    # Отрисовка фона и игрока
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_rect)
    for plt in platforms:
      plt.draw(screen)
    pygame.display.flip()
    collide_check = False
    #  установим FPS на 100
    clock.tick(100)
