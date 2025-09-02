
from djinn import djinn
from djinn.constants import TOKEN
from loguru import logger

if __name__ == "__main__":
    if TOKEN != None and TOKEN != "":
        logger.success("TOKEN found")
        djinn.run(token=TOKEN)
    else: 
        logger.error("TOKEN not found")
