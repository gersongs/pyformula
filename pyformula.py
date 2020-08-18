#**************************************
#Pyformula is an easy to use mathematical formula interpreter written in pyhton.
#Written by Gerson Garcia dos Santos
#contact: gersongs@gmail.com
#May, 2020
#This software is completely free for any kind of use or modification.
#**************************************

from enum import Enum
import math
import re

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def isTrue(x):
    if(abs(x)>=0.001):
        return True
    return False

def fact(x):
    if(x<=1):
        return 1
    return x * fact(x-1)


class Node:
    def __init__(self):
        self.bIsVisited = False
        
    def getValue(self):
        if(self.bIsVisited):
            raise Exception("Circular reference.")
            #pass
        self.bIsVisited = True
        #return None

    def setVisited(self, visited):
        self.bIsVisited = visited
    
class Literal(Node):
    def __init__(self, value = None):        
        super(Literal, self).__init__()
        self.value = value
        
    def getValue(self):
        #super().getValue()
        if isNumber(self.value):
            return float(self.value)
        return self.value #not numeric value - for future implementations
        
class Variable(Node):
    def __init__(self, expresssion, parentFormula): #, formula, expression = None):
        super(Variable, self).__init__()
        self.innerFormula = Formula(expresssion)
        self.innerFormula.parentFormula = parentFormula

    def getValue(self):
        super().getValue()
        returnValue = self.innerFormula.getValue()
        self.bIsVisited = False
        return returnValue

class Name(Node):
    #all the names must point to the uper formula
    def __init__(self, name, parentFormula):
        super(Name, self).__init__()
        self.name = name
        self.theFormula = parentFormula

    def getValue(self):
        #super().getValue()
        if self.name not in self.theFormula.variables:
            raise Exception("Variable \"" + self.name + "\" not defined.")

        return self.theFormula.variables[self.name].getValue()

        
class Function(Node):
    functionsCreated = False
        
    def __init__(self, name = ""):
        #if not functionsCreated:
            #functionsCreated = True
        #createFunctions()

        #print("estou no construtor de Function")
        super(Function, self).__init__()
        #print("vou setar o name " + name)
        self.name = name
        #print("setei o name " + self.name)
        
        
        self.nodes = list()
        #self.name = ""        
    
    def getValue(self):
        #super().getValue()
        #return None
        #pass
        #print("vou buscar a funcao " + self.name)
        
        #the discovering of the function is lazy now. just in evaluation time:
        theFuncion = Function.getFunctionByName(self.name)
        if theFuncion is None:
            raise Exception("Function \"" + self.name + "\" not found.")

        for node in self.nodes:
            theFuncion.nodes.append(node)
            
        return theFuncion.getValue()

    def setVisited(self, visited):
        super().setVisited(visited)
        for node in self.nodes:
            node.setVisited(visited)

#--------------------EXTERNAL FUNCTIONS------
    @staticmethod
    def createFunctions():
        # if if hasattr(a, 'property') is not None:
        if Function.functionsCreated:
            return

        Function.functionsCreated = True

        Function.functions = {}
        Function.functions["sum"] = Sum
        Function.functions["mul"] = Mul
        Function.functions["neg"] = Neg
        Function.functions["e"] = E
        Function.functions["pi"] = Pi
        Function.functions["if"] = If
        Function.functions["floor"] = Floor
        Function.functions["ceil"] = Ceil
        Function.functions["max"] = Max
        Function.functions["min"] = Min
        Function.functions["sqrt"] = Sqrt
        Function.functions["exp"] = E
        Function.functions["log"] = Log
        Function.functions["trunc"] = Trunc
        Function.functions["round"] = Round
        Function.functions["sin"] = Sin
        Function.functions["cos"] = Cos
        Function.functions["tan"] = Tan
        Function.functions["asin"] = Asin
        Function.functions["acos"] = Acos
        Function.functions["atan"] = Atan
        Function.functions["and"] = And
        Function.functions["or"] = Or

#--------------------END OF EXTERNAL FUNCTIONS------

    @staticmethod
    def getFunctionByName(name):
        if name in Function.functions:
            return Function.functions[name](name) #instantiates tne function
        return None
    
