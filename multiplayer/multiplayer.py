import os.path
# import subprocess

from datetime import datetime
# from zoneinfo import ZoneInfo

import multiplayer_filehandler


# def run_git_command(command: list[str]) -> bool:
#     result = subprocess.run(command, capture_output=True, text=True)
#
#     if result.returncode == 0:
#         return True
#
#     print(result.stderr)
#     return False


def _get_categories() -> list:
    categories = [
        "full_random",
        "category",
        "top_easy",
        "top_medium",
        "top_hard",
    ]
    return categories


def _get_user_score_file(new_user: str, timestamp: str) -> dict:
    categories = _get_categories()
    player_scores = {}
    player_scores["player"] = new_user
    player_scores["created_at"] = timestamp
    player_scores["last_updated"] = timestamp
    player_scores["personal_records"] = {}
    player_scores["personal_records"]["normal"] = {}
    player_scores["personal_records"]["normal"]["least_attempts"] = {}
    player_scores["personal_records"]["normal"]["fastest"] = {}
    player_scores["personal_records"]["ironman"] = {}
    player_scores["personal_records"]["ironman"]["least_attempts"] = {}
    player_scores["personal_records"]["ironman"]["fastest"] = {}
    player_scores["runs"] = {}
    for category in categories:
        player_scores["personal_records"]["normal"]["least_attempts"][category] = None
        player_scores["personal_records"]["normal"]["fastest"][category] = None
        player_scores["personal_records"]["ironman"]["least_attempts"][category] = None
        player_scores["personal_records"]["ironman"]["fastest"][category] = None
        player_scores["runs"][category] = []
    return player_scores


def _check_player_exists(user_file: str):
    if not os.path.exists(user_file):
        return False
    return True


def _create_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_player_file_exists(user_name: str = "Vincent") -> bool:
    user_filename = user_name + "_multiplayer.json"
    existing_player = _check_player_exists(user_filename)
    if existing_player:
        return True
    timestamp = _create_timestamp()
    score_file = _get_user_score_file(user_name, timestamp)
    multiplayer_filehandler.save_file(user_filename, score_file)
    return True



if __name__ == "__main__":
    ensure_player_file_exists()