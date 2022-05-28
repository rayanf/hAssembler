from ast import operator
import re


registers = [ 
    {'name':'rax','size':64,'code':0b000},
    {'name':'rbx','size':64,'code':0b011},
    {'name':'rcx','size':64,'code':0b001},
    {'name':'rdx','size':64,'code':0b010},
    {'name':'rsp','size':64,'code':0b100},
    {'name':'rsi','size':64,'code':0b110},
    {'name':'rdi','size':64,'code':0b111},
    {'name':'rbp','size':64,'code':0b101},
    {'name':'r8','size':64,'code':0b1000},
    {'name':'r9','size':64,'code':0b1001},
    {'name':'r10','size':64,'code':0b1010},
    {'name':'r11','size':64,'code':0b1011},
    {'name':'r12','size':64,'code':0b1100},
    {'name':'r13','size':64,'code':0b1101},
    {'name':'r14','size':64,'code':0b1110},
    {'name':'r15','size':64,'code':0b1111},

    {'name':'eax','size':32,'code':0b000},
    {'name':'ebx','size':32,'code':0b011},
    {'name':'ecx','size':32,'code':0b001},
    {'name':'edx','size':32,'code':0b010},
    {'name':'esp','size':32,'code':0b100},
    {'name':'esi','size':32,'code':0b110},
    {'name':'edi','size':32,'code':0b111},
    {'name':'ebp','size':32,'code':0b101},
    {'name':'r8d','size':32,'code':0b1000},
    {'name':'r9d','size':32,'code':0b1001},
    {'name':'r10d','size':32,'code':0b1010},
    {'name':'r11d','size':32,'code':0b1011},
    {'name':'r12d','size':32,'code':0b1100},
    {'name':'r13d','size':32,'code':0b1101},
    {'name':'r14d','size':32,'code':0b1110},
    {'name':'r15d','size':32,'code':0b1111},

    {'name':'ax','size':16,'code':0b000},
    {'name':'bx','size':16,'code':0b011},
    {'name':'cx','size':16,'code':0b001},
    {'name':'dx','size':16,'code':0b010},
    {'name':'sp','size':16,'code':0b100},
    {'name':'si','size':16,'code':0b110},
    {'name':'di','size':16,'code':0b111},
    {'name':'bp','size':16,'code':0b101},
    {'name':'r8w','size':16,'code':0b1000},
    {'name':'r9w','size':16,'code':0b1001},
    {'name':'r10w','size':16,'code':0b1010},
    {'name':'r11w','size':16,'code':0b1011},
    {'name':'r12w','size':16,'code':0b1100},
    {'name':'r13w','size':16,'code':0b1101},
    {'name':'r14w','size':16,'code':0b1110},
    {'name':'r15w','size':16,'code':0b1111},

    {'name':'al','size':8,'code':0b000},
    {'name':'bl','size':8,'code':0b011},
    {'name':'cl','size':8,'code':0b001},
    {'name':'dl','size':8,'code':0b010},
    {'name':'ah','size':8,'code':0b100},
    {'name':'bh','size':8,'code':0b111},
    {'name':'ch','size':8,'code':0b101},
    {'name':'dh','size':8,'code':0b110},
    {'name':'r8b','size':8,'code':0b1000},
    {'name':'r9b','size':8,'code':0b1001},
    {'name':'r10b','size':8,'code':0b1010},
    {'name':'r11b','size':8,'code':0b1011},
    {'name':'r12b','size':8,'code':0b1100},
    {'name':'r13b','size':8,'code':0b1101},
    {'name':'r14b','size':8,'code':0b1110},
    {'name':'r15b','size':8,'code':0b1111},
]
operators = [
            {'name':'mov','operands':2},
            {'name':'add','operands':2},
            {'name':'adc','operands':2},
            {'name':'sub','operands':2},
            {'name':'sbb','operands':2},
            {'name':'neg','operands':1},
            {'name':'mul','operands':2},
            {'name':'imul','operands':2},
            {'name':'div','operands':2},
            {'name':'idiv','operands':2},
            {'name':'inc','operands':1},
            {'name':'dec','operands':1},
            {'name':'push','operands':1},
            {'name':'pop','operands':1},
            {'name':'call','operands':1},
            {'name':'ret','operands':0},
            {'name':'jmp','operands':1},
            {'name':'xor','operands':2},
            {'name':'or','operands':2},
            {'name':'and','operands':2},
            {'name':'not','operands':1},
            {'name':'shl','operands':2},
            {'name':'shr','operands':2},
            {'name':'cmp','operands':2},
            {'name':'test','operands':2},
            {'name':'xchg','operands':2},
            {'name':'xadd','operands':2},
            {'name':'std','operands':1},
            {'name':'stc','operands':1},
            {'name':'clc','operands':0},
            {'name':'cld','operands':0},
            {'name':'jcc','operands':2},
            {'name':'jecxz','operands':1},
        ]




class Instruction():
    def __init__(self):
        self.operator = {}
        self.operands = []

        self.prefix = []
        
        self.rex = 0        
        self.rex_w = 0b0
        self.rex_r = 0b0
        self.rex_x = 0b0
        self.rex_b = 0b0

        self.opcode = 0b000000
        self.d = 0b0
        self.w = 0b0
        
        self.addrMod = 0
        self.mod = 0b00
        self.reg = 0b000
        self.rm = 0b000
        
        self.sib = 0
        self.scale = 0b00
        self.index = 0b000
        self.base = 0b000

        self.disp = 0

        self.data = 0

    
class Assembler:
    def __init__(self):
        pass
    
    def process(self,nasm):
        self.nasm = re.split(',| ',nasm)
    
        self.instructions = Instruction()
        self.instructions.operator = self.get_operator() 
        self.instructions.operands = self.get_operands()

        print(self.instructions.operands)



    def get_operator(self):
        opt = self.nasm[0]
        for opterator in operators:
            if opt == opterator['name']:
                return opterator
    def get_operands(self):
        operands = []
        for operand in self.nasm[1:]:
            if operand[0] == '[' and operand[-1] == ']':
                memory = True
            else:
                memory = False
            

            if memory:
                operand_splited = operand[1:-1].split('+')
                base = {}
                index = {}
                scale = 0b00
                disp = 0
                for op in operand_splited:
                    if self.check_constant(op):
                        disp += int(op)
                    else:
                        if self.get_register(op) != {}:
                            if base:
                                index = self.get_register(op)
                            else:
                                base = self.get_register(op)

                        else:
                            exp = op.split('*')
                            if len(exp)>0:
                                scale = int(exp[1])
                                index = self.get_register(exp[0])

                operands.append({'type':'mem','data':{'base':base,'index':index,'scale':scale,'disp':disp}})

            else:
                if self.get_register(operand) != {}:
                    operands.append({'type':'reg','data':self.get_register(operand)})

                else:
                    operands.append({'type':'imd','data':int(operand,16)})
        return operands

    def get_register(self,reg):
        for register in registers:
            if reg == register['name']:
                return register
        return {}
    def check_constant(self,constant):
        try:
            int(constant)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    test = ['mov rax,rbx',
            'add rax,3',
            'sub rax,[123]',
            'mul rax,[rax+12]',
            'add rax,[rax+rbx*4+12]',]
    for t in test:
        print('{}: '.format(t))
        assembler = Assembler()
        # nasm = input()
        nasm = t
        assembler.process(nasm)
        del assembler
        print('\n')

