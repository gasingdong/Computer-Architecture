"""CPU functionality."""

import sys

HALT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
NOP = 0b00000000
MULT = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 64

    def load(self, file):
        """Load a program into memory."""
        address = 0
        program = []

        with open(file) as f:
            for line in f:
                line = line.partition('#')[0]
                line = line.rstrip()
                if line:
                    program.append(int(str.encode(line), 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, num):
        self.ram[index] = num

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def next_instruction(self, opcode):
        return (opcode >> 6 & 0b11) + 1

    def run(self):
        """Run the CPU."""
        running = True
        pc = 0
        while running:
            command = self.ram_read(pc)
            if command == HALT:
                running = False
            elif command == LDI:
                reg_index = self.ram_read(pc + 1)
                num = self.ram_read(pc + 2)
                self.reg[reg_index] = num
            elif command == PRN:
                reg_index = self.ram_read(pc + 1)
                print(self.reg[reg_index])
            elif command == MULT:
                reg_index = self.ram_read(pc + 1)
                multiplier = self.ram_read(pc + 2)
                self.reg[reg_index] = self.reg[reg_index] * \
                    self.reg[multiplier]
            elif command != NOP:
                print(f"Unknown instruction: {command}")
                sys.exit(1)
            pc += self.next_instruction(command)
