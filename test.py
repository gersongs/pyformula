import pyformula as pf

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

#print(formula.getValue())

#formula.unsetVariable("a")

#Baskhara´s formula:
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

#formula = pf.Formula("0|0|0|0|0")
#print(formula.getValue())

#formula = pf.Formula("(if(x<>0, 1/x, x))")
#formula.setVariable("x","4")

#Pythagora´s formula:
#formula = pf.Formula("sqrt(a^2+b^2)")
#formula.setVariable("a","3")
#formula.setVariable("b","4")

#approximation of "e":
# formula = pf.Formula("(1+1/(n))^(n)")
# formula.setVariable("n","100000")


# formula = pf.Formula("sum(2,3)")

#print(formula.getValue())


#print(formula.getValue())
#print(formula.getVariables())