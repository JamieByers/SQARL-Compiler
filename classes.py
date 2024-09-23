from typing import List, Optional, Union
from dataclasses import dataclass, field

@dataclass
class ASTNode:
    type: str
    code: str = field(default=None, init=False)

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    initial_value: Union[str, int, float, bool]
    var_type: Optional[Union[str,type]]

@dataclass
class VariableAssignment(ASTNode):
    name: str
    value: Union[str, int ,float, bool]


@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    params : List[str]
    code_block: Union[List[ASTNode]]
    return_type: Optional[str]

@dataclass
class IfStatement(ASTNode):
    condition: "Expression"
    code_block: Union[List[ASTNode]]
    else_block: str
    else_if_block: str

@dataclass
class WhileStatement(ASTNode):
    condition: "Expression"
    code_block: Union[List[ASTNode]]

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
    value:  Union[str, int, float, bool, 'Expression'] = None

@dataclass
class Condition(ASTNode):
    value: Union[str, int, float, bool, 'Expression'] = None

@dataclass
class Parameter:
    type: Union[str] = ""
    value: str = ""
