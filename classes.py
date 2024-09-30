from typing import List, Optional, Union, Any
from dataclasses import dataclass

@dataclass
class ASTNode:
    type: str

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class Token:
    type: str
    value: Union[str, int, float]

@dataclass
class VariableDeclaration(ASTNode):
    identifier: Any
    initial_value: Any
    var_type: Optional[Union[str,type]]

@dataclass
class VariableAssignment(ASTNode):
    identifier: Any
    value: Any

@dataclass
class DisplayStatement(ASTNode):
    value: Any

@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    params : List[str]
    code_block: Union[List[ASTNode], str]
    return_type: Optional[str]
    returning_type: Any

@dataclass
class FunctionCall(ASTNode):
    idenitifer: str
    params: Union[str, int, float, bool, ASTNode, List[str]]
    value: Any

@dataclass
class IfStatement(ASTNode):
    condition: "Condition"
    code_block: Union[List[ASTNode], str]
    else_block: str
    else_if_block: str

@dataclass
class WhileStatement(ASTNode):
    condition: "Condition"
    code_block: Union[List[ASTNode], str]

@dataclass
class ForStatement(ASTNode):
    variable: str
    start: str
    end: str
    step: int
    code_block: Union[List[ASTNode], str]

@dataclass
class ForEachStatement(ASTNode):
    variable: str
    loop_from: str
    code_block: Union[List[ASTNode], str]

@dataclass
class ReturnStatement(ASTNode):
    value: Union[str, int, float, bool, "Expression"]

@dataclass
class Expression(ASTNode):
    value: Union[str, int, float, bool]

@dataclass
class SimpleStatement(ASTNode):
    value:  Union[str, int, float, bool, 'Expression'] = ""

@dataclass
class Condition(ASTNode):
    value: Union[str, int, float, bool, 'Expression'] = ""

@dataclass
class Parameter:
    value: str = ""
    type: str = ""

@dataclass
class ArrayElement(ASTNode):
    elements: List[Any]
    value: str

@dataclass
class ElifElement(ASTNode):
    condition: Union[str, Condition]
    code_block: List[ASTNode]

@dataclass
class ElseElement(ASTNode):
    code_block: List[ASTNode]
