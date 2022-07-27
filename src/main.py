"""
Main module
Translates .vm files to hack assembly language
"""
import sys
import os
from parser import Parser
from codewriter import CodeWriter
from utility import write_file


def init(prog_name):
    """
    Bootstrapping code to call Sys.init
    :param prog_name: (str) name of directory containing program
    :return: (str) bootstrapping code
    """
    code_writer = CodeWriter(prog_name)
    init_output = "@256\nD=A\n@SP\nM=D\n"
    code_writer.write_call_function("Sys.init", 0)
    init_output += code_writer.get_output()
    return init_output


def translate_file(prog_name, input_file_path):
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
    path = os.path.realpath(dir_input)
    directory_name = os.path.basename(path)
    output = init(directory_name)
    # traverse files in dir
    # if .vm extension, translate file
    for filename in os.listdir(path):
        classname, extension = os.path.splitext(filename)
        if extension == ".vm":
            print(f"*** Translating {filename}")
            output += translate_file(classname, os.path.join(path, filename))
    out_filename = directory_name + ".asm"
    out_file_path = os.path.join(path, out_filename)
    write_file(out_file_path, output)
    print(f"*** Writing output file {out_filename} to {path}")
