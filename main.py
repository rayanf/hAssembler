from ast import operator
import re

from pickle_mixin import test


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
            {'name':'neg','operands':1,'opcode':0b111101,'rcode':0b011},
            {'name':'imul','operands':1,'opcode':0b111101,'rcode':0b101},
            {'name':'idiv','operands':1,'opcode':0b111101,'rcode':0b111},
            {'name':'inc','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'dec','operands':1,'opcode':0b111111,'rcode':0b001},
            {'name':'push','operands':1,'opcode':0b0101,'rcode':0b110},
            {'name':'pop','operands':1,'opcode':0b0101,'rcode':0b000},
            {'name':'call','operands':1,'opcode':0b111111,'rcode':0b010},
            {'name':'ret','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'ret','operands':0, 'opcode':0b11000011},
            {'name':'jmp','operands':1,'opcode':0b111111,'rcode':0b100},
            {'name':'xor','operands':2},
            {'name':'or','operands':2},
            {'name':'and','operands':2},
            {'name':'not','operands':1,'opcode':0b111101,'rcode':0b010},
            {'name':'shl','operands':2},
            {'name':'shr','operands':2},
            {'name':'cmp','operands':2},
            {'name':'test','operands':2},
            {'name':'xchg','operands':2},
            {'name':'xadd','operands':2},
            {'name':'std','operands':0,'opcode':0b11111101},
            {'name':'stc','operands':0,'opcode':0b11111001},
            {'name':'clc','operands':0,'opcode':0b11111000},
            {'name':'cld','operands':0,'opcode':0b11111100},
            {'name':'jcc','operands':1},
            {'name':'syscall','operands':0,'opcode':0b0000111100000101},
        ]


memory_size = {'BYTE':8,'WORD':16,'DWORD':32,'QWORD':64}

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
        
        self.RegAddrMod = 0
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
    def get_operator(self):
        opt = self.nasm[0]
        for opterator in operators:
            if opt == opterator['name'] and len(self.instructions.operands) == opterator['operands']:
                return opterator
    def get_operands(self):
        operands = []
        self.nasm = [x for x in self.nasm if x != '']
        
        for operand in self.nasm[1:]:
            if operand == 'BYTE' or operand == 'WORD' or operand == 'DWORD' or operand == 'QWORD':
                size = memory_size[operand]
                continue

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

                operands.append({'type':'mem','data':{'base':base,'index':index,'scale':scale,'disp':disp},'size':size})

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

    def set_size(self,size,address):
        if address:
            if size == 32:
                self.instructions.prefix.append(0x67)
        else:
            if size == 8:
                self.instructions.w = 0b0
            elif size == 16:
                self.instructions.w = 0b1
                self.instructions.prefix.append(0x66)
            elif size == 32:
                self.instructions.w = 0b1
            elif size == 64:
                self.instructions.w = 0b1
                self.instructions.rex = 0b0100
                self.instructions.rex_w = 0b1
    def bit_len(self,num):
        if -2**7 <= num < 2**7:
           return 8
        elif (-2**31 <= num < 2**31):
            return 32
        elif -2**63 <= num < 2**63:
            return 64

    def setDisp(self, val, size):
        self.instructions.disp = [0x00] * (size // 8)
        for i in range(len(self.instructions.disp)):
            self.instruction.disp[i] = val & 0xFF
            val >>= 8

    def process_None_operand(self):
        self.opcode = self.instructions.operator['opcode']
        print(str(hex(self.opcode)[2:]))

        return self.opcode
        
    def process_Unary_operand(self):
        if self.instructions.operands[0]['type'] == 'reg':
            self.instructions.opcode = self.instructions.operator['opcode']
            self.instructions.d = 1
            self.set_size(self.instructions.operands[0]['data']['size'],False)
            if self.instructions.rex == 0:
                self.instructions.mod = 0b11
                self.instructions.reg = self.instructions.operator['rcode']
                self.instructions.rm = self.instructions.operands[0]['data']['code']
                if len(self.instructions.prefix) == 0:
                    self.instructions.prefix.append(0x0)
                result = (self.instructions.prefix[0] << 16) + (self.instructions.opcode << 10) + (self.instructions.w << 9) + (self.instructions.d << 8) + (self.instructions.mod << 6) + (self.instructions.reg << 3) + self.instructions.rm
                print(str(hex(result))[2:])
                # print(self.instructions.opcode)
                # print(self.instructions.w)
                # print(self.instructions.d)
                # print(self.instructions.mod)
                # print(self.instructions.reg)
                # print(self.instructions.rm)
            else:
                if self.instructions.operator['name'] == 'push':
                    if self.instructions.operands[0]['data']['code']/8 == 0:
                        self.instructions.rex_b = 0b0
                        self.instructions.rex_r = 0b0
                        self.instructions.rex_x = 0b0
                        self.instructions.rex_w = 0b0
                        self.instructions.rex = 0
                    self.instructions.rm = self.instructions.operands[0]['data']['code']%8
                    self.instructions.rex_b = self.instructions.operands[0]['data']['code']/8
                    result = self.instructions.rm + (self.instructions.opcode << 4) + (int(self.instructions.rex_b) << 8) + (self.instructions.rex_x << 9) + (self.instructions.rex_r << 10) + (self.instructions.rex_w << 11) + (self.instructions.rex << 12)
                    print(str(hex(result))[2:])
                
                elif self.instructions.operator['name'] == 'pop':
                    if self.instructions.operands[0]['data']['code']/8 == 0:
                        self.instructions.rex_b = 0b0
                        self.instructions.rex_r = 0b0
                        self.instructions.rex_x = 0b0
                        self.instructions.rex_w = 0b0
                        self.instructions.rex = 0
                    self.instructions.rm = self.instructions.operands[0]['data']['code']%8
                    self.instructions.rex_b = self.instructions.operands[0]['data']['code']/8
                    result = self.instructions.rm + (self.instructions.opcode << 4) + (int(self.instructions.rex_b) << 8) + (self.instructions.rex_x << 9) + (self.instructions.rex_r << 10) + (self.instructions.rex_w << 11) + (self.instructions.rex << 12) + (1 << 3)
                    print(str(hex(result))[2:])

                elif self.instructions.operator['name'] == 'jmp':
                    self.instructions.mod = 0b11
                    self.instructions.reg = self.instructions.operator['rcode']
                    self.instructions.rm = self.instructions.operands[0]['data']['code']%8
                    self.instructions.rex_b = self.instructions.operands[0]['data']['code']/8
                    prefix_len = len(self.instructions.prefix)
                    if len(self.instructions.prefix) == 0:
                        self.instructions.prefix.append(0x0)
                    result = (self.instructions.prefix[0] << 16) + (self.instructions.opcode << 10) + (self.instructions.w << 9) + (self.instructions.d << 8) + (self.instructions.mod << 6) + (self.instructions.reg << 3) + int(self.instructions.rm)
                    result = int(result)
                    print(str(hex(result))[2:])

                elif self.instructions.operator['name'] == 'call':
                    self.instructions.mod = 0b11
                    self.instructions.reg = self.instructions.operator['rcode']
                    self.instructions.rm = self.instructions.operands[0]['data']['code']%8
                    self.instructions.rex_b = self.instructions.operands[0]['data']['code']/8
                    prefix_len = len(self.instructions.prefix)
                    if len(self.instructions.prefix) == 0:
                        self.instructions.prefix.append(0x0)
                    result = (self.instructions.prefix[0] << 16) + (self.instructions.opcode << 10) + (self.instructions.w << 9) + (self.instructions.d << 8) + (self.instructions.mod << 6) + (self.instructions.reg << 3) + int(self.instructions.rm)
                    result = int(result)
                    print(str(hex(result))[2:])
                else:
                    self.instructions.mod = 0b11
                    self.instructions.reg = self.instructions.operator['rcode']
                    self.instructions.rm = self.instructions.operands[0]['data']['code']%8
                    self.instructions.rex_b = self.instructions.operands[0]['data']['code']/8
                    prefix_len = len(self.instructions.prefix)
                    if len(self.instructions.prefix) == 0:
                        self.instructions.prefix.append(0x0)
                    result = (self.instructions.rex << (20+prefix_len*8))+(self.instructions.rex_w << (19+prefix_len*8))+(self.instructions.rex_r << (18+prefix_len*8))+(self.instructions.rex_x << (17+prefix_len*8))+(int(self.instructions.rex_b) << (16+prefix_len*8))+(self.instructions.prefix[0] << 16) + (self.instructions.opcode << 10) + (self.instructions.w << 9) + (self.instructions.d << 8) + (self.instructions.mod << 6) + (self.instructions.reg << 3) + int(self.instructions.rm)
                    result = int(result)
                    print(str(hex(result))[2:])
        elif self.instructions.operands[0]['type'] == 'mem':
            self.instructions.opcode = self.instructions.operator['opcode']
            self.instructions.reg = self.instructions.operator['rcode']
            self.instructions.r = 1
            self.instructions.disp == self.instructions.operands[0]['data']['disp']
            self.instructions.base = self.instructions.operands[0]['data']['base']
            self.instructions.index = self.instructions.operands[0]['data']['index']
            self.instructions.scale = self.instructions.operands[0]['data']['scale']

            if (self.instructions.disp == 0) and (self.instructions.base == {} or self.instructions.base['code']&0b111 != 0b101):
                self.instructions.mod = 0b00
            elif self.bit_len(self.instructions.disp) == 8:
                self.instructions.mod = 0b01
                self.instructions.disp = self.setDisp(self.instructions.disp,self.bit_len(self.instructions.disp))
            elif self.bit_len(self.instructions.disp) == 32:
                self.instructions.mod = 0b10
                self.instructions.disp = self.setDisp(self.instructions.disp,self.bit_len(self.instructions.disp))

            if self.instructions.index == {} and self.instructions.base != {} and self.instructions.base['code'] & 0b111 == 0b100:
                fake = True
                self.instructions.index = self.instructions.base.copy()
                self.instructions.index['code'] &= 0b111
                self.self.instructions.rm = self.instructionsv.base['code']
                self.self.instructions.set_ize(self.instructions.base['size'], True)


            if  self.instructions.index != {} and self.instructions.base != {} and self.instructions.base['code'] & 0b111 == 0b101:
                fake = True
                self.self.instructions.set_size(self.instructions.base['size'], True)

            if self.instructions.index != {} and self.instructions.base == {}:
                fake = True
                self.instructions.mod = 0b00
                self.instructions.base = self.get_register('ebp')
                self.setDisp(self.instructionsdisp, 32)
                self.set_size(self.instructions.index['size'], True)
            # direct addressing [disp]
            elif self.instructions.index == {} and self.instructions.base == {}:
                fake = True
                self.instructions.mod = 0b00
                self.instructions.base = self.get_register('ebp')
                self.instructions.index = self.get_register('esp')
                self.instructions.scale = 1
                self.setDisp(self.instructions.disp, 32)


            # register addressing [base]
            if self.instructions.index == {} and self.instructions.base != {}:
                self.instructions.rm = self.instructions.base['code']
                self.set_size(self.instructions.base['size'], True)
            # complete addresing [base + scale * index + disp]
            elif self.instructions.index != {} and self.instructions.base != {}:
                self.instructions.rm = 0b100
                self.instructions.sib = True
                if self.instructions.scale == 1:
                    self.instructions.scale = 0b00
                elif self.instructions.scale == 2:
                    self.instructions.scale = 0b01
                elif self.instructions.scale == 4:
                    self.instructions.scale = 0b10
                elif self.instructions.scale == 8:
                    self.instructions.scale = 0b11
                self.instructions.index = self.instructions.index['code']
                self.instructions.base = self.instructions.base['code']
                if not fake:
                    self.set_size(self.instructions.base['size'], True)
            
        elif self.instructions.operands[0]['type'] == 'imd':
            pass

    
    def process_Binary_operand(self):
        pass


    def process(self,nasm):
        self.nasm = re.split(',| |PTR',nasm)
        # print(self.nasm)
        self.instructions = Instruction()
        self.instructions.operands = self.get_operands()
        self.instructions.operator = self.get_operator() 

        print(self.instructions.operands)
        # print(self.instructions.operator)

        if self.instructions.operator['operands'] == 0:   
            self.process_None_operand()
            

        elif self.instructions.operator['operands'] == 1:
            self.process_Unary_operand()
            

        elif self.instructions.operator['operands'] == 2:
            self.process_Binary_operand()
        
if __name__ == '__main__':
    test1 = ['mov rax,rbx',
            'add rax,3',
            'sub rax,[123]',
            'mul rax,[rax+12]',
            'add rax,[rax+rbx*4+12]'
            'not rax',]
    test2 = ['syscall','cld','stc','clc','std']
    test3 = ['ret','ret 16']
    test4 = ['dec eax','inc ebx','dec rax','inc rax']
    
    test5 = ['dec rax',
            'inc rax',
            'push rax',
            'pop rax',
            'call rax',
            'jmp rax',
            'not rax',
            'neg rax',
            'idiv rbx',
            'imul rbx']
    test6 = ['inc WORD PTR [rax]',
            'add rax,WORD PTR [rax]',]

    for t in test6:
        print('{}: '.format(t))
        assembler = Assembler()
        # nasm = input()
        nasm = t
        assembler.process(nasm)
        del assembler

# print(str(hex(0b010)))
