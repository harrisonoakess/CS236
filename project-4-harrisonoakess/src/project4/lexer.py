"""Turn a input string into a stream of tokens with lexical analysis.

The `lexer(input_string: str)` function is the entry point. It generates a
stream of tokens from the `input_string`.

Examples:

    >>> from project4.lexer import lexer
    >>> input_string = ":\\n  \\n:"
    >>> for i in lexer(input_string):
    ...     print(i)
    ...
    (COLON,":",1)
    (COLON,":",3)
    (EOF,"",3)
"""

from typing import Iterator

from project4.token import Token, TokenType
from project4.fsm import (
    FiniteStateMachine,
    Colon,
    WhiteSpace,
    run_fsm,
    Colon_dash,
    Comma,
    comment,
    Eof,
    facts,
    left_paren,
    period,
    queries,
    q_mark,
    right_paren,
    rules,
    schemes,
    string,
    id,
)


def _is_last_token(token: Token) -> bool:
    if token.token_type == "EOF" or token.token_type == "UNDEFINED":
        return True
    return False


def _get_token(input_string: str, fsms: list[FiniteStateMachine]) -> Token:
    max_char = 0
    max_token = Token.undefined("")
    for token_finder in fsms:
        numcharread, token = run_fsm(token_finder, input_string)
        if numcharread > max_char:
            max_char = numcharread
            max_token = token
    if max_token.token_type == "UNDEFINED":
        max_token.value = input_string[0]
    return max_token


def _get_new_lines(value: str) -> int:
    return value.count("\n")


def lexer(input_string: str) -> Iterator[Token]:
    fsms: list[FiniteStateMachine] = [
        Colon(),
        Eof(),
        WhiteSpace(),
        Colon_dash(),
        Comma(),
        comment(),
        facts(),
        left_paren(),
        period(),
        queries(),
        q_mark(),
        right_paren(),
        rules(),
        schemes(),
        string(),
        id(),
    ]
    hidden: list[TokenType] = ["WHITESPACE", "COMMENT"]
    line_num: int = 1
    token: Token = Token.whitespace("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token

    """Produce a stream of tokens from a given input string.

    Pseudo-code:

    ```
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace()]
    hidden: list[TokenType] = ["WHITESPACE"]
    line_num: int = 1
    token: Token = Token.undefined("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token
    ```


    The `_get_token` function should return the token from the FSM that reads
    the most characters. In the case of two FSMs reading the same number of
    characters, the one that comes first in the list of FSMs, `fsms`, wins.
    Some care must be given to determining when the _last_ token has been
    generated and how to update the new `line_num` for the next token.

    Args:
        input_string: Input string for token generation.

    Yields:
        token: The current token resulting from the string.
    """
