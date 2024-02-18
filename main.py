# Import necessary libraries
import pygame
# knowing that level_1.py contains the start_level1 function
from level_1 import start_level1
from level_2 import start_level2
from replit import audio

# Sound file for button click
sound = "click.wav"

# Window dimensions
WIDTH = 420
HEIGHT = 250

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Color
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the main window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu with Buttons")

# Load background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load button images
button_image = pygame.image.load('button_image.png')
button_image = pygame.transform.scale(button_image,
                                      (BUTTON_WIDTH, BUTTON_HEIGHT))

dark_button_image = pygame.image.load('dark_button_image.png')
dark_button_image = pygame.transform.scale(dark_button_image,
                                           (BUTTON_WIDTH, BUTTON_HEIGHT))

# Create buttons - 6 in total
buttons = []
for i in range(1, 7):
  x = (i - 1) % 3 * (BUTTON_WIDTH + 10) + 50
  y = (i - 1) // 3 * (BUTTON_HEIGHT + 10) + 50
  button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
  buttons.append(button_rect)
print(buttons)

# Main program loop
running = True
while running:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      # Left mouse button clicked
      if event.button == 1:
        # Check if the current mouse position (event.pos) is within the area of the current button
        for i, button in enumerate(buttons):
          if button.collidepoint(event.pos):
            print("Button Clicked!")
            audio.play_file(sound)
            # Since Python indexes start from 0
            level = i + 1
            # Execute the corresponding level function
            exec("start_level" + str(level) + "()")

  # Draw the screen
  window.blit(background_image, (0, 0))

  # Draw buttons
  for i, button in enumerate(buttons):
    if button.collidepoint(pygame.mouse.get_pos()):
      window.blit(dark_button_image, button)
    else:
      window.blit(button_image, button)

    font = pygame.font.SysFont(None, 30)
    # Render text on the button
    text = font.render(str(i + 1), True, BLACK)
    text_rect = text.get_rect(center=button.center)
    window.blit(text, text_rect)

  pygame.display.flip()
