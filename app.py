from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Создаем соединение с БД
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базу данных
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))

    def __repr__(self):
        return f'<User {self.username}>'

# Создаем таблицы в БД
Base.metadata.create_all(engine)


class Main:
    def __init__(self):
        self.weather = "Weather"
        self.auth = "Authorization"
        self.info = "Info about service"
        self.contacts = "Contacts"


@app.route('/')
def index():
    main = Main()
    username = request.cookies.get('username')
    return render_template('index.html', main=main, username=username)


@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Проверяем совпадение паролей
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Проверяем, что пользователь с таким именем не существует
        user = session.query(User).filter_by(username=username).first()
        if user:
            return render_template('register.html', error='User already exists')

        # Создаем нового пользователя
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)