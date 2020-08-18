import pyformula as pf

#approximation of "e":
formula = pf.Formula("(1+1/n)^n")
formula.setVariable("n","100000")
print(formula.getValue())
