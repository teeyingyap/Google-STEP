# instead of converting digit by digit
# find the index range and convert it by float(line[start: end]) 
def readNumber(line, index):
  end = index
  while end < len(line) and (line[end].isdigit() or line[end] == '.'):
    end += 1
  number = float(line[index:end])
  token = {'type': 'NUMBER', 'number': number}
  return token, end


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readMultiply(line, index):
  token = {'type': 'MULTIPLY'}
  return token, index + 1


def readDivide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1


def readLBracket(line, index):
  token = {'type': 'LEFT'}
  return token, index + 1


def readRBracket(line, index):
  token = {'type': 'RIGHT'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  operatorFlag = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
      operatorFlag = 0
    elif line[index] in ['+', '-', '*', '/'] and operatorFlag == 0:
      if line[index] == '+':
        (token, index) = readPlus(line, index)
      elif line[index] == '-':
        (token, index) = readMinus(line, index)
      elif line[index] == '*':
        (token, index) = readMultiply(line, index)
      elif line[index] == '/':
        (token, index) = readDivide(line, index)
      operatorFlag = 1
    elif line[index] == '(':
      (token, index) = readLBracket(line, index)
    elif line[index] == ')':
      (token, index) = readRBracket(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluateMultiplyDivide(tokens):
  index = 0
  new_token_list = []
  last_number_token = 0
  while index < len(tokens):
    if tokens[index]['type'] == 'MULTIPLY':
      result = new_token_list[last_number_token - 1]['number'] * tokens[index + 1]['number']
      token = {'type': 'NUMBER', 'number': result}
      new_token_list[-1] = token
      index += 2
    elif tokens[index]['type'] == 'DIVIDE':
      if tokens[index + 1]['number'] == 0:
        print('Cannot divide by zero!')
        exit(1)
      else:
        result = new_token_list[last_number_token  - 1]['number'] / tokens[index + 1]['number']
        token = {'type': 'NUMBER', 'number': result}
        new_token_list[-1] = token
        index += 2
    else:
      new_token_list.append(tokens[index])
      last_number_token +=1
      index += 1
  return new_token_list


def evaluatePlusMinus(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


# some kind of recursion is needed
# when i see + or -, i have to skip it and call the function to evaluate * or /
# after evaluating * or /, i have to go back to that parent index and do + or - with the result


# Evaluate the terms inside the brackets using recursion
def evaluateInside(tokens, index):
  temp_new_tokens = []
  brack_index = index
  while index < len(tokens) and tokens[brack_index]['type'] != 'RIGHT':
    if tokens[brack_index]['type'] == 'LEFT':
      answer_token, brack_index = evaluateInside(tokens, brack_index + 1)
      temp_new_tokens.append(answer_token)
      index = brack_index + 1
    else:
      temp_new_tokens.append(tokens[brack_index])
    brack_index += 1
  evaluatedTokens = evaluateMultiplyDivide(temp_new_tokens)
  answer = evaluatePlusMinus(evaluatedTokens)
  token = {'type': 'NUMBER', 'number': answer}
  return token, brack_index 


# remove the brackets in the list
# return new list with no brackets 
def evaluateBrackets(tokens):
  index = 0
  new_token_list = []
  while index < len(tokens):
    if tokens[index]['type'] == 'LEFT':
      token, index = evaluateInside(tokens, index + 1)
      new_token_list.append(token)
    else:
      new_token_list.append(tokens[index])
    index += 1
  # print(new_token_list)
  return new_token_list 


def test(line):
  tokens = tokenize(line)
  tokens.insert(0, {'type': 'LEFT'})
  tokens.append({'type': 'RIGHT'})
  actualAnswerToken, index = evaluateInside(tokens, 0)
  actualAnswer = actualAnswerToken['number']
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1.1")
  test("1+2")
  test("1")
  test("1.1+2.1")
  test("1.1-2.1")
  test("1.1*2.2")
  test("1.1/2.2")
  test("1.0+2.1-3")
  test("1.0*2.1/3")
  test("1.0-2.1-3")
  test("1.0+2.1+3")
  test("1.0*2.1*3")
  test("1.0/2.1/3")
  test("1+2*3")
  test("7/8*3")
  test("3/5/6/3")
  test("3*5*6*3")
  test("1-2-3")
  test("10.0+80.4/9.2/8.9+7.9-3.0*8.1")
  test("10.0+80.4+9.2-8.9-7.9/3.0/8.1*1.3*4.4")
  test("(3.0+4)*5") 
  test("(1+1)")
  test("(1+2)/(3-4)")
  test("(1-2)+(3*4)")
  test("1+(3.0+4)*5") 
  test("1+(2+(3*6)/7)")
  test("1+(3.0+4)*(3+5)") 
  test("(1*2)+(3.0+4)*(3+5)") 
  test("(1*2*2*3)+(3.0+4)*(3+5)") 
  test("(1*2+2*3)+(3.0+4)/(3+5)") 
  test("((3+1)+5)*8") 
  test("(3.0+4*(2-1))/5")
  test("(3.0+4*(2-1))/(4+5*(8*2))")
  test("(3.0+4*(2-(1+1+1*4)))/5")
  test("12++1")
  test("12+1")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  # add dummy pair of parentheses
  tokens.insert(0, {'type': 'LEFT'})
  tokens.append({'type': 'RIGHT'})
  answer = evaluateInside(tokens, 0)
  print("answer = %f\n" % answer['number'])