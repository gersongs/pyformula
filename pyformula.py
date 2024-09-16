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
import os.path
import sys

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

def isFalse(x):
    return not isTrue(x)

def fact(x):
    if(x<=1):
        return 1
    return x * fact(x-1)
    
class Stack:
    def __init__(self):
        self.vet = []
        
    def push(self, n):
        self.vet.append(n)
        
    def pop(self):
        if len(self.vet) == 0:
            return None
        return self.vet.pop()
        
    def depth(self):
        return len(self.vet)
        
    def top(self):
        if len(self.vet) == 0:
            return None
        return self.vet[len(self.vet)-1]


class Node:
    def __init__(self, parentFormula = None):
        self.bIsVisited = False
        self.nodes = list()
        self.name = ""
        self.the_completeName = ""
        self.theFormula = parentFormula
        
    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False
        
    def completeName(self):
        self.the_completeName = "" #reseting the complete name in case of reorganizing the nodes

        if len(self.nodes) == 0:
            return self.name

        if self.the_completeName != "":
            return self.the_completeName

        self.the_completeName = self.name + "("
        
        if len(self.nodes) != 0:
            self.the_completeName += self.nodes[0].completeName()
            
        for i in range(1, len(self.nodes)):
            self.the_completeName += "," + self.nodes[i].completeName()

        self.the_completeName += ")"

        return self.the_completeName
        
    def getValue(self):
        if(self.bIsVisited):
            raise Exception("Circular reference.")
            #pass
        self.bIsVisited = True
        #return None

    def setVisited(self, visited):
        self.bIsVisited = visited
    
class Literal(Node):
    def __init__(self, value = None, parentFormula = None):
        super(Literal, self).__init__(parentFormula)
        self.value = value
        self.name = str(value)
        self.theFormula = parentFormula

        if self.theFormula is not None:
            if self.theFormula.callback is not None:
                self.theFormula.callback(self)
        
    def getValue(self):
        #super().getValue()
        if isNumber(self.value):
            return float(self.value)
        return self.value #not numeric value - for future implementations
        
class Variable(Node):
    def __init__(self, expresssion, parentFormula, strName): #, formula, expression = None):
        super(Variable, self).__init__(parentFormula)
        self.innerFormula = Formula(expresssion)
        self.innerFormula.parentFormula = parentFormula
        self.name = strName

        if self.theFormula is not None:
            if self.theFormula.callback is not None:
                self.theFormula.callback(self)

    def getValue(self):
        super().getValue()
        returnValue = self.innerFormula.getValue()
        self.bIsVisited = False
        return returnValue

class Name(Node):
    #all the names must point to the uper formula
    def __init__(self, name, parentFormula = None):
        super(Name, self).__init__(parentFormula)
        self.name = name
        self.theFormula = parentFormula

        if self.theFormula is not None:
            if self.theFormula.callback is not None:
                self.theFormula.callback(self)

    def getValue(self):
        #super().getValue()
        if self.name not in self.theFormula.variables:
            raise Exception("Variable \"" + self.name + "\" not defined.")

        return self.theFormula.variables[self.name].getValue()

        
