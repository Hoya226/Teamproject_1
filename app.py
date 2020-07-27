from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging
import pymysql
from passlib.hash import pbkdf2_sha256
# from data import Articles

app = Flask(__name__)
app.debug=True

db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='myflaskapp')
#init mysql 
# mysql = MySQL(app)
# cur  = mysql.connection.cursor()
# result  = cur.execute("SELECT * FROM users;")
# users  = cur.fetchall()
# print(users)
# print(result)

@app.route('/')
def index():
    print("Success")
    # return "TEST"
    return render_template('home.html',hello="GaryKim")

# @app.route('/about')
# def about():
#     print("Success")
#     # return "TEST"
#     return render_template('about.html',hello="GaryKim")

@app.route('/register',methods=['GET' ,'POST'])
def register():
    if request.method == 'POST':
        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        # name = form.name.data
        if(pbkdf2_sha256.verify(re_password,password )):
            print(pbkdf2_sha256.verify(re_password,password ))
            cursor = db.cursor()
            sql = '''
                INSERT INTO users (name , email , username , password) 
                VALUES (%s ,%s, %s, %s )
             '''
            cursor.execute(sql , (name,email,username,password ))
            db.commit()
            
            # cursor = db.cursor()
            # cursor.execute('SELECT * FROM users;')
            # users = cursor.fetchall()
            
            return redirect(url_for('login'))
        else:
            return "Invalid Password"
        db.close()
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['email']
        pw = request.form.get('password')
        print([id])
        sql='SELECT * FROM users WHERE email = %s'
        cursor  = db.cursor()
        cursor.execute(sql, [id])
        users = cursor.fetchone()
        print(users)
        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                return redirect(url_for('articles'))
            else:
                return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

# @app.route('/articles')
# def articles():
#     # data = Articles()
#     # print(len(articles))
#     cursor = db.cursor()
#     sql='SELECT * FROM topic;'
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     print(data)
#     return render_template('articles.html',articles=data)
#     # return "GET Success"

# @app.route('/article/<string:id>')
# def article(id):
#     # print(type(id))
#     # articles= Articles()[id-1]
#     cursor = db.cursor()
#     sql = 'SELECT * FROM topic WHERE id= %s;'
#     cursor.execute(sql, [id])
#     topic = cursor.fetchone()
#     print(topic)
#     return render_template('article.html',data =topic)
    
# @app.route('/add_articles',methods=['GET','POST'])
# def add_articles():
#     if request.method == 'POST':
#         # print(request.form['title'])
#         title = request.form['title']
#         body = request.form['body']
#         author = request.form['author']
#         cursor = db.cursor()
#         sql = '''
#             INSERT INTO topic (title, body , author)
#             VALUES (%s ,%s ,%s)
#         '''
#         cursor.execute(sql,(title, body , author))
#         db.commit()


#         # sql = 'SELECT * FROM topic WHERE id= %s;'
#         # cursor.execute(sql, [id])
#         # topic = cursor.fetchone()
#         return redirect("/articles")
#     else:
#         return render_template('add_articles.html')

#     db.close()


# @app.route('/article/<string:id>/edit_article',methods=['GET', 'POST'])
# def edit_article(id):
#     if request.method =="POST":
#         title = request.form['title']
#         body = request.form['body']
#         author = request.form['author']
#         cur = db.cursor()
#         sql = '''
#             UPDATE `topic` SET `title`=%s,`body`=%s, `author`=%s  WHERE  `id`= %s;
#         '''
#         cur.execute(sql , (title,body,author, id ))
#         db.commit()
#         return redirect(url_for('articles'))
#     else:
#         print(id)
#         cur = db.cursor()
#         sql = 'SELECT * FROM topic WHERE id=%s'
#         cur.execute(sql , [id])
#         topic = cur.fetchone()
#         return render_template('edit_article.html', data= topic)


# @app.route('/delete/<string:id>', methods=['POST'])
# def delete(id):
#     cursor = db.cursor()
#     sql = 'DELETE FROM `topic` WHERE  `id`=%s'
#     cursor.execute(sql ,[id])
#     db.commit()

#     return redirect(url_for('articles'))

if __name__ =='__main__':
    # app.run(host='0.0.0.0', port='8080')
    app.run()