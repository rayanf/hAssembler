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
            {'name':'mov','operands':2,'opcode': 0b100010,'iopcode':0b110001000},
            {'name':'mov','operands':1,'opcode': 0b0},
            {'name':'add','operands':2,'opcode': 0b000000,'iopcode':0b100000000},
            {'name':'add','operands':1,'opcode': 0b0},
            {'name':'adc','operands':2,'opcode': 0b000100,'iopcode':0b100000010},
            {'name':'adc','operands':1,'opcode': 0b0},
            {'name':'sub','operands':2,'opcode': 0b001010,'iopcode':0b100000101},
            {'name':'sbb','operands':2,'opcode': 0b000110,'iopcode':0b100000011},
            {'name':'sub','operands':1,'opcode': 0b0},
            {'name':'sbb','operands':1,'opcode': 0b0},
            {'name':'neg','operands':1,'opcode':0b111101,'rcode':0b011},
            {'name':'imul','operands':1,'opcode':0b111101,'rcode':0b101},
            {'name':'imul','operands':2,'opcode': 0b00001111101011,'iopcode':0b0},
            {'name':'idiv','operands':1,'opcode':0b111101,'rcode':0b111},
            {'name':'inc','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'dec','operands':1,'opcode':0b111111,'rcode':0b001},
            {'name':'push','operands':1,'opcode':0b111111,'rcode':0b110},
            {'name':'pop','operands':1,'opcode':0b0101,'rcode':0b000},
            {'name':'call','operands':1,'opcode':0b111111,'rcode':0b010},
            {'name':'ret','operands':1,'opcode':0b111111,'rcode':0b000},
            {'name':'ret','operands':0, 'opcode':0b11000011},
            {'name':'ret','operands':1},
            {'name':'jmp','operands':1,'opcode':0b111111,'rcode':0b100},
            {'name':'xor','operands':2,'opcode': 0b001100,'iopcode':0b100000110},
            {'name':'xor','operands':1,'opcode': 0b0},
            {'name':'or','operands':2,'opcode': 0b000010,'iopcode':0b100000001},
            {'name':'and','operands':2,'opcode': 0b001000,'iopcode':0b100},
            {'name':'and','operands':1,'opcode': 0b0},
            {'name':'not','operands':1,'opcode':0b111101,'rcode':0b010},
            {'name':'shl','operands':2,'opcode': 0b0,'iopcode':0b110000100},
            
            {'name':'shl','operands':1,'opcode':0b110100,'rcode':0b100},
            {'name':'shr','operands':1,'opcode':0b110100,'rcode':0b101},
            
            {'name':'shr','operands':2,'opcode': 0b0,'iopcode':0b110000101},
            {'name':'cmp','operands':2,'opcode': 0b001110,'iopcode':100000111},
            {'name':'test','operands':2,'opcode': 0b100001,'iopcode':0b111101000},
            {'name':'test','operands':1,'opcode': 0b0},
            {'name':'xchg','operands':2,'opcode': 0b100001,'iopcode':0b0},
            {'name':'xchg','operands':1,'opcode': 0b0},
            {'name':'xadd','operands':2,'opcode': 0b00001111110000,'iopcode':0b0},
            {'name':'std','operands':0,'opcode':0b11111101},
            {'name':'stc','operands':0,'opcode':0b11111001},
            {'name':'clc','operands':0,'opcode':0b11111000},
            {'name':'cld','operands':0,'opcode':0b11111100},
            {'name':'syscall','operands':0,'opcode':0b0000111100000101},
            {'name':'bsf','operands':2,'opcode':0b00001111101111,'iopcode':0b0},
            {'name':'bsr','operands':2,'opcode':0b00001111101111,'iopcode':0b0},
            # {'name':'jo','operands': 1,'opcode':0b0000},
            # {'name':'jno','operands': 1,'opcode':0b0001},
            # {'name':'jb','operands': 1,'opcode':0b0010},
            # {'name':'jnae','operands': 1,'opcode':0b0010},
            # {'name':'jnb','operands': 1,'opcode':0b0011},
            # {'name':'jae','operands': 1,'opcode':0b0011},
            # {'name':'je','operands': 1,'opcode':0b0100},
            # {'name':'jz','operands': 1,'opcode':0b0100},
            # {'name':'jne','operands': 1,'opcode':0b0101},
            # {'name':'jnz','operands': 1,'opcode':0b0101},
            # {'name':'jbe','operands': 1,'opcode':0b0110},
            # {'name':'jna','operands': 1,'opcode':0b0110},
            # {'name':'jnbe','operands': 1,'opcode':0b0111},
            # {'name':'ja','operands': 1,'opcode':0b0111},
            # {'name':'js','operands': 1,'opcode':0b1000},
            # {'name':'jns','operands': 1,'opcode':0b1001},
            # {'name':'jp','operands': 1,'opcode':0b1010},
            # {'name':'jpe','operands': 1,'opcode':0b1010},
            # {'name':'jnp','operands': 1,'opcode':0b1011},
            # {'name':'jpo','operands': 1,'opcode':0b1011},
            # {'name':'jl','operands': 1,'opcode':0b1100},
            # {'name':'jnge','operands': 1,'opcode':0b1100},
            # {'name':'jnl','operands': 1,'opcode':0b1101},
            # {'name':'jge','operands': 1,'opcode':0b1101},
            # {'name':'jle','operands': 1,'opcode':0b1110},
            # {'name':'jng','operands': 1,'opcode':0b1110},
            # {'name':'jnle','operands': 1,'opcode':0b1111},
            # {'name':'jg','operands': 1,'opcode':0b1111},

        ]


memory_size = {'BYTE':8,'WORD':16,'DWORD':32,'QWORD':64}



class inst:
    def __init__(self):
        self.memory = False
        self.memory_size = False
        self.base = {}
        self.index = {}
        self.scale = 0
        self.disp = 0
        self.disp_size = 0

        self.prefix = 0

        self.opcode = 0
        self.operands = []
        self.operator = {}
