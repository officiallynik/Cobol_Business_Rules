class Variable:
    def __init__(self, name):
        self.name = name
        self.statements = []

class Model:
    def __init__(self):
        self.prog = {
            'IDENTIFICATION': {},
            'ENVIRONMENT': {},
            'DATA': {},
            'PROCEDURE': []
        }

    def process_iden_statement(self, words):
        if 'PROGRAM-ID.' in words:
            self.prog['IDENTIFICATION']['program_id'] = words[len(words) - 1]
        elif 'AUTHOR-ID' in words and words[len(words-1)] != 'AUTHOR-ID':
            self.prog['IDENTIFICATION']['author'] = words[len(words) - 1]
        elif 'SOURCE-ID' in words and words[len(words)-1] != 'SOURCE-ID':
            self.prog['IDENTIFICATION']['source'] = words[len(words) - 1]

    def process_env_statement(self, words):
        if 'SECTION.' in words:
            self.prog['ENVIRONMENT']['conf'] = {}
        else:
            if 'SOURCE-COMPUTER.' in words and words[len(words)-1] != 'SOURCE-COMPUTER.':
                self.prog['ENVIRONMENT']['conf']['src_comp'] = words[len(words)-1]
            elif 'OBJECT-COMPUTER.' in words and words[len(words)-1] != 'OBJECT-COMPUTER.':
                self.prog['ENVIRONMENT']['conf']['obj_comp'] = words[len(words)-1]
        

    def process_data_statement(self, words):
        if 'SECTION.' in words:
            self.prog['DATA']['work_store'] = {'group': [], 'elementary': []}
        else:
            if words[1] == '01':
                pass
            elif words[1] == '77':
                self.prog['DATA']['work_store']['elementary'].append(Variable(words[3]))
            else:
                words = ' '.join(words[1:]).strip().split(' ')
                self.prog['DATA']['work_store']['elementary'].append(Variable(words[1]))
            

    def process_proc_statement(self, line):
        self.prog['PROCEDURE'].append(line) 

    def build_model(self, code):
        lines = code.split("\n")
        type = 0

        for line in lines:
            words = line.split(" ")
            if 'DIVISION.' in words:
                type += 1
            else:
                if type == 1:
                    self.process_iden_statement(words)
                elif type == 2:
                    self.process_env_statement(words)
                elif type == 3:
                    self.process_data_statement(words)
                elif type == 4:
                    self.process_proc_statement(line)