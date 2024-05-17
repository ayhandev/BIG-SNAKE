import pygame
import random
import webbrowser


pygame.init()

# Установка размеров экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIG SNAKE")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)

# Шрифты
font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 30)

# Функция отрисовки текста на экране
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Открытие сайта BigCode
def open_bigcode():
    webbrowser.open('https://bigcode.pythonanywhere.com')

# Открытие вашего GitHub
def open_github():
    webbrowser.open('https://github.com/your_github_username')  # Замените на ваш реальный URL

# Кнопки для выбора скорости
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
            if click[0] == 1 and self.action:
                self.action()
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        draw_text(self.text, font_medium, BLACK, self.rect.centerx, self.rect.centery)

def start_screen():
    buttons = [
        Button("Speed 1", WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 50, GREEN, YELLOW, lambda: gameLoop(5, 200)),
        Button("Speed 2", WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 50, GREEN, YELLOW, lambda: gameLoop(10, 150)),
        Button("Speed 3", WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 50, GREEN, YELLOW, lambda: gameLoop(15, 120)),
        Button("Speed 4", WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 50, GREEN, YELLOW, lambda: gameLoop(20, 100)),
        Button("Speed 5", WIDTH // 2 - 150, HEIGHT // 2 + 140, 300, 50, GREEN, YELLOW, lambda: gameLoop(25, 80))
    ]
    
    y_pos = -100  # Начальная позиция текста для анимации

    while True:
        screen.fill(BLACK)
        draw_text("BIGCODE", font_big, WHITE, WIDTH // 2, y_pos)
        y_pos += 5  # Скорость движения текста

        if y_pos > HEIGHT // 4:
            y_pos = HEIGHT // 4

        draw_text("", font_medium, WHITE, WIDTH // 2, HEIGHT // 2 - 150)
        draw_text("GitHub: github.com/ayhandev/BIG-SNAKE", font_small, WHITE, WIDTH // 2, HEIGHT - 30)

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()

# Основная функция игры
def gameLoop(snake_speed, target_score):
    # Параметры змейки
    snake_block = 20
    x1 = WIDTH // 2
    y1 = HEIGHT // 2
    x1_change = 0
    y1_change = 0

    # Параметры "яблок"
    languages = ["Python", "Java", "JavaScript", "C++", "Ruby", "PHP", "Swift", "Go"]
    current_language = random.choice(languages)
    foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

    # Параметры счетчика и жизней
    score = 0
    lives = 3

    # Основной игровой цикл
    snake_list = []
    snake_length = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        # Проверка на столкновение со стенами
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            lives -= 1
            if lives == 0:
                game_over()
            x1 = WIDTH // 2
            y1 = HEIGHT // 2
            snake_list = []
            snake_length = 1

        # Проверка на столкновение с самим собой
        for segment in snake_list[:-1]:
            if segment == [x1, y1]:
                lives -= 1
                if lives == 0:
                    game_over()
                x1 = WIDTH // 2
                y1 = HEIGHT // 2
                snake_list = []
                snake_length = 1
                break

        screen.fill(BLACK)
        draw_text("Score: " + str(score), font_small, WHITE, WIDTH // 2, 20)
        draw_text("Lives: " + str(lives), font_small, WHITE, WIDTH - 80, 20)

        draw_text(current_language, font_small, RED, foodx + snake_block // 2, foody + snake_block // 2)

        # Отрисовка границ
        pygame.draw.line(screen, RED, (0, 0), (WIDTH, 0), 5)  # Верхняя граница
        pygame.draw.line(screen, RED, (0, HEIGHT), (WIDTH, HEIGHT), 5)  # Нижняя граница
        pygame.draw.line(screen, RED, (0, 0), (0, HEIGHT), 5)  # Левая граница
        pygame.draw.line(screen, RED, (WIDTH, 0), (WIDTH, HEIGHT), 5)  # Правая граница

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for i, segment in enumerate(snake_list):
            color = ORANGE if i == len(snake_list) - 1 else GRAY
            pygame.draw.rect(screen, color, [segment[0], segment[1], snake_block, snake_block])

        pygame.display.update()

        # Проверка на съедание "яблок"
        if x1 == foodx and y1 == foody:
            score += 1
            snake_length += 1
            current_language = random.choice(languages)
            foodx = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block

        # Проверка условия победы
        if score >= target_score:
            open_bigcode()

        pygame.time.Clock().tick(snake_speed)

# Экран окончания игры
def game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", font_big, RED, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(2000)
    start_screen()


start_screen()
