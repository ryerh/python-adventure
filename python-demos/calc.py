#!/usr/bin/python3
# encoding: utf-8
"""
# Program to convert Infix notation to Expression Tree
https://www.geeksforgeeks.org/program-to-convert-infix-notation-to-expression-tree/

# Evaluation of Expression Tree
https://www.geeksforgeeks.org/evaluation-of-expression-tree/
"""

import logging
import math
import unittest


TOKEN_LITERAL = set("0123456789abcdefghijklmnopqrstuvwxyz")
TOKEN_OPERAND = set("()+-*/^!.,=")
TOKEN_PRIOR = {
    ")": 0,
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
}
TOKEN_TYPE = {
    " ": "TOKEN_SPACE",
    "(": "TOKEN_LPARAN",
    ")": "TOKEN_RPARAN",
    "pi": "TOKEN_C_PI",
    "e": "TOKEN_C_E",
    "sin": "TOKEN_FN_SIN",
    "cos": "TOKEN_FN_COS",
    "tan": "TOKEN_FN_tan",
    "+": "TOKEN_OP_ADD",
    "-": "TOKEN_OP_SUB",
    "*": "TOKEN_OP_MUL",
    "/": "TOKEN_OP_DIV",
    "^": "TOKEN_OP_EXP",
    "!": "TOKEN_OP_BANG",
    "__number__": "TOKEN_NUMBER",
    "__unknown__": "TOKEN_UNKNOWN",
}


def tokentype(token):
    simpletype = TOKEN_TYPE.get(token)
    if simpletype is not None:
        return simpletype

    try:
        float(token)
        return "TOKEN_NUMBER"
    except ValueError:
        return "TOKEN_UNKNOWN"


class Node(object):
    """表达式树的节点"""

    def __init__(self, typ, data, left=None, right=None, arg=None):
        self.typ = typ
        self.data = data
        self.left = left
        self.right = right
        self.arg = arg

    def __repr__(self):
        return "Node(typ=%s, data=%s)" % (self.typ, self.data)


class Stack(object):
    """生成表达式树的辅助栈"""

    def __init__(self):
        self._s = []

    def push(self, data):
        return self._s.append(data)

    def pop(self):
        return self._s.pop()

    def top(self):
        return self._s[len(self._s) - 1]

    def empty(self):
        return len(self._s) == 0

    def __repr__(self):
        return repr(self._s)


def tokenizer(input_expr):
    """词法分析"""
    tokens = []
    idx = -1
    max_len = len(input_expr) - 1
    buf = ""

    while idx < max_len:
        idx += 1

        char = input_expr[idx]
        if char in TOKEN_LITERAL:
            buf += char
            if idx == max_len:
                tokens.append(buf)
                buf = ""
            continue

        if buf != "":
            tokens.append(buf)
            buf = ""

        if char == " ":
            continue

        if char in TOKEN_OPERAND:
            tokens.append(char)
            continue

        raise SyntaxError("非法字符：%s" % char)

    logging.debug("TOKENS: ", " ".join(tokens))
    return tokens


