from pathlib import Path

from simple_term_menu import TerminalMenu

from slack_sdk import WebClient
from messages import build_get_conversation_messages

USER_TOKEN_PATH = Path(__file__).parents[1] / ".token"


def main():
    client = WebClient(token=USER_TOKEN_PATH.read_text())
    conversations = client.conversations_list(types=['public_channel']).get("channels", [])  # ['public_channel', 'private_channel', 'mpim', 'im'] 
    name_id_mapping = {c.get("name"): c.get("id") for c in conversations}

    main_menu = TerminalMenu(
        name_id_mapping, 
        preview_command=build_get_conversation_messages(client, name_id_mapping),
        preview_title="messages",
        preview_size=0.5,
    )
    main_menu_exit = False

    while not main_menu_exit:
        main_sel = main_menu.show()
        
        if main_sel is not None:
            pass
        else:
            main_menu_exit = True



if __name__ == "__main__":
    main()
