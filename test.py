import pyformula as pf

def callback_function(obj):
   print("estou na callback_function. sou uma " + str(type(obj)) + ". meu nome eh: " + obj.name)

#formula = pf.Formula("sqrt(9)", False, callback_function)
#formula.compile()
#print(formula.getValue())

#formula = pf.Formula("pi(1)")
#formula = pf.Formula("sum()") #,3)")
#formula = pf.Formula("8\\3")
#formula = pf.Formula("(2)*(5-3)*10*(-1)")
#formula = pf.Formula("((5)!)-(9**0.5)")
#formula = pf.Formula("((11%3)^3)**(1/3)")
#formula = pf.Formula("(2)-3")
#formula = pf.Formula("sum(e(), pi(), 1)-5")
#formula = pf.Formula("if(1,2,3)")
#formula = pf.Formula("(3*2)==(12/2)")
#formula = pf.Formula("sum(1,2,3,4,5)")
#formula = pf.Formula("mul(1,2,3,4,5)-5!")
#formula = pf.Formula("mul(4.0,2,-5)")
#formula = pf.Formula("trunc(-2.9)")
#formula = pf.Formula("asin(1.0)*2")
#formula = pf.Formula("sin(pi()/2)^2+cos(pi()/2)^2")
#formula = pf.Formula("(pi()+pi())/2")
#formula = pf.Formula("5+(5+5+5+2+2)*2")
#formula = pf.Formula("log(e())")
#formula = pf.Formula("log(e()**(-3))")
#formula = pf.Formula(" 5   *           3     + 25 * 4-  2.5 *2*2")
#formula = pf.Formula(" -5*3.00+25*4-2.5*2*2")
#formula = pf.Formula("round(sin(pi()),4)")
#formula = pf.Formula("3+4")
#formula = pf.Formula(" -13+4 ")
#formula = pf.Formula("   5              ! ")
#formula = pf.Formula("a+b+c")
#formula.setVariable("a","sqrt(b)")
#formula.setVariable("b","sqrt(c)")
#formula.setVariable("c","81")
#formula.setVariable("a","5")

#callbacks = {}
#callbacks["Function"] = callback_function
#callbacks["Name"] = callback_name
#print(formula.getValue())

#formula.unsetVariable("a")

#Baskhara´s formula:
#x1 = pf.Formula("(-b-sqrt(delta))/(2*a)", False, callback_function)
#x2 = pf.Formula("(-b+sqrt(delta))/(2*a)", False, callback_function)
#x1.setVariable("a","1")
#x2.setVariable("a","1")
#x1.setVariable("b","-5")
#x2.setVariable("b","-5")
#x1.setVariable("c","6")
#x2.setVariable("c","6")
#x1.setVariable("delta","b^2-4*a*c")
#x2.setVariable("delta","b^2-4*a*c")
#print(x1.getValue())
#print(x2.getValue())

#x1.compile()

#formula = pf.Formula("0|0|0|0|0")
#print(formula.getValue())

#formula = pf.Formula("(if(x<>0, 1/x, x))")
#formula.setVariable("x","4")

#Pythagora´s formula:
#formula = pf.Formula("sqrt(a^2+b^2)")
#formula.setVariable("a","3")
#formula.setVariable("b","4")

#approximation of "e":
#formula = pf.Formula("(1+1/(n))^(n)", False, callback_function)
# formula.setVariable("n","100000")
#formula.compile()
#print(formula.print_tree())

# formula = pf.Formula("sum(2,3)")

# formula = pf.Formula("2*pi()")
# print(formula.getValue())

#print(pf.Formula("(4+5)^2").getValue())
#print(pf.Formula("6/2*(2+1)").getValue())

#formula = pf.Formula("3^2+((15-(3-sqrt(1))^2)*(7+(sqrt(100)/sqrt(25))^2))*2")
#formula = pf.Formula("2*sqrt(3)-1/3^(1/2)")

# formula = pf.Formula("F<->F")
# formula.setVariable("T", "1")
# formula.setVariable("F", "0")

formula = pf.Formula("a+b+c+d+e+f+g+h+i+j")
print(formula.expression)
print(formula.completeName())
print(formula.print_tree())

#print(formula.getValue())
#print(formula.getVariables())

#formula = pf.Formula("(x,y)")
#formula.compile()
#print(formula.print_tree())