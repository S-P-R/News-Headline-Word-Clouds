"""
File: filter_parser.py
Author: Sean Reilly
Description: Contains functionality used to lex and parse the $filter query 
             parameter that's accepted by the API's GET routes, creating
             SQLAlchemy objects that can be used to make
             database queries

             The syntax expected by the lexer and parser is inspired by the 
             OData API specifications 
"""

import ply.lex as lex
import ply.yacc as yacc
from sqlalchemy import or_, and_
from exceptions import FilterParseException

def construct_parser(model):  
    """
    Creates a lexer and parser that can be used to parse OData-inspired $filters

    Args:
        model: An object that maps onto the database data that's being filtered

    Returns:
        A (parser, lexer) tuple
        parser: Used to parse the tokens created by the lexer, creating a 
                SQLAlchemy object that can be used to make database queries
        lexer: Converts a $filters string value into a series of tokens that 
               can then be parsed
    
    Notes: 
        Variables and inner functions that are seemingly unused are used by
        ply to create the lexer and parser.
        Despite lexers being independent of a specific model unlike parsers, I 
        couldn't find a way to create a lexer and parser in seperate functions
    """
    ops = {
        'and' : 'AND',
        'or' : 'OR',
        'eq' : 'EQ',
        'neq' : 'NEQ',
        'ge' : 'GE',
        'gt' : 'GT',
        'le' : 'LE',
        'lt' : 'LT',
    }

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
    )

    tokens = ['FIELD_NAME', 'STRING_VAL', 'NUM_VAL', 'LPAREN', 'RPAREN'] + list(ops.values())

    ##########################
    # ####### LEXING ####### #
    ##########################

    # Match a character from alphabet or '_', followed by any number of alphanumeric 
    # characters or '_'s, followed by whitespace
    def t_FIELD_NAME(t):
        r'[a-zA-Z_][\w]*'
        # Prevents ops from being lexed as field names
        t.type = ops.get(t.value,'FIELD_NAME') 
        return t

    # Match characters enclosed by single quotes, single quotes can be escaped 
    # with another single quote in accordance with the OData specifications
    def t_STRING_VAL(t):
        r'\'([^\']|\'\')*\'' 
        t.value = t.value[1:-1] # Stop outer quotes from being included in string
        return t

    def t_NUM_VAL(t):
        r'[+-]?(\d+(\.\d*)?|\.\d+)'
        t.value = float(t.value)    
        return t

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    lexer = lex.lex()

    ###########################
    # ####### PARSING ####### #
    ###########################

    def p_expression_parens(p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_and(p):
        'expression : expression AND expression'
        p[0] = and_(p[1], p[3])

    def p_expression_or(p):
        'expression : expression OR expression'
        p[0] = or_(p[1], p[3])

    def p_expression_constraint(p):
        'expression : constraint'
        p[0] = p[1]

    def p_value(p):
        '''value : NUM_VAL 
                | STRING_VAL'''
        p[0] = p[1]

    def p_constraint(p):
        '''constraint : FIELD_NAME EQ value
                    | FIELD_NAME NEQ value
                    | FIELD_NAME GE value
                    | FIELD_NAME GT value
                    | FIELD_NAME LE value
                    | FIELD_NAME LT value'''
        if p[1] not in model.__table__.columns:
            column_names = str([column.name for column in model.__table__.columns])
            raise FilterParseException(f"Properties in $filter must be one of {column_names}")
        # uses model's type annotations (if present) to check that the value
        # is of the correct type
        elif (p[1] in model.__annotations__ and model.__annotations__[p[1]] != type(p[3])):
            raise FilterParseException(f"Values used to constrain {p[1]} must be "
                                       f"of type {model.__annotations__[p[1]].__name__}, "
                                       f"not {type(p[3]).__name__}")
        elif p[2] == 'eq':
            p[0] = (getattr(model, p[1]) == p[3])
        elif p[2] == 'neq':
            p[0] =  p[0] = (getattr(model, p[1]) != p[3])
        elif p[2] == 'ge':
            p[0] = (getattr(model, p[1]) >= p[3])
        elif p[2] == 'gt':
            p[0] = (getattr(model, p[1]) > p[3])
        elif p[2] == 'le':
            p[0] = (getattr(model, p[1]) <= p[3])
        elif p[2] == 'lt':
            p[0] = (getattr(model, p[1]) < p[3])

    def p_error(p):
        raise FilterParseException("Invalid $filter syntax")

    parser = yacc.yacc()
    return (parser, lexer)