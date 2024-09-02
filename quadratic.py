import pyformula as pf

#Quadratic formula:
x1 = pf.Formula("(-b-sqrt(delta))/(2*a)")
x2 = pf.Formula("(-b+sqrt(delta))/(2*a)")
x1.setVariable("a","1")
x2.setVariable("a","1")
x1.setVariable("b","-5")
x2.setVariable("b","-5")
x1.setVariable("c","6")
x2.setVariable("c","6")
x1.setVariable("delta","b^2-4*a*c")
x2.setVariable("delta","b^2-4*a*c")
print(x1.getValue())
print(x2.getValue())

print(x1.root.completeName())
print(x1.print_tree())