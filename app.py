from flask import Flask, render_template_string, request

app = Flask(__name__)

# Plantilla HTML con estilos integrados y motor Jinja2 para variables
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Flask</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            padding: 2.5rem;
            background: rgba(30, 41, 59, 0.7);
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            animation: fadeIn 1s ease-out;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(45deg, #38bdf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .form-group {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        input, select, button {
            padding: 12px;
            border-radius: 8px;
            border: none;
            font-size: 1.1rem;
            outline: none;
        }
        input {
            background: #334155;
            color: white;
            width: 120px;
            text-align: center;
        }
        select {
            background: #475569;
            color: white;
            cursor: pointer;
        }
        button {
            background: linear-gradient(45deg, #38bdf8, #c084fc);
            color: white;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            transition: opacity 0.3s;
        }
        button:hover {
            opacity: 0.8;
        }
        .result {
            margin-top: 20px;
            font-size: 1.8rem;
            font-weight: bold;
            color: #f472b6;
        }
        .error {
            color: #ef4444;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculadora 🧮</h1>
        
        <form method="POST">
            <div class="form-group">
                <input type="number" step="any" name="num1" placeholder="Nº 1" required value="{{ num1 }}">
                
                <select name="operator">
                    <option value="+" {% if operator == '+' %}selected{% endif %}>+</option>
                    <option value="-" {% if operator == '-' %}selected{% endif %}>-</option>
                    <option value="*" {% if operator == '*' %}selected{% endif %}>&times;</option>
                    <option value="/" {% if operator == '/' %}selected{% endif %}>&divide;</option>
                </select>
                
                <input type="number" step="any" name="num2" placeholder="Nº 2" required value="{{ num2 }}">
            </div>
            
            <button type="submit">Calcular</button>
        </form>

        {% if result is not none %}
            <div class="result">Resultado: {{ result }}</div>
        {% endif %}
        
        {% if error %}
            <div class="result error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    num1 = ""
    num2 = ""
    operator = "+"

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            num1_str = request.form.get('num1')
            num2_str = request.form.get('num2')
            operator = request.form.get('operator')

            if num1_str and num2_str:
                num1 = float(num1_str)
                num2 = float(num2_str)

                # Realizar el cálculo basado en el operador
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        error = "No se puede dividir por cero"
                    else:
                        result = num1 / num2
                        
                # Formatear el resultado para quitar decimales innecesarios
                if result is not None and result.is_integer():
                    result = int(result)

        except ValueError:
            error = "Por favor, ingresa números válidos."

    return render_template_string(HTML_TEMPLATE, result=result, error=error, num1=num1, num2=num2, operator=operator)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)