from sys import argv
from app import run

if __name__ == "__main__":
    production = len(argv) > 1 and argv[1] == '--production'
    debug = not production
    run(debug)
