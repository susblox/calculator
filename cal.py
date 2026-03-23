import pygame
import pyttsx3

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
GREEN = (0, 180, 0)
RED = (255, 0, 0)

# Voice setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Buttons layout
buttons = [
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+'],
    ['DEL']  # replaced C with DEL
]

btn_w = WIDTH // 4
btn_h = 100

# Calculator state
current_input = ""
last_answer = ""
running = True

while running:
    screen.fill(BLACK)

    # Draw display for input
    pygame.draw.rect(screen, GRAY, (0,0,WIDTH,100))
    input_surface = font.render(current_input, True, BLACK)
    screen.blit(input_surface, (10, 20))

    # Draw display for answer
    pygame.draw.rect(screen, GREEN, (0,100,WIDTH,50))
    answer_surface = font.render(f"Ans: {last_answer}", True, BLACK)
    screen.blit(answer_surface, (10, 105))

    # Draw buttons
    for i, row in enumerate(buttons):
        for j, label in enumerate(row):
            x = j * btn_w
            y = 150 + i * btn_h
            w = btn_w if label != 'DEL' else WIDTH
            h = btn_h
            pygame.draw.rect(screen, ORANGE if label in ['=','DEL'] else WHITE, (x, y, w, h))
            pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
            txt = font.render(label, True, BLACK)
            txt_rect = txt.get_rect(center=(x + w//2, y + h//2))
            screen.blit(txt, txt_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    last_answer = str(eval(current_input))
                    speak(f"The answer is {last_answer}")
                    current_input = last_answer
                except:
                    last_answer = "Error"
                    speak("Error")
                    current_input = ""
            elif event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.unicode in "0123456789+-*/.":
                current_input += event.unicode
            elif event.key == pygame.K_c:  # changed C to DEL behavior
                current_input = current_input[:-1]

        # Mouse click input
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, row in enumerate(buttons):
                for j, label in enumerate(row):
                    x = j * btn_w
                    y = 150 + i * btn_h
                    w = btn_w if label != 'DEL' else WIDTH
                    h = btn_h
                    if x <= mx <= x+w and y <= my <= y+h:
                        if label == 'DEL':  # Delete last character
                            current_input = current_input[:-1]
                        elif label == '=':
                            try:
                                last_answer = str(eval(current_input))
                                speak(f"The answer is {last_answer}")
                                current_input = last_answer
                            except:
                                last_answer = "Error"
                                speak("Error")
                                current_input = ""
                        else:
                            current_input += label

pygame.quit()