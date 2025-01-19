from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Fungsi untuk menghitung probabilitas Poisson
def poisson_probability(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == 'POST':
        try:
            # Ambil nilai dari form
            lambda_avg = float(request.form['lambda_avg'])
            k_expected = int(request.form['k_expected'])

            # Perhitungan probabilitas
            prob_exact_k = poisson_probability(lambda_avg, k_expected)
            prob_less_than_k = sum(poisson_probability(lambda_avg, i) for i in range(k_expected))
            prob_more_than_k = 1 - prob_less_than_k

            # Data untuk ditampilkan di template
            data = {
                "lambda_avg": lambda_avg,
                "k_expected": k_expected,
                "prob_exact_k": round(prob_exact_k, 4),
                "prob_less_than_k": round(prob_less_than_k, 4),
                "prob_more_than_k": round(prob_more_than_k, 4),
            }
        except KeyError:
            data["error"] = "Data form tidak lengkap. Pastikan semua field telah diisi!"
        except ValueError:
            data["error"] = "Input harus berupa angka. Mohon periksa kembali!"
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
