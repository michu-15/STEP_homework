#! /usr/bin/python3
import sys

#数字と小数の計算をしていく
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal   #累乗をdeciamlとしてwhile中増えていく
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

#各記号の定義
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1
def read_mul(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1
def read_div(line, index):
    token = {'type': 'DIVID'}
    return token, index + 1
def read_open_paren(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1
def read_close_paren(line, index):
    token = {'type': 'CLOSE'}
    return token, index + 1

#左から順番に見ていってリストに数字や'+'などを入れていく操作
def tokenize(line):
    tokens = []
    index = 0
    while index <len(line):  
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            (token, index) = read_open_paren(line, index)
        elif line[index] == ')':
            (token, index) = read_close_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

#掛け算・割り算 Multiplication and division
def evaluate_1(tokens):
    tokens_2 = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                calculate = tokens[index - 2]['number'] * tokens[index]['number']
                tokens.insert(index + 1, {'type': 'NUMBER', 'number': calculate})
                del tokens[index-2 : index+1]
                index -= 1
            elif tokens[index - 1]['type'] == 'DIVID':
                calculate = tokens[index - 2]['number'] / tokens[index]['number']
                tokens.insert(index + 1, {'type': 'NUMBER', 'number': calculate})
                del tokens[index-2 : index+1]
                index -= 1
        index +=1
    return tokens

#足し算・引き算　Addition and subtraction
def evaluate_2(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':       #一個前が足し算か
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':      #一個前が引き算か
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

#四則演算を一つの関数にまとめる Summary of arithmetic operations
def calculate(tokens):
    tempo_tokens = evaluate_1(tokens)
    tokens = evaluate_2(tempo_tokens)
    return tokens


#括弧の数が正しいか＆正しいならどのインデックスがペアかどうか
#Check the order of parentheses. If correct, return the index of the first pair.
def judge_paren(tokens):
    stack = []      #カッコだけを入れていくもの
    for i, token in enumerate(tokens):
        #秋カッコは入れていく
        if token['type'] == 'OPEN':
            stack.append(i)
        elif token['type'] == 'CLOSE':
            if stack:
                open_index = stack.pop()
                # 最初のペアを返す前に、残りも正しいかチェック
                temp_stack = stack[:]
                for t in tokens[i+1:]:
                    if t['type'] == 'OPEN':
                        temp_stack.append(0)
                    elif t['type'] == 'CLOSE':
                        if temp_stack:
                            temp_stack.pop()
                        else:
                            return "Invalid fomula"
                if not temp_stack:
                    return {open_index: i}
            return "Invalid fomula"

    return "Invalid fomula"


#カッコの中の計算
def calculate_paren(tokens):
    #カッコが式に存在する間
    while any(t['type'] in ['OPEN', 'CLOSE'] for t in tokens):
        first_paren_pair = judge_paren(tokens)
        if not isinstance(first_paren_pair, dict):
            print("Invalid formula")
            return None  # または raise ValueError("Invalid formula")
        #最小の括弧のペアだけ計算する
        for start, end in first_paren_pair.items():
            tempo_tokens = tokens[start+1 : end]
            tempo_ans = calculate(tempo_tokens)
            tempo_ans = tokenize(str(tempo_ans))    #tempo_tokensは計算結果の数値ででるけどlinesは文字列
            #括弧部分を抜いて、計算結果をいれこむ
            del tokens[start:end+1]
            tokens[start:start] = tempo_ans
    
    ans = calculate(tokens)
    return ans

#実際の値とずれてないか確認
def test(line):
    tokens = tokenize(line)
    actual_answer = calculate_paren(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("5*2")
    test("7.5/1.25+3-4*2.78")
    test("1/3")
    test("2.2*3*6.4/4+1")
    #括弧のデバッグ
    test('1+(2*3)')
    # test('(1+(2+3)')
    # test(')1+(2+3)')
    # test('1+(2+3))')
    #test('1+{2+3)')
    test('2*(7.5/1.25)+(3-4)*2.78')
    #test('2*(7.5/1.25(+)3-4)*2.78')
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    new_tokens = evaluate_1(tokens)
    answer = evaluate_2(new_tokens)   
    print("answer = %f\n" % answer)
