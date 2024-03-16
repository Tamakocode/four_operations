import random
from sympy import simplify, cancel

OPERATORS = ['+', '-', '×', '÷']


def generate_expression(max_value, num_operands):
    # 随机生成操作数
    int_operands = [random.randint(1, max_value) for num in range(num_operands)]
    int_operands = [str(num) for num in int_operands]
    frc_operands = [generate_fraction(max_value) for num in range(num_operands)]
    operands = int_operands + frc_operands
    random.shuffle(operands)
    print(operands)

    # 随机生成运算符
    operators = [random.choice(OPERATORS) for num in range(num_operands - 1)]
    print(operators)

    mark = random.randint(1, 100)
    if mark in range(1, 40):
        operands_list = operands
    elif mark in range(41, 60):
        operands_list = int_operands
    else:
        operands_list = frc_operands

    expression = ' '.join([operands_list[i] + " " + operators[i] for i in range(num_operands - 1)] + [operands[-1]])
    return expression


def generate_fraction(max_value):
    # 随机生成分母
    denominator = random.randint(2, max_value)
    # 随机生成分子
    numerator = random.randint(1, denominator - 1)
    # 生成第一个真分数
    fraction = f"({numerator}/{denominator})"
    return fraction


# 示例用法
max_value = 10
num_operands = 3
for i in range(10):
    expression = generate_expression(max_value, random.randint(2, 5))
    expression = expression.replace('÷', '/').replace('×', '*')
    print(expression, "=", simplify(expression))
    print("---------------------------------")