class Function(Node):
    functionsCreated = False
        
    def __init__(self, name = "", parentFormula = None):
        #if not functionsCreated:
            #functionsCreated = True
        #createFunctions()

        #print("estou no construtor de Function")
        super(Function, self).__init__(parentFormula)
        #print("vou setar o name " + name)
        self.name = name
        #print("setei o name " + self.name)
        
        
        #self.nodes = list()
        #self.name = ""

        self.theFormula = parentFormula

        #if self.theFormula is None:
            #self.theFormula = self

        if self.theFormula is not None:
            if self.theFormula.callback is not None:
                self.theFormula.callback(self)
            
    def __eq__(self, other):
        if not (self.name == other.name):
            return False
            
        if len(self.nodes) == len(other.nodes):
            return True
        
        return False
    
    def getValue(self):
        #super().getValue()
        #return None
        #pass
        #print("vou buscar a funcao " + self.name)
        
        #the discovering of the function is lazy now. just in evaluation time:
        theFunction = Function.getFunctionByName(self.name)
        if theFunction is None:
            raise Exception("Function \"" + self.name + "\" not found.")

        for node in self.nodes:
            theFunction.nodes.append(node)
            
        return theFunction.getValue()

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
        Function.functions["istrue"] = IsTrue
        Function.functions["parenthesis"] = Parenthesis
        Function.functions["unaryplus"] = UnaryPlus
        Function.functions["sum"] = Sum
        Function.functions["sub"] = Sub
        Function.functions["mul"] = Mul
        Function.functions["div"] = Div
        Function.functions["integerdiv"] = IntegerDiv
        Function.functions["mod"] = Mod
        Function.functions["if"] = If
        Function.functions["neg"] = Neg
        Function.functions["pow"] = Pow
        Function.functions["e"] = E
        Function.functions["pi"] = Pi
        Function.functions["fact"] = Fact
        Function.functions["equals"] = Equals
        Function.functions["notequals"] = NotEquals
        Function.functions["lt"] = Lt
        Function.functions["gt"] = Gt
        Function.functions["lte"] = Lte
        Function.functions["gte"] = Gte
        Function.functions["floor"] = Floor
        Function.functions["ceil"] = Ceil
        Function.functions["min"] = Min
        Function.functions["max"] = Max
        Function.functions["sqrt"] = Sqrt
        Function.functions["exp"] = Exp
        Function.functions["log"] = Log
        Function.functions["trunc"] = Trunc
        Function.functions["round"] = Round
        Function.functions["sin"] = Sin
        Function.functions["cos"] = Cos
        Function.functions["tan"] = Tan
        Function.functions["asin"] = Asin
        Function.functions["acos"] = Acos
        Function.functions["atan"] = Atan
        Function.functions["not"] = Not
        Function.functions["and"] = And
        Function.functions["or"] = Or        
        Function.functions["implication"] = Implication
        Function.functions["double_implication"] = DoubleImplication
        Function.functions["variable"] = VariableDefinition
        Function.functions["define"] = Definition
        Function.functions["concatenate"] = Concatenation

#--------------------END OF EXTERNAL FUNCTIONS------

    @staticmethod
    def getFunctionByName(name):
        if name in Function.functions:
            return Function.functions[name](name) #instantiates tne function
        return None
    
