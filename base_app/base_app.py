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
from i_o.io import (
    clear_screen,
    get_category_selection,
    get_difficulty_selection,
    get_menu_selection,
    get_user_input,
    output,
    output_howto,
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

            wiki_content = get_dispatch_menu()[selection]()

            if not wiki_content:
                continue

            print(
                f"\ndev: playing with wiki content:\n{wiki_content['header']}",
            )
            print(
                "\ndev: get inital clou demo: ~this will take a while, wait~",
            )
            print(
                f"dev: wiki by choosen_topic:\n{wiki_content['header']}",
            )

            game_statistics = interact_with_user(wiki_content)
            print("Round finished!")
            print(game_statistics)


def _idle_after_input() -> None:
    """Idle with prompt to continue."""
    get_user_input("\npress Enter to continue ")


def get_dispatch_menu() -> dict:
    return {
        1: show_howto,
        2: play_with_random_category,
        3: play_with_category,
        4: play_by_difficulty,
        0: _quit_program,
    }


def show_howto():
    output_howto()
    _idle_after_input()


def play_with_random_category():
    return get_random_wikipedia_article_data()


def play_with_category():
    choosen_topic = get_category_selection()
    output(
        f"\n~~~~~~~~~~\nSelected category: {choosen_topic}\n~~~~~~~~~~\n",
        rainbow=True,
    )
    if choosen_topic is not None:
        return get_random_wikipedia_article_data(choosen_topic)
    return None


def play_by_difficulty():
    choosen_difficulty = get_difficulty_selection()
    if choosen_difficulty is not None:
        output(
            f"\n~~~~~~~~~~\nSelected difficulty: "
            f"{choosen_difficulty}\n"
            "~~~~~~~~~~\n",
            rainbow=True,
        )
        return get_random_wikipedia_article_data(
            user_difficulty=choosen_difficulty,
        )
    return None


def dummy() -> None:
    print("dev: I'm a dummy menu item dispatch function")


def _quit_program() -> None:
    """Quit with farewell."""
    output("Bye!")
    sys.exit()
