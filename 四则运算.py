import argparse
import random
from fractions import Fraction
from sympy import simplify, sympify

# 定义四则运算符号
OPERATORS = ['+', '-', '×', '÷']


# 生成一个算术表达式
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


# 生成指定数量的题目
def generate_exercises(num_exercises, max_value):
    exercises = set()
    count = 0
    while True:
        expression = generate_expression(max_value, random.randint(2, 5))
        expression_test = expression
        expression_test = expression_test.replace('×', '*').replace('÷', '/')
        answer_test = simplify(expression_test)
        if answer_test >= 0:
            exercises.add(expression)
            count += 1

        if count == num_exercises:
            return exercises


# 计算表达式的答案
def calculate_answer(expression):
    expression = expression.replace('×', '*').replace('÷', '/')
    answer = simplify(expression)
    return answer


# 判断答案是否正确
def is_correct(expression, answer_str):
    try:
        # 将表达式中的乘除号替换为Python中的乘除号
        expression = expression.replace('×', '*').replace('÷', '/')
        # 计算表达式的值
        calculated_answer = simplify(expression)
        # 将输入的答案字符串转换为SymPy对象
        answer = sympify(answer_str)
        # 判断计算得到的答案与输入的答案是否相同
        return calculated_answer == answer
    except Exception as e:
        # 如果出现任何错误（如表达式或答案字符串格式不正确），打印错误并返回False
        print(f"Error: {e}")
        return False


# 生成题目与答案
def generate_questions_and_answers(args_n, args_r):
    exercises = generate_exercises(args_n, args_r)
    answers = []

    with open('Exercises.txt', 'w') as exercise_file, open('Answers.txt', 'w') as answer_file:
        for i, exercise in enumerate(exercises, start=1):
            exercise_file.write(f"四则运算题目{i}: {exercise}\n")
            answer = calculate_answer(exercise)
            answers.append(answer)
            answer_file.write(f"{answer}\n")

    print(f"{args_n} 题目已生成.")


# 检查答案
def check_answers(args_e, args_a):
    # 读取题目文件和答案文件
    with open(args_e, 'r') as exercise_file, open(args_a, 'r') as answer_file:
        exercises = exercise_file.readlines()
        answers = answer_file.readlines()

    correct_exercises = []
    wrong_exercises = []

    # 判断每个题目的答案是否正确
    for i, (exercise, answer) in enumerate(zip(exercises, answers), start=1):
        exercise = exercise.strip().split(': ')[1]
        answer = Fraction(answer.strip())

        if is_correct(exercise, answer):
            correct_exercises.append(i)
        else:
            wrong_exercises.append(i)

    # 输出统计结果到文件Grade.txt
    with open('Grade.txt', 'w') as grade_file:
        grade_file.write(f"Correct: {len(correct_exercises)} ({', '.join(map(str, correct_exercises))})\n")
        grade_file.write(f"Wrong: {len(wrong_exercises)} ({', '.join(map(str, wrong_exercises))})\n")


# 生成与检查同时
def generate_and_check(args_n, args_r, args_e, args_a):
    generate_questions_and_answers(args_n, args_r)
    check_answers(args_e, args_a)


def main():
    parser = argparse.ArgumentParser(description="生成和统计四则运算题目答案的正确性.")
    parser.add_argument('-n', type=int, help="生成题目的数量.")
    parser.add_argument('-r', type=int, help="数值范围（不包括该数）.")
    parser.add_argument('-e', type=str, help="题目文件名.")
    parser.add_argument('-a', type=str, help="答案文件名.")
    args = parser.parse_args()

    if args.n and args.r:
        generate_questions_and_answers(args.n, args.r)
    elif args.e and args.a:
        check_answers(args.e, args.a)
    elif args.n and args.r and args.e and args.a:
        generate_and_check(args.n, args.r, args.e, args.a)
    else:
        parser.error(
            '''
                        1.若只需要生成题目与答案：python 【脚本名.py】 -n 10 -r 10
                          -n -----> 生成的题目数量
                          -r -----> 最大数值
                        2.统计题目与答案的正确与否：python 【脚本名.py】 -e 【题目文件】 -a 【答案文件】 
                          -e -----> 题目文件.txt
                          -a -----> 答案文件.txt
                        3.两者同时：python 【脚本名.py】 -n 10 -r 10 -e 【题目文件】 -a 【答案文件】
        ''')


if __name__ == "__main__":
    main()
