import sys

sys.path.append("./")
from cosmos.main import run

if __name__ == "__main__":
    from bin.env import set_env

    set_env()
    run()