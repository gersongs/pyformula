import pyformula as pf

#formula1 = pf.UnifiableFormula("func1(x,y,func2(z1,z2,z3), func3(a,b), w)")
formula1 = pf.Formula("x") #Knows(John, x)->Hates(John, x)")
formula2 = pf.Formula("Knows(John, Mary)")
#formula = pf.UnifiableFormula("func(x + y)")

formula1.prepare_traversal()
formula2.prepare_traversal()

print("formula1:")
print(formula1.print_tree())

print("formula2:")
print(formula2.print_tree())

#print(formula.nameOccurs("z"))

while True:
    if (formula1.currentNode is None) and (formula2.currentNode is None):
        break

    if formula1.currentNode is not None:
        print("formula1:")
        print(formula1.currentNode.completeName())
        formula1.next_node()
    
    if formula2.currentNode is not None:
        print("formula2:")
        print(formula2.currentNode.completeName())
        formula2.next_node()

print("ACABOU!")

