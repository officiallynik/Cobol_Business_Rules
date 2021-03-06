import re
class Statement:
    def __init__(self):
        self.text = ""
        self.conditionVariable = {}
        self.indexVariable = {}
        self.sourceVariable = {}
        self.targetVariable = {}
        self.conditionStatements = []
        self.tag = None
        self.line_number = None 
        self.next = []

class Variable:
    def __init__(self):
        self.name = ""
        self.statements = []

keywords = set({"FUNCTION","RANDOM"})
def enter_variable(var, variables, type, statement):
    # check if var is a keyword
    if var in keywords:
        return

    if var in variables:
        # variable is already present in variables dictionary
        if type == "source":
            statement.sourceVariable[var] = variables[var]
        elif type == "target":
            statement.targetVariable[var] = variables[var]
        elif type == "conditional":
            statement.conditionVariable[var] = variables[var]
        variables[var].statements.append(statement)
    else:
        # variable not present in variables dictionary
        variable = Variable()
        variable.name = var
        variable.statements.append(statement)
        variables[var] = variable
        if type == "source":
            statement.sourceVariable[var] = variable
        elif type == "target":
            statement.targetVariable[var] = variable
        elif type == "conditional":
            statement.conditionVariable[var] = variables[var]

def move_statement(tokens, line_number, variables, variable_classification):
    # MOVE TO statement
    # Syntax: 005102 MOVE A TO E
    statement =  Statement()
    statement.tag = "move"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])
    i = 2

    # All Source Variables
    while tokens[i].lower() != "to":
        source = tokens[i]
        if source.isnumeric() is True:
            i = i + 1
            continue
        enter_variable(source,variables,"source",statement)
        i = i + 1

    i = i + 1
    target = tokens[i]
    enter_variable(target,variables,"target",statement)
    variable_classification["target"].append(variables[target])
    return statement 

def add_statement(tokens, line_number, variables, variable_classification):
    # ADD TO statement
    # Syntax: 005102 ADD A B C D TO E
    statement =  Statement()
    statement.tag = "add"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])
    i = 2

    # All Source Variables
    while tokens[i].lower() != "to":
        source = tokens[i]
        if source.isnumeric() is True:
            i = i + 1
            continue
        enter_variable(source,variables,"source",statement)
        i = i + 1

    i = i + 1
    target = tokens[i]
    enter_variable(target,variables,"target",statement)
    variable_classification["target"].append(variables[target])
    return statement
    
def subtract_statement(tokens, line_number, variables, variable_classification):
    # SUBTRACT FROM statement
    # Syntax: 005102 SUBTRACT A B C D FROM E
    statement =  Statement()
    statement.tag = "subtract"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])
    i = 2

    # All Source Variables
    while tokens[i].lower() != "from":
        source = tokens[i]
        if source.isnumeric() is True:
            i = i + 1
            continue
        enter_variable(source,variables,"source",statement)
        i = i + 1

    i = i + 1
    target = tokens[i]

    enter_variable(target,variables,"target",statement)
    
    variable_classification["target"].append(variables[target])
    return statement

def remove_operators(tokens):
    st = " ".join(tokens)
    common_operators = set({'+','*','=','/','(',')','.'})
    clean_st = ""
    for index, char in enumerate(st):
        if char in common_operators :
            clean_st+=" "
        elif char == '-':
            if st[index-1]==" " or st[index-1]==")" or st[index+1]==" " or st[index+1]=="(" :
                clean_st+=" "
            else:
                clean_st+=char
        else:
            clean_st+=char
    #print(clean_st)
    return clean_st.split()
    
def compute_statement(tokens, line_number, variables, variable_classification):
    # COMPUTE statement
    # Syntax: 005102 COMPUTE WS-NUMC= (WS-NUM1 * WS-NUM2) - (WS-NUMA / WS-NUMB) + WS-NUM3.

   
    statement =  Statement()
    statement.tag = "compute"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])

    # Remove operators from statement
    tokens = remove_operators(tokens)

    # Target Variable
    target = tokens[2]
    enter_variable(target,variables,"target",statement) 
    variable_classification["target"].append(variables[target])

    
    # All Source Variables
    for i in range(3,len(tokens)):
        source = tokens[i]
        if source.isnumeric() is True: 
            continue
        enter_variable(source,variables,"source",statement)
    return statement
    
def if_statement(tokens, line_number, variables, variable_classification):
    # IF statement
    statement =  Statement()
    statement.tag = "if"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])

    # Remove operators from statement
    tokens = remove_operators(tokens)

    condition_operators = set({"=",">","<",">=","<=","AND","OR","IS","NOT","THEN","THAN","LESS","GREATER","ARE"})
    for i in range(2,len(tokens)):
        var = tokens[i]
        if var in condition_operators:
            continue
        if var.isnumeric() is True:
            continue
        enter_variable(var,variables,"conditional",statement)
        variable_classification["conditional"].append(variables[var])

    return statement

