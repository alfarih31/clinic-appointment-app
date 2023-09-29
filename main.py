import os

import dotenv
import uvicorn

dotenv.load_dotenv()


def start():
    uvicorn.run("src.app:App", port=int(os.getenv("SERVER_PORT", "8080")))


def dev():
    uvicorn.run("src.app:App", reload=True, port=int(os.getenv("SERVER_PORT", "8080")))


if __name__ == "__main__":
    start()
