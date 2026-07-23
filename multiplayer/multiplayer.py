import os
# from zoneinfo import ZoneInfo
import random
from . import multiplayer_filehandler
# import subprocess
from datetime import datetime
from i_o.io import output


USER_FILES_FOLDER: str = os.path.join(
    os.path.dirname(__file__),
    "user_files",
)


def _ensure_player_file_exists(user_name: str) -> bool:
    user_filename = os.path.join(
        USER_FILES_FOLDER,
        user_name + "_multiplayer.json",
    )
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
    player_scores["created_at"] = create_timestamp()
    player_scores["last_updated"] = create_timestamp()
    player_scores["total_runs"] = 0
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



def create_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _create_run_profile(save_game: tuple, user_name: str) -> dict:
    (
        modus,
        title,
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
        "title",
        "timestamp_start",
        "duration_seconds",
        "tries",
        "wrong_answers",
        "help_needed",
    ]

    file_values = [
        user_name,
        modus,
        title,
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
    user_file: dict,
    run_profile: dict,
):  # run_profile wird geadded
    modus = run_profile["modus"]
    r_n_least = user_file["personal_records"]["normal"]["least_attempts"]
    r_n_fastest = user_file["personal_records"]["normal"]["fastest"]
    r_i_least = user_file["personal_records"]["ironman"]["least_attempts"]
    r_i_fastest = user_file["personal_records"]["ironman"]["fastest"]
    if r_n_least[modus] is None or r_n_least[modus]["tries"] > run_profile["tries"]:
        r_n_least[modus] = run_profile
        _announce_record(
            modus,
            "fewest attempts",
            "normal",
            run_profile,
        )  # 1st = modus, 2nd = normal, 3rd = run_file

    if (
        r_n_fastest[modus] is None
        or r_n_fastest[modus]["duration_seconds"] > run_profile["duration_seconds"]
    ):
        r_n_fastest[modus] = run_profile
        _announce_record(
            modus,
            "fastest run",
            "normal",
            run_profile,
        )  # 1st = modus, 2nd = normal, 3rd = run_file

    if (
        r_i_least[modus] is None or r_i_least[modus]["tries"] > run_profile["tries"]
    ) and run_profile["help_needed"] == 0:
        r_i_least[modus] = run_profile
        _announce_record(
            modus,
            "fewest attempts",
            "ironman",
            run_profile,
        )  # 1st = modus, 2nd = normal, 3rd = run_file

    if (
        r_i_fastest[modus] is None
        or r_i_fastest[modus]["duration_seconds"] > run_profile["duration_seconds"]
    ) and run_profile["help_needed"] == 0:
        r_i_fastest[modus] = run_profile
        _announce_record(
            modus,
            "fastest run",
            "ironman",
            run_profile,
        )  # 1st = modus, 2nd = normal, 3rd = run_file


def _announce_record(
    modus: str,
    record_modus: str,
    record_version: str,
    run_profile: dict,
):
    output(
        f"NEW PERSONAL {record_version.upper()} RECORD for the {record_modus} in category: {modus}",
    )


def _print_current_run(run: dict):
    print()
    output("Deine Statistik:")
    print()
    for k, v in run.items():
        if v in PRETTY_MODI_KEYS:
            v = PRETTY_MODI_KEYS[v]
        output(f"     {PRETTY_STATS_KEYS[k]}: {v}")
    print()

    # output(
    #     f"title: {run['title']} - Category: {run['modus']}, tries: {run['tries']}, wrong answers: {run['wrong_answers']}, seconds: {run['duration_seconds']}, help needed: {run['help_needed']}",
    # )  # Platzhalter print


def _update_last_updated(user_file):
    user_file["last_updated"] = create_timestamp()


def get_existing_users() -> list[str]:
    users = []

    for filename in os.listdir(USER_FILES_FOLDER):
        if filename.endswith("_multiplayer.json"):
            user_name = filename.removesuffix("_multiplayer.json")
            users.append(user_name)

    users.sort()
    return users


def init_user(user_name: str) -> None:
    _ensure_player_file_exists(user_name)


def convert_to_vincents_unnice_para_requests(dictus):
    return (
        dictus["modus"],
        dictus["title"],
        dictus["timestamp_start"],
        dictus["timestamp_end"],
        dictus["tries"],
        dictus["wrong_answers"],
        dictus["help_needed"],
    )

PRETTY_STATS_KEYS = {
    "user_name": "Nutzername",
    "modus": "Spielmodus",
    "title": "Wikipedia-Artikel",
    "timestamp_start": "Startzeit",
    "duration_seconds": "Dauer (s)",
    "tries": "Versuche",
    "wrong_answers": "Falsche Antworten",
    "help_needed": "Hilfe geholt",
}
PRETTY_MODI_KEYS = {
    "full_random": "zufällig",
    "category": "Nach Kategorie",
    "top_easy": "Top 100 - Schwierigkeit einfach",
    "top_medium": "Top 400 - Schwierigkeit mittel",
    "top_hard": "Top 1000 - Schwierigkeit schwer",
}

def save_run(
    save_game: tuple[str, str, str, str, int, int, int],
    user_name: str,
) -> None:
    user_filename = os.path.join(
        USER_FILES_FOLDER,
        user_name + "_multiplayer.json",
    )

    user_file = multiplayer_filehandler.load_file(user_filename)
    run_profile = _create_run_profile(save_game, user_name)

    _print_current_run(run_profile)
    _add_run_to_file(user_file, run_profile)

    user_file["total_runs"] += 1

    _update_personal_records(user_file, run_profile)
    _update_last_updated(user_file)

    multiplayer_filehandler.save_file(
        user_filename,
        user_file,
    )

    final_global_leaderboard = get_global_leaderboard()

    handle_leaderboard_output(
        final_global_leaderboard,
        run_profile,
    )


