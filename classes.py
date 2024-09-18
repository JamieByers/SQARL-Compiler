from typing import List, Optional, Union
from dataclasses import dataclass

@dataclass
class ASTNode:
    type: str

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    initial_value: Union[str, int, float, bool]
    var_type: str

@dataclass
class VariableAssignment(ASTNode):
    name: str
    value = Union[str, int ,float, bool]


@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    params : List[str]
    code_block: List[ASTNode]
    return_type: Optional[str]

@dataclass
class IfStatement(ASTNode):
    condition: "Expression"
    code_block: List[ASTNode]
    else_block: Optional[List[ASTNode]]

@dataclass
class WhileStatement(ASTNode):
    condition: "Expression"
    code_block: List[ASTNode]

@dataclass
class ForStatement(ASTNode):
    variable: str
    start: str
    end: str
    step: Optional[Union[int, "Expression"]]
    code_block: List[ASTNode]

@dataclass
class ReturnStatement(ASTNode):
    value: Union[str, int, float, bool, "Expression"]

@dataclass
class Expression(ASTNode):
    operator: str
    left: Union[str, int, float, bool, 'Expression']
    right: Optional[Union[str, int, float, bool, 'Expression']] = None

@dataclass
class SimpleStatement(ASTNode):
    value:  Union[str, int, float, bool, 'Expression'] = None
