import hashlib
import forms
from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
admin = Admin(app)

from models import Category, User, Order, Dish

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Dish, db.session))

title = "Stepik Delivery"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_cart():
    cart = session.get("cart", [])
    dishes = []
    sum = 0
    count = 0
    if cart:
        for item in cart:
            dish = db.session.query(Dish).filter(Dish.id == item).first()
            dishes.append(dish)
            count = count+1
            sum = sum + dish.price

    return {'dishes': dishes, 'cnt': count, 'sum': sum}


@app.route('/')
def route_main():
    return render_template(
        'main.html', categories=db.session.query(Category).all(), cart=session.get("cart", [])
    )


@app.route('/addtocart/<item>/')
def route_addtocart(item):
    cart = session.get("cart", [])
    cart.append(item)
    session['cart'] = cart
    return redirect("/cart/")


@app.route('/cart/')
def route_cart():
    if request.method == "POST":

        # Получаем отправленные данные
        name = request.form.get("name")
        mail = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")
        address = request.form.get("order_summ")
        dishes = request.form.get("order_cart")

        user = db.session.query(User).filter(User.password == password, User.mail == email).first()
        # Проверяем полученные данные
        if user:

            # Устанавливаем в сессии признак, что пользователь аутентифицирован
            session["is_auth"] = True
            session["user_id"] = user.id
            session["user_email"] = user.mail

            # Редиректим пользователя на приватную страницу
            return redirect("/account/")
    return render_template(
        'cart.html', cart=get_cart(), form=forms.OrderForm()
    )


@app.route('/account/')
def route_account():
    if not session.get("is_auth"):
        return redirect("/auth/")

    email = session.get("user_email")

    user = db.session.query(User).filter(User.mail == email).first()

    if not user:
        return redirect("/auth/")

    return render_template(
        'account.html', user=user
    )


@app.route('/auth/', methods=["GET", "POST"])
def route_auth():
    # Если пользователь авторизован
    if session.get("is_auth"):
        # то редиректим его на приватную страницу
        return redirect("/")

    # Переменная для хранения за ошибок авторизации
    error_msg = ""  # Пока ошибок нет

    # Пришел запрос на аутентификацию
    if request.method == "POST":

        # Получаем отправленные данные
        email = request.form.get("email")
        password = hash_password(request.form.get("password"))

        user = db.session.query(User).filter(User.password == password, User.mail == email).first()
        # Проверяем полученные данные
        if user:

            # Устанавливаем в сессии признак, что пользователь аутентифицирован
            session["is_auth"] = True
            session["user_id"] = user.id
            session["user_email"] = user.mail

            # Редиректим пользователя на приватную страницу
            return redirect("/account/")

        else:

            error_msg = "Неверное имя или пароль"

    # Отображаем форму аутентификации
    return render_template(
        'auth.html', form=forms.AuthForm()
    )


@app.route('/register/', methods=["GET", "POST"])
def route_register():
    # Если пользователь авторизован
    if session.get("is_auth"):
        # то редиректим его на приватную страницу
        return redirect("/")

    # Переменная для хранения за ошибок авторизации
    error_msg = ""  # Пока ошибок нет

    # Пришел запрос на аутентификацию
    if request.method == "POST":

        # Получаем отправленные данные
        email = request.form.get("email")
        password = hash_password(request.form.get("password"))

        userc = db.session.query(User).filter(User.password == password, User.mail == email).count()
        # Проверяем полученные данные
        if userc == 0:
            user = User(mail=email, password=password)
            db.session.add(user)
            db.session.commit()

            # Устанавливаем в сессии признак, что пользователь аутентифицирован
            session["is_auth"] = True
            session["user_id"] = user.id
            session["user_email"] = user.mail

            # Редиректим пользователя на приватную страницу
            return redirect("/account/")

        else:

            error_msg = "Неверное имя или пароль"

    return render_template(
        'register.html', form=forms.AuthForm()
    )


@app.route('/logout/')
def route_logout():
    session.clear()
    return redirect("/")


@app.route('/ordered/')
def route_ordered():
    return render_template(
        'ordered.html',
    )


if __name__ == '__main__':
    app.run()
