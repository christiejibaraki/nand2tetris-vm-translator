import sys
import os
from parser import Parser

if __name__ == "__main__":
    user_file_input = sys.argv[1]
    try:
        path, input_filename = os.path.split(os.path.realpath(user_file_input))
        print(path)
        _, extension = os.path.splitext(input_filename)
        print(f"*** Translating {input_filename}")
        parser = Parser(user_file_input )
        out_filename = input_filename.split(".vm")[0] + ".asm"
        out_file_path = os.path.join(path, out_filename)
        # write_file(out_file_path, binary_codes[0:-1])  # since last char is newline
        print(f"*** Writing output file {out_filename} to {path}")
    except FileNotFoundError as e:
        print("Input file not found")
        print(e)