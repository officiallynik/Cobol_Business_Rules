import re
class Statement:
    def __init__(self):
        self.text = ""
        self.conditionVariable = {}
        self.indexVariable = {}
        self.sourceVariable = {}
        self.targetVariable = {}
        self.tag = None
        self.line_number = None 
        self.next = []

class Variable:
    def __init__(self):
        self.name = ""
        self.statements = []


def enter_variable(var, variables, type, statement):

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
    statement.tag = "compute"
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
    # Assuming code is already splitted into different lines and only consists of procedure division
    # variables is a list/set of all data items found in data division
    # {
    #     "money": Variable("money",[])
    # }
    # Eg: money
    line_number = 1
    statements = []
    variable_classification={
        "target":[],
        "in-out":[],
        "conditional":[]
    }
    for line in code:
        tokens = line.split()

        if len(tokens) == 0:
            # empty line
            continue

        # tokens[0] is the number i.e. 003000
        first_token = tokens[1].lower()
        
        if first_token == 'procedure':
            # procedure division 
            pass
        elif first_token == "if":
            # IF statement
            statement = if_statement(tokens,line_number,variables, variable_classification)
            statements.append(statement)
            line_number = line_number + 1
        elif first_token == "else":
            # else
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "else"
            statement.text = " ".join(tokens[1:])
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "display":
            # display statement
            statement = display_statement(tokens,line_number,variables, variable_classification)
            statements.append(statement)
            line_number = line_number + 1
            pass
        elif first_token == "perform":
            # PERFORM THROUGH statement
            pass
        elif first_token == "go":
            # GO TO statement
            pass
        elif first_token == "add":
            # ADD TO statement
            # ADD 1 TO BAG
            statement = add_statement(tokens,line_number,variables, variable_classification)
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "subtract":
            # SUBTRACT FROM statement
            statement = subtract_statement(tokens,line_number,variables, variable_classification)
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "compute":
            # COMPUTE statement
            statement = compute_statement(tokens,line_number,variables, variable_classification)
            statements.append(statement)
            line_number = line_number + 1
            
        elif first_token == "stop":
            # STOP RUN statement
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "stop"
            statement.text = " ".join(tokens[1:])
            statements.append(statement)
            line_number = line_number + 1
            pass
        elif first_token == "fin":
            # FIN Statement
            statement = Statement()
            statement.line_number = line_number
            statement.tag = "fin"
            statement.text = " ".join(tokens[1:])
            statements.append(statement)
            line_number = line_number + 1
            pass
        else:
            # This statement can be of two types:
            # Paragraph entry name Eg: BUY-VEG.
            # Paragraph exit Eg: BUY-VEG. EXIT.
            pass


if __name__ == '__main__':
    str = "IF NEED = (QT-A + QT-B) AND QT-MEAT > 0"
    print(remove_operators(str.split()))

