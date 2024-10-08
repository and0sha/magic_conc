from flask import Flask, render_template, request

app = Flask(__name__)


def find_representation(n):
    def decompose(num):
        result = []
        num_str = str(num)
        num_len = len(num_str)

        while num != 0:
            digits = [int(d) for d in str(num)]
            k = digits[0]
            kkkk = int(str(k) * num_len)

            if num >= kkkk:
                result.append((kkkk, '+'))
                num -= kkkk
            else:
                result.append((kkkk, '-'))
                num = kkkk - num

            if num == 0:
                break

            num_str = str(num)
            num_len = len(num_str)

        return result

    def format_expression(decomposition):
        if not decomposition:
            return ""
        value, sign = decomposition[0]
        if len(decomposition) == 1:
            return str(value)
        inner_expression = format_expression(decomposition[1:])
        if sign == '+':
            return f"{value} + ({inner_expression})"
        else:
            return f"{value} - ({inner_expression})"

    decomposition = decompose(n)
    expression = f"{n} = {format_expression(decomposition)}"
    return expression


def evaluate_expression(expression):
    def evaluate(expr):
        stack = []
        num = 0
        sign = 1
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isdigit():
                num = num * 10 + int(char)
            elif char == '+':
                stack.append(sign * num)
                num = 0
                sign = 1
            elif char == '-':
                stack.append(sign * num)
                num = 0
                sign = -1
            elif char == '(':
                j = i
                balance = 0
                while i < len(expr):
                    if expr[i] == '(':
                        balance += 1
                    if expr[i] == ')':
                        balance -= 1
                    if balance == 0:
                        break
                    i += 1
                num = evaluate(expr[j + 1:i])
            i += 1
        stack.append(sign * num)
        return sum(stack)

    try:
        left, right = expression.split('=')
        left = int(left.strip())
        right = right.strip()
        return evaluate(right) == left
    except Exception as e:
        print(f"Ошибка при оценке выражения: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    is_correct = None
    if request.method == 'POST':
        input_number = request.form.get('number')
        try:
            n = int(input_number)
            expression = find_representation(n)
            is_correct = evaluate_expression(expression)
            result = f"{expression}"
        except ValueError:
            result = "Пожалуйста, введите корректное число."
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run()
