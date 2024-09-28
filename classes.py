from typing import List, Optional, Union, Any
from dataclasses import dataclass

@dataclass
class ASTNode:
    type: str
    code: str


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class Token:
    type: str
    value: Union[str, int, float]

@dataclass
class VariableDeclaration(ASTNode):
    idenitifer: Any
    initial_value: Any
    var_type: Optional[Union[str,type]]

@dataclass
class VariableAssignment(ASTNode):
    idenitifer: Any
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
    step: Optional[Union[int, "Expression"]]
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