class Formula:    
    
    parentFormula = None
    def __init__(self, expression = ""):

        Function.createFunctions()
        Operator.createOperators()

        self.expression = expression.replace(" ","")
        self.variables = {}
        self.root = None
        self.isCompiled = False
            
    def setVariable(self, name, expression):
        #self.variables[name] = Variable(name, expression, self)
        self.variables[name.replace(" ","")] = Variable(expression, self)

    def unsetVariable(self, name):
        self.variables.pop(name, None)

    def getExpression(self):
        return self.expression

    def getVariables(self):
        returnList=[]
        for key in self.variables.keys():
            returnList.append([key, self.variables[key].innerFormula.expression])
        return returnList

    def isSpecialSymbol(s):
        if s in ["!", "@", "#", "$", "%", "&", "*", "-", "+", "=", "/", "\\", "|", "^", "~", "?", "<", ">", ":"]:
            return True
        return False

    def isTermInitialSymbol(s):
        if (ord('a') <= ord(s) <= ord('z')) or (ord('A') <= ord(s) <= ord('Z')) or s=='_':
            return True
        return False

    def findTuple(self, pos1, pos2):
        returnTuple = []
        levelParenthesis = 0

        commas = []
        for i in range(pos1, pos2):
            if self.expression[i] == "(":
                levelParenthesis += 1
            if self.expression[i] == ")":
                levelParenthesis -= 1
            if self.expression[i] == "," and levelParenthesis == 0:
                commas.append(i)

        #commas = list([m.start() for m in re.finditer(',', self.expression[pos1:pos2])])
        #k=0
        #for comma in commas:
            #returnTuple.append(self.compileNode(pos1+k, pos1+comma-1))
            #k=comma+1
        #if pos1!=pos2:
            #returnTuple.append(self.compileNode(pos1+k, pos2-1))
        k=pos1
        for comma in commas:
            returnTuple.append(self.compileNode(k, comma-1))
            k=comma+1
        if k!=pos2:
            returnTuple.append(self.compileNode(k, pos2-1))

        #while j<=pos2:
        #    if self.expression[j] == ",":
        #        if(len(returnTuple)==0):
        #            returnTuple.append(self.compileNode(i,j))
        #        else:
        #            returnTuple.append(self.compileNode(i+1,j-1))
        #        i = j
        #    j+=1
        #if i!=j:
        #    returnTuple.append(self.compileNode(i+1,pos2-1))

        return returnTuple

    def compileNode(self, pos1, pos2):
        levelParenthesis=0
        minPriority=9999
        opInit=0
        opEnd=0
        operatorMinPriority = None
        operator = None 

        j = pos2
        while j>=pos1:
            while (self.expression[j] == " ") and (j>pos1):
                j-=1

            if self.expression[j] == ")":
                levelParenthesis+=1

            if self.expression[j] == "(":
                levelParenthesis-=1
            
            if Formula.isSpecialSymbol(self.expression[j]) and (levelParenthesis==0):
                i=j-1

                while (i>=pos1) and Formula.isSpecialSymbol(self.expression[i]):
                    i-=1
                    
                #i=j-1

                #if i<pos1:
                    #i=pos1                    

                #print("operador: " + self.expression[i+1:j+1])
                
                if self.expression[i+1:j+1] not in Operator.operators:
                    raise Exception("Unknown operator \"" + self.expression[i+1:j+1] + "\"")

                operators = Operator.operators[self.expression[i+1:j+1]]

                iTermPositions=0

                #if (i>=pos1) and self.expression[pos1:i+1].replace(' ', '')!="":
                if self.expression[pos1:i+1].replace(' ', '')!="":
                    iTermPositions += Operator.POSITION_LEFT

                #if (j<pos2) and self.expression[j+1:pos2].replace(' ', '')!="":
                if(j<pos2):
                    if j+1==pos2:
                        right = self.expression[j+1:pos2+1]
                    else:
                        right = self.expression[j+1:pos2]

                    if right.replace(' ', '')!="":
                        iTermPositions += Operator.POSITION_RIGHT

                if iTermPositions not in operators:
                    raise Exception("Misuse of operator " + self.expression[i+1:j+1])

                operator = operators[iTermPositions]

                if operator.priority < minPriority:
                    minPriority=operator.priority
                    operatorMinPriority=operator
                    opInit=i+1
                    opEnd=j
                    j = opInit

            j-=1

        if operatorMinPriority is not None:
            #print("operador: " + str(operatorMinPriority.implementingFunction) + "\n")
            returnValue = operatorMinPriority.implementingFunction()
            if( (operatorMinPriority.termsPosition & Operator.POSITION_LEFT) != 0):
                returnValue.nodes.append(self.compileNode(pos1, opInit-1))
            if( (operatorMinPriority.termsPosition & Operator.POSITION_RIGHT) != 0):
                returnValue.nodes.append(self.compileNode(opEnd+1, pos2))
        else:
            if self.expression[pos1] == "(":
                returnValue = Nop()
                returnValue.nodes.append(self.compileNode(pos1+1, pos2-1))
                #return returnValue
            else:
                if Formula.isTermInitialSymbol(self.expression[pos1]):
                    if "(" in self.expression[pos1:pos2]:
                        k = self.expression[pos1:pos2].find("(")
                        #returnValue = Function.getFunctionByName(self.expression[pos1:k+pos1])
                        returnValue = Function(self.expression[pos1:k+pos1])
                        # if returnValue is None:
                            # raise Exception("Function \"" + self.expression[pos1:k+pos1] + "\" not found.")
                        if pos1+k < pos2-1:
                            parameters = self.findTuple(pos1+k+1, pos2)
                            for node in parameters:
                                returnValue.nodes.append(node)
                        #return returnValue
                    else:
                        if self.parentFormula is None:
                            returnValue = Name(self.expression[pos1:pos2+1], self)
                        else:
                            returnValue = Name(self.expression[pos1:pos2+1], self.parentFormula)
                        #return returnValue

                    #k1=pos1
                    #k2=pos2
                    #bHasParenthesis = False
                    #while k1<pos2:
                    #    if(self.expression[k1] == "("):
                    #        bHasParenthesis = True                            
                    #        while k2>k1:
                    #            if(self.expression[k2] == ")"):
                    #                break
                    #            k2-=1
                    #        break
                    #    k1+=1
                    #if (k1 != k2):
                    #    returnValue = Function.getFunctionByMnemonic(self.expression[pos1:k1])
                    #    if returnValue is None:
                    #        raise Exception("Function " + self.expression[pos1:k1] + " not found.")
                    #    if k2-k1>1:
                    #        parameters = self.findTuple(k1, k2)
                    #        for node in parameters:
                    #            returnValue.nodes.append(node)

                    #if not bHasParenthesis:
                    #    if self.parentFormula is None:
                    #        returnValue = Name(self.expression[pos1:k1+1], self)
                    #    else:
                    #        returnValue = Name(self.expression[pos1:k1+1], self.parentFormula)
                else:
                    #returnValue=Literal(float(self.expression[pos1:pos2+1]))
                    returnValue=Literal(self.expression[pos1:pos2+1])

        return returnValue
        
    def compile(self):
         #testing if the parenthesis are unbalanced:
        k = 0
        levelParenthesis=0
        while k<len(self.expression):
            if self.expression[k] == "(":
                levelParenthesis+=1
            if self.expression[k] == ")":
                levelParenthesis-=1            
            if levelParenthesis<0:
                raise Exception("Unbalanced parenthesis.")# at position " + str(k))
            k+=1
        if levelParenthesis!=0:
                raise Exception("Unbalanced parenthesis.")

        self.root = self.compileNode(0, len(self.expression)-1)
        self.isCompiled = True
        
    def getValue(self):
        if not self.isCompiled:
            self.compile()

        self.root.setVisited(False)
        return self.root.getValue()

    def setVisited(self, visited):
        self.root.setVisited(visited)