class Formula:
    
    special_symbols = set(["!", "@", "#", "$", "%", "&", "*", "-", "+", "=", "/", "\\", "|", "^", "~", "?", "<", ">", ":", ";"])
    
    parentFormula = None

    def __init__(self, expression = "", autoCompile = False, callback_function = None):
        
        Operator(None, None, None, None) #just to invoke the static constructor of Operator class
    
        self.callback = None

        Function.createFunctions()
      
        self.expression = expression.replace(" ","")
        self.variables = {}
        self.root = None
        self.isCompiled = False
        
        if autoCompile:
            self.compile()
            
        if callback_function is not None:
            self.callback = callback_function
            
    def set_expression(self, new_expression):
        self.expression = new_expression.replace(" ","")
        self.isCompiled = False
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Formula):
            return self.expression == other.expression
        return False

    def completeName(self):
        if not self.isCompiled:
            self.compile()
    
        return self.root.completeName()

    def replace_symbol(self, old_symbol, new_symbol, node = None):

        if self.root is None:
            return

        if node is None:
            node = self.root
            if self.root.name == old_symbol:
                if isinstance(new_symbol, str):
                    self.root = Formula(new_symbol, True).root
                else:
                    self.root = new_symbol

        if node is None:
            return
        if len(node.nodes) == 0:
            return

        i = 0
        while i < len(node.nodes):
            if node.nodes[i].name == old_symbol:
                if isinstance(new_symbol, str):
                    node.nodes[i] = Formula(new_symbol, True).root
                else:
                    node.nodes[i] = new_symbol
            else:
                self.replace_symbol(old_symbol, new_symbol, node.nodes[i])

            i += 1
        
    def print_tree(self, node = None, depth = 0, stackTemp = []):
        if not self.isCompiled:
            self.compile()
            
        strSaida = ""
        strIdent = ""
        
        if node is None:
            node = self.root
        
        for i in range(0, depth-1):
            if stackTemp[i]:
                strIdent += " |"
            else:
                strIdent += "  "
              
        if depth != 0:
            strIdent += " |"    
        
        strTemp = strIdent
        if depth != 0:
            strTemp += "->"
        strTemp += node.name
        
        #print(strTemp)
        strSaida += strTemp
        
        i = 0
        for n in node.nodes:
            if (i != len(node.nodes)-1):# or (len(node.nodes)==1):
                stackTemp.append(True)
            else:
                stackTemp.append(False)
                
            strSaida += "\n" + self.print_tree(n, depth+1, stackTemp)

            i += 1
            
        if len(stackTemp) != 0:
            stackTemp.pop()   

        return strSaida
        
    def prepare_traversal(self):
        if not self.isCompiled:
            self.compile()
            
        self.currentNode = self.root
        self.stackNodes = Stack()
        self.stackOrdinals = Stack()
        self.stackOrdinals.push(-1)
        
    def node_up(self):        
        self.stackOrdinals.pop()
        #self.stackOrdinals.push(-1)
        self.currentNode = self.stackNodes.pop()
        
    def next_node(self):
        if self.currentNode is None:
            return            
        
        if len(self.currentNode.nodes) == 0:
            self.node_up()
            self.next_node()
            return
            
        if self.stackOrdinals.top() == (len(self.currentNode.nodes) - 1):
            self.node_up()
            self.next_node()
            return
                
        nextChild = self.stackOrdinals.pop() + 1
        self.stackNodes.push(self.currentNode)
        self.currentNode = self.currentNode.nodes[nextChild]
        self.stackOrdinals.push(nextChild)
        self.stackOrdinals.push(-1)
        
        
    def name_occurs(self, varName, node=None):        
        if node is None:
            node = self.root
            
        #print(type(node))
        
        if type(node) is Name:
            if node.name == varName:
                return True
            return False
                
        if isinstance(node, Function):
            for n in node.nodes:
                if self.name_occurs(varName, n):
                    return True
            return False
            
    def setVariable(self, name, expression):
        #self.variables[name] = Variable(name, expression, self)
        strName = name.replace(" ","")
        self.variables[strName] = Variable(expression, self, strName)

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
        if s in Formula.special_symbols:
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
        minPriority=999999
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
                
                if self.expression[i+1:j+1] not in Operator.operators.keys():
                    
                    b_found = False
                    
                    #The substring is nos a simple operator. We need to detect the operator within the expression.
                    str_operators = self.expression[i+1:j+1]
                    
                    for op_temp in Operator.get_operators_by_priority():# Operator.operators.keys():
                        index_str_operator = str_operators.find(op_temp.symbol)
                        if index_str_operator >= 0:
                            b_found = True
                            i += index_str_operator
                            j = i + len(op_temp.symbol)
                            break
                                
                    if not b_found:
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
                else:
                    j = i# - 1

            j-=1

        if operatorMinPriority is not None:
            #print("operador: " + str(operatorMinPriority.implementingFunction) + "\n")
            #returnValue = operatorMinPriority.implementingFunction(operatorMinPriority.implementingFunction.__name__, self)
            returnValue = Function.getFunctionByName(operatorMinPriority.implementingFunction)
            if( (operatorMinPriority.termsPosition & Operator.POSITION_LEFT) != 0):
                returnValue.nodes.append(self.compileNode(pos1, opInit-1))
            if( (operatorMinPriority.termsPosition & Operator.POSITION_RIGHT) != 0):
                returnValue.nodes.append(self.compileNode(opEnd+1, pos2))
        else:
            if self.expression[pos1] == "(":
                #returnValue = Parenthesis(Parenthesis.__name__, self)
                returnValue = Parenthesis("parenthesis", self)
                returnValue.nodes.append(self.compileNode(pos1+1, pos2-1))
                #return returnValue
            else:
                if Formula.isTermInitialSymbol(self.expression[pos1]):
                    if "(" in self.expression[pos1:pos2]:
                        k = self.expression[pos1:pos2].find("(")
                        #returnValue = Function.getFunctionByName(self.expression[pos1:k+pos1])
                        returnValue = Function(self.expression[pos1:k+pos1], self)
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
                    if self.parentFormula is None:
                        returnValue=Literal(self.expression[pos1:pos2+1], self) #, None, self)
                    else:
                        returnValue=Literal(self.expression[pos1:pos2+1], self.parentFormula) #, None, self)

        return returnValue
        
    def compile(self):
        if self.isCompiled:
            return
            
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
        
    def setOperators(oprs):
        Operator.setOperators(oprs)


#----------------INTERNAL FUNCTIONS------------
class IsTrue(Function):
    def getValue(self):
        #super().getValue()
        return isTrue(nodes[0])
    