def print_all_global_leaderboards() -> None:
    fake_run_profile = {
        "modus": "all",
        "help_needed": 0,
    }

    final_global_leaderboard = get_global_leaderboard()

    handle_leaderboard_output(
        final_global_leaderboard,
        fake_run_profile,
    )


def handle_leaderboard_output(
    final_global_leaderboard: dict,
    run_profile: dict,
) -> None:
    _print_current_run_leaderboards(
        final_global_leaderboard,
        run_profile,
    )


def _print_current_run_leaderboards(
    final_global_leaderboard: dict,
    run_profile: dict,
) -> None:
    if run_profile["modus"] == "all":
        game_modes = _get_categories()

    else:
        game_modes = [
            run_profile["modus"],
        ]

    record_versions = []

    if run_profile["help_needed"] == 0:
        record_versions.append("ironman")

    record_versions.append("normal")

    record_types = [
        "fastest",
        "least_attempts",
    ]

    output("")
    output("Global Leaderboard:")

    for record_version in record_versions:
        for record_type in record_types:
            for game_mode in game_modes:
                leaderboard = final_global_leaderboard[
                    record_version
                ][record_type][game_mode]

                _print_global_leaderboard(
                    leaderboard,
                    record_version,
                    record_type,
                    game_mode,
                )


def _print_global_leaderboard(
    leaderboard: list[dict],
    record_version: str,
    record_type: str,
    game_mode: str,
) -> None:
    output("")
    output("")
    output(f"### {record_version} ###")
    output(f"## {record_type} ##")
    output(f"# {game_mode} #")

    for position, record in enumerate(
        leaderboard[:5],
        start=1,
    ):
        _print_global_leaderboard_entry(
            position,
            record,
            record_type,
        )


def _print_global_leaderboard_entry(
    position: int,
    record: dict,
    record_type: str,
) -> None:
    output("")
    output(f"{position}. Platz")

    output(
        f'{record["user_name"]} "{record["title"]}"'
    )

    if record_type == "fastest":
        output(
            f"{record['duration_seconds']} Sekunden | "
            f"{record['tries']} Versuche | "
            f"{record['wrong_answers']} falsche Antworten"
        )

    elif record_type == "least_attempts":
        output(
            f"{record['tries']} Versuche | "
            f"{record['duration_seconds']} Sekunden | "
            f"{record['wrong_answers']} falsche Antworten"
        )


def _sort_global_leaderboards(
    filled_global_leaderboard: dict,
) -> dict:
    for record_version in filled_global_leaderboard:
        for record_type in filled_global_leaderboard[record_version]:
            for game_mode in filled_global_leaderboard[
                record_version
            ][record_type]:
                leaderboard = filled_global_leaderboard[
                    record_version
                ][record_type][game_mode]

                if record_type == "least_attempts":
                    leaderboard.sort(
                        key=lambda record: record["tries"]
                    )

                elif record_type == "fastest":
                    leaderboard.sort(
                        key=lambda record: record[
                            "duration_seconds"
                        ]
                    )

    return filled_global_leaderboard


def _fill_global_records(
    global_leaderboards: dict,
) -> dict:
    users = get_existing_users()

    for user_name in users:
        user_filename = os.path.join(
            USER_FILES_FOLDER,
            user_name + "_multiplayer.json",
        )

        user_file = multiplayer_filehandler.load_file(
            user_filename
        )

        for record_version in global_leaderboards:
            for record_type in global_leaderboards[
                record_version
            ]:
                for game_mode in global_leaderboards[
                    record_version
                ][record_type]:
                    record = user_file[
                        "personal_records"
                    ][record_version][record_type][game_mode]

                    if record is not None:
                        global_leaderboards[
                            record_version
                        ][record_type][game_mode].append(
                            record
                        )

    return global_leaderboards


def _get_global_records_structure() -> dict:
    record_versions = [
        "normal",
        "ironman",
    ]

    record_types = [
        "least_attempts",
        "fastest",
    ]

    game_modes = _get_categories()

    global_leaderboards = {}

    for record_version in record_versions:
        global_leaderboards[record_version] = {}

        for record_type in record_types:
            global_leaderboards[
                record_version
            ][record_type] = {}

            for game_mode in game_modes:
                global_leaderboards[
                    record_version
                ][record_type][game_mode] = []

    return global_leaderboards


def get_global_leaderboard() -> dict:
    global_leaderboards = (
        _get_global_records_structure()
    )

    filled_global_leaderboard = (
        _fill_global_records(
            global_leaderboards
        )
    )

    sorted_global_leaderboard = (
        _sort_global_leaderboards(
            filled_global_leaderboard
        )
    )

    return sorted_global_leaderboard

# For development only:
def _random_run_generator(user_name) -> tuple[
    tuple[str, str, str, str, int, int, int],
    str,
]:
    """Return randomly generated run data for the given user."""

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
    title = random.choice(titles)

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
        title,
        timestamp_start.isoformat(timespec="seconds"),
        timestamp_end.isoformat(timespec="seconds"),
        tries,
        wrong_answers,
        help_needed,
    ), user_name


if __name__ == "__main__":
    user_name = "Debugging"
    init_user(user_name)
    save_game, user_name = _random_run_generator(user_name)
    save_run(save_game, user_name)
    print_all_global_leaderboards()


    # users = ["Dani", "Toby", "Duclos", "Jan", "Vincent"]
    #
    # for user_name in users:
    #     init_user(user_name)
    #
    #     for _ in range(10):
    #         save_game, user_name = _random_run_generator(user_name)
    #         save_run(save_game, user_name)
