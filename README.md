# nand2tetris-vm-translator
VM Translator, Week 5-6, Project 7 & 8.

- Project 7: Stack Arithmetic, Memory Access
- Project 8: Program Flow, Function Calls

The main module runs the VM translator which translates from a virtual machine language to the Hack assembly language.

Input should be a directory containing one more `.vm` files.
The machine code will be written to a file with the same filename as the *directory* and extension `.asm`.

- Input: `<directory>` containing one or more files `<filename>.vm`
- Output: `<directory>/<directory>.asm`

### To run the module:
Specify the location of `main.py` and the input directory, e.g.:

`python3 IbarakiChristieProject7/src/main.py <directory>`

### Known issues:
I pass the tests for Project 8, but

when I translate the Square .vm files (Project 9) and run the resulting .asm file in the CPUEmulator, I get an illegal memory address error (I run out of memory... the SP ends up at 24578), so I wonder if I'm not clearing things off the stack when I return (?). I tried to make sure I understood every line in the worksheet and checked it against my code, but I'm not sure that I understand Square...