from model import Model
from procedure import build_cfg, procedure_division, extract_execution_path
import sys
import os

if __name__ == "__main__":
    input_file = None
    output_file = None
    
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except:
        pass

    if not input_file:
        print("No input file is provided")
        exit() 

    if not output_file:
        print("No output file is provided")
        exit()

    sys.stdout = open(output_file, 'w')
    with open(input_file) as f:
        code = f.read()
        cbl_model = Model()
        cbl_model.build_model(code)
        variables = cbl_model.prog['DATA']['work_store']['elementary']
        code=cbl_model.prog['PROCEDURE']
        # print(variables)
        business_variabes, statements, paragraphs = procedure_division(code,variables)
        
        cfg = build_cfg(statements, paragraphs)
        for var in business_variabes:
            print('#'*50)
            print()
            print("Extracting business rules for "+var.name +" ...........")            
            extract_execution_path(var,cfg)
            print()
            