'''
test_filter_parser.py

Contains unit tests for the functionality of the HeadlineAPI that lexes and
parses the '$filter' query parameter
'''
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HeadlineAPI')))

from exceptions import FilterParseException
from filter_parser import construct_parser
from models import Headline, Source, DateSummary

@pytest.mark.parametrize("test_input, expected_token_strs", 
                         [
                             # test if a single constraint can be tokenized
                            ("property eq 'value'",
                                ["LexToken(FIELD_NAME,'property',1,0)", 
                                 "LexToken(EQ,'eq',1,9)", 
                                 "LexToken(STRING_VAL,'value',1,12)"]),
                            # test if boolean ops can be tokenized
                            ("property eq 'value' and property2 neq 3", 
                                ["LexToken(FIELD_NAME,'property',1,0)", 
                                 "LexToken(EQ,'eq',1,9)", 
                                 "LexToken(STRING_VAL,'value',1,12)", 
                                 "LexToken(AND,'and',1,20)",
                                 "LexToken(FIELD_NAME,'property2',1,24)", 
                                 "LexToken(NEQ,'neq',1,34)", 
                                 "LexToken(NUM_VAL,3.0,1,38)"]),
                            # test that a string containing a quote is tokenized correctly
                            ("property eq 'string with quote: '''", 
                                ["LexToken(FIELD_NAME,'property',1,0)",
                                 "LexToken(EQ,'eq',1,9)",
                                 'LexToken(STRING_VAL,"string with quote: \'\'",1,12)']),
                             # test that illegal chars are skipped over durting lexing
                            ("property lt @ -5",
                                ["LexToken(FIELD_NAME,'property',1,0)",
                                 "LexToken(LT,'lt',1,9)",
                                 "LexToken(NUM_VAL,-5.0,1,14)"])
                        ], 
                        ids=['simple_constraint', 'boolean_ops', 'string_containing_quote', 'illegal_character'])
def test_lexing(test_input, expected_token_strs):
    """Test that the lexer tokenizes input correctly"""
    _, lexer  = construct_parser(Headline)
    lexer.input(test_input)
    token_count = 0
    while True:
        tok = lexer.token()
        if not tok: 
            break      
        assert expected_token_strs[token_count] == str(tok)
        token_count += 1

@pytest.mark.parametrize("test_input, expected_sqlalchemy_str", 
                         [
                            # test if a single constraint can be parsed
                            ("text eq 'value'", "news_headlines.headline.text = :text_1"),
                            # test if expressions with boolean ops can be parsed
                            ("text eq 'value' or sentiment gt .5 and source neq 'src_name'", 
                                ("news_headlines.headline.text = :text_1 OR "
                                 "news_headlines.headline.sentiment > :sentiment_1 "
                                 "AND news_headlines.headline.source != :source_1"))
                        ], 
                        ids=['simple_constraint', 'boolean_ops'])
def test_parsing(test_input, expected_sqlalchemy_str):
    """Test that the parser parses tokens correctly"""
    parser, lexer  = construct_parser(Headline)
    result = parser.parse(test_input, lexer=lexer)
    assert str(result) == expected_sqlalchemy_str
  
@pytest.mark.parametrize("test_input", 
                         [
                            # test that trying to filter on a field that doesn't
                            # exist on the specified model raises an exception
                            "fake_field eq 1",
                            # test that trying to parse an expression with a partial
                            # boolean op raises an exception
                            "text eq 1 and",
                            # test that trying to parse an expression with unclosed
                            # parentheses raises an exception
                            "((text eq 1)"
                        ], 
                        ids=['nonexistant_field', 'partial_boolean_op', 'unclosed_parens'])
def test_parsing_error(test_input):
    """Test that the parser raises exceptions when it should"""
    with pytest.raises(Exception):
        parser, lexer  = construct_parser(Headline)
        parser.parse(test_input, lexer=lexer)