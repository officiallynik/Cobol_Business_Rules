from model import Model
from procedure import procedure_division

with open('input/shop.cbl') as f:
    code = f.read()
    cbl_model = Model()
    cbl_model.build_model(code)
    variables = cbl_model.prog['DATA']['work_store']['elementary']
    code=cbl_model.prog['PROCEDURE']
    procedure_division(code,variables)
