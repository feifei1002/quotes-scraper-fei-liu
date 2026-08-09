import os
from dataclasses import dataclass
from dotenv import load_dotenv

# A small container to store the username and password for the quotes website.
@dataclass
class Credentials:

    username: str
    password: str

def load_credentials() -> Credentials:
    # Read .env file
    load_dotenv()

    # Get the username and password from environment variables
    username = os.getenv("QUOTES_USERNAME")
    password = os.getenv("QUOTES_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing login details. Please set the QUOTES_USERNAME and QUOTES_PASSWORD in your .env file."
        )
    return Credentials(username=username, password=password)