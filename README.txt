**************************************
Pyformula is an easy to use flexible mathematical formula interpreter written in Python.
Written by Gerson Garcia dos Santos
contact: gersongs@gmail.com
May, 2020
This software is completely free for any kind of use or modification.
**************************************

Example of use:
>>> import pyformula as pf
>>> formula = pf.Formula("2+4*5")
>>> formula.getValue()
22.0

IMPORTANT: All computations are carried out using float numbers.

Any number os parenthesis are allowed:
>>> formula = pf.Formula("(2+4)*5")
>>> formula.getValue()
30.0

>>> formula = pf.Formula("(((((2+4)))))*5")
>>> formula.getValue()
30.0

All the basic aritmetic operators are implemented, as well as some functions:
>>> formula = pf.Formula("sqrt(3^2+4^2)") #sqrt: square root
>>> formula.getValue()
5.0

It´s possible to define variables:
>>> formula = pf.Formula("(1+1/N)^N") #approximation of Euler´s number
>>> formula.setVariable("N", "100000")
>>> formula.getValue()
2.7182682371922975

A variable can be another formula:
>>> x1 = pf.Formula("(-b-sqrt(delta))/(2*a)") #quadratic formula
>>> x2 = pf.Formula("(-b+sqrt(delta))/(2*a)") #quadratic formula
>>> x1.setVariable("a","1")
>>> x2.setVariable("a","1")
>>> x1.setVariable("b","-5")
>>> x2.setVariable("b","-5")
>>> x1.setVariable("c","6")
>>> x2.setVariable("c","6")
>>> x1.setVariable("delta","b^2-4*a*c") #another formula
>>> x2.setVariable("delta","b^2-4*a*c") #another formula
>>> x1.getValue()
2.0
>>> x2.getValue()
3.0

Many common mathematical functions are implemented: 
>>> formula = pf.Formula("asin(1)*2") #arcsin
>>> formula.getValue()
3.141592653589793

IMPORTANT: In all comparisons, a value different from 0 is considered as true,
and 0 is false. The tolerance is abs(x)>=0.001. Similarly, when an operations results true, 
it returns 1.0, or returns 0.0 otherwise:
>>> formula = pf.Formula("1 + 1 == 2")
>>> formula.getValue()
1.0
>>> formula = pf.Formula("1 + 1 == 3")
>>> formula.getValue()
0.0

Logical operators are also implemented:
>>> formula = pf.Formula("A & B -> C")
>>> formula.setVariable("A", "1")
>>> formula.setVariable("B", "1")
>>> formula.setVariable("C", "1")
>>> formula.getValue()
1.0

Variable substitutions can be done. Call the completeName functions to see a canonical form of the formula.
>>> formula = pf.Formula("Mortal(x)")
>>> formula.completeName()
'Mortal(x)'
>>> formula.replace_symbol("x", "Socrates")
>>> formula.completeName()
'Mortal(Socrates)'

From the above example we can see the Pyformula can parse a formula even if 
a function in the formula is not defined (function Mortal() in the example).

Once the formula is defined, we can call the print_tree function to friendly print 
a execution tree of the formula, even if there is a undefined variable:
>>> formula = pf.Formula("a+b/c^d")
>>> print(formula.print_tree())
sum
 |->a
 |->div
   |->b
   |->pow
     |->c
     |->d


Another example of the print_tree function:
>>> formula = pf.Formula("(a+b)^2")
>>> print(formula.print_tree())
pow
 |->parenthesis
 | |->sum
 |   |->a
 |   |->b
 |->2
 
The most important feature of Pyformula is to define, at run time, a operator, through 
the reading of a file:
>>> pf.Operator.readOperatorsFromFile("operators.txt")

Here is an example of an operators file:
symbol	operands_left_or_right	function	priority
->	3	implication	1
==	3	equals	2
<	3	lt	2
>	3	gt	2
<=	3	lte	2
>=	3	gte	2
!=	3	notequals	2
<>	3	notequals	2
+	3	sum	5
-	3	sub	5
*	3	mul	10
/	3	div	10
\	3	integerdiv	10
%	3	mod	10
|	3	or	14
&	3	and	15
^	3	pow	20
**	3	pow	20
+	1	unaryplus	999
-	1	neg	999
!	1	not	999
!	2	fact	1000

The operator file is a ascii file of tab-separated columns. The first line is ignored.

- First column (symbol): the operator itself.

- Second column (operands_left_or_right): a number (1, 2 or 3) that defines if the operator have one or two operands and, 
if it has only one operand, whether it is on the left or on the right.
The  column is interpreted as a bit map, in the following way:
If the operator has only a left operand, the left bit is set to 1:							10
If the operator has only a right operand, the left bit is set to 1:							01
If the operator has a left and a right operand, a bitwise "or" is done from 10 and 01:		11

- Third column (function): the internal name of the implementing function of the operator.

- Fourth column (priority): the relative priority of the operator. The bigger the number, the higher the priority.

As we can realize, the same symbol is defined more than one time in the example above. 
For example:

3! means "three factorial"
!3 means "not three" (logical "not")

>>> formula = pf.Formula("3!")
>>> formula.getValue()
6.0
>>> formula = pf.Formula("!3") #remember that in Pyformula any value different from zero is true.
>>> formula.getValue()
0.0
>>> formula = pf.Formula("!3!")
>>> formula.getValue()
0.0

That great flexbility enable us to define any operator we want, using the internal formulas. 
For example, let´s define the operator "!", that will take both left and right operands, and returns the sum between them.
To acomplish that, let´s append to the operands file the line below:

!	3	sum	5

Then we reload the operands file and run a test:
>>> pf.Operator.readOperatorsFromFile("operators.txt")
>>> formula = pf.Formula("2!3")
>>> formula.getValue()
5.0

