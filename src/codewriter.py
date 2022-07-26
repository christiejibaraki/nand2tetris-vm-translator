"""
The CodeWriter module
"""

SEGMENT_DICT = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"}

CALL_TEMPLATE = "@SP\nAM=M+1\nA=A-1\nM=D\n"
INITIALIZE_LOCAL_VAR_TEMPLATE = "@SP\nAM=M+1\nA=A-1\nM=0\n"


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
            self.__output += (f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n"
                              "@CONTINUE_GT_{self.__counter}\nD;JGT\n@SP\nA=M-1\nM=0\n(CONTINUE_GT_{self.__counter})\n")
            self.__counter += 1
        elif command == "lt":
            self.__output += (f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n"
                              "@CONTINUE_LT{self.__counter}\nD;JLT\n@SP\nA=M-1\nM=0\n(CONTINUE_LT{self.__counter})\n")
            self.__counter += 1
        elif command == "eq":
            self.__output += (f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n"
                              "@CONTINUE_EQ_{self.__counter}\nD;JEQ\n@SP\nA=M-1\nM=0\n(CONTINUE_EQ_{self.__counter})\n")
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
            self.__output += f"@{ram_var}\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
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

    def write_label(self, label):
        """
        Translate label command and add it to self.output
        :param label: (str) label
        :return: NA, updates self.output
        """
        self.__output += f"({label})\n"

    def write_goto(self, label):
        """
        Translate goto command and add it to self.output
        :param label: (str) label
        :return: NA, updates self.output
        """
        self.__output += f"@{label}\n0;JMP\n"

    def write_if(self, label):
        """
        Translate if-goto command and add it to self.output

        This is a conditional jump. Pop topmost element off stack
        if not false (0), jump

        :param label: (str) label
        :return: NA, updates self.output
        """
        self.__output += f"@SP\nAM=M-1\nD=M\n@{label}\nD;JNE\n"

    def write_call_function(self, function_name, nArgs):
        """
        Translate function call and add it to self.output
        :param function_name: (str) name of function
        :param nArgs: (str) number of arguments (already pushed onto the stack)
        :return: NA, updates self.output
        """
        nArgs_int = int(nArgs)
        return_label = f"RETURN_{function_name}_{self.__counter}"
        self.__counter += 1
        self.__output += (f"@{return_label}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n"  # push return address onto stack
                          + self.push_variable("LCL")
                          + self.push_variable("ARG")
                          + self.push_variable("THIS")
                          + self.push_variable("THAT")
                          + f"@SP\nD=M\n@{nArgs_int+5}\nD=D-A\n@ARG\nM=D\n"  # make ARG point to function args
                          + "@SP\nD=M\n@LCL\nM=D\n"  # make LCL point to where SP is pointing
                          + f"@{function_name}\n0;JMP\n"  # goto function
                          + f"({return_label})\n"  # (return address)
                          )

    def write_function_def(self, function_name, nVar):
        """
        Translate function definition and add it to self.output

        :param function_name: (str) name of function
        :param nVar: (str) number of local variables
        :return: NA, updates self.output
        """
        self.__output += f"({function_name})\n"
        nVar_int = int(nVar)
        for _ in range(nVar_int):
            self.__output += INITIALIZE_LOCAL_VAR_TEMPLATE

    def write_return(self):
        """
        Translate return and add it to self.output
        :return: NA, updates self.output
        """
        self.__output += ("@LCL\nD=M\n@FRAME\nM=D\n"  # save LCL in temp variable, FRAME
                          "@FRAME\nD=M\n@5\nA=D-A\nD=M\n@RET\nM=D\n"  # take what's in FRAME-5 and put in RET
                          "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"  # pop off stack and put it where ARG points to
                          "@ARG\nD=M\n@SP\nM=D+1\n"  # restore SP of caller (move SP to ARG+1)
                          "@FRAME\nA=M-1\nD=M\n@THAT\nM=D\n"  # restore THAT of caller
                          "@FRAME\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"  # restore THIS of caller
                          "@FRAME\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n"  # restore ARG of caller
                          "@FRAME\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n"   # restore LCL of caller
                          "@RET\nA=M\n0;JMP\n"  # go to return address (in caller's code)
                          )

    @staticmethod
    def push_variable(variable):
        return f"@{variable}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"

    def get_output(self):
        """
        Returns hack assembly language
        :return: (str) translated commands
        """
        return self.__output
