from base_app.config import PLAYER_MENU_ITEMS, USER_TYPE_MENU_ITEMS
from i_o.io import get_menu_selection_multi, get_user_input, output


def _get_player_selection() -> str | None:
    sel = get_menu_selection_multi(
        ("wähle spielart", PLAYER_MENU_ITEMS),
        "Or press ENTER again quit.",
    )
    if sel is not None:
        return sel[1]
    return None


def _get_user_type_selection() -> str | None:
    sel = get_menu_selection_multi(
        ("Benutzer", USER_TYPE_MENU_ITEMS),
        "Or press ENTER again to return",
    )
    if sel is not None:
        return sel[1]
    return None


def _get_existing_user_selection(user_list: list[str]) -> str | None:
    if not user_list:
        output("Keine bestehenden User gefunden.", rainbow=True)
        return None

    menu_items = [[name] for name in user_list]
    sel = get_menu_selection_multi(
        ("bekannte user: ", menu_items),
        "Or press ENTER again to return",
    )
    if sel is not None:
        return sel[0]
    return None


def _get_new_username(known_users: list) -> str | None:
    username = get_user_input("\nUsername eingeben: ").strip()
    if username == "":
        output("username cant be empty")
        return _get_new_username(known_users)
    if username in known_users:
        output("username already exists")
        return _get_new_username(known_users)

    return username


def get_user_menu(
    user_list: list,
) -> str | None:
    """Choose user name from existing, new or anonym.

    Returns username as string.
    """
    player_choice = _get_player_selection()
    if player_choice is None:
        return None
    if player_choice == "anonym":
        return "anonym"

    user_type = _get_user_type_selection()
    if user_type is None:
        return get_user_menu(user_list)

    if user_type == "existing":
        if user_type is None:
            return get_user_menu(user_list)
        existing_user_name = _get_existing_user_selection(user_list)
        if existing_user_name is None:
            return get_user_menu(user_list)
        return existing_user_name

    if user_type == "new":
        return _get_new_username(user_list)

    return None
