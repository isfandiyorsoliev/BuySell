import os
from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'


@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()

    cur.execute("""select * from products;""")
    news_list = []

    for line in cur.fetchall():
        news_list.append(line)

    conn.close()

    # context = {'news': news_list}
    context = {'products': news_list}
    return render_template('index_manual.html', **context)

    # ------------------------------------


@app.route('/category_draft')
def category_draft():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()

    cur.execute("""select category from products group by category;""")
    news_list = []

    for line in cur.fetchall():
        news_list.append(line)

    conn.close()

    context = {'news': news_list}
    return render_template('category_draft.html', **context)
    # ------------------------------------


# ---------------------------------
@app.route('/category')
def category():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    product_category = 'Ноутбук'  # example
    cur.execute("""select * from products where  category= ?;""",
                (product_category,))
    news_list = []

    for line in cur.fetchall():
        news_list.append(line)

    conn.close()

    context = {'news': news_list}
    return render_template('category.html', **context)


# ---------------------------------

@app.route('/need_aut')
def index_manual():
    return render_template('need_aut.html')


@app.route('/index')
def index_user():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()
    cur.execute("""select * from products;""")
    news_list = []
    for line in cur.fetchall():
        news_list.append(line)
    conn.close()
    context2 = {'products': news_list}
    return render_template('index.html', **context2)


@app.route('/ad_input', methods=['GET', 'POST'])
def ad_input():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            image.save(
                os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

            foto_name = image.filename
            print(foto_name)

            conn = sqlite3.connect('products.db')
            cur = conn.cursor()

            name = request.form.get('name')
            tip = request.form.get('tip')
            price = request.form.get('price')
            # condition = request.form.get('condition')
            description = request.form.get('description')
            phone_num = request.form.get('phone_num')
            city = request.form.get('city')
            name_foto = foto_name

            cur.execute(
                """insert into products (title, category, price, description, number, city, photo) values (?,?,?,?,?,?,?)""",
                (name, tip, price, description, phone_num, city, name_foto))
            conn.commit()
            print(name, tip, price, description, phone_num, city, name_foto)
            conn.close()
            return redirect(request.url)
    return render_template('ad_input.html')


# def ad_input():
#   if request.method == 'POST':
#     if request.files:
#       image = request.files['image']
#       image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
#       return redirect(request.url)
#   return render_template('ad_input.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#   if request.method == 'POST':
#     # username = request.form.get('username') 
#     # password = request.form.get('password')

#     conn = sqlite3.connect('reg.db')
#     cur = conn.cursor()  
#     username = request.form.get('username') 
#     password = request.form.get('password')
#     cur.execute("""select * from reg where email= ? and password=?;""",(username,password))
#     log_list = []

#     for line in cur.fetchall():
#       log_list.append(line)
#     print(log_list)
#     conn.close()
#     if log_list:
#       context = {'news': log_list}
#       return render_template('index.html', **context)
#   else:
#     return render_template('login.html')
# ----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # username = request.form.get('username') 
        # password = request.form.get('password')

        conn = sqlite3.connect('reg.db')
        cur = conn.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        cur.execute("""select * from reg where email= ? and password=?;""",
                    (username, password))
        log_list = []

        for line in cur.fetchall():
            log_list.append(line)
        print(log_list)
        conn.close()
        if log_list:
            context1 = {'news': log_list}
            conn = sqlite3.connect('products.db')
            cur = conn.cursor()

            cur.execute("""select * from products;""")
            news_list = []

            for line in cur.fetchall():
                news_list.append(line)

            conn.close()

            # context = {'news': news_list}
            context2 = {'products': news_list}
            return render_template('index.html', **context1, **context2)
        else:
            return render_template('login.html',
                                   error="Неверный пароль или логин")
    else:
        return render_template('login.html')

        # ----------------------------------------
    #   if username == 'admin' and password == 'admin':
    #     return render_template('index.html')
    # else:
    #   return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        conn = sqlite3.connect('reg.db')
        cur = conn.cursor()

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        cur.execute(
            """insert into reg (name, email, password) values (?, ?, ?);""",
            (name, email, password))
        conn.commit()
        # print(name, email, password)
        conn.close()
        # return 'register'
        return redirect('/login')
    return render_template('register.html')


@app.route('/users')
def users():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()

    cur.execute("""select * from products;""")
    news_list = []

    for line in cur.fetchall():
        news_list.append(line)

    conn.close()

    context = {'news': news_list}
    return render_template('users.html', **context)


@app.route('/draft')
def draft():
    conn = sqlite3.connect('reg.db')
    cur = conn.cursor()

    cur.execute("""select * from reg;""")
    reg_list = []

    for line in cur.fetchall():
        reg_list.append(line)

    conn.close()

    context = {'reg': reg_list}
    return render_template('draft.html', **context)


@app.route('/about')
def about():
    return render_template('about.html')


app.run(host='0.0.0.0', port=81)