#----------------INTERNAL FUNCTIONS------------
class IsTrue(Function):
    def getValue(self):
        #super().getValue()
        return isTrue(nodes[0])
    
class Nop(Function): #no operation
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue()
    
class Sum(Function):
    def getValue(self):
        #super().getValue()
        dblReturn = 0.0
        for node in self.nodes:
            dblReturn += node.getValue()
        return dblReturn

class Sub(Function):
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue() - self.nodes[1].getValue()

class Mul(Function):
    def getValue(self):
        #super().getValue()
        dblReturn = 1.0
        for node in self.nodes:
            dblReturn *= node.getValue()
        return dblReturn

class Div(Function):
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue() / self.nodes[1].getValue()

class IntegerDiv(Function):
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue() // self.nodes[1].getValue()

class Mod(Function):
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue() % self.nodes[1].getValue()
    
class If(Function):
    def getValue(self):
        #super().getValue()
        if isTrue(self.nodes[0].getValue()):
            return self.nodes[1].getValue()
        return self.nodes[2].getValue()

class Neg(Function):
    def getValue(self):
        #super().getValue()
        return -self.nodes[0].getValue()

class Pow(Function):
    def getValue(self):
        #super().getValue()
        return pow(self.nodes[0].getValue(), self.nodes[1].getValue())

