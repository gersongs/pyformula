import pyformula as pf

formula = pf.Formula("(-b-sqrt(delta))/(2*a)")
#formula = pf.Formula("(-b+sqrt(delta))/(2*a)")
#formula = pf.Formula("func(x,y,func(z1,z2,z3))")
#formula = pf.Formula("pi()")
#formula = pf.Formula("2+3^2-2*5")

formula.setVariable("a","1")
formula.setVariable("b","-5")
formula.setVariable("c","6")
formula.setVariable("delta","b^2-4*a*c")
formula.compile()

#print("resultado: " + str(formula.getValue()))
print(formula.expression)
print(formula.print_tree())
print(formula.root.completeName())
print(formula.getValue())