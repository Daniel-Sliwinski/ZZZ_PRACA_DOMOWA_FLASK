# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sandi_secret_key_2025"

# BAZA UŻYTKOWNIKÓW
users = {
    "admin": {"name": "admin", "pass": "admin123"},
    "Anna": {"name": "Anna", "pass": "user123"},
    "Maria": {"name": "Maria", "pass": "user123"},
}
reviews = []
all_messages = []

# KSIĄŻKI OMAWIANE
books_discussed = [
    {
        "title": "Kwiaty dla Algernona", 
        "author": "Daniel Keyes", 
        "img": "https://s.lubimyczytac.pl/upload/books/4875000/4875015/732927-352x500.jpg", 
        "desc": "Trzydziestodwuletni Charlie Gordon jest niepełnosprawny intelektualnie. Dwaj naukowcy prowadzą badania nad wzrostem inteligencji. Udało im się zwiększyć zdolności umysłowe myszy o imieniu Algernon i teraz chcą przeprowadzić taki sam eksperyment z człowiekiem."
    },
    {
        "title": "Wiek czerwonych mrówek", 
        "author": "Tania Pijankowa", 
        "img": "https://s.lubimyczytac.pl/upload/books/5048000/5048595/1065896-352x500.jpg", 
        "desc": "Przejmująca powieść o Wielkim Głodzie w Ukrainie w latach 1932-1933. Historia ludzi, którzy muszą zjednoczyć się przeciwko czerwonemu mrowisku swoich radzieckich ciemiężycieli."
    },
    {
        "title": "Człowiek w poszukiwaniu sensu", 
        "author": "Viktor Frankl", 
        "img": "https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/czlowiek-w-poszukiwaniu-sensu-b-iext199921942.jpg", 
        "desc": "Wstrząsający esej o pobycie w Auschwitz. Frankl wierzy, że najgłębszym popędem człowieka nie jest seks czy władza, ale poszukiwanie sensu i celu życia."
    },
    {
        "title": "Osobiste doświadczenie", 
        "author": "Kenzaburo Oe", 
        "img": "https://s.lubimyczytac.pl/upload/books/5029000/5029192/1011130-352x500.jpg", 
        "desc": "Noblista stawia pytania o odpowiedzialność za drugiego człowieka. Główny bohater zmaga się z lękami wobec wychowywania niepełnosprawnego dziecka."
    }
]

# KSIĄŻKI NADCHODZĄCE
books_upcoming = [
    {
        "title": "Zanim powiesz żegnaj", 
        "author": "Reese Witherspoon, Harlan Coben", 
        "img": "https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/zanim-powiesz-zegnaj-b-iext202849963.jpg", 
        "desc": "Maggie McCabe, elitarny chirurg, wkracza do świata niewypowiedzianego bogactwa w tajemniczej klinice. Gdy jej pacjent znika bez śladu, Maggie wie, że musi uciekać, by nie podzielić jego losu."
    },
    {
        "title": "Pomoc domowa", 
        "author": "Freida McFadden", 
        "img": "https://s.lubimyczytac.pl/upload/books/5217000/5217086/1320177-352x500.jpg", 
        "desc": "Millie sprząta luksusową willę Winchesterów. Widzi kłamstwa i cienie, które przygniatają tę rodzinę. Ale Winchesterowie nie wiedzą, kim naprawdę jest Millie i do czego jest zdolna."
    },
    {
        "title": "Billy Summers", 
        "author": "Stephen King", 
        "img": "https://s.lubimyczytac.pl/upload/books/5211000/5211561/1310173-352x500.jpg", 
        "desc": "Billy Summers jest snajperem, który eliminuje tylko złych ludzi. Przyjmuje ostatnie zlecenie przed zasłużoną emeryturą. Czy uda mu się odejść z branży bez szwanku?"
    },
    {
        "title": "Poniedziałek z matchą", 
        "author": "Michiko Aoyama", 
        "img": "https://s.lubimyczytac.pl/upload/books/5218000/5218728/1323322-352x500.jpg", 
        "desc": "Ciepła opowieść o nowych początkach przy filiżance matchy w Marble Cafe. Idealna lektura dla tych, którzy szukają spokoju i własnej siły."
    }
]

reviews = []

@app.route('/')
def index():
    return render_template(
        'index.html',
        discussed=books_discussed,
        upcoming=books_upcoming,
        reviews=reviews,
        users=users
    )

@app.route('/about-me') # <--- TO MUSI BYĆ TAKIE SAME JAK W <A HREF>
def about():
    return render_template('about_me.html') # <--- PLIK MUSI SIĘ TAK NAZYWAĆ

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Zapisujemy wiadomość jako słownik do listy
        all_messages.append({
            "name": name, 
            "email": email, 
            "text": message
        })

        print(f"Odebrano wiadomość od {name}!") # Zostawiamy dla Twojej kontroli w terminalu
        return render_template('contact.html', success="Wiadomość została wysłana do administratora!")
    
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        if login and password:
            users[login] = {"name": login.capitalize(), "pass": password}
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Sprawdzamy czy użytkownik jest w bazie (słownik users)
        if username in users and users[username]['pass'] == password:
            session['user'] = username
            # PO ZALOGOWANIU MUSI BYĆ PRZEKIEROWANIE (302), A NIE 200
            return redirect(url_for('dashboard'))
        else:
            # Jeśli błędne dane, odświeżamy stronę logowania z błędem
            return render_template('login.html', error="Błędny login lub hasło")
            
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Tutaj zbieramy dane z formularza recenzji
        rev = {
            "user": session['user'], 
            "book": request.form.get('book'), 
            "rating": request.form.get('rating'),
            "text": request.form.get('review')
        }
        reviews.append(rev)
        
    # DODAJ TUTAJ: all_messages=all_messages
    return render_template('dashboard.html', 
                           users=users, 
                           reviews=reviews, 
                           books=books_discussed, 
                           all_messages=all_messages)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)