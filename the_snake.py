import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная ячейка игрового поля:
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# Цвета:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (93, 216, 228)

BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = LIGHT_BLUE
APPLE_COLOR = RED
SNAKE_COLOR = GREEN

# Скорость движения змейки:
SPEED = 20

TURNS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на игровом поле"""
        raise NotImplementedError(
            f'Определите метод draw в классе {type(self).__name__}.'
        )

    def draw_cell(self, position, body_color=None, border_color=BORDER_COLOR):
        """Отрисовывает одну ячейку поля по указанным координатам"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color or self.body_color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Яблоко, которое змейка ест"""

    def __init__(self, occupied_positions=(), body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Задача яблоку случайную позицию вне занятых клеток"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Список координат сегментов змейки и логика ее движения"""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def reset(self):
        """Возврат змейки в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTIONS)
        self.last = None

    def update_direction(self, direction):
        """Обновление направления движения после нажатия на кнопку"""
        self.direction = direction

    def get_head_position(self):
        """Возврат позиции головы змейки"""
        return self.positions[0]

    def move(self):
        """Перемещение змейки на одну ячейку в текущем направлении"""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop() if len(self.positions) > self.length else None
        )

    def draw(self):
        """Отрисовка змейки и стирание следа ее хвоста"""
        for position in self.positions:
            self.draw_cell(position)

        if self.last:
            self.draw_cell(
                self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR
            )


def handle_keys(game_object):
    """Обработка нажатия клавиш и закрытие окна игры

    Возвращает направление движения с учётом нажатых клавиш
    """
    direction = game_object.direction
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            direction = TURNS.get((event.key, direction), direction)
    return direction


def main():
    """Запуск игры"""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        snake.update_direction(handle_keys(snake))
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
