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

from ai.ai import get_initial_clou
from i_o.io import get_user_input, output, show_menu


def run_game() -> None:
    """Start the game."""
    print("dev: running")
    show_start_screen()
    _ = show_menu()  # not used
    choosen_topic = get_user_input("What topic?")
    print(f"dev: user choose {choosen_topic}")
    print(get_initial_clou())


def show_start_screen() -> None:
    """Print a welcome screen."""
    output("Welcome Screen\n~~Hello User~~")
