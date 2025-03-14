"""
awww cammy wammy is so cool and awesome
"""

from player_colors import PlayerColors
from abc import ABC, abstractmethod
# why is that grey??? ^^^^^ i use it

class GamePlayer:
    def __init__(self, player_color: PlayerColors, capture_count: int = 0, skip_count: int = 0): # default capture and skip count is 0
        if not isinstance(player_color, PlayerColors):
            raise TypeError("player_color has to be enum value 0 or 1")
        if capture_count < 0:
            raise ValueError("capture_count can't be negative")
        if skip_count < 0:
            raise ValueError("skip count can't be negative")

        self.__player_color = player_color # should (hopefully) be one of the enums player_colors.py
        self.__capture_count = capture_count
        self.__skip_count = skip_count

    @property # readable
    def player_color(self) -> PlayerColors:
        return self.__player_color

    @property # readable
    def capture_count(self) -> int:
        return self.__capture_count

    @capture_count.setter # writable
    def capture_count(self, value: int):
        if value < 0:
            raise ValueError("you can't have a negative capture count")
        self.__capture_count = value

    @property # readable
    def skip_count(self) -> int:
        return self.__skip_count

    @skip_count.setter # writable
    def skip_count(self, value: int):
        if value < 0:
            raise ValueError("you can't have negative skips")
        self.__skip_count = value

    def __str__(self) -> str:
        return f'GamePlayer(color: {self.__player_color.name}, captures: {self.__capture_count}, skips: {self.__skip_count})'
