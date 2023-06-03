import os

import dataclasses
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

COLUMN_SEPARATOR = ",,,,,,,"
MESSAGES_CACHE_PATH = Path(__file__).parent / ".cache"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
REFRESH_FREQUENCY_SECONDS = 5


@dataclasses.dataclass
class MessageRow:
    ts: float
    user: str
    text: str

    def __init__(self, ts, user, text):
        self.ts = float(ts)
        self.user = str(user)
        self.text = str(text)

    def __str__(self):
        return f"{datetime.fromtimestamp(float(self.ts)).strftime(TIMESTAMP_FORMAT)} - @{self.user}: {self.text}"

    def to_write(self):
        return COLUMN_SEPARATOR.join([str(s) for s in dataclasses.astuple(self)]) + "\n"

def build_get_conversation_messages(client: WebClient, mapping: Dict):
    def get_conversation_messages(conversation_name: str, limit: int = 10):
        conversation_id = mapping[conversation_name]
        try:
            messages = get_messages_from_cache(conversation_id)

            stale = False
            request_args = {"channel": conversation_id, "limit": limit}
            if messages:
                last_ts = messages[-1].ts
                request_args["oldest"] = last_ts
                time_since_last_refresh = datetime.now() - datetime.fromtimestamp(last_ts)
                stale = time_since_last_refresh.seconds > REFRESH_FREQUENCY_SECONDS

            if stale or len(messages) < limit:
                response_messages = fetch_messages(client, request_args)
                messages += response_messages
                store_messages(conversation_id, response_messages)
            
            return "\n".join([str(m) for m in messages])

        except SlackApiError as e:
            print(f"Error: {e}")

    return get_conversation_messages


def fetch_messages(client: WebClient, args: Dict) -> List[MessageRow]:
    response = client.conversations_history(**args)
    return [MessageRow(float(m['ts']), m['user'], m['text']) for m in reversed(response.get("messages"))]


def get_messages_from_cache(channel_id: str, limit: int = 10) -> List[MessageRow]:
    try:
        with open(MESSAGES_CACHE_PATH / channel_id, 'r') as file:
            return [MessageRow(*line.removesuffix("\n").split(COLUMN_SEPARATOR)) for line in list(file.readlines())[-limit:] if len(line) > 1]
    except FileNotFoundError:
        return []



def store_messages(channel_id: str, messages: List[MessageRow]):
    try:
        os.makedirs(MESSAGES_CACHE_PATH)
    except FileExistsError:
        pass
    with open(MESSAGES_CACHE_PATH / channel_id, 'a') as file:
        file.writelines(m.to_write() for m in messages)
