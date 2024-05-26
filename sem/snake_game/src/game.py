"""Imports"""
import sys

import src.config as conf
from src.game_objects import PlayerSnake, Food, EnemySnake
from src.grid import Grid

import pygame
from pygame.math import Vector2

class Game:
    """Main class managing the game"""

    # pylint: disable=too-many-instance-attributes
    # This class needs to handle all game objects, so 9 attributes are reasonable in this case.

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake game")
        self.screen = pygame.display.set_mode(
            (conf.TILE_SIZE * conf.GRID_SIZE, conf.TILE_SIZE * conf.GRID_SIZE))
        self.clock = pygame.time.Clock()
        self.player_update = pygame.USEREVENT
        self.enemy_update = pygame.USEREVENT + 1
        self.game_is_running = False

        self.grid = None
        self.player = None
        self.enemy = None
        self.food = None

        self.display_main_menu()

    def write_text(self, text, font, font_size, color, pos_vector):
        """Displays given text on the sceen"""
        # pylint: disable=too-many-arguments
        # In this case removing any arguments would make the function less universal or more complicated
        pg_font = pygame.font.SysFont(font, font_size)
        text_to_display = pg_font.render(text, True, color)
        text_rect = text_to_display.get_rect(center=(pos_vector))
        self.screen.blit(text_to_display, text_rect)

    def display_main_menu(self):
        """Displays main menu"""
        self.disable_timers()
        self.screen.fill(conf.MENU_BACKGROUND_COLOR)
        self.write_text("Snake Against AI", conf.TITLE_FONT,
                        conf.TITLE_FONT_SIZE, conf.TITLE_COLOR, conf.TITLE_POS)
        self.write_text("Press SPACE to play or ESC to exit",
                        conf.TEXT_FONT, conf.TEXT_FONT_SIZE, conf.TEXT_COLOR, conf.TEXT_POS)

    def start_game(self):
        """Begins the game. Redraws screen with playing board, snakes and food."""
        self.screen.fill(conf.BACKGROUND_COLOR)

        self.game_is_running = True
        self.grid = Grid()
        self.player = PlayerSnake(self.grid, self.screen)
        self.enemy = EnemySnake(self.grid, self.screen)
        self.food = Food(self.grid, self.screen)

        # timers form moving the snakes
        pygame.time.set_timer(self.player_update, conf.MOVE_INTERVAL)
        # offset enemy snake's timer (so that they won't move at the same time)
        pygame.time.delay(conf.MOVE_INTERVAL // 2)
        pygame.time.set_timer(self.enemy_update, conf.MOVE_INTERVAL)

    def display_end_screen(self, player_win):
        """Displays game over screen and if player won"""
        self.game_is_running = False
        Food.is_spawned = False
        self.disable_timers()
        self.screen.fill(conf.MENU_BACKGROUND_COLOR)

        if player_win:
            self.write_text("YOU WIN", conf.TITLE_FONT,
                            conf.TITLE_FONT_SIZE, conf.TITLE_COLOR, conf.TITLE_POS)
        else:
            self.write_text("YOU LOSE", conf.TITLE_FONT,
                            conf.TITLE_FONT_SIZE, conf.TITLE_COLOR, conf.TITLE_POS)

        self.write_text("Press SPACE to play or ESC to exit",
                        conf.TEXT_FONT, conf.TEXT_FONT_SIZE, conf.TEXT_COLOR, conf.TEXT_POS)

    def display_score(self, score, score_pos, color):
        """Displayes player and enemy length"""
        pg_font = pygame.font.SysFont(conf.TEXT_FONT, conf.SCORE_FONT_SIZE)
        # redraw tile to cover previous score
        self.grid.get_tile(score_pos).draw(self.screen)
        text_to_display = pg_font.render(str(score), True, color)
        score_world_pos = Vector2(
            score_pos*conf.TILE_SIZE + Vector2(conf.TILE_SIZE//2, conf.TILE_SIZE//2))
        text_rect = text_to_display.get_rect(center=score_world_pos)
        self.screen.blit(text_to_display, text_rect)

    def end_game(self):
        """Quits pygame and the whole program"""
        pygame.quit()
        sys.exit()

    def check_size_diff(self):
        """If one snake is significantly larger than the other, the bigger one wins"""
        player_len = self.player.get_snake_len()
        enemy_len = self.enemy.get_snake_len()

        if enemy_len > player_len + conf.MAX_LEN_DIFF:
            self.display_end_screen(False)
        elif enemy_len + conf.MAX_LEN_DIFF < player_len:
            self.display_end_screen(True)

    def disable_timers(self):
        """Turns off snake move timers"""
        pygame.time.set_timer(self.player_update, 0)
        pygame.time.set_timer(self.enemy_update, 0)

    def player_input(self, event):
        """Handles player input"""
        if self.game_is_running:
            # Movement
            if event.key == pygame.K_UP:
                self.player.change_direction(Vector2(0, -1))
            elif event.key == pygame.K_DOWN:
                self.player.change_direction(Vector2(0, 1))
            elif event.key == pygame.K_RIGHT:
                self.player.change_direction(Vector2(1, 0))
            elif event.key == pygame.K_LEFT:
                self.player.change_direction(Vector2(-1, 0))
        else:
            # Menu input
            if event.key == pygame.K_SPACE:
                self.game_is_running = True
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.end_game()

    def update_after_snake_move(self):
        """Updates all things that could change after one of the snakes moved."""
        self.food.try_to_spawn()
        self.display_score(self.player.get_snake_len(),
                           conf.PLAYER_SCORE_POS, conf.PLAYER_COLOR)
        self.display_score(self.enemy.get_snake_len(),
                           conf.ENEMY_SCORE_POS, conf.ENEMY_COLOR)
        self.check_size_diff()

    def update(self):
        """
        Checks and updates everything important for the game to run properly.
        Happens every tick of the clock.
        """
        for event in pygame.event.get():
            # Quit button
            if event.type == pygame.QUIT:
                self.end_game()

            if event.type == self.player_update:
                # Player lost if he collided (move method returned false)
                if not self.player.move():
                    self.display_end_screen(False)
                    continue
                self.update_after_snake_move()

            elif event.type == self.enemy_update:
                # Player wins if enemy colides
                if not self.enemy.move():
                    self.display_end_screen(True)
                    continue
                self.update_after_snake_move()

            if event.type == pygame.KEYDOWN:
                self.player_input(event)

        pygame.display.update()
        self.clock.tick(conf.FRAMERATE)