'''
02900 PROCEDURE DIVISION.
003000 INIT.
003200    IF OP = 1
003201      DISPLAY "SHOP IS OPEN"
003202      PERFORM INIT-PRD THROUGH INIT-PRD-FN
003203      GO TO INIT-FN
004300    ELSE
004301      DISPLAY "SHOP IS CLOSED"
004400    	GO TO INIT.
004402 INIT-FN. EXIT.
004500 BUY-VEG.
004501 PERFORM ISNEEDED THROUGH ISNEEDED-FN.
004700 IF NEED = 1 AND QT-VEG > 0
004800    IF MONEY > PR-VEG AND BAG < MAX-CAP
004900 	ADD 1 TO BAG
005000 	COMPUTE MONEY = MONEY - PR-VEG
005100 	SUBTRACT 1 FROM QT-VEG
005101    ELSE
005102       GO TO PRINT
005103 ELSE
005104     GO TO BUY-MEAT.
005105 BUY-VEG-FN. EXIT.
005200 BUY-MEAT.
005201 PERFORM ISNEEDED THROUGH ISNEEDED-FN.    		
005400 IF NEED = 1 AND QT-MEAT > 0
005500    IF MONEY > PR-MEAT AND BAG < MAX-CAP
005600 	ADD 1 TO BAG
005700 	COMPUTE MONEY = MONEY - PR-MEAT
005800 	SUBTRACT 1 FROM QT-MEAT
005801    ELSE
005802      GO TO PRINT
005803 ELSE
005804     GO TO BUY-BREAD.
005805 BUY-MEAT-FN. EXIT.
005900 BUY-BREAD.
005901 PERFORM ISNEEDED THROUGH ISNEEDED-FN.    		
006100 IF NEED = 1 AND QT-BREAD > 0
006200    IF MONEY > PR-BREAD AND BAG < MAX-CAP
006300 	ADD 1 TO BAG
006400 	COMPUTE MONEY = MONEY - PR-BREAD
006500 	SUBTRACT 1 FROM QT-BREAD
006501    ELSE
006502      GO TO PRINT
006503 ELSE
006504     GO TO BUY-MILK.
006505 BUY-BREAD-FN. EXIT.    		
006600 BUY-MILK.
006601 PERFORM ISNEEDED THRU ISNEEDED-FN.    		
006800 IF NEED = 1 AND QT-MILK > 0
006900    IF MONEY > PR-MILK AND BAG < MAX-CAP
007000 	ADD 1 TO BAG
007100 	COMPUTE MONEY = MONEY - PR-MILK
007200 	SUBTRACT 1 FROM QT-MILK
007201     ELSE
007202      GO TO PRINT
007203 ELSE
007204     GO TO BUY-FRUIT.
007205 BUY-MILK-FN. EXIT.
007300 BUY-FRUIT.
007301 PERFORM ISNEEDED THRU ISNEEDED-FN.    		
007500 IF NEED = 1 AND QT-FRUIT > 0
007600    IF MONEY > PR-FRUIT AND BAG < MAX-CAP
007700 	ADD 1 TO BAG
007800 	COMPUTE MONEY = MONEY - PR-FRUIT
007900 	SUBTRACT 1 FROM QT-FRUIT
007901     ELSE
007902      GO TO PRINT
007903 ELSE
007904     GO TO CHECK.
007905 BUY-FRUIT-FN. EXIT.
008000 CHECK.
008100 IF MONEY <= 0 OR BAG >= MAX-CAP
008200 	GO TO PRINT
008201 ELSE
008202     GO TO BUY-VEG.
008203 CHECK-FN. EXIT.
008300 PRINT.
008400 MOVE MONEY TO REST.
008401 DISPLAY "REST:" MONEY.
008402 DISPLAY "NB OF PRODUCTS:" BAG.			
008500 FIN.
008600    STOP RUN.
008601 ISNEEDED.
008602   COMPUTE NEED = FUNCTION RANDOM (1) * 2.
008603 ISNEEDED-FN. EXIT.
008604 INIT-PRD.
008605    COMPUTE QT-VEG = FUNCTION RANDOM (1) * 10
008606    COMPUTE QT-MEAT = FUNCTION RANDOM (1) * 10
008607    COMPUTE QT-BREAD = FUNCTION RANDOM (1) * 10
008608    COMPUTE QT-MILK = FUNCTION RANDOM (1) * 10
008609    COMPUTE QT-FRUIT = FUNCTION RANDOM (1) * 10
008610    COMPUTE PR-VEG = FUNCTION RANDOM (1) * 10 + 3
008611    COMPUTE PR-MEAT = FUNCTION RANDOM (1) * 10 + 5
008612    COMPUTE PR-BREAD = FUNCTION RANDOM (1) * 10 + 1
008613    COMPUTE PR-MILK = FUNCTION RANDOM (1) * 10 + 2
008614    COMPUTE PR-FRUIT = FUNCTION RANDOM (1) * 10 + 1.
008615 INIT-PRD-FN. EXIT.
'''