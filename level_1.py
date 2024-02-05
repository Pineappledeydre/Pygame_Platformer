def start_level1():
  # Import necessary libraries
  import pygame
  import sys

  # Initialization of Pygame
  pygame.init()

  # Define colors
  WHITE = (255, 255, 255)

  # Define screen dimensions
  SCREEN_WIDTH = 420
  SCREEN_HEIGHT = 250

  # Create the game window
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Simple Pygame Game")

  # Load platform image
  platform_img = pygame.image.load("images_level_1/platform.png")

  # Load background image
  background = pygame.image.load("images_level_1/background.png")
  background = pygame.transform.scale(background,
                                      (SCREEN_WIDTH, SCREEN_HEIGHT))

  # Load player image
  player_image = pygame.image.load("images_level_1/player.png")
  player_image = pygame.transform.scale(
      player_image,
      (player_image.get_width() * 2, player_image.get_height() * 2))
  player_rect = player_image.get_rect()
  player_rect.topleft = (100, 50)

  # 'blueprint' for our platdorms
  class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, image_path):
      super().__init__()

      # Load platform image
      self.image = image_path
      self.image = pygame.transform.scale(self.image, (width, height))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

      # Set hitbox (collision rectangle)
      self.hitbox = pygame.Rect(x, y, width, height)

    # drawing a platform on the screen
    def draw(self, screen):
      screen.blit(self.image, (self.rect.x, self.rect.y))

    # check platform - user collision
    def collision_check(self, player_rect):
      return self.hitbox.colliderect(player_rect)

  # Clock to take care of the game timings
  clock = pygame.time.Clock()

  # List of platforms
  platforms = []

  # function to create  a platform + add it to the list of platforms
  def add_platform(x, y, x1, y2):
    platform = Platform(x, y, x1, y2, platform_img)
    platforms.append(platform)

  add_platform(10, 200, 175, 25)
  add_platform(200, 150, 175, 25)

  # variables that we need in our game for mvements tracking
  collide_check = False
  gravity = 5
  jump_speed = 15
  jumping = False
  running = True
  player_speed = 3

  # Main game loop
  while running:
    # Handle events (end the game if the user closes the window)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Check collision of a user with platform for each platform
    for plt in platforms:
      if plt.collision_check(player_rect):
        player_center = player_rect.center
        platform_center = plt.rect.center
        dx = player_center[0] - platform_center[0]
        dy = player_center[1] - platform_center[1] - 100
        if abs(dx) <= abs(dy):
          if dy <= 0:
            collide_check = True
        break

    keys = pygame.key.get_pressed()

    # Move right - d, left - a
    if keys[pygame.K_d]:
      player_rect.x += player_speed
    elif keys[pygame.K_a]:
      player_rect.x -= player_speed

    # Jump
    #  If the player is not jumping
    if not jumping:
      # Space is pressed and collision has been detected
      if keys[pygame.K_SPACE] and collide_check:
        jumping = True
        # Move the player upwards
        player_rect.y -= jump_speed
    # If the player is already in a jumping state
    else:
      # Reduce the height of a jump every time till it becomes 0
      player_rect.y -= jump_speed
      jump_speed -= 1
      if jump_speed == 0:
        jumping = False
        jump_speed = 15

    # The player is not jumping and not on the platform
    if not collide_check and jump_speed >= 0:
      player_rect.y += gravity

    # Draw background, player, platforms
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_rect)
    for plt in platforms:
      plt.draw(screen)

    # Depict all the changes on the screen
    pygame.display.flip()
    collide_check = False

    # Set the game speed
    clock.tick(100)