def remove_string_literal(tokens):
    # removing line no. and display keyword
    # "Hello 'world'"
    # 'Hello "world'
    str = " ".join(tokens)
    edited_st = re.sub(r'".+?"'," ",str) # remove everything between double quotes
    edited_st = re.sub(r'".+?"'," ",edited_st) # remove everything between single quotes
    return edited_st.split()

def display_statement(tokens, line_number, variables, variable_classification):
    # DISPLAY statement 
    # Assuming display statement consists of only one variable   
    statement =  Statement()
    statement.tag = "display"
    statement.line_number = line_number
    statement.text = " ".join(tokens[1:])

    # Remove string literal from statement
    tokens = remove_string_literal(tokens)
    # tokens: ['some_number','DISPLAY','variable']
    
    if len(tokens) == 2:
        return statement

    var = tokens[2]
    enter_variable(var,variables,"in-out",statement)
    variable_classification["in-out"].append(variables[var])

    return statement

def procedure_division(code, variables):
    # Assuming all statements are separated by new line 
    # Assuming code is already splitted into different lines and only consists of procedure division
    # variables is a list/set of all data items found in data division
    # {
    #     "money": Variable("money",[])
    # }
    # Eg: money
    # 
    line_number = 1
    statements = []
    variable_classification={
        "target":[],
        "in-out":[],
        "conditional":[]
    }
    paragraphs = {}

    temp_stack = [] # to keep track of if statements
    else_stack = [] # to keep track of else statements

    for line in code:
        line = line.replace('.','')
        line = line.replace('\t','')
        #print(line)
        tokens = line.split()
        #print(tokens)

        if len(tokens) == 0:
            # empty line
            continue

        # tokens[0] is the number i.e. 003000
        first_token = tokens[1].lower()
        #print(first_token)
        if first_token == 'procedure':
            # procedure division 
            pass
        elif first_token == "if":
            # IF statement
            statement = if_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
            temp_stack.append(statement)
        elif first_token == "else":
            # else
            if_stmt = temp_stack[len(temp_stack)-1]
            
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "else"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1

            if_stmt.alt = line_number # alternate: first line of else
            if_stmt.else_line = line_number-1 # last: else
        elif first_token == "end-if":
            if_stmt = temp_stack.pop()

            statement = Statement()
            statement.line_number = line_number
            statement.tag = "end-if"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1

            #if_stmt.alt_last = line_number-2
            # if_stmt.next_line = line_number
            if_stmt.endif = line_number - 1

        elif first_token == "display":
            # display statement
            statement = display_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
        elif first_token == "perform":
            # PERFORM THROUGH statement
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "perform"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
        elif first_token == "go":
            # GO TO statement
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "go"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
        elif first_token == "move":
            # MOVE TO statement
            statement = move_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
        elif first_token == "add":
            # ADD TO statement
            # ADD 1 TO BAG
            statement = add_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "subtract":
            # SUBTRACT FROM statement
            statement = subtract_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "compute":
            # COMPUTE statement
            statement = compute_statement(tokens,line_number,variables, variable_classification)
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "stop":
            # STOP RUN statement
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "stop"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
            
        # elif first_token == "fin":
        #     # FIN Statement
        #     statement = Statement()
        #     statement.line_number = line_number
        #     statement.tag = "fin"
        #     statement.text = " ".join(tokens[1:])
        #     statements.append(statement)
        #     line_number = line_number + 1
            
        elif first_token == "exit":
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "exit"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            line_number = line_number + 1
        else:
            # This statement consists of paragraph name
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "paragraph_name"
            statement.text = " ".join(tokens[1:])
            statement.conditionStatements = temp_stack.copy()
            statements.append(statement)
            paragraphs[tokens[1]] = statement
            line_number = line_number + 1
    
    business_variables = set()
    for var in variable_classification["target"]:   
        business_variables.add(var)

    for var in variable_classification["in-out"]:   
        business_variables.add(var)
    
    for var in variable_classification["conditional"]:   
        business_variables.add(var)

    return business_variables, statements, paragraphs

def display(statement):
    print(statement.tag, statement.text, statement.line_number)
    statements = statement.next
    for statement in statements:
        print(statement.tag, statement.text, statement.line_number)

