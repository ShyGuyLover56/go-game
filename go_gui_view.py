import pygame as pg
from enum import Enum
import pygame_gui as gui
import time

from go_model import GoModel, UndoException
from game_piece import GamePiece
from position import Position

BOARD_SIZE = 19  # Default size (Change as needed)
CELL_SIZE = 40
GRID_COLOR = (0, 0, 0)
BOARD_COLOR = (255, 200, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STONE_RADIUS = 12

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
SIDE_BOX_WIDTH = 350 # side terminal width
SIDE_BOX_HEIGHT = 550 # side terminal height


# Buttons sizes
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

class StoneColor(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    
class GUI:
    def __init__(self):
        pg.init()
        self.__model = GoModel(BOARD_SIZE, BOARD_SIZE)
        self._screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_BOX_WIDTH, SCREEN_HEIGHT + SIDE_BOX_HEIGHT))
        pg.display.set_caption("Laker's Go Game")
        self._ui_manager = gui.UIManager((SCREEN_WIDTH + SIDE_BOX_WIDTH, SCREEN_HEIGHT + SIDE_BOX_HEIGHT))

        # Board positioning
        self.board_x_offset = 50
        self.board_y_offset = 50

        # Side Box (Game Info)
        self._side_box = gui.elements.UITextBox(
            f'{self.__model.message}<br />',
            relative_rect=pg.Rect((SCREEN_WIDTH - 10, 50), (SIDE_BOX_WIDTH, SIDE_BOX_HEIGHT)),
            manager=self._ui_manager
        )

        # Buttons (Below Board)
        button_y = self.board_y_offset + BOARD_HEIGHT + 30  # Extra spacing between board and buttons

        self._undo_button = gui.elements.UIButton(
            relative_rect=pg.Rect((100, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Undo',
            manager=self._ui_manager
        )
        self._restart_button = gui.elements.UIButton(
            relative_rect=pg.Rect((250, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Reset',
            manager=self._ui_manager
        )
        self._pass_button = gui.elements.UIButton(
            relative_rect=pg.Rect((400, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Pass Turn',
            manager=self._ui_manager
        )

    def get_board_position(self, mouse_pos):
        """Converts mouse position to board (x, y) indices."""
        mouse_x, mouse_y = mouse_pos

        # Adjust for board offset
        board_x = (mouse_x - self.board_x_offset) // CELL_SIZE
        board_y = (mouse_y - self.board_y_offset) // CELL_SIZE

        # Ensure click is inside the board
        if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
            return [board_x, board_y]
        else:
            self._side_box.append_html_text(f"Clicked outside..<br />")

    def __display_game_over__(self):
        """Displays 'Game Over' message in the center of the screen."""
        scores = self.__model.calculate_score()
        # Font setup
        font = pg.font.SysFont("Arial", 36)

        # Multiline text
        winner = "BLACK" if scores[0] > scores[1] else "WHITE"
        lines = ["Game Over!", f"BLACK: {scores[0]}  WHITE: {scores[1]}", f"Winner: {winner}"]

        # Calculate the total height of the text block
        line_spacing = 10
        text_surfaces = [font.render(line, True, WHITE) for line in lines]
        text_width = max(text.get_width() for text in text_surfaces)
        text_height = sum(text.get_height() for text in text_surfaces) + (len(lines) - 1) * line_spacing

        # Full-width rectangle, centered vertically
        bg_rect = pg.Rect(0, (SCREEN_HEIGHT // 2 - text_height // 2 - 20),
                          SCREEN_WIDTH + 350,
                          text_height + 40)
        pg.draw.rect(self._screen, BLACK, bg_rect)  # Draw background

        # Render each line and center it horizontally
        y_offset = SCREEN_HEIGHT // 2 - text_height // 2
        for text in text_surfaces:
            text_x = (SCREEN_WIDTH - text.get_width()) // 2
            self._screen.blit(text, (text_x, y_offset))
            y_offset += text.get_height() + line_spacing  # Move to next line

        # Update screen and keep message displayed for 2 seconds
        pg.display.flip()
        time.sleep(3)

    def run_game(self):
        running = True
        clock = pg.time.Clock()
        time_delta = 0
        button_y = self.board_y_offset + BOARD_HEIGHT + 30
        undo_button = pg.Rect(100, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        reset_button = pg.Rect(250, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pass_button = pg.Rect(400, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                # # action for buttons
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # Left click
                    if undo_button.collidepoint(event.pos):
                        try:
                            self.__model.undo()
                            self._side_box.append_html_text(f"{self.__model.message}<br />")
                        except UndoException as msg:
                            self._side_box.append_html_text(f"Cannot Undo anymore..<br />")
                    elif reset_button.collidepoint(event.pos):
                        self.__model = GoModel()
                        self._side_box.append_html_text(f"Restarting game...<br />")
                    elif pass_button.collidepoint(event.pos):
                        self.__model.pass_turn()
                        self._side_box.append_html_text(f"{self.__model.message}<br />")
                    else: # click on board
                        pos = self.get_board_position(event.pos)
                        pos = Position(pos[0], pos[1]) # x is cols and y is rows
                        cell = self.__model.piece_at(pos)
                        if not cell:
                            piece = GamePiece(self.__model.current_player.player_color)
                            if self.__model.is_valid_placement(pos, piece):
                                self.__model.set_piece(pos, piece)
                                self.__model.capture()
                                self.__model.set_next_player()
                        self._side_box.append_html_text(f"{self.__model.message}<br />")
                    if self.__model.is_game_over():
                        running = False
                        self.__display_game_over__()

                self._ui_manager.process_events(event)



            # Draw everything
            self._screen.fill(WHITE)
            self.__draw_board__()
            self._ui_manager.draw_ui(self._screen)
            self._ui_manager.update(time_delta)
            pg.display.flip()
            time_delta = clock.tick(30) / 1000.0
    def __draw_board__(self):
        """Draws the Go board grid."""
        pg.draw.rect(
            self._screen, BOARD_COLOR,
            (self.board_x_offset, self.board_y_offset, BOARD_WIDTH, BOARD_HEIGHT)
        )

        # Draw grid lines
        for x in range(BOARD_SIZE):
            pg.draw.line(
                self._screen, GRID_COLOR,
                (self.board_x_offset + CELL_SIZE // 2 + x * CELL_SIZE, self.board_y_offset + CELL_SIZE // 2),
                (self.board_x_offset + CELL_SIZE // 2 + x * CELL_SIZE, self.board_y_offset + BOARD_HEIGHT - CELL_SIZE // 2)
            )
            pg.draw.line(
                self._screen, GRID_COLOR,
                (self.board_x_offset + CELL_SIZE // 2, self.board_y_offset + CELL_SIZE // 2 + x * CELL_SIZE),
                (self.board_x_offset + BOARD_WIDTH - CELL_SIZE // 2, self.board_y_offset + CELL_SIZE // 2 + x * CELL_SIZE)
            )
        for row in range(self.__model.nrows):
            for col in range(self.__model.ncols):
                if self.__model.board[row][col] is not None:
                    color = StoneColor[self.__model.board[row][col].color.name].value
                    center_x = self.board_x_offset + CELL_SIZE // 2 + row * CELL_SIZE
                    center_y = self.board_y_offset + CELL_SIZE // 2 + col * CELL_SIZE
                    pg.draw.circle(self._screen, color, (center_x, center_y), STONE_RADIUS)

if __name__ == '__main__':
    g = GUI()
    g.run_game()
