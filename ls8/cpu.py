"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0b0] * 256
        self.reg[7] = 0xF4
        self.sp = self.reg[7]

    def load(self):
        """Load a program into memory."""

        address = 0
        

        #for instruction in program:
        #    self.ram[address] = instruction
        #    address += 1
        
        #Un-hardcode
        
        with open(sys.argv[1]) as f:
            address = 0
            for line in f:
                value = line.split("#")[0].strip()
                if value == '':
                    continue
                v = int(value, 2)
                self.ram[address] = v
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # Our instruction register set to ram indexed at program counter 
            self.ir = self.ram[self.pc]

            # HALT command
            if self.ir == 0b00000001:
                running = False

            # LDI, or Load Immediate; set specified register to specific value
            elif self.ir == 0b10000010:
                operand_a = self.ram[self.pc + 1] # Our register of interest
                operand_b = self.ram[self.pc + 2] # Value for that register

                self.reg[operand_a] = operand_b
                # Increment program counter by 3 steps in RAM
                self.pc += 3

            # PRN, or Print; printing value at given register
            elif self.ir == 0b01000111:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2

            # MULT, or Multiply; multiply values inside 2 registers provided
            elif self.ir == 0b10100010:    
                operand_a = self.ram[self.pc + 1] # register 1
                operand_b = self.ram[self.pc + 2] # register 2
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # If instruction unknown, print location for bug fixing
            else:
                print(f"Unknown instruction {self.ir} at address {self.pc}")
                sys.exit(1)