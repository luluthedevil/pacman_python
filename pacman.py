import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 20, True, False)

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
PINK = (255, 15, 192)
CYAN = (0, 255, 255)
SPEED = 1
ABOVE = 1
BELOW = 2
RIGHT = 3
LEFT = 4


class GameElement(metaclass=ABCMeta):
    @abstractmethod
    def toPaint(self, screen):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def process_events(self, events):
        pass


class Movable(metaclass=ABCMeta):
    @abstractmethod
    def accept_movement(self):
        pass

    @abstractmethod
    def deny_movement(self, directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass


class Scenario(GameElement):
    def __init__(self, size, pac):
        self.pacman = pac
        self.movables = []
        self.points = 0
        # possible states: 0-playing  1-Pause  2-GameOver  3-Victory
        self.state = 0
        self.size = size
        self.lifes = 5
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def add_Movable(self, obj):
        self.movables.append(obj)

    def toPaint_score(self, screen):
        points_x = self.size * 30
        points_img = font.render("Score {}".format(self.points), True, YELLOW)
        lifes_img = font.render("Lifes {}".format(self.lifes), True, YELLOW)
        screen.blit(points_img, (points_x, 50))
        screen.blit(lifes_img, (points_x, 100))

    def toPaint_row(self, screen, number_row, row):
        for number_column, column in enumerate(row):
            x = number_column * self.size
            y = number_row * self.size
            half = self.size // 2
            color = BLACK
            if column == 2:
                color = BLUE
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(screen, YELLOW, (x + half, y + half),
                                   self.size // 10, 0)

    def toPaint(self, screen):
        if self.state == 0:
            self.toPaint_playing(screen)
        elif self.state == 1:
            self.toPaint_playing(screen)
            self.toPaint_paused(screen)
        elif self.state == 2:
            self.toPaint_playing(screen)
            self.toPaint_gameover(screen)
        elif self.state == 3:
            self.toPaint_playing(screen)
            self.toPaint_victory(screen)

    def toPaint_text_center(self, screen, text):
        text_img = font.render(text, True, YELLOW)
        text_x = (screen.get_width() - text_img.get_width()) // 2
        text_y = (screen.get_height() - text_img.get_height()) // 2
        screen.blit(text_img, (text_x, text_y))

    def toPaint_victory(self, screen):
        self.toPaint_text_center(screen, "C O N G R A T U L A T I O N S   Y O U   W I N  ! ! !")

    def toPaint_gameover(self, screen):
        self.toPaint_text_center(screen, "G A M E   O V E R")

    def toPaint_paused(self, screen):
        self.toPaint_text_center(screen, "P A U S E")

    def toPaint_playing(self, screen):
        for number_row, row in enumerate(self.matrix):
            self.toPaint_row(screen, number_row, row)
        self.toPaint_score(screen)

    def get_directions(self, row, column):
        directions = []
        if self.matrix[int(row - 1)][int(column)] != 2:
            directions.append(ABOVE)
        if self.matrix[int(row + 1)][int(column)] != 2:
            directions.append(BELOW)
        if self.matrix[int(row)][int(column - 1)] != 2:
            directions.append(LEFT)
        if self.matrix[int(row)][int(column + 1)] != 2:
            directions.append(RIGHT)
        return directions

    def calculate_rules(self):
        if self.state == 0:
            self.calculate_rules_playing()
        elif self.state == 1:
            self.calculate_rules_paused()
        elif self.state == 2:
            self.calculate_rules_gameover()

    def calculate_rules_gameover(self):
        pass

    def calculate_rules_paused(self):
        pass

    def calculate_rules_playing(self):
        for Movable in self.movables:
            lin = int(Movable.row)
            col = int(Movable.column)
            lin_intention = int(Movable.row_intention)
            col_intention = int(Movable.column_intention)
            directions = self.get_directions(lin, col)
            if len(directions) >= 3:
                Movable.corner(directions)
            if isinstance(Movable, Ghost) and Movable.row == self.pacman.row and \
                    Movable.column == self.pacman.column:
                self.lifes -= 1
                if self.lifes <= 0:
                    self.state = 2
                else:
                    self.pacman.row = 1
                    self.pacman.column = 1
            else:
                if 0 <= col_intention < 28 and 0 <= lin_intention < 29 and \
                        self.matrix[lin_intention][col_intention] != 2:
                    Movable.accept_movement()
                    if isinstance(Movable, Pacman) and self.matrix[lin][col] == 1:
                        self.points += 1
                        self.matrix[lin][col] = 0
                        if self.points >= 306:
                            self.state = 3
                else:
                    Movable.deny_movement(directions)

    def process_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.state == 0:
                        self.state = 1
                    else:
                        self.state = 0


class Pacman(GameElement, Movable):
    def __init__(self, size):
        self.column = 1
        self.row = 1
        self.center_x = 400
        self.center_y = 300
        self.size = size
        self.vel_x = 0
        self.vel_y = 0
        self.radius = self.size // 2
        self.column_intention = self.column
        self.row_intention = self.row
        self.opening = 0
        self.SPEED_opening = 1

    def calculate_rules(self):
        self.column_intention = self.column + self.vel_x
        self.row_intention = self.row + self.vel_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.row * self.size + self.radius)

    def toPaint(self, screen):
        # Desenhar o corpo do Pacman
        pygame.draw.circle(screen, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        self.opening += self.SPEED_opening
        if self.opening > self.radius:
            self.SPEED_opening = -1
        if self.opening <= 0:
            self.SPEED_opening = 1

        # Desenho da boca do Pacman
        canto_boca = (self.center_x, self.center_y)
        labio_superior = (self.center_x + self.radius, self.center_y - self.opening)
        labio_inferior = (self.center_x + self.radius, self.center_y + self.opening)
        points = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(screen, BLACK, points, 0)

        # eye do Pacman
        eye_x = int(self.center_x + self.radius / 3)
        eye_y = int(self.center_y - self.radius * 0.70)
        eye_radius = int(self.radius / 10)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_radius, 0)

    def process_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = SPEED
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -SPEED
                elif e.key == pygame.K_UP:
                    self.vel_y = -SPEED
                elif e.key == pygame.K_DOWN:
                    self.vel_y = SPEED
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def accept_movement(self):
        self.row = self.row_intention
        self.column = self.column_intention

    def deny_movement(self, directions):
        self.row_intention = self.row
        self.column_intention = self.column

    def corner(self, directions):
        pass


class Ghost(GameElement):
    def __init__(self, color, size):
        self.column = 13.0
        self.row = 15.0
        self.row_intention = self.row
        self.column_intention = self.column
        self.SPEED = 1
        self.direction = BELOW
        self.size = size
        self.color = color

    def toPaint(self, screen):
        slice = self.size // 8
        px = int(self.column * self.size)
        py = int(self.row * self.size)
        outline = [(px, py + self.size),
                    (px + slice, py + slice * 2),
                    (px + slice * 2, py + slice // 2),
                    (px + slice * 3, py),
                    (px + slice * 5, py),
                    (px + slice * 6, py + slice // 2),
                    (px + slice * 7, py + slice * 2),
                    (px + self.size, py + self.size)]
        pygame.draw.polygon(screen, self.color, outline, 0)

        eye_radius_ext = slice
        eye_radius_int = slice // 2

        eye_e_x = int(px + slice * 2.5)
        eye_e_y = int(py + slice * 2.5)

        eye_d_x = int(px + slice * 5.5)
        eye_d_y = int(py + slice * 2.5)

        pygame.draw.circle(screen, WHITE, (eye_e_x, eye_e_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_e_x, eye_e_y), eye_radius_int, 0)
        pygame.draw.circle(screen, WHITE, (eye_d_x, eye_d_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_d_x, eye_d_y), eye_radius_int, 0)

    def calculate_rules(self):
        if self.direction == ABOVE:
            self.row_intention -= self.SPEED
        elif self.direction == BELOW:
            self.row_intention += self.SPEED
        elif self.direction == LEFT:
            self.column_intention -= self.SPEED
        elif self.direction == RIGHT:
            self.column_intention += self.SPEED

    def change_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.change_direction(directions)

    def accept_movement(self):
        self.row = self.row_intention
        self.column = self.column_intention

    def deny_movement(self, directions):
        self.row_intention = self.row
        self.column_intention = self.column
        self.change_direction(directions)

    def process_events(self, evts):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Ghost(RED, size)
    inky = Ghost(CYAN, size)
    clyde = Ghost(ORANGE, size)
    pinky = Ghost(PINK, size)
    Scenario = Scenario(size, pacman)
    Scenario.add_Movable(pacman)
    Scenario.add_Movable(blinky)
    Scenario.add_Movable(inky)
    Scenario.add_Movable(clyde)
    Scenario.add_Movable(pinky)


    while True:
        # Calculate rules
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        Scenario.calculate_rules()

        # Paint the screen
        screen.fill(BLACK)
        Scenario.toPaint(screen)
        pacman.toPaint(screen)
        blinky.toPaint(screen)
        inky.toPaint(screen)
        clyde.toPaint(screen)
        pinky.toPaint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Catch the events
        events = pygame.event.get()
        pacman.process_events(events)
        Scenario.process_events(events)
