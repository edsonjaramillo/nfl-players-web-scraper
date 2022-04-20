from typing import List, Tuple
from browser import Browser
from playwright.sync_api import ElementHandle
from player import Player
import json


class NFLPlayersScraper(Browser):
    """NFL Players Scraper class gets all the active players from NFL.com for the latest active season."""
    _players: List[Player] = []

    def get_players(self) -> List[Player]:
        """Gets the players from NFL.com

        Returns:
            `List[Players]`: The players."""
        self._start_browser(is_headless=False)
        alphabet = self._get_alphabet()
        for letter in alphabet:
            self._open_url(f"https://www.nfl.com/players/active/{letter}")
            while True:
                self._wait(1)
                self._scroll_down()
                self._get_player_data()
                if self._is_last_page():
                    break
                self._go_to_next_page()

        self._close_browser()
        return self._players

    def _get_alphabet(self) -> List[str]:
        """Gets the alphabet because the NFL url is seperated by letter routes.
        Example: https://www.nfl.com/players/active/a|b|c...

        Returns:
            `list`: [`a`, `b`, `c`, `...`]"""
        return list("abcdefghijklmnopqrstuvwxyz")

    def _is_last_page(self) -> bool:
        """Checks if the current page is the last page.

        Returns:
            `bool`: True if the current page is the last page, False otherwise."""
        inactive = self.page.query_selector(
            '.nfl-o-table-pagination__next.d3-is-inactive')
        return inactive is not None

    def _go_to_next_page(self) -> None:
        """Goes to the next page."""
        self.page.query_selector('.nfl-o-table-pagination__next').click()

    def _get_player_data(self) -> None:
        table = self._get_table()
        rows = self._get_players_rows(table)
        for _, row in enumerate(rows):
            name = self._get_player_name(row)
            team, pos, status = self._get_team_poistion_status(row)
            player = Player(name, team, pos, status)
            self._players.append(player)

    def _get_table(self) -> ElementHandle:
        """Gets the table. The table is the main container for the players.

        Returns:
            `ElementHandle`: The table."""
        return self.page.query_selector("tbody")

    def _get_players_rows(self, table: ElementHandle) -> List[ElementHandle]:
        """Gets the rows from the table.

        Arguments:
            `table` (ElementHandle): The table to get the rows from."""
        return table.query_selector_all("tr")

    def _get_player_name(self, row: ElementHandle) -> str:
        """Gets the player name from the row.

        Arguments:
            `row` (ElementHandle): The row to get the player name from.

        Returns:
            name (str): The player name."""
        name = row.query_selector(".d3-o-player-fullname").inner_text()
        return name

    def _get_team_poistion_status(self, row: ElementHandle) -> Tuple[str, str, str]:
        """Gets the team, position, and status from the row.

        Arguments:
            `row` (ElementHandle): The row to get the team, position, and status from.

        Returns:
            `tuple`: (`team`, `position`, `status`)"""
        stats = row.query_selector_all("td")
        team = stats[1].inner_text()
        position = stats[2].inner_text()
        status = stats[3].inner_text()
        return self._format_team(team), position, status

    def _format_team(self, team: str) -> str:
        """Formats the team name.

        Arguments:
            `team` (str): The team name to format.

        Returns:
            `str`: The formatted team name."""
        return team.split(' ')[-1]


def main() -> None:
    players = NFLPlayersScraper().get_players()
    # write to players.json file
    with open("players.json", "w+") as json_file:
        json.dump([player.__dict__ for player in players], json_file, indent=2)


if __name__ == "__main__":
    main()
