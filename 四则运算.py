import argparse
import random
from fractions import Fraction
from sympy import simplify, Symbol, Eq

# 定义四则运算符号
OPERATORS = ['+', '-', '×', '÷']


# 生成一个算术表达式
def generate_expression(max_value):
    # 随机选择运算符
    operator = random.choice(OPERATORS)
    if operator == '÷':  # 如果是除法运算
        # 随机生成分母
        denominator = random.randint(2, max_value)
        # 随机生成分子
        numerator = random.randint(1, denominator - 1)
        # 生成第二个真分数
        second_fraction = Fraction(numerator, denominator)
        # 生成第一个真分数
        first_number = random.randint(1, max_value // numerator)
        first_fraction = Fraction(first_number * numerator, denominator)
        # 组合成算术表达式
        expression = f"{first_fraction} {operator} {second_fraction}"
    else:  # 其他运算
        # 随机生成两个数
        first_number = random.randint(1, max_value)
        second_number = random.randint(1, max_value)
        # 组合成算术表达式
        expression = f"{first_number} {operator} {second_number}"
    return expression


# 简化表达式
def simplify_expression(expression):
    # 将除法符号替换为合法的除法运算符 "/"
    expression = expression.replace('÷', '/')
    # 将乘法符号替换为合法的乘法运算符 "*"
    expression = expression.replace('×', '*')
    # 使用 Sympy 简化表达式
    simplified_expr = simplify(expression)
    # 将简化后的表达式转换为字符串形式
    simplified_expr_str = str(simplified_expr)
    return simplified_expr_str


# 生成指定数量的题目
def generate_exercises(num_exercises, max_value):
    exercises = set()
    while len(exercises) < num_exercises:
        # 生成一个表达式
        expression = generate_expression(max_value)
        # 简化表达式，确保所有的除法操作都使用合法的除法运算符 "/"
        simplified_expression = simplify_expression(expression)
        # 直接使用简化后的表达式作为条件
        if '=' in simplified_expression:
            exercises.add(expression)
    return exercises


# 计算表达式的答案
def calculate_answer(expression):
    # 将表达式中的乘除号替换为Python中的乘除号
    expression = expression.replace('×', '*').replace('÷', '/')
    # 使用eval计算表达式的值，并将结果转换为真分数形式
    answer = Fraction(eval(expression))
    return answer


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="生成四则运算题目.")
    parser.add_argument('-n', type=int, help="生成题目的数量.")
    parser.add_argument('-r', type=int, help="数值范围（不包括该数）.")
    args = parser.parse_args()

    # 如果缺少参数，则报错并给出帮助信息
    if not args.n or not args.r:
        parser.error("参数 -n 和 -r 是必须的.")

    # 生成题目和答案
    exercises = generate_exercises(args.n, args.r)
    answers = []

    print("1")

    # 将题目和答案写入文件
    with open('Exercises.txt', 'w') as exercise_file, open('Answers.txt', 'w') as answer_file:

        print("2")

        for i, exercise in enumerate(exercises, start=1):
            # 写入题目到文件
            exercise_file.write(f"四则运算题目{i}: {exercise}\n")
            # 计算答案
            answer = calculate_answer(exercise)
            answers.append(answer)
            # 写入答案到文件
            answer_file.write(f"{answer}\n")

    print(f"{args.n} 题目已生成.")


if __name__ == "__main__":
    main()
