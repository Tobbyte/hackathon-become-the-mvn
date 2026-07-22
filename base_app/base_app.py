"""Main Brain of the Game.

#show_start_screen() -> None
    #show_menu() -> None
    #wiki_response = call_wiki_api(thema:str)->str
    #wiki_response_parsed = parse_api_response(wiki_response:str)->dict
    #append_conversation_history()->None # as dictionary
    #persona = construct_persona()->str
    #llm_response = call_llm(wiki_response_parsed, persona) #Response ohne Bezug auf das Thema
    #append_conversation_history()->None # as dictionary
    #While-Loop bis der User richtig erraten oder sein Leben verbraucht hat
        #user_input = take_user_response()->str
        #append_conversation_history()->None # as dictionary
        #response = call_llm(user_input)->str # response ist
        #append_conversation_history()->None # as dictionary
    #Endloop
    #show_result(conversation_history)->str#Dany generate ascii code


"""
# TODO:
#   - add animation while waiting for ai response

import sys

from base_app.config import MENU_ITEMS
from base_app.life_loop import interact_with_user
from base_app.player_select import get_user_menu
from i_o.io import (
    clear_screen,
    get_ab_choice,
    get_category_selection,
    get_difficulty_selection,
    get_menu_selection,
    get_user_input,
    output,
    output_howto,
)
from multiplayer.multiplayer import (
    convert_to_vincents_unnice_para_requests,
    get_existing_users,
    init_user,
    save_run,
)
from splash.splash_screen import show_splashscreen
from wiki_calls.wiki import get_random_wikipedia_article_data


def run_game() -> None:
    clear_screen()
    """Start the game."""
    show_splashscreen()

    first_run = True

    while True:
        if not first_run:
            clear_screen()
        first_run = False
        known_users = get_existing_users()
        user_name = get_user_menu(known_users)
        if not user_name:
            _quit_program()
        else:
            init_user(user_name)

        output(
            f"~~~~~~~~~~\nHallo {user_name}!\n~~~~~~~~~~\n",
            rainbow=True,
        )
        play_again = True
        while play_again:
            selection = get_menu_selection()
            if not selection:
                _quit_program()

            else:
                clear_screen()
                output(
                    f"~~~~~~~~~~\nSelected menu item: "
                    f"{MENU_ITEMS[selection - 1][0]}\n"
                    "~~~~~~~~~~\n",
                    rainbow=True,
                )

                wiki_content, modus = get_dispatch_menu()[selection]()

                if not wiki_content:
                    continue

                # print(
                #     f"\ndev: playing with wiki content:\n{wiki_content['header']}",
                # )
                print(
                    "\ndev: get inital clou demo: ~this will take a while, wait~",
                )

                game_statistics = interact_with_user(wiki_content)
                # for dev w/o llm use:
                # game_statistics = {
                #     "modus": "full_random",
                #     "title": "Seven Samurai",
                #     "timestamp_start": "2026-07-22T16:15:44+02:00",
                #     "timestamp_end": "2026-07-22T16:15:51+02:00",
                #     "tries": 0,
                #     "wrong_answers": 0,
                #     "help_needed": 0,
                #     "exit": True or False
                # }

                game_statistics["modus"] = modus

                output("Round finished!")
                is_exit = game_statistics["exit"]
                game_statistics = convert_to_vincents_unnice_para_requests(
                    game_statistics,
                )
                assert user_name  # noqa: S101

                if not is_exit:
                    save_run(game_statistics, user_name)

                play_again = get_ab_choice(
                    "play again? (y)es or (n)o: ",
                    ["y", "Y"],
                    ["n", "N"],
                )
        _quit_program()


def _idle_after_input() -> None:
    """Idle with prompt to continue."""
    get_user_input("\npress Enter to continue ")


def get_dispatch_menu() -> dict:
    return {
        1: show_howto,
        2: play_with_random_category,
        3: play_with_category,
        4: play_by_difficulty,
        5: show_scoreboard,
        0: _quit_program,
    }


def show_howto():
    output_howto()
    _idle_after_input()
    return None, None


def show_scoreboard():
    # scoreboar_data =    <<< Vincent hier von multiplayer daten holen
    print_scoreboard()
    _idle_after_input()
    return None, None


def print_scoreboard(scoreboard_data: dict = {}) -> None:
    output("Hier könnte ihr scoreboard stehen")
    for k, v in scoreboard_data.items():
        output(f"{k}: {v}")


def play_with_random_category():
    # return ("get_random_wikipedia_article_data()", "full_random")
    return (get_random_wikipedia_article_data(), "full_random")


def play_with_category():
    choosen_topic = get_category_selection()
    output(
        f"\n~~~~~~~~~~\nSelected category: {choosen_topic}\n~~~~~~~~~~\n",
        rainbow=True,
    )
    if choosen_topic is not None:
        # return ("get_random_wikipedia_article_data(choosen_topic)", "category")
        return (get_random_wikipedia_article_data(choosen_topic), "category")
    return None, None


def play_by_difficulty():
    choosen_difficulty = get_difficulty_selection()
    if choosen_difficulty is not None:
        output(
            f"\n~~~~~~~~~~\nSelected difficulty: {choosen_difficulty}\n~~~~~~~~~~\n",
            rainbow=True,
        )
        # return (
        #     "get_random_wikipedia_article_data(user_difficulty=choosen_difficulty)",
        #     "top_" + choosen_difficulty,
        # )
        return (
            get_random_wikipedia_article_data(
                user_difficulty=choosen_difficulty,
            ),
            "top_" + choosen_difficulty,
        )
    return None, None


def dummy() -> None:
    print("dev: I'm a dummy menu item dispatch function")


def _quit_program() -> None:
    """Quit with farewell."""
    output("Bye!")
    sys.exit()
