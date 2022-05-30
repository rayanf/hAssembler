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
            {'name':'neg','operands':1,'opcode':0b111101,'rcode':0b011},
            {'name':'imul','operands':1,'opcode':0b111101,'rcode':0b101},
            {'name':'imul','operands':2},
            {'name':'idiv','operands':1,'opcode':0b111101,'rcode':0b111},
            {'name':'inc','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'dec','operands':1,'opcode':0b111111,'rcode':0b001},
            {'name':'push','operands':1,'opcode':0b0101,'rcode':0b110},
            {'name':'pop','operands':1,'opcode':0b0101,'rcode':0b000},
            {'name':'call','operands':1,'opcode':0b111111,'rcode':0b010},
            {'name':'ret','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'ret','operands':0, 'opcode':0b11000011},
            {'name':'ret','operands':1,},
            {'name':'jmp','operands':1,'opcode':0b111111,'rcode':0b100},
            {'name':'xor','operands':2},
            {'name':'or','operands':2},
            {'name':'and','operands':2},
            {'name':'not','operands':1,'opcode':0b111101,'rcode':0b010},
            {'name':'shl','operands':2},
            {'name':'shl','operands':1,'opcode':0b110100,'rcode':0b100},
            {'name':'shr','operands':1,'opcode':0b110100,'rcode':0b101},
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
                        disp += int(op,16)
                    else:
                        if self.get_register(op) != {}:
                            if base:
                                index = self.get_register(op)
                            else:
                                base = self.get_register(op)

                        else:
                            exp = op.split('*')
                            # print(exp)
                            if len(exp)>1:
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
            int(constant,16)
            return True
        except ValueError:
            return False

    def set_size(self,operand,address):
        if address == 32:
            if operand == 8:
                self.instructions.w = 0b0
                self.instructions.prefix.append(0x67)

            elif operand == 16:
                self.instructions.prefix.append(0x67)
                self.instructions.w = 0b1

            elif operand == 32:
                self.instructions.prefix.append(0x67)                
                self.instructions.w = 0b1
            elif operand == 64:
                self.instructions.w = 0b1
                self.instructions.rex = 0b0100
                self.instructions.rex_w = 0b1
                self.instructions.prefix.append(0x67)                

        elif address == 64:
            if operand == 8:
                self.instructions.w = 0b0

            elif operand == 16:
                self.instructions.prefix.append(0x66)
                self.instructions.w = 0b1
                
            elif operand == 32:
                self.instructions.w = 0b1
                pass
            elif operand == 64:
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

            self.instructions.disp[i] = val & 0xFF
            val >>= 8
        # print(self.instructions.disp)
    def disp_to_str(self):
        if self.instructions.disp == 0:
            return 0
        else:
            res = ''
            for i,d in enumerate(self.instructions.disp):
                res += str(hex(d))[2:]   

            res = int(res,16)         
            return res

    def get_address_size(self,data):
        disp = data['disp']
        base = data['base']
        index = data['index']
        scale = data['scale']
        if base:
            return base['size']
        elif index:
            return index['size']
        elif disp:
            return self.bit_len(disp)
        else:
            return 0
            
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
            self.operand_size = self.instructions.operands[0]['size']
            self.address_size = self.get_address_size(self.instructions.operands[0]['data'])

            self.instructions.opcode = self.instructions.operator['opcode']
            self.instructions.reg = self.instructions.operator['rcode']
            self.instructions.d = 1
            self.ebp = False

            disp = self.instructions.operands[0]['data']['disp']
            base = self.instructions.operands[0]['data']['base']
            index = self.instructions.operands[0]['data']['index']
            scale = self.instructions.operands[0]['data']['scale']
            fake = False
            


            # disp
            if (disp == 0) and (base == {} or base['code']&0b111 != 0b101):
                self.instructions.mod = 0b00
            elif self.bit_len(disp) == 8:
                self.instructions.mod = 0b01
                self.setDisp(disp,self.bit_len(disp))
            elif self.bit_len(disp) == 32:
                self.instructions.mod = 0b10
                self.setDisp(disp,self.bit_len(disp))

            # print(disp)
            # print(self.bit_len(disp))

            # print(self.instructions.disp)
            # esp
            if index == {} and base != {} and base['code'] & 0b111 == 0b100:
                fake = True
                index = base.copy()
                index['code'] &= 0b111
                self.self.instructions.rm = self.instructionsv.base['code']
                self.set_size(self.operand_size,self.address_size)

            # ebp
            if  index != {} and base != {} and base['code'] & 0b111 == 0b101:
                fake = True
                self.instructions.set_size(self.instructions.operands[0]['size'], True)
                self.ebp = True
                self.instructions.mod = 0b01
                disp_len = 8


            self.index_new_reg = 0
            # scale
            if index != {} and base == {}:
                fake = True
                self.instructions.mod = 0b00
                base = self.get_register('ebp')
                self.setDisp(disp, 60)
                self.set_size(self.operand_size,self.address_size)
                if index['code'] & 0b000 != 0:
                    self.index_new_reg = True

                index['code'] &= 0b111

            # direct addressing [disp]
            elif index == {} and base == {}:
                fake = True
                self.instructions.mod = 0b00
                base = self.get_register('ebp')
                index = self.get_register('esp')
                scale = 1
                self.setDisp(disp, self.bit_len(disp))
                self.set_size(self.operand_size,self.address_size)

            self.direct_addressing = False
            self.base_new_reg = False
            # register addressing [base]
            if index == {} and base != {}:
                self.instructions.rm = base['code'] & 0b111
                self.set_size(self.operand_size,self.address_size)
                self.direct_addressing = True
                
                if self.instructions.operands[0]['data']['base']['code'] & 0b1000 != 0:
                    self.base_new_reg = True


            # complete addresing [base + scale * index + disp]
            elif index != {} and base != {}:
                try:
                    if self.instructions.operands[0]['data']['base']['code'] & 0b1000 != 0:
                        self.base_new_reg = True
                        base['code'] &= 0b111
                    if self.instructions.operands[0]['data']['index']['code'] & 0b1000 != 0:
                        self.index_new_reg = True
                        index['code'] &= 0b111
                except:
                    pass

                self.instructions.rm = 0b100 
                self.instructions.sib = True
                if scale == 1:
                    self.instructions.scale = 0b00
                elif scale == 2:
                    self.instructions.scale = 0b01
                elif scale == 4:
                    self.instructions.scale = 0b10
                elif scale == 8:
                    self.instructions.scale = 0b11

                self.instructions.index = index['code']
                self.instructions.base = base['code']
                if not fake:
                    self.set_size(self.operand_size,self.address_size)
            
            prefix_len = 1
            if len(self.instructions.prefix) == 0:
                self.instructions.prefix.append(0x0)
            # result = (self.instructions.rex << (20+prefix_len*8))+(self.instructions.rex_w << (19+prefix_len*8))+(self.instructions.rex_r << (18+prefix_len*8))+(self.instructions.rex_x << (17+prefix_len*8))+(int(self.instructions.rex_b) << (16+prefix_len*8))+(self.instructions.prefix[0] << 16) + (self.instructions.opcode << 10) + (self.instructions.w << 9) + (self.instructions.d << 8) + (self.instructions.mod << 6) + (self.instructions.reg << 3) + int(self.instructions.rm)
            # result <<= 8
            print('rex: ' , self.instructions.rex)
            print('rex_w: ' , self.instructions.rex_w)
            print('rex_r: ' , self.instructions.rex_r)
            print('rex_x: ' , self.instructions.rex_x)
            print('rex_b: ' , self.instructions.rex_b)

            print('opcode:',end='')
            print(self.instructions.opcode)
            print('w:',end='')
            print(self.instructions.w)
            print('d:',end='')
            print(self.instructions.d)

            print('mod:',end='')
            print(self.instructions.mod)
            print('reg:',end='')
            print(self.instructions.reg)
            print('rm:',end='')
            print(self.instructions.rm)


            print('index:',end='')
            print(self.instructions.index)
            print('base:',end='')
            print(self.instructions.base)
            print('scale:',end='')
            print(self.instructions.scale)
            print('disp:',end='')
            print(self.instructions.disp) 



            if self.base_new_reg:
                self.instructions.rex = 0b0100
                self.instructions.rex_b = 0b1
            if self.index_new_reg:
                self.instructions.rex = 0b0100
                self.instructions.rex_x = 0b1
            

            if not self.ebp:
                disp_len = self.bit_len(disp)
            # print(str(hex(self.instructions.prefix[0])))
                if self.instructions.disp == 0:
                    disp_len = 0
                if self.instructions.operands[0]['data']['index'] != {} and self.instructions.operands[0]['data']['base'] == {}:
                    disp_len = 32
                # print('hah')
            if self.instructions.rex == 0:
                # print(self.disp_to_str())
                result = ((self.instructions.prefix[0]<< disp_len + 24 )+(self.instructions.rm << disp_len+8)+(self.instructions.reg << disp_len+11)+(self.instructions.mod << disp_len+14)+(self.instructions.w << disp_len+16)+(self.instructions.d << disp_len+17)+ (self.instructions.opcode << disp_len+18)+  (self.instructions.scale << (disp_len +6)) + (self.instructions.index << (disp_len+3)) + (self.instructions.base << disp_len) + self.disp_to_str())
            else:
                result = ((self.instructions.prefix[0]<< disp_len + 32 )+(self.instructions.rm << disp_len+8)+(self.instructions.reg << disp_len+11)+(self.instructions.mod << disp_len+14)+(self.instructions.w << disp_len+16)+(self.instructions.d << disp_len+17)+ (self.instructions.opcode << disp_len+18)+ (self.instructions.rex_b << disp_len+24)+ (self.instructions.rex_x << disp_len+25)+ (self.instructions.rex_r << disp_len+26)+ (self.instructions.rex_w << disp_len+27)+ (self.instructions.rex << disp_len+28)+(self.instructions.scale << (disp_len +6)) + (self.instructions.index << (disp_len+3)) + (self.instructions.base << disp_len) + self.disp_to_str())
            
            if self.direct_addressing:
                if self.instructions.rex == 0:
                    # print(self.disp_to_str())
                    result = ((self.instructions.prefix[0]<< disp_len + 24-8 )+(self.instructions.rm << disp_len)+(self.instructions.reg << disp_len+11-8)+(self.instructions.mod << disp_len+14-8)+(self.instructions.w << disp_len+16-8)+(self.instructions.d << disp_len+17-8)+ (self.instructions.opcode << disp_len+18-8) + self.disp_to_str())
                else:
                    result = ((self.instructions.prefix[0]<< disp_len + 32-8 )+(self.instructions.rm << disp_len)+(self.instructions.reg << disp_len+11-8)+(self.instructions.mod << disp_len+14-8)+(self.instructions.w << disp_len+16-8)+(self.instructions.d << disp_len+17-8)+ (self.instructions.opcode << disp_len+18-8)+ (self.instructions.rex_b << disp_len+24-8)+ (self.instructions.rex_x << disp_len+25-8)+ (self.instructions.rex_r << disp_len+26-8)+ (self.instructions.rex_w << disp_len+27-8)+ (self.instructions.rex << disp_len+28-8)+ self.disp_to_str())
                

            print(str(hex(result))[2:])     
            # print(self.address_size)
            # print(self.operand_size)
        elif self.instructions.operands[0]['type'] == 'imd':
            if self.instructions.operator['name'] == 'push':
                res = 0b0110000
                imd = self.instructions.operands[0]['data']
                pass
            elif self.instructions.operator['name'] == 'jmp':
                if self.bit_len(self.instructions.operands[0]['data']) == 8:
                    res = 0b11101011
                    res = (res<< 8)
                    imd = self.instructions.operands[0]['data']
                    self.setDisp(imd,)
                else:
                    res = 0b11101001
                    res = (res<< 32)

            elif self.instructions.operator['name'] == 'ret':
                res = 0b11000010
                imd = self.instructions.operands[0]['data']
                self.setDisp(imd,31)
                res = (res<< 16)
                result = str(hex(res + self.disp_to_str()))[2:]
                print(result)

    def process_Binary_operand(self):
        pass


    def process(self,nasm):
        self.nasm = re.split(',| |PTR',nasm)
        # print(self.nasm)
        self.instructions = Instruction()
        self.instructions.operands = self.get_operands()
        self.instructions.operator = self.get_operator() 

        # print(self.instructions.operands)
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
    test6 = [ 
            'dec QWORD PTR [0x5555551e]',
            'dec WORD PTR [rax]',
            'dec WORD PTR [rbp]',
            'dec WORD PTR [rax+0x12]',
            'dec WORD PTR [rbx*4]',
            'dec WORD PTR [rbx*4+0x12]',
            'dec WORD PTR [rax+rbx*4]',
            'dec WORD PTR [rax+rbx*4+0x12]',
            'dec WORD PTR [r8]',
            'dec QWORD PTR [r8]',
            'dec WORD PTR [r8+r9*1]',
            'jmp WORD PTR [rax]'
    ]
    test7 = ['dec QWORD PTR [ebp]',
    ]
    test8 = ['dec BYTE [rax]',
            'dec WORD [rax]',
            'dec DWORD [rax]',
            'dec QWORD [rax]',
            'dec BYTE [eax]',
            'dec WORD [eax]',
            'dec DWORD [eax]',
        ]
    test9 = ['jmp QWORD PTR [rax]']

    test10 = ['ret 0x16']
    for t in test10:
        print('{}: '.format(t))
        assembler = Assembler()
        # nasm = input()
        nasm = t
        assembler.process(nasm)
        del assembler
        print('##################################')

# print(str(hex(0b010)))
