import random
from fractions import Fraction
from sympy import simplify, cancel

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
        second_fraction = f"({numerator}/{denominator})"
        # 生成第一个真分数
        first_number = random.randint(1, max_value // numerator)
        first_fraction = f"({first_number * numerator}/{denominator})"
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
    # 将乘法符号替换为合法的乘法运算符 "*"
    expression = expression.replace('÷', '/').replace('×', '*')

    # 使用 Sympy 简化表达式
    simplified_expr = simplify(expression)
    # 将简化后的表达式转换为字符串形式
    simplified_expr_str = str(simplified_expr)
    return simplified_expr_str


# 生成指定数量的题目
def generate_exercises(num_exercises, max_value):
    exercises = set()
    attempts = 0
    max_attempts = 1000  # 设置最大尝试次数，避免无限循环

    while len(exercises) < num_exercises and attempts < max_attempts:
        # 增加尝试次数
        attempts += 1
        # 生成一个表达式
        expression = generate_expression(max_value)
        print("原始", expression)

        # 简化表达式，确保所有的除法操作都使用合法的除法运算符 "÷"
        simplified_expression = None
        try:
            simplified_expression = cancel(expression)
        except Exception as e:
            print(f"Error simplifying expression: {e}")

        # 如果简化后的表达式不为空，并且表达式中含有等号
        # if simplified_expression and '=' in str(simplified_expression):
        #     exercises.add(expression)
        # else:
        #     print("No =")

        exercises.add(expression)

    # 检查是否达到最大尝试次数
    if attempts >= max_attempts:
        print("无法生成题目，请检查代码和参数设置以避免无限循环。")

    return exercises


# 计算表达式的答案
def calculate_answer(expression):
    # 将表达式中的乘除号替换为Python中的乘除号
    expression = expression.replace('×', '*').replace('÷', '/')
    # 使用eval计算表达式的值，并将结果转换为真分数形式
    answer = Fraction(eval(expression))
    return answer


def main():
    num_exercises = 10  # 题目数量
    max_value = 10  # 数值范围

    # 生成题目和答案
    exercises = generate_exercises(num_exercises, max_value)
    answers = []

    print("题目及答案：")
    for i, exercise in enumerate(exercises, start=1):
        # 打印题目
        print(f"{i}. {exercise}", end=' = ')
        # 计算答案
        answer = calculate_answer(exercise)
        answers.append(answer)
        # 打印答案
        print(answer)

    # 将题目和答案写入文件
    with open('Exercises.txt', 'w') as exercise_file, open('Answers.txt', 'w') as answer_file:
        for i, exercise in enumerate(exercises, start=1):
            # 写入题目到文件
            exercise_file.write(f"四则运算题目{i}: {exercise}\n")
            # 写入答案到文件
            answer_file.write(f"{calculate_answer(exercise)}\n")

    print(f"\n{num_exercises} 题目已生成.")


if __name__ == "__main__":
    main()
