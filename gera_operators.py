import pyformula as pf

formula = pf.Formula("sum(1+2,+3)")

for key1, value1 in pf.Operator.operators.items():
    for key2, value2 in value1.items():
        strTemp = key1 + ";"
        strTemp += str(key2) + ";"
        strTemp += value2.implementingFunction + ";"
        strTemp += str(value2.priority)
        print(strTemp)