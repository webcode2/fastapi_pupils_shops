import string
import random
from datetime import datetime
from typing import Dict


def generate_unique_code() -> dict[str, str]:
    today = datetime.today().strftime('%Y-%m-%d')
    base_chars = string.ascii_uppercase + string.digits
    used_codes = set()

    while True:
        code = ''.join(random.sample(base_chars, 4))
        if code not in used_codes and f"{today}-{code}" not in used_codes:
            used_codes.add(f"{today}-{code}")
            print(f"{today}-{code}")
            return {"token": code, "created_at": today}
