**************************************
Pyformula is an easy to use mathematical formula interpreter written in pyhton.
Written by Gerson Garcia dos Santos
contact: gersongs@gmail.com
May, 2020
This software is completely free for any kind of use or modification.
**************************************

Example of use:

import pyformula as pf
formula = pf.Formula("(2)*(5-3)*10*(-1)")
print(formula.getValue())

Some functions are also available:

>>> pf.Formula("asin(1)*2").getValue()
3.141592653589793