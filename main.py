from model import Model
from procedure import build_cfg, procedure_division, extract_execution_path

with open('input/shop.cbl') as f:
    code = f.read()
    cbl_model = Model()
    cbl_model.build_model(code)
    variables = cbl_model.prog['DATA']['work_store']['elementary']
    code=cbl_model.prog['PROCEDURE']
    business_variabes, statements, paragraphs = procedure_division(code,variables)
    statements = build_cfg(statements, paragraphs)
    extract_execution_path(variables["BAG"],statements)