from boltiotai import openai
import os

from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_tutorial(components):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant"
        }, {
            "role": "user",
            "content": f"Suggest a recipe using the items listed as available. Make sure you have a nice name for this recipe listed at the start. Also, include a funny version of the name of the recipe on the following line. Then share the recipe in a step-by-step manner. In the end, write a fun fact about the recipe or any of the items used in the recipe. Here are the items available: {components}, Haldi, Chilly Powder, Tomato Ketchup, Water, Garam Masala, Oil"
        }]
    )
    return response['choices'][0]['message']['content']

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    output = ""
    if request.method == 'POST':
        components = request.form['components']
        output = generate_tutorial(components)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Recipe Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .output { background-color: #f4f4f4; padding: 20px; margin-top: 20px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Recipe Generator</h1>
        <form method="POST">
            <label>Enter ingredients (comma-separated):</label>
            <textarea name="components" rows="4" placeholder="e.g., chicken, rice, onions"></textarea>
            <button type="submit">Generate Recipe</button>
        </form>
        {% if output %}
        <div class="output">
            <h2>Your Recipe:</h2>
            {{ output }}
        </div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, output=output)
@app.route('/generate', methods=['POST'])
def generate():
    components = request.form['components']
    return generate_tutorial(components)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)