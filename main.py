from nfl_players_scraper import NFLPlayersScraper
import json


def main() -> None:
    players = NFLPlayersScraper().get_players()
    # write to players.json file
    with open("players.json", "w+") as json_file:
        json.dump([player.__dict__ for player in players], json_file, indent=2)


if __name__ == "__main__":
    main()
