import sys
import os
from parser import Parser
from codewriter import CodeWriter
from utility import write_file


def translate(prog_name, input_file_path):
    """
    Translate VM language file to hack assembly language

    :param prog_name: (str) directory name
    :param input_file_path: (str) path to input file
    :return: (str) hack assembly language
    """
    parser = Parser(input_file_path)
    code_writer = CodeWriter(prog_name)
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.get_current_command_type()
        if command_type == Parser.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.get_current_command())
        elif command_type == Parser.C_PUSH:
            code_writer.write_push(parser.get_arg1(), parser.get_arg2())
        elif command_type == Parser.C_POP:
            code_writer.write_pop(parser.get_arg1(), parser.get_arg2())
        elif command_type == Parser.C_LABEL:
            code_writer.write_label(parser.get_arg1())
        elif command_type == Parser.C_GOTO:
            code_writer.write_goto(parser.get_arg1())
        elif command_type == Parser.C_IF:
            code_writer.write_if(parser.get_arg1())
        elif command_type == Parser.C_RETURN:
            code_writer.write_return()
        elif command_type == Parser.C_FUNCTION:
            code_writer.write_function_def(parser.get_arg1(), parser.get_arg2())
        elif command_type == Parser.C_CALL:
            code_writer.write_call_function(parser.get_arg1(), parser.get_arg2())
    return code_writer.get_output()


if __name__ == "__main__":
    dir_input = sys.argv[1]
    try:
        path = os.path.realpath(dir_input)
        directory_name = os.path.basename(path)
        input_filename = "Sys" + ".vm"
        print(f"*** Translating {input_filename}")
        hack_assembly_lang = translate(directory_name, os.path.join(path, input_filename))
        out_filename = directory_name + ".asm"
        out_file_path = os.path.join(path, out_filename)
        write_file(out_file_path, hack_assembly_lang)
        print(f"*** Writing output file {out_filename} to {path}")
    except FileNotFoundError as e:
        print(f"Input file {input_filename} not found")
        print(e)
