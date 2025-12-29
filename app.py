from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-me')
def about_me():
    return render_template('about_me.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')
        message = f"Dziękujemy za kontakt, {name}! Odpowiemy na {email} wkrótce."
    return render_template('contact.html', message=message)

# Endpoint do chatbota
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'response': 'Nie otrzymałem wiadomości!'})

    response = client.chat.completions.create(model="gpt-3.5-turbo",   # lub nowszy model
    messages=[{"role": "user", "content": user_message}],
    max_tokens=150)

    bot_reply = response.choices[0].message.content.strip()
    return jsonify({'response': bot_reply})


if __name__ == '__main__':
    app.run(debug=True)
