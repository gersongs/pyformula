import pyformula as pf

formula1 = pf.Formula("a+b+sin(c)") #Knows(John, x)->Hates(John, x)")
#formula2 = pf.Formula("Knows(John, Mary)")
#formula = pf.UnifiableFormula("func(x + y)")

formula1.prepare_traversal()
#formula2.prepare_traversal()

print("formula1:")
print(formula1.expression)
print(formula1.completeName())
print(formula1.print_tree())

#print("formula2:")
#print(formula2.print_tree())

#print(formula.nameOccurs("z"))

while True:
    if (formula1.currentNode is None):# and (formula2.currentNode is None):
        break

    #if formula1.currentNode is not None:
        #print("formula1:")
    print(formula1.currentNode.completeName())
    formula1.next_node()
    
    #if formula2.currentNode is not None:
    #    print("formula2:")
    #    print(formula2.currentNode.completeName())
    #    formula2.next_node()
    
print("FINISHED!")


