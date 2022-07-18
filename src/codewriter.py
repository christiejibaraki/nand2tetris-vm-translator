"""
The CodeWriter module
"""
from src.utility import write_file

SEGMENT_DICT = {
    "local": "LCL",
    "argument":"ARG",
    "this": "THIS",
    "that": "THAT"}


class CodeWriter:
    """
    Translate VM commands into Hack assembly code
    """
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.output_file = None
        self.output = ""
        self.counter = 0

    def __set_output_file(self):
        self.output_file

    def write_file(self):
        write_file(self.output_file, self.output)

    def write_arithmetic(self, command):
        """
        Translate arithmetic command and add it to self.output
        Increment counter if necessary
        :param command: (str) arithmetic or boolean command
        :return: NA, update self.output
        """
        if command == "add":
            self.output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
        elif command == "sub":
            self.output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
        elif command == "and":
            self.ouput += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n"
        elif command == "or":
            self.output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n"
        elif command == "neg":
            self.output += "@SP\nA=M-1\nM=-M\n"
        elif command == "not":
            self.output += "@SP\nA=M-1\nM=!M\n"
        elif command == "gt":
            self.output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_GT_{self.counter}\nD;JGT\n@SP\nA=M-1\nM=0\n(CONTINUE_GT_{self.counter})\n"
            self.counter += 1
        elif command == "lt":
            self.output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_LT{self.counter}\nD;JLT\n@SP\nA=M-1\nM=0\n(CONTINUE_LT{self.counter})\n"
            self.counter += 1
        elif command == "eq":
            self.output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_EQ_{self.counter}\nD;JEQ\n@SP\nA=M-1\nM=0\n(CONTINUE_EQ_{self.counter})\n"
            self.counter += 1

    def write_push(self, segment, index):
        """
        Translate push command and add it to self.output
        :param segment: (str) segment eg local, argument, this, that, constant, temp, pointer, static
        :param index: (str) number
        :return: NA, updates self.output
        """
        if segment in {"local", "argument", "this", "that"}:
            ram_var = SEGMENT_DICT[segment]
            self.output += f"@{ram_var}\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n"
        elif segment == "constant":
            self.output += f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "temp":
            temp_var = 5 + int(index)
            self.output += f"@{temp_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "pointer":
            pointer_var = "THIS" if index == "0" else "THAT"
            self.output += f"@{pointer_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "static":
            static_var = f"{self.output_folder}Static{index}"
            self.output += f"@{static_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def write_pop(self, segment, index):
        """
        Translate pop command and add it to self.output
        :param segment: (str) segment eg local, argument, this, that, constant, temp, pointer, static
        :param index: (str) number
        :return: NA, updates self.output
        """
        if segment in {"local", "argument", "this", "that"}:
            ram_var = SEGMENT_DICT[segment]
            self.output += f"@{ram_var}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "temp":
            temp_var = 5 + int(index)
            self.output += f"@SP\nAM=M-1\nD=M\n@{temp_var}\nM=D\n"
        elif segment == "pointer":
            pointer_var = "THIS" if index == "0" else "THAT"
            self.output += f"@SP\nAM=M-1\nD=M\n@{pointer_var}\nM=D\n"
        elif segment == "static":
            static_var = f"{self.output_folder}Static{index}"
            self.output += f"@SP\nAM=M-1\nD=M\n@{static_var}\nM=D\n"
