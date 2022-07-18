"""
The CodeWriter module
"""

SEGMENT_DICT = {
    "local": "LCL",
    "argument":"ARG",
    "this": "THIS",
    "that": "THAT"}


class CodeWriter:
    """
    Translate VM commands into Hack assembly code
    """
    def __init__(self, prog_name):
        self.__prog_name = prog_name
        self.__output = ""
        self.__counter = 0

    def write_arithmetic(self, command):
        """
        Translate arithmetic command and add it to self.output
        Increment counter if necessary
        :param command: (str) arithmetic or boolean command
        :return: NA, update self.output
        """
        if command == "add":
            self.__output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"
        elif command == "sub":
            self.__output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
        elif command == "and":
            self.__output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n"
        elif command == "or":
            self.__output += "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n"
        elif command == "neg":
            self.__output += "@SP\nA=M-1\nM=-M\n"
        elif command == "not":
            self.__output += "@SP\nA=M-1\nM=!M\n"
        elif command == "gt":
            self.__output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_GT_{self.__counter}\nD;JGT\n@SP\nA=M-1\nM=0\n(CONTINUE_GT_{self.__counter})\n"
            self.__counter += 1
        elif command == "lt":
            self.__output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_LT{self.__counter}\nD;JLT\n@SP\nA=M-1\nM=0\n(CONTINUE_LT{self.__counter})\n"
            self.__counter += 1
        elif command == "eq":
            self.__output += f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE_EQ_{self.__counter}\nD;JEQ\n@SP\nA=M-1\nM=0\n(CONTINUE_EQ_{self.__counter})\n"
            self.__counter += 1

    def write_push(self, segment, index):
        """
        Translate push command and add it to self.output
        :param segment: (str) segment eg local, argument, this, that, constant, temp, pointer, static
        :param index: (str) number
        :return: NA, updates self.output
        """
        if segment in {"local", "argument", "this", "that"}:
            ram_var = SEGMENT_DICT[segment]
            self.__output += f"@{ram_var}\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n"
        elif segment == "constant":
            self.__output += f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "temp":
            temp_var = 5 + int(index)
            self.__output += f"@{temp_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "pointer":
            pointer_var = "THIS" if index == "0" else "THAT"
            self.__output += f"@{pointer_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "static":
            static_var = f"{self.__prog_name}Static{index}"
            self.__output += f"@{static_var}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def write_pop(self, segment, index):
        """
        Translate pop command and add it to self.output
        :param segment: (str) segment eg local, argument, this, that, constant, temp, pointer, static
        :param index: (str) number
        :return: NA, updates self.output
        """
        if segment in {"local", "argument", "this", "that"}:
            ram_var = SEGMENT_DICT[segment]
            self.__output += f"@{ram_var}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "temp":
            temp_var = 5 + int(index)
            self.__output += f"@SP\nAM=M-1\nD=M\n@{temp_var}\nM=D\n"
        elif segment == "pointer":
            pointer_var = "THIS" if index == "0" else "THAT"
            self.__output += f"@SP\nAM=M-1\nD=M\n@{pointer_var}\nM=D\n"
        elif segment == "static":
            static_var = f"{self.__prog_name}Static{index}"
            self.__output += f"@SP\nAM=M-1\nD=M\n@{static_var}\nM=D\n"

    def get_output(self):
        """
        Returns hack assembly language
        :return: (str) translated commands
        """
        return self.__output
