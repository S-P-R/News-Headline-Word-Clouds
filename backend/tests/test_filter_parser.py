'''
test_filter_parser.py

Contains unit tests for the functionality of the HeadlineAPI that lexes and
parses the '$filter' query parameter
'''
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HeadlineAPI.filter_parser import construct_parser
from HeadlineAPI.models import Headline, Source, DateSummary

@pytest.mark.parametrize("test_input, expected_token_strs", 
                         [
                             # test if a single constraint can be tokenized
                            ("property eq 'value'",
                                ["LexToken(FIELD_NAME,'property',1,0)", 
                                 "LexToken(EQ,'eq',1,9)", 
                                 "LexToken(STRING_VAL,'value',1,12)"]),
                            # test if boolean osp can be tokenized
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
    """
        Test that the lexer tokenizes input correctly 
    """
    _, lexer  = construct_parser(Headline)
    lexer.input(test_input)
    token_count = 0
    while True:
        tok = lexer.token()
        if not tok: 
            break      
        assert expected_token_strs[token_count] == str(tok)
        token_count += 1
