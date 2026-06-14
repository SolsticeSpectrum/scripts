import pygame
import sys
import time
from collections import deque

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 300
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scroll speed")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

last_scroll_time = 0
scroll_time_ms = 0
scroll_count = 0
average_scroll_times = deque(maxlen=10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                current_time = time.time()
                scroll_time_ms = (current_time - last_scroll_time) * 1000
                last_scroll_time = current_time
                scroll_count += 1
                average_scroll_times.append(scroll_time_ms)

            elif event.button == 5:
                current_time = time.time()
                scroll_time_ms = (current_time - last_scroll_time) * 1000
                last_scroll_time = current_time
                scroll_count += 1
                average_scroll_times.append(scroll_time_ms)

    screen.fill(BACKGROUND_COLOR)

    text = font.render(f"Doba od posledního scrollu (ms): {scroll_time_ms:.2f}", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(text, text_rect)

    if average_scroll_times:
        average_speed = sum(average_scroll_times) / len(average_scroll_times)
    else:
        average_speed = 0

    average_text = small_font.render(f"Průměrná rychlost (ms): {average_speed:.2f}", True, TEXT_COLOR)
    average_text_rect = average_text.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))

    screen.blit(average_text, average_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
