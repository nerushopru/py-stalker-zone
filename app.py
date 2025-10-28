from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_python():
    code = request.json.get('code', '')
    
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Выполняем код с таймаутом
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10  # 10 секунд таймаут
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nОшибка: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        output = "Ошибка: время выполнения превышено (10 секунд)"
    except Exception as e:
        output = f"Ошибка: {str(e)}"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file)
    
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
