
from time import strftime

def gettime() -> str:
    time = strftime("%H %M")
    return time
    
def main() -> str:
    return f"The time is {gettime()}"