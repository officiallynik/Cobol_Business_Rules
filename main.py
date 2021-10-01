from model import Model

with open('input/shop.cbl') as f:
    code = f.read()
    cbl_model = Model()
    cbl_model.build_model(code)

    print(cbl_model.prog)