class E(Function):
    def getValue(self):
        #super().getValue()
        return math.e

class Pi(Function):
    def getValue(self):
        #super().getValue()
        return math.pi

class Fact(Function):
    def getValue(self):
        #super().getValue()
        return fact(self.nodes[0].getValue())

class Equals(Function):
    def getValue(self):
        #super().getValue()
        if(not isTrue(self.nodes[0].getValue() - self.nodes[1].getValue())):
            return 1.0
        return 0.0

class NotEquals(Function):
    def getValue(self):
        #super().getValue()
        if(isTrue(self.nodes[0].getValue() - self.nodes[1].getValue())):
            return 1.0
        return 0.0

class Lt(Function):
    def getValue(self):
        #super().getValue()
        if(self.nodes[0].getValue() < self.nodes[1].getValue()):
            return 1.0
        return 0.0

class Gt(Function):
    def getValue(self):
        #super().getValue()
        if(self.nodes[0].getValue() > self.nodes[1].getValue()):
            return 1.0
        return 0.0

class Lte(Function):
    def getValue(self):
        #super().getValue()
        if(self.nodes[0].getValue() <= self.nodes[1].getValue()):
            return 1.0
        return 0.0

class Gte(Function):
    def getValue(self):
        #super().getValue()
        if(self.nodes[0].getValue() >= self.nodes[1].getValue()):
            return 1.0
        return 0.0

class Floor(Function):
    def getValue(self):
        #super().getValue()
        return math.floor(self.nodes[0].getValue())

class Ceil(Function):
    def getValue(self):
        #super().getValue()
        return math.ceil(self.nodes[0].getValue())

class Min(Function):
    def getValue(self):
        #super().getValue()
        vet = []
        for node in self.nodes:
            vet.append(node.getValue())
        return min(vet)

class Max(Function):
    def getValue(self):
        #super().getValue()
        vet = []
        for node in self.nodes:
            vet.append(node.getValue())
        return max(vet)

class Sqrt(Function):
    def getValue(self):
        #super().getValue()
        return math.sqrt(self.nodes[0].getValue())

class Exp(Function):
    def getValue(self):
        #super().getValue()
        return math.exp(self.nodes[0].getValue())

class Log(Function):
    def getValue(self):
        #super().getValue()
        if len(self.nodes) == 2:
            return math.log(self.nodes[0].getValue(), self.nodes[1].getValue())
        else:
            return math.log(self.nodes[0].getValue())

class Trunc(Function):
    def getValue(self):
        #super().getValue()
        return math.trunc(self.nodes[0].getValue())

class Round(Function):
    def getValue(self):
        #super().getValue()
        if len(self.nodes) == 2:
            return round(self.nodes[0].getValue(), int(self.nodes[1].getValue()))
        else:
            return round(self.nodes[0].getValue())

class Sin(Function):
    def getValue(self):
        #super().getValue()
        return math.sin(self.nodes[0].getValue())

class Cos(Function):
    def getValue(self):
        #super().getValue()
        return math.cos(self.nodes[0].getValue())

class Tan(Function):
    def getValue(self):
        #super().getValue()
        return math.tan(self.nodes[0].getValue())

