from sys import argv
from app import run

if __name__ == "__main__":
    debug = len(argv) > 1 and argv[1] == 'debug'
    run(debug)