def parser(tokens):
    """语法分析"""
    stN, stC = Stack(), Stack()
    idx = -1
    max_len = len(tokens) - 1
    while idx < max_len:
        idx += 1
        token = tokens[idx]
        ttype = tokentype(token)

        if ttype == "TOKEN_LPARAN":
            stC.push(token)
            continue

        if ttype == "TOKEN_NUMBER":
            stN.push(Node(ttype, token))
            continue

        if ttype.startswith("TOKEN_C_"):
            stN.push(Node(ttype, token))
            continue

        if ttype.startswith("TOKEN_FN_"):
            jstC = Stack()
            jstC.push("(")
            jdx = idx + 2
            while not jstC.empty() and jdx < max_len:
                if tokens[jdx] == "(":
                    jstC.push("(")
                if tokens[jdx] == ")":
                    jstC.pop()
                jdx += 1
            arg = parser(tokens[idx+1:jdx])
            logging.debug("ARG: ", idx, jdx, arg)
            stN.push(Node(ttype, token, arg=arg))
            idx = jdx - 1
            continue

        if ttype.startswith("TOKEN_OP_"):
            tprio = TOKEN_PRIOR[token]
            if tprio > 0:
                while (
                        not stC.empty() and stC.top() != "(" and
                        (
                            (token != "^" and TOKEN_PRIOR[stC.top()] >= tprio)
                            or
                            (token == "^" and TOKEN_PRIOR[stC.top()] > tprio)
                        )
                ):

                    t1 = stN.pop()
                    t2 = stN.pop()
                    t = Node(ttype, stC.pop(), t2, t1)
                    stN.push(t)
                stC.push(token)
                continue

        if ttype == "TOKEN_RPARAN":
            while not stC.empty() and stC.top() != "(":
                t1 = stN.pop()
                t2 = stN.pop()
                t = Node(ttype, stC.pop(), t2, t1)
                stN.push(t)
            stC.pop()
            continue
    logging.debug("stN: ", stN)
    return stN.top()


def evaluator(root):
    """表达式树求值"""
    if root is None:
        return 0
    if root.typ == "TOKEN_C_E":
        return math.e
    if root.typ == "TOKEN_C_PI":
        return math.pi
    if root.typ == "TOKEN_NUMBER":
        return float(root.data)

    left_sum = evaluator(root.left)
    right_sum = evaluator(root.right)
    if root.data == '+':
        return left_sum + right_sum
    if root.data == '-':
        return left_sum - right_sum
    if root.data == '*':
        return left_sum * right_sum
    if root.data == "/":
        return left_sum / right_sum
    if root.data == "^":
        return left_sum ** right_sum

    if root.typ.startswith("TOKEN_FN_SIN"):
        return math.sin(evaluator(root.arg))
    if root.typ.startswith("TOKEN_FN_COS"):
        return math.cos(evaluator(root.arg))
    if root.typ.startswith("TOKEN_FN_TAN"):
        return math.tan(evaluator(root.arg))


def calc(expr):
    """包装函数，最终暴露给用户的函数"""
    tokens = tokenizer(expr)
    ast = parser(tokens)
    rlt = evaluator(ast)
    return rlt


def postorder(root, result=None):
    """遍历表达式树"""
    if result is None:
        result = []
    if root is not None:
        postorder(root.left, result)
        postorder(root.right, result)
        if root.typ.startswith("TOKEN_FN_"):
            result.append("%s(%s)" % (root.data, " ".join(postorder(root.arg))))
        else:
            result.append(root.data)
    return result


def printer(ast):
    """打印表达式树"""
    result = postorder(ast)
    logging.info("AST: ", " ".join(result))


class CalculatorTest(unittest.TestCase):

    def test_tokenizer(self):
        test_cases = {
            "1": ["1"],
            "+1": ["+", "1"],
            "+2x": ["+", "2x"],
            "log(10)": ["log", "(", "10", ")"],
            "a^3+1,a=2": ["a", "^", "3", "+", "1", ",", "a", "=", "2"],
            "1 + (20+3123) ": ["1", "+", "(", "20", "+", "3123", ")"],
        }
        for input_expr, expected_val in test_cases.items():
            self.assertListEqual(tokenizer(input_expr), expected_val)

    def test_buildtree(self):
        test_cases = {
            "(1)": (1),
            "(1+1)": (1+1),
            "(1+2-3)": (1+2-3),
            "(1+(2-3))": (1+(2-3)),
            "(1-(2-3))": (1-(2-3)),
            "(2^3^(3/1/e-10))": (2**3**(3/1/math.e-10)),
            "(2^3^(3/1/e-10)+sin(30+(1-10)))": (2**3**(3/1/math.e-10)+math.sin(30+(1-10))),
        }
        for input_expr, expected_val in test_cases.items():
            self.assertEqual(calc(input_expr), expected_val)


if __name__ == "__main__":
    unittest.main()
