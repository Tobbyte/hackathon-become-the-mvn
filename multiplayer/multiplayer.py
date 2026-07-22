import os.path

# import subprocess
from datetime import datetime

# from zoneinfo import ZoneInfo
import random
import multiplayer_filehandler
from i_o.io import output


def _ensure_player_file_exists(user_name: str = "Vincent") -> bool:
    user_filename = user_name + "_multiplayer.json"
    existing_player = _check_player_exists(user_filename)
    if existing_player:
        return True
    score_file = _get_user_score_file(user_name)
    multiplayer_filehandler.save_file(user_filename, score_file)

    return True


def _check_player_exists(user_file: str):
    if not os.path.exists(user_file):
        return False
    return True


def _get_user_score_file(new_user: str) -> dict:
    categories = _get_categories()
    player_scores = {}
    player_scores["player"] = new_user
    player_scores["created_at"] = _create_timestamp()
    player_scores["last_updated"] = _create_timestamp()
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


def _get_categories() -> list[str]:
    categories = [
        "full_random",
        "category",
        "top_easy",
        "top_medium",
        "top_hard",
    ]
    return categories


def _create_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _create_run_profile(save_game: tuple, user_name: str) -> dict:
    (
        modus,
        titel,
        timestamp_start,
        timestamp_end,
        tries,
        wrong_answers,
        help_needed,
    ) = save_game

    start_seconds = datetime.fromisoformat(timestamp_start).timestamp()
    end_seconds = datetime.fromisoformat(timestamp_end).timestamp()
    duration_seconds = int(end_seconds - start_seconds)

    file_keys = [
        "user_name",
        "modus",
        "titel",
        "timestamp_start",
        "duration_seconds",
        "tries",
        "wrong_answers",
        "help_needed",
    ]

    file_values = [
        user_name,
        modus,
        titel,
        timestamp_start,
        duration_seconds,
        tries,
        wrong_answers,
        help_needed,
    ]

    run_profile = {}
    counter = 0
    for value in file_values:
        run_profile[file_keys[counter]] = value
        counter += 1
    return run_profile


def _add_run_to_file(user_file: dict, run_profile: dict):
    modus = run_profile["modus"]
    for game_mode in user_file["runs"]:
        if game_mode == modus:
            user_file["runs"][game_mode].append(run_profile)


def _update_personal_records(
    user_file: dict, run_profile: dict
):  # run_profile wird geadded
    modus = run_profile["modus"]
    r_n_least = user_file["personal_records"]["normal"]["least_attempts"]
    r_n_fastest = user_file["personal_records"]["normal"]["fastest"]
    r_i_least = user_file["personal_records"]["ironman"]["least_attempts"]
    r_i_fastest = user_file["personal_records"]["ironman"]["fastest"]
    if r_n_least[modus] is None or r_n_least[modus]["tries"] > run_profile["tries"]:
        r_n_least[modus] = run_profile
        _announce_record(
            modus, "fewest attempts", "normal", run_profile
        )  # 1st = modus, 2nd = normal, 3rd = run_file
        print()

    if (
        r_n_fastest[modus] is None
        or r_n_fastest[modus]["duration_seconds"] > run_profile["duration_seconds"]
    ):
        r_n_fastest[modus] = run_profile
        _announce_record(
            modus, "fastest run", "normal", run_profile
        )  # 1st = modus, 2nd = normal, 3rd = run_file
        print()

    if (
        r_i_least[modus] is None or r_i_least[modus]["tries"] > run_profile["tries"]
    ) and run_profile["help_needed"] == 0:
        r_i_least[modus] = run_profile
        _announce_record(
            modus, "fewest attempts", "ironman", run_profile
        )  # 1st = modus, 2nd = normal, 3rd = run_file
        print()

    if (
        r_i_fastest[modus] is None
        or r_i_fastest[modus]["duration_seconds"] > run_profile["duration_seconds"]
    ) and run_profile["help_needed"] == 0:
        r_i_fastest[modus] = run_profile
        _announce_record(
            modus, "fastest run", "ironman", run_profile
        )  # 1st = modus, 2nd = normal, 3rd = run_file
        print()


def _announce_record(
    modus: str, record_modus: str, record_version: str, run_profile: dict
):
    output(
        f"NEW PERSONAL {(record_version).upper()} RECORD for the {record_modus} in category: {modus}"
    )
    _print_current_run(run_profile)


def _print_current_run(run: dict):
    output(
        f"title: {run['titel']} - Category: {run['modus']}, tries: {run['tries']}, wrong answers: {run['wrong_answers']}, seconds: {run['duration_seconds']}, help needed: {run['help_needed']}"
    )  # Platzhalter print


def _update_last_updated(user_file):
    user_file["last_updated"] = _create_timestamp()


def init_user(user_name: str) -> None:
    _ensure_player_file_exists(user_name)


def save_run(save_game: tuple[str, str, str, str, int, int, int], user_name: str):
    (
        modus,
        titel,
        timestamp_start,
        timestamp_end,
        tries,
        wrong_answers,
        help_needed,
    ) = save_game
    user_filename = user_name + "_multiplayer.json"
    user_file = multiplayer_filehandler.load_file(user_filename)
    run_profile = _create_run_profile(save_game, user_name)
    _add_run_to_file(user_file, run_profile)
    _update_personal_records(user_file, run_profile)
    _update_last_updated(user_file)
    multiplayer_filehandler.save_file(user_filename, user_file)


# For development only:
def _random_run_generator() -> tuple[
    tuple[str, str, str, str, int, int, int],
    str,
]:
    """Return randomly generated run data for the given user."""
    user_name = "Vincent"
    game_modes = [
        "full_random",
        "category",
        "top_easy",
        "top_medium",
        "top_hard",
    ]

    titles = [
        "Lion",
        "Orangutan",
        "European hedgehog",
        "Theodore Roosevelt",
        "Albert Einstein",
        "Berlin",
        "The Godfather",
        "Michael Jackson",
        "Cristiano Ronaldo",
        "World War II",
    ]

    modus = random.choice(game_modes)
    titel = random.choice(titles)

    timestamp_end = datetime.now().astimezone()

    duration_seconds = random.randint(60, 600)

    timestamp_start = datetime.fromtimestamp(
        timestamp_end.timestamp() - duration_seconds,
        tz=timestamp_end.tzinfo,
    )

    tries = random.randint(5, 20)
    wrong_answers = random.randint(0, min(5, tries))
    help_needed = random.randint(0, 5)

    return (
        modus,
        titel,
        timestamp_start.isoformat(timespec="seconds"),
        timestamp_end.isoformat(timespec="seconds"),
        tries,
        wrong_answers,
        help_needed,
    ), user_name


if __name__ == "__main__":
    init_user("Vincent")
    save_game, user_name = _random_run_generator()
    save_run(save_game, user_name)
