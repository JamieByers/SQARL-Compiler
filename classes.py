from typing import List, Optional, Union
from dataclasses import dataclass

@dataclass
class ASTNode:
    type: str

@dataclass
class Program:
    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    initial_value: Union[str, int, float, bool]
    var_type: str

@dataclass
class VariableAssignment:
    name: str
    value = Union[str, int ,float, bool]


@dataclass
class FunctionDeclaration:
    name: str
    params : List[str]
    code_block: List[ASTNode]
    return_type: Optional[str]

@dataclass
class IfStatement:
    condition: "Expression"
    code_block: List[ASTNode]
    else_block: Optional[List[ASTNode]]

@dataclass
class WhileStatement:
    condition: "Expression"
    code_block: List[ASTNode]

@dataclass
class ForStatement:
    variable: str
    start: str
    end: str
    step: Optional[Union[int, "Expression"]]
    code_block: List[ASTNode]

@dataclass
class ReturnStatement:
    value: Union[str, int, float, bool, "Expression"]


