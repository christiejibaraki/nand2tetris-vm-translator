"""
The Parser Module
"""
import os
from utility import read_file, clean_code


class Parser:
    """
    Handles parsing of a single .vm file
    Encapsulates access to the input code
    Reads VM commands, parses them, and provides convenient access to their components.
    Additionally removes all white space and comments
    """
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"

    def __init__(self, input_file):
        self.vm_lang = clean_vm_lang_file(input_file)
        self.commands = self.vm_lang.split("\n")
        self.__current_index = None
        self.__current_command = None
        self.__current_command_type = None
        self.__arg1 = None
        self.__arg2 = None

    def has_more_commands(self):
        """
        Indicates whether there are more commands in the input
        :return: (Boolean)
        """
        return self.__current_index is None or self.__current_index < len(self.commands) - 1

    def advance(self):
        """
        Read next command from input and makes it current command
        :return: NA, updates self.current_command
        """
        if self.__current_index is None:
            self.__current_index = 0
        else:
            if self.__current_index == len(self.commands) - 1:
                raise Exception("No more commands in the input")
            self.__current_index += 1
        self.__current_command = self.commands[self.__current_index]
        self.__update_command_properties()

    def __update_command_properties(self):
        """
        Set current command type
        :return: NA, updates self.__current_command_type
        """
        self.__reset_properties()

        if self.__current_command is None:
            self.__current_command_type = None
        else:
            command_list = parse_command(self.__current_command)
            if len(command_list) == 1:
                if self.__current_command == "return":
                    self.__current_command_type = Parser.C_RETURN
                else:
                    self.__current_command_type = Parser.C_ARITHMETIC
            elif len(command_list) == 2:
                command, self.__arg1 = command_list
                self.__current_command_type = COMMAND_MAP[command]
            else:
                command, self.__arg1, self.__arg2 = command_list
                self.__current_command_type = COMMAND_MAP[command]

    def __reset_properties(self):
        """
        Resent command properties
        :return: NA
        """
        self.__current_command_type = None
        self.__arg1 = None
        self.__arg2 = None

    def get_current_command_type(self):
        """
        Returns current command type of current command
        :return: (String) command type
        """
        return self.__current_command_type

    def get_current_command(self):
        """
        Returns current command
        :return: (str) command
        """
        return self.__current_command

    def get_arg1(self):
        """
        Returns arg1
        "return: (str) arg1
        """
        return self.__arg1

    def get_arg2(self):
        """
        Returns arg2
        "return: (str) arg2
        """
        return self.__arg2


COMMAND_MAP = {
    "push": Parser.C_PUSH,
    "pop": Parser.C_POP,
    "label": Parser.C_LABEL,
    "if-goto": Parser.C_IF,
    "goto": Parser.C_GOTO,
    "function": Parser.C_FUNCTION,
    "call": Parser.C_CALL
}


def parse_command(command):
    """
    Splits command into [command, arg1, arg2]
    where arg1 and arg2 are optional
    :param command: (str) command
    :return: list of str, parsed commands
    """
    return command.split()


def clean_vm_lang_file(input_file_arg):
    """
    Cleans text in file by stripping starting/trailing whitespace and removing comments
    Reads input file, cleans text
    :param input_file_arg: file ending in .vm
    :return: (str) cleaned vm language
    """
    try:
        _, input_filename = os.path.split(os.path.realpath(input_file_arg))
        _, extension = os.path.splitext(input_filename)
        if extension == ".vm":
            clean_string = clean_code(read_file(input_file_arg))
            return clean_string
        print(f"For file {input_filename},expected extension .vm; actual extension: {extension}")
    except FileNotFoundError as e:
        print("Input file not found")
        print(e)
    return None
