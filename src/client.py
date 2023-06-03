from datetime import datetime
from pathlib import Path

from simple_term_menu import TerminalMenu

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


USER_TOKEN_PATH = Path(__file__).parents[1] / ".token"


def main():
    client = WebClient(token=USER_TOKEN_PATH.read_text())
    conversations = client.conversations_list(types=['public_channel']).get("channels", [])  # ['public_channel', 'private_channel', 'mpim', 'im'] 
    name_id_mapping = {c.get("name"): c.get("id") for c in conversations}

    main_menu = TerminalMenu(
        name_id_mapping, 
        preview_command=build_preview_command(client, name_id_mapping),
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


def build_preview_command(client, mapping):
    def get_conversation_messages(conversation_name, limit=10):
        conversation_id = mapping[conversation_name]
        try:
            response = client.conversations_history(channel=conversation_id, limit=limit)
            return "\n".join(reversed([f"{datetime.fromtimestamp(float(m['ts']))} - @{m['user']}: {m['text']}" for m in response.get("messages")]))

        except SlackApiError as e:
            print(f"Error: {e}")

    return get_conversation_messages


def get_conversation_messages(client, conversation_id, limit=10):
    try:
        response = client.conversations_history(channel=conversation_id, limit=limit)
        return "\n".join(reversed([f"{m['ts']} - @{m['user']}: {m['text']}" for m in response.get("messages")]))

    except SlackApiError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