class Parenthesis(Function): #no operation
    def getValue(self):
        #super().getValue()
        return self.nodes[0].getValue()
    
class UnaryPlus(Function): #no operation
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
        
class Implication(Function):
    def getValue(self):
        if isTrue(self.nodes[1].getValue()):
            return 1.0
        if isTrue(self.nodes[0].getValue()):
            return 0.0
        return 1.0
    
class DoubleImplication(Function):
    def getValue(self):       
        a = self.nodes[0].getValue()
        b = self.nodes[1].getValue()
        
        if isTrue(a) & isTrue(b):
            return 1.0
        
        if isFalse(a) & isFalse(b):
            return 1.0     

        return 0.0

class VariableDefinition(Function):
    def getValue(self):        
        return 1.0

class Definition(Function):
    def getValue(self):        
        return 1.0
        
class Concatenation(Function):
    def getValue(self):        
        return 1.0

#----------------END OF INTERNAL FUNCTIONS-----

#----------------OPERATORS-----
#The operatros are stored in a dictionary of dictionary. The first index is the symbol of the operator.
#The secont is the position of terms (left, right or both), that depends on if the operation is unary or not and the position of the terms.
#For example, the symbol "-" can represent the unary operator "-", like in "-2" or the binary operator "-", like in "3-2". In the
#first example, "-" is a RIGHT operator , because the operand is in the right. In the second example, the operator has it operands
# in both left and right of the operator symbol.
#Operator.POSITION_LEFT and Operator.POSITION_RIGHT are integers that are used as bit vectors (1 is the rightmost bit and 2 is the second bit).
        

class Operator:
    POSITION_LEFT = 2
    POSITION_RIGHT = 1
    operatorsCreated = False

    def __init__(self, symbol, implementingFunction, termsPosition, priority):
        if not Operator.operatorsCreated:
            Operator.operatorsCreated = True
            Operator.createDefaultOperators()

        self.symbol = symbol
        self.termsPosition = termsPosition
        self.implementingFunction = implementingFunction
        self.priority = priority
        
    def setOperators(oprs):
        Operator.operators = oprs
        #Operator.operatorsCreated = True
        
        Operator.index_operators()
        
    def createDefaultOperators():

        lines=[
        "->	3	implication	1",
        "<->	3	double_implication	1",
        "==	3	equals	2",
        "<	3	lt	2",
        ">	3	gt	2",
        "<=	3	lte	2",
        ">=	3	gte	2",
        "!=	3	notequals	2",
        "<>	3	notequals	2",
        "+	3	sum	5",
        "-	3	sub	5",
        "*	3	mul	10",
        "/	3	div	10",
        "\	3	integerdiv	10",
        "%	3	mod	10",
        "|	3	or	14",
        "&	3	and	15",
        "^	3	pow	20",
        "**	3	pow	20",
        "+	1	unaryplus	999",
        "-	1	neg	999",
        "!	1	not	999",
        "!	2	fact	1000"
        ]

        dic_temp = {}
        
        for line in lines:
            [symbol, operator] = Operator.readOperatorFromInputLine(line)

            if symbol not in dic_temp:
                dic_temp[symbol] = {}
            dic_temp[symbol][operator.termsPosition] = operator

        Operator.setOperators(dic_temp)
        
    
    def readOperatorFromInputLine(line):
        vet = re.split(r'\t+', line)
        symbol = vet[0]
        positions = int(vet[1])
        function = vet[2]
        priority = int(vet[3])
        return symbol, Operator(symbol, function, positions, priority)
        
        
    def readOperatorsFromFile(filename):
        f = open(filename, "r")
        dic_temp = {}
        
        i = -1
        
        for line in f:
            i += 1

            if i == 0: #head
                continue
            
            [symbol, operator] = Operator.readOperatorFromInputLine(line)

            if symbol not in dic_temp:
                dic_temp[symbol] = {}
            dic_temp[symbol][operator.termsPosition] = operator
            
        f.close()
        Operator.setOperators(dic_temp)


    def index_operators():
        
        Operator.list_priority_asc = []
        
        for value1 in Operator.operators.values():
            for value2 in value1.values():
                Operator.list_priority_asc.append(value2)
                
        Operator.list_priority_asc.sort(key=lambda x: x.priority, reverse=False)
        
    def get_operators_by_priority():
        return Operator.list_priority_asc
                
        pass
        

