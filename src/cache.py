from pathlib import Path

CACHE_PATH = Path().home() / ".slack_cli"
MESSAGES_CACHE_PATH = CACHE_PATH / "messages"
TOKEN_PATH_CACHE = CACHE_PATH / ".token_path"
