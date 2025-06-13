#! /usr/bin/python3


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
def evaluate_multiplication_and_division(tokens):
    index = 2
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
def evaluate_addition_and_subtraction(tokens):
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
def evaluate(tokens):
    print(tokens)
    tokens = evaluate_parentheses(tokens)
    print(tokens)
    tokens = evaluate_multiplication_and_division(tokens)
    return evaluate_addition_and_subtraction(tokens)


#括弧の数が正しいか＆正しいならどのインデックスがペアかどうか
#Check the order of parentheses. If correct, return the index of the first pair.
def get_paren(tokens):
    closest_open_paren_index = -1
    diff_left_right = 0
    for i, token in enumerate(tokens):
        #秋カッコは入れていく
        if token['type'] == 'OPEN':
            closest_open_paren_index = i
            diff_left_right += 1
        elif token['type'] == 'CLOSE':
            diff_left_right -= 1
            if closest_open_paren_index >= 0:
                # 最初のペアを返す前に、残りも正しいかチェック
                for t in tokens[i+1:]:
                    if t['type'] == 'OPEN':
                        diff_left_right += 1
                    elif t['type'] == 'CLOSE':
                        diff_left_right -= 1
                        if diff_left_right < 0:
                            return {'success': False}
                if diff_left_right == 0:
                    return {'success': True, 'left_index': closest_open_paren_index, 'right_index': i}
            return {'success': False}

    return {'success': False}


#カッコの中の計算
def evaluate_parentheses(tokens):
    #カッコが式に存在する間
    while any(t['type'] in ['OPEN', 'CLOSE'] for t in tokens):
        first_paren_pair = get_paren(tokens)
        if not first_paren_pair['success']:
            print("Invalid formula")
            return None  # または raise ValueError("Invalid formula")
        #最小の括弧のペアだけ計算する
        left_index = first_paren_pair['left_index']
        right_index = first_paren_pair['right_index']

        print(left_index, right_index)
        tokens_in_parens = tokens[left_index+1 : right_index]
        temp_ans = evaluate(tokens_in_parens)

        #括弧部分を抜いて、計算結果をいれこむ
        del tokens[left_index+1:right_index+1]
        tokens[left_index] = {'type': 'NUMBER', 'number': temp_ans}
    

    return tokens

#実際の値とずれてないか確認
def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    #test("1")
    test("-3+(-1)")
    # test("1+2")
    # test("1.0+2.1-3")
    # test("5*2")
    # test("7.5/1.25+3-4*2.78")
    # test("1/3")
    # test("2.2*3*6.4/4+1")
    # #括弧のデバッグ
    # test('1+(2*3)')
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
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
