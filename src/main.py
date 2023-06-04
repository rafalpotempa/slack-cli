from pathlib import Path

from simple_term_menu import TerminalMenu

from slack_sdk import WebClient
from messages import build_get_conversation_messages, post_message

USER_TOKEN_PATH = Path(__file__).parents[1] / ".token"


def main():
    client = WebClient(token=USER_TOKEN_PATH.read_text())
    conversations = client.conversations_list(types=['public_channel']).get("channels", [])  # ['public_channel', 'private_channel', 'mpim', 'im'] 
    name_id_mapping = {c.get("name"): c.get("id") for c in conversations}

    main_menu = TerminalMenu(["conversations", "settings"])
    conversations_menu = TerminalMenu(
        name_id_mapping, 
        preview_command=build_get_conversation_messages(client, name_id_mapping),
        preview_title="messages",
        preview_size=0.5,
    )
    settings_menu = TerminalMenu([])

    exit = False
    while not exit:
        main_select = main_menu.show()
        
        if main_select is None:
            exit = True
        # Conversations
        elif main_select == 0:
            back = False
            while not back:
                select = conversations_menu.show()
                if select is None:
                    back = True
                else:
                    channel_name = list(name_id_mapping.keys())[select]
                    post_message(client, channel_name, name_id_mapping)
        # Settings
        elif main_select == 1:
            back = False
            while not back:
                select = settings_menu.show()
                if select is None:
                    back = True



if __name__ == "__main__":
    main()
