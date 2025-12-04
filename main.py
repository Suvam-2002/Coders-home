from boltiotai import openai
import os
from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_tutorial(components):
    response = openai.Images.create(
        prompt=components,
        model="dall-e-3",
        size="1024x1024",
        response_format="url")
    image_url = response['data'][0]['url']
    return image_url

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    image_url = ""
    if request.method == 'POST':
        prompt = request.form['components']
        image_url = generate_tutorial(prompt)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .output { background-color: #f4f4f4; padding: 20px; margin-top: 20px; text-align: center; }
            .output img { max-width: 100%; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>AI Image Generator</h1>
        <form method="POST">
            <label>Enter your image prompt:</label>
            <textarea name="components" rows="4" placeholder="e.g., a beautiful sunset over mountains"></textarea>
            <button type="submit">Generate Image</button>
        </form>
        {% if image_url %}
        <div class="output">
            <h2>Your Generated Image:</h2>
            <img src="{{ image_url }}" alt="Generated image">
        </div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, image_url=image_url)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['components']
    return generate_tutorial(prompt)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)