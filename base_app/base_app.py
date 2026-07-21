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


from ai.ai import get_initial_clou
from i_o.io import clear_screen, get_user_input, output, show_menu
from splash.splash_screen import show_splashscreen


def run_game() -> None:
    clear_screen()
    print("\n\n\n\n")  ## spacer
    """Start the game."""
    print("dev: running")
def _idle_after_input() -> None:
    """Idle with prompt to continue."""
    get_user_input("\npress Enter to continue ")


def get_dispatch_menu() -> dict:
    return {
        1: play_game,
        2: dummy,
        0: _quit_program,
    }


def play_game() -> None:
    print("dev: play_game")
    choosen_topic = get_user_input("What topic?")
    print(f"dev: user choose {choosen_topic}")
    print(get_initial_clou())


def dummy() -> None:
    print("dev: I'm a dummy menu item dispatch function")


def _quit_program() -> None:
    """Quit with farewell."""
    output("Bye!")
    sys.exit()
