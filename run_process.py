import logging
from process import Model
import argparse

def main():
    # Determines which process we're working with - provides identifier for logging & communication
    parser = argparse.ArgumentParser(
                    description = 'Specify the process number it should take')
    parser.add_argument('--p', type=int)
    args = parser.parse_args()

    # int 0, 1, 2
    process = args.p
    if process in [0, 1, 2]:
        # Establishes logging functionality
        logging.basicConfig(filename=f'{process}.log', encoding='utf-8', level=logging.DEBUG, filemode="w")
        
        model = Model(process)
        model.run()
    else:
        print("Must include a tag --p with the process number from 0 to 2")

main()