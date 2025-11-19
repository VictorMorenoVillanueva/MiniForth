grammar forth;

program
    : element* EOF
    ;

element
    : definition
    | instruction
    ;

definition
    : COLON IDENT instruction* SEMI
    ;

instruction
    : IF trueBranch+=instruction* (ELSE falseBranch+=instruction*)? ENDIF   # ifInstr
    | NUMBER                                                                # numberInstr
    | IDENT                                                                 # callInstr
    | builtin                                                               # builtinInstr
    ;

builtin
    : DOT
    | DOTS
    | PLUS | MINUS | MULT | DIV | MOD
    | SWAP | TWOSWAP
    | DUP | TWODUP
    | OVER | TWOOVER
    | ROT
    | DROP | TWODROP
    | LT | LE | GT | GE | EQ | NEQ
    | AND | OR | NOT
    | RECURSE
    ;

// -------- TOKENS --------

// Palabras clave y símbolos
COLON   : ':' ;
SEMI    : ';' ;

IF      : 'if' ;
ELSE    : 'else' ;
ENDIF   : 'endif' ;
RECURSE : 'recurse' ;

PLUS  : '+' ;
MINUS : '-' ;
MULT  : '*' ;
DIV   : '/' ;
MOD   : 'mod' ;

DOT  : '.' ;
DOTS : '.s' ;

SWAP    : 'swap' ;
TWOSWAP : '2swap' ;
DUP     : 'dup' ;
TWODUP  : '2dup' ;
OVER    : 'over' ;
TWOOVER : '2over' ;
ROT     : 'rot' ;
DROP    : 'drop' ;
TWODROP : '2drop' ;

LT  : '<' ;
LE  : '<=' ;
GT  : '>' ;
GE  : '>=' ;
EQ  : '=' ;
NEQ : '<>' ;

AND : 'and' ;
OR  : 'or' ;
NOT : 'not' ;

// Nombres i números
NUMBER : '-'? [0-9]+ ;
IDENT  : [a-zA-Z_][a-zA-Z0-9_]* ;

// Comentarios i espai
COMMENT : '(' ~[)]* ')' -> skip ;
WS      : [ \t\r\n]+ -> skip ;
