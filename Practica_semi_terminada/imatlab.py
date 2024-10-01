### LIBRERIAS ###
from io import FileIO
import modular
import os, sys



### CONSTANTES ###

    #PRETTY
BOLD = '\033[1m'
END = '\033[m'

    #ARGUMENTOS
FLAGS = {'help': ['-h','-help'], 'iterative': ['-i','-it'], 'batch': ['-b', '-batch']}

    #ERRORES
NOP_TYPES = {0: 'flag_error', 1: 'argv_error', 2: 'file_error', 3: 'command_error', 4: 'params_error'}
NOP_MESAGES = {
    0: 'use flag -h or -help for help',
    1: 'two files required, less given',
    2: 'first file does not exist or second file format is not ".txt"',
    3: 'invalid command',
    4: 'incorrect parameters'
}

    #COMANDOS
COMANDOS = {
    'primo': [modular.es_primo, 'int', 1],
    'primos': [modular.lista_primos, 'int', 2],
    'factorizar': [modular.factorizar, 'int', 1],
    'mcd': [modular.mcd, 'int', 2],
    'bezout': [modular.bezout, 'int', 2],
    'coprimos': [modular.coprimos,'int', 2],
    'pow': [modular.potencia_mod_p, 'int', 3],
    'inv': [modular.inversa_mod_p, 'int', 2],
    'euler': [modular.euler, 'int', 1],
    'legendre': [modular.legendre, 'int', 2],
    'resolverSistema': [modular.resolver_sistema_congruencias, 'list1', 3],
    'raiz': [modular.raiz, 'int', 2],
    'ecCuadratica': [modular.ecuacion_cuadratica, 'int', 4]
}


### CLASES ###

class ErrorNOP():
    def __init__(self, type: int) -> None:
        self.type = type
    
    def __str__(self):
        return 'NOP'

    def message(self):
        print(f'{BOLD}NOP ->{END} {NOP_TYPES[self.type]}: {NOP_MESAGES[self.type]}')

class Interface():
    
    def __init__(self):
        self.argvs = sys.argv
        self.flag_order = None
        self.files = [None,None]

    #INITTIALIZATION
    def __process_arguments__(self):
        '''
        FLAGS
        FILES
        '''

        def check_flag(flag):
            return flag if flag[0] == '-' else None

        def get_flag_order(flag: str):
            
            for key in FLAGS:
                if flag in FLAGS[key]: return key
            return 'iterative' #ErrorNOP(0)

        
        #FLAGS
        try: 
            flag = self.argvs[1]
            check_flag(flag)
        except Exception: flag = None
        self.flag_order = get_flag_order(flag)


        #FILES
        if self.flag_order == 'batch':
            #fin
            try: 
                self.files = [self.argvs[2], self.argvs[3]]
            except Exception:
                self.files = None

    def help(self):
        '''
        Show help message
        '''
        message ="\n\
        SYNOPSYS\n\
            Starting guide for IMATLAB\n\n\
        ARGVS STRUCTURE\n\
            python imatlab.py [FLAG]  [FILE IN]  [FILE OUT]\n\
            Note: FILES are only required for batch mode\n\n\
        FLAGS\n\
            -h, -help  --show starting guide\n\
            \n\
            -i, -it    --start IMATLAB in iterative mode\n\
            \n\
            -b, -batch --start IMATLAB in batch mode"
        print(message)
        
    def open(self):
        
        self.__process_arguments__()

        if type(self.flag_order) == ErrorNOP:
            self.flag_order.message()

        elif self.flag_order == 'help':
            self.help()

        elif self.flag_order == 'iterative':
            exit = False
            while not exit:
                clear()
                exit = self.run_iterative()

        elif self.flag_order == 'batch':

            if self.files:
                
                if self.__openfiles__():    #hacer open de los ficheros
                    print('Running...')
                    run_commands(self.files[0], self.files[1]) #llamar funcion batch
                    clear()
                    print('Done')
                    self.__closefiles__()   #hacer close de los ficheros

                else: ErrorNOP(2).message()

            else: ErrorNOP(1).message()
            
    #ITERATIVE
    def run_iterative(self, operate = True) -> bool:

        def title() -> None:
            print(f'\t\t\t\t\t  {BOLD}ITERATIVE MODE ACTIVATED{END}')
    
        def leyenda_comandos(comandos_dict: dict, longitud: int = 4, i = 0, keys = []):
            print('COMANDOS:')

            for k in comandos_dict: keys.append(k)

            while i < len(keys):

                j = i

                line = ''
                while (j < longitud + i) and (j < len(keys)):

                    line += f'\t{keys[j]}()\t\t'
                    j += 1
                print(line)

                i += longitud
            print('\tCLEAR\t\t\t\tEXIT')
            ...

        def get_input():

            op = input('\nOPERACION: ')

            if op == 'CLEAR': return False
            elif op == 'EXIT': return True
            else: return op

        def process_input(op: str):
            
            result = function(op)
            
            print(result) if type(result) != ErrorNOP else result.message()

        title()
        leyenda_comandos(COMANDOS)
        
        while operate:

            op = get_input()
            if type(op) == bool: return op

            process_input(op)

        ...

    #BATCH
    def __openfiles__(self) -> bool:

        try:
            if self.files[1][-4:] != '.txt':  return False
            self.files = [open(self.files[0],'r'), open(self.files[1], 'w')]
            return True
        except Exception: return False

    def __closefiles__(self):
        self.files[0].close()
        self.files[1].close()


### FUNCIONES ###

def clear() -> None:
    os.system('cls')
    
    
#RUN FUNCTIONS
def __getparams__(inside: str, type: str, n: int) -> tuple:
    plist = inside.split(',')

    try:    
        if type == 'int':
            params = [int(p) for p in plist]
        
        elif type == 'list0':
            params = [[int(i) for i in p[1:len(p)-1].split(';')] for p in plist]
        
        elif type == 'list1':
            a, b, c = [], [], []
            for p in plist:
                l =  p[1:len(p)-1].split(';')
                a.append(int(l[0]))
                b.append(int(l[1]))
                c.append(int(l[2]))
            params = [a,b,c]
    except Exception: return False
    
    if len(params) != n: return False
    
    return tuple(params)

def function(entry: str):
    """
    RETURN:\n
    ErrorNE() if it doesn't exist\n
    ErrorNOP() if the input is incorrect\n
    Numerical or Boolean result if al OK (depends on the function)
    """
        
    flist = entry.split('(')
    name = flist[0]

    try: f = COMANDOS[name][0]
    except Exception: return ErrorNOP(3)

    params = __getparams__(flist[1][:-1], COMANDOS[name][1], COMANDOS[name][2])
    if not params: return ErrorNOP(4)

    return f(*params)

def run_commands(fin: FileIO, fout: FileIO) -> None:
    
    for line in fin:    
        fout.write(str(function(line[:-1])) + '\n')


if __name__ == '__main__':

    clear()

    interface = Interface()
    interface.open()