def build_cfg(statements, paragraphs):
    stop_found = False

    for i in range(len(statements)):
        if statements[i].tag == "perform":
            # PERFORM PARA1 THROUGH PARA2
            # Next statement will be first statement of PARA1
            tokens = statements[i].text.split()
            para1_name = tokens[1]
            para2_name = tokens[3]

            # index will be line_number - 1
            next_statement_index = (paragraphs[para1_name].line_number + 1) - 1 
            statements[i].next.append(statements[next_statement_index])
            
            # last stat in PERFORM - THRU
            # statement before para-2 must point to i+1
            para2_index = paragraphs[para2_name].line_number - 1
            # setting next of statement just before para2 
            statements[para2_index - 1].next.append(statements[i+1])
            # display(statements[para2_index - 1])
        elif statements[i].tag == "if":
            statements[i].next = [statements[statements[i].line_number], statements[statements[i].alt - 1]]
            statements[statements[i].else_line - 1].next.append(statements[statements[i].endif - 1])
            #statements[statements[i].alt_last - 1].next.append(statements[statements[i].next_line - 1])

            # display(statements[i])
            # display(statements[statements[i].last - 1])
            # display(statements[statements[i].alt_last - 1])
        elif statements[i].tag == "else":
            pass        
        elif statements[i].tag == "go":
            # GO TO PARA
            # Next statement will be first statement of PARA
            tokens = statements[i].text.split()
            para_name = tokens[2]
       

            # index will be line_number - 1
            next_statement_index = (paragraphs[para_name].line_number + 1) - 1 
            statements[i].next.append(statements[next_statement_index])
            # display(statements[i])
        elif statements[i].tag == "exit":
            if not stop_found:
                statements[i].next.append(statements[i+1])
        elif statements[i].tag == "stop":
            stop_found = True            
        elif statements[i].tag == "paragraph_name":
            statements[i].next.append(statements[i+1])            
            # display(statements[i])            
        else:
            statements[i].next.append(statements[i+1])

class Rule_fragment:
    def __init__(self, statement):
        self.statement = statement
        self.next = None

def dfs(statement, path, vis, rules, rule_fragments, head, prev, tag,prev_line_number,temp_vis):
    line_number = statement.line_number
    
    if line_number in path:
        return
    
    if line_number in rule_fragments:
        if line_number in path:
            return
        path.add(line_number)
        if line_number in vis:
            # already visited rule fragment
            if line_number in rules:
                # head of some rule
                prev.next = rules[line_number]

                # delete from rules
                del rules[line_number]
                return
            else:
                prev.next = rule_fragments[line_number]
                return
        else:
            # if rule fragment is not visited
            vis.add(line_number)
            temp_vis.append(line_number)
            prev.next = rule_fragments[line_number]
            prev = prev.next
    
    # if statement.tag == "paragraph_name":
    #     path.add(line_number)

    if tag == "perform":
        # parent statement was perform
        for next in statement.next:
            if next.line_number == prev_line_number + 1 or next.line_number == line_number+1:
                dfs(next, path ,vis, rules, rule_fragments, head, prev, statement.tag,line_number,temp_vis)
        return
    path.add(line_number)
    for next in statement.next:                       
        dfs(next, path ,vis, rules, rule_fragments, head, prev, statement.tag,line_number, temp_vis)


def insert_fragment(node, fragment):
    temp = node.next
    node.next = fragment
    fragment.next = temp

def add_conditional_statements(rule):
    added_fragments = set()
    head = rule
    temp = head
    prev = None 
    while temp != None:
        st = temp.statement
        added_fragments.add(st.line_number)
        for conditional in st.conditionStatements:
            if conditional.line_number not in added_fragments:
                fragment = Rule_fragment(conditional)
                if prev == None:
                    fragment.next = head
                    head = fragment
                    prev = head
                else: 
                    insert_fragment(prev, fragment)
                    prev = prev.next
                added_fragments.add(conditional.line_number)
        prev = temp
        temp = temp.next
    return head
    

            
def extract_execution_path(variable, statements):
    rules = {}
    variable_statements = variable.statements
    rule_fragments={}
    for stmt in variable_statements:
        #print(stmt.line_number, stmt.text)
        rule_fragments[stmt.line_number] = Rule_fragment(stmt)

    vis = set()
    # vis contain already added rule fragments
    temp_vis = []
    for fragment in variable_statements:
        if fragment.line_number in vis:
            #print("visited")
            continue
        path = set()
        path.add(fragment.line_number)
        vis.add(fragment.line_number)
        temp_vis.append(fragment.line_number)
        head = rule_fragments[fragment.line_number]
        rules[fragment.line_number] = head
        prev= head
        for next in fragment.next:        
            dfs(next, path ,vis, rules, rule_fragments, head, prev, fragment.tag,fragment.line_number, temp_vis)
        

    
            # display(statements[i])            
    for key in rules:
        head = rules[key]
        head = add_conditional_statements(head)
        rules[key] = head


        print("RULE")
        head = rules[key]
        temp = head
        while temp!=None:
            print(temp.statement.text)            
            temp = temp.next            
    # return statements
        
    

if __name__ == '__main__':
    str = "IF NEED = (QT-A + QT-B) AND QT-MEAT > 0"
    print(remove_operators(str.split()))