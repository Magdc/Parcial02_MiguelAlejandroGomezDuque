"""
Microservicio simple (un solo archivo) que expone:
GET /factorial/<n>
Devuelve JSON con:
- numero: el número recibido
- factorial: el factorial (como cadena para evitar problemas con tamaños enormes)
- paridad: "par" o "impar" según corresponda al factorial

Uso:
pip install -r requirements.txt
python app.py

Ejemplo: GET http://localhost:5000/factorial/5
"""
from flask import Flask, jsonify
from math import factorial

app = Flask(__name__)


def compute_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser entero no negativo")
    # Usamos math.factorial (maneja enteros grandes)
    return factorial(n)


@app.route('/factorial/<int:n>', methods=['GET'])
def factorial_route(n: int):
    try:
        if n < 0:
            return jsonify({"error": "n debe ser entero no negativo"}), 400
        fact = compute_factorial(n)
        # Para evitar problemas de serialización con enteros enormes, lo devolvemos como string.
        parity = "par" if n % 2 == 0 else "impar"
        return jsonify({
            "numero": n,
            "factorial": str(fact),
            "paridad": parity
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "error interno: " + str(e)}), 500


if __name__ == '__main__':
    # Modo desarrollo. En producción usar un WSGI server (gunicorn/uWSGI).
    app.run(host='0.0.0.0', port=5000, debug=True)
