from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def generate_magic_square(n):
    if n % 2 == 0:
        raise ValueError("Only odd n is supported for now.")
    magic_square = np.zeros((n, n), dtype=int)

    num = 1
    i, j = 0, n // 2

    while num <= n**2:
        magic_square[i, j] = num
        num += 1
        new_i, new_j = (i - 1) % n, (j + 1) % n
        if magic_square[new_i, new_j]:
            i += 1
        else:
            i, j = new_i, new_j
    return magic_square

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        n = int(request.form["size"])
        missing_count = int(request.form["missing_count"])
        magic_square = generate_magic_square(n)

        # Randomly remove some elements
        missing_indices = np.random.choice(n * n, missing_count, replace=False)
        for idx in missing_indices:
            magic_square[idx // n][idx % n] = 0

        grid_columns = n + 2
        return render_template("magic_square.html", magic_square=magic_square, grid_columns=grid_columns)

    return render_template("index.html")

@app.route("/calculate_sums", methods=["POST"])
def calculate_sums():
    data = request.get_json()
    square = data.get('square')

    if not square:
        return jsonify({'error': 'No square provided'}), 400

    n = len(square)
    correct_sum = n * (n * n + 1) // 2

    row_sums = [sum(row) for row in square]
    col_sums = [sum([square[i][j] for i in range(n)]) for j in range(n)]
    diag_sum_1 = sum([square[i][i] for i in range(n)])
    diag_sum_2 = sum([square[i][n - i - 1] for i in range(n)])

    return jsonify({
        'row_sums': row_sums,
        'col_sums': col_sums,
        'diag_sum_1': diag_sum_1,
        'diag_sum_2': diag_sum_2,
        'correct_sum': correct_sum
    })

@app.route("/check_magic_square", methods=["POST"])
def check_magic_square():
    data = request.get_json()
    square = data.get('square')

    if not square:
        return jsonify({'error': 'No square provided'}), 400

    n = len(square)
    magic_sum = n * (n * n + 1) // 2

    # Check rows and columns
    for i in range(n):
        if sum(square[i]) != magic_sum:
            correct_square = generate_magic_square(n).tolist()
            return jsonify({'is_magic': False, 'correct_square': correct_square})
        if sum([square[j][i] for j in range(n)]) != magic_sum:
            correct_square = generate_magic_square(n).tolist()
            return jsonify({'is_magic': False, 'correct_square': correct_square})

    # Check diagonals
    if sum([square[i][i] for i in range(n)]) != magic_sum:
        correct_square = generate_magic_square(n).tolist()
        return jsonify({'is_magic': False, 'correct_square': correct_square})
    if sum([square[i][n - i - 1] for i in range(n)]) != magic_sum:
        correct_square = generate_magic_square(n).tolist()
        return jsonify({'is_magic': False, 'correct_square': correct_square})

    return jsonify({'is_magic': True, 'magic_sum': magic_sum})

if __name__ == "__main__":
    app.run(debug=True)
