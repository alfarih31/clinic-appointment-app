import uvicorn

from src.shared.providers.env import Env

env = Env()


def start():
    uvicorn.run("src.app:App", host=env.get_str("SERVER_HOST", "0.0.0.0"), port=env.get_int("SERVER_PORT", 8080))


def dev():
    uvicorn.run("src.app:App", reload=True, port=env.get_int("SERVER_PORT", 8080))


if __name__ == "__main__":
    start()