class Asin(Function):
    def getValue(self):
        #super().getValue()
        return math.asin(self.nodes[0].getValue())

class Acos(Function):
    def getValue(self):
        #super().getValue()
        return math.acos(self.nodes[0].getValue())

class Atan(Function):
    def getValue(self):
        #super().getValue()
        return math.atan(self.nodes[0].getValue())

class Not(Function):
    def getValue(self):
        return 0.0 if isTrue(self.nodes[0].getValue()) else 1.0

class And(Function):
    def getValue(self):
        for node in self.nodes:
            if not isTrue(node.getValue()):
                return 0.0
        return 1.0

class Or(Function):
    def getValue(self):
        for node in self.nodes:
            if isTrue(node.getValue()):
                return 1.0
        return 0.0

#----------------END OF INTERNAL FUNCTIONS-----
#----------------OPERATORS-----
class Operator:
    POSITION_LEFT = 2
    POSITION_RIGHT = 1
    operatorsCreated = False

    def __init__(self, implementingFunction, termsPosition, priority):
        if not Operator.operatorsCreated:
            operatorsCreated = True
            Operator.createOperators()            

        self.termsPosition = termsPosition
        self.implementingFunction = implementingFunction
        self.priority = priority

    @staticmethod
    def createOperators():
        if Operator.operatorsCreated:
            return

        Operator.operatorsCreated = True

        #Dictionary of dictionary. The first index is the symbol of the operator.
        #The secont is the position of terms (left, right or both), that depends on if the operation is unary or not and the position of the terms.
        #For example, the symbol "-" can reppresent the unary operator "-", like in "-2" or the binary operator "-", like in "3-2". In the
        #first example, "-" is a RIGHT operator , because the operand is in the right. In the second example, the operator has it operands
        # in both left and right of the operator symbol.
        #Operator.POSITION_LEFT and Operator.POSITION_RIGHT are integers that are used as bit vectors (1 is the rightmost bit and 2 is the second bit).
        Operator.operators = {}

        Operator.operators["+"] = {}
        Operator.operators["+"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Sum, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))
        Operator.operators["+"][Operator.POSITION_RIGHT] = (Operator(Nop, Operator.POSITION_RIGHT, 999)) #Simplesmente retorna o valor do literal

        Operator.operators["-"] = {}
        Operator.operators["-"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Sub, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))
        Operator.operators["-"][Operator.POSITION_RIGHT] = (Operator(Neg, Operator.POSITION_RIGHT, 999))

        Operator.operators["|"] = {}
        Operator.operators["|"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Or, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators["*"] = {}
        Operator.operators["*"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Mul, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 2))

        Operator.operators["/"] = {}
        Operator.operators["/"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Div, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 2))

        Operator.operators["\\"] = {}
        Operator.operators["\\"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(IntegerDiv, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 2))

        Operator.operators["%"] = {}
        Operator.operators["%"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Mod, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 2))

        Operator.operators["&"] = {}
        Operator.operators["&"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(And, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 2))

        Operator.operators["^"] = {}
        Operator.operators["^"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Pow, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 3))

        Operator.operators["**"] = {}
        Operator.operators["**"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Pow, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 3))

        Operator.operators["!"] = {}
        Operator.operators["!"][Operator.POSITION_LEFT] = (Operator(Fact, Operator.POSITION_LEFT, 999))
        Operator.operators["!"][Operator.POSITION_RIGHT] = (Operator(Not, Operator.POSITION_RIGHT, 999))

        Operator.operators["=="] = {}
        Operator.operators["=="][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Equals, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators["<"] = {}
        Operator.operators["<"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Lt, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators[">"] = {}
        Operator.operators[">"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Gt, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators["<="] = {}
        Operator.operators["<="][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Lte, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators[">="] = {}
        Operator.operators[">="][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(Gte, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators["!="] = {}
        Operator.operators["!="][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(NotEquals, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))

        Operator.operators["<>"] = {}
        Operator.operators["<>"][Operator.POSITION_LEFT + Operator.POSITION_RIGHT] = (Operator(NotEquals, Operator.POSITION_LEFT + Operator.POSITION_RIGHT, 1))
        
#----------------END OF OPERATORS-----
