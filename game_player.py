
# awww cammy wammy is so cool and awesome


from player_colors import PlayerColors
from abc import ABC, abstractmethod

class GamePlayer:
    """
    Represents a player in the game, keeping track of their color, capture count, and skip count.

    The player has a color, a capture count to track how many pieces they have captured, and a skip count to track how many turns they have skipped.
    """
    def __init__(self, player_color: PlayerColors, capture_count: int = 0, skip_count: int = 0): # default capture and skip count is 0
        """
        Initializes a new GamePlayer with the given player color, capture count, and skip count.

        Args:
            player_color (PlayerColors): The color of the player, must be an instance of the PlayerColors enum.
            capture_count (int): The number of pieces the player has captured (default is 0).
            skip_count (int): The number of turns the player has skipped (default is 0).

        Raises:
            TypeError: If the player_color is not an instance of PlayerColors.
            ValueError: If capture_count or skip_count is negative.
        """
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
        """
        Gets the color of the player.

        Returns:
            PlayerColors: The color of the player.
        """
        return self.__player_color

    @property # readable
    def capture_count(self) -> int:
        """
        Gets the number of pieces the player has captured.

        Returns:
            int: The number of captures.
        """
        return self.__capture_count

    @capture_count.setter # writable
    def capture_count(self, value: int):
        """
        Sets the capture count for the player.

        Args:
            value (int): The new capture count.

        Raises:
            ValueError: If the capture count is negative.
        """
        if value < 0:
            raise ValueError("you can't have a negative capture count")
        self.__capture_count = value

    @property # readable
    def skip_count(self) -> int:
        """
        Gets the number of turns the player has skipped.

        Returns:
            int: The number of skips.
        """
        return self.__skip_count

    @skip_count.setter # writable
    def skip_count(self, value: int):
        """
        Sets the skip count for the player.

        Args:
            value (int): The new skip count.

        Raises:
            ValueError: If the skip count is negative.
        """
        if value < 0:
            raise ValueError("you can't have negative skips")
        self.__skip_count = value

    def __str__(self) -> str:
        """
        Returns a string representation of the GamePlayer.

        Returns:
            str: A string representation of the GamePlayer showing their color, captures, and skips.
        """
        return f'GamePlayer(color: {self.__player_color.name}, captures: {self.__capture_count}, skips: {self.__skip_count})'
