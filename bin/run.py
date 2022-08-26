import sys

sys.path.append("./")
import uvicorn

if __name__ == "__main__":
    from bin.env import set_env
    set_env()
    uvicorn.run("src.cosmos.api:api", host="0.0.0.0")