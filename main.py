from flask import Flask,render_template,request,redirect,session,url_for
import urllib.request
from functools import wraps
from db import Database





app=Flask(__name__)
app.secret_key='1234'

db=Database()
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args,**kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('Home.html')





@app.route('/perform_login',methods=['POST'])
def perform_login():
    email=request.form.get('User_email')
    password=request.form.get('User_password')
    user=db.login(email,password)
    if user:  
        session['user_id']=user['id']
        session['user_name']=user['name']
        return redirect(url_for('dashboard'))
    else:
        return render_template('Home.html',message='Invalid Email or Password')
    

@app.route('/register',methods=['GET','POST'])
def register_page():
    
   # session['user_type']='user'
    return render_template('register.html')
@app.route('/perform_registration',methods=['POST'])
def perform_registration():
    name=request.form.get('user_name')
    email=request.form.get('user_email')
    password=request.form.get('user_password')
    user_type=session.get('user_type')
    response=db.insert(name,email,password,user_type)
    
    if response:
        return redirect(url_for('index'))
    else:
        return render_template('home.html',message="Email Already registered")
@app.route('/dashboard')
@login_required
def dashboard():
    posts=db.get_all_posts()
    return render_template('dashboard.html',posts=posts)


@app.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title=request.form.get('title')
        content=request.form.get('content')
        Author_ID=session.get('user_id')
        
        db.insert_post(title,content,Author_ID)
        return redirect(url_for('dashboard'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post=db.get_post_by_id(post_id)
    comments=db.get_comments(post_id)
    return render_template('post.html',post=post,comments=comments)


@app.route('/add_comment/<int:post_id>',methods=['POST'])
@login_required
def add_comment(post_id):
    comment=request.form.get('comment')
    user_id=session.get('user_id')
    
    db.insert_comment(comment,user_id,post_id)
    return redirect(url_for('view_post',post_id=post_id))


@app.route('/edit_post/<int:post_id>',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post=db.get_post_by_id(post_id)
    
    
    if post['author_id'] != session['user_id']:
        return 'Unauthorized'
    
    if request.method == 'POST':
        title=request.form.get('title')
        content=request.form.get('content')
        
        db.update_post(post_id,title,content)
        return redirect(url_for('dashboard'))
    
    return render_template('edit_post.html',post=post)



@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post=db.get_post_by_id(post_id)
    
    
    if post['author_id'] == session['user_id']:
        db.delete_post(post_id)
        
        
        return redirect(url_for('dashboard'))


@app.route('/profile')
@login_required
def profile():
    user_id=session.get('user_id')
    user=db.get_user(user_id)
    posts=db.get_user_posts(user_id)
    
    return render_template('profile.html',user=user,posts=posts)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))





    
if __name__=='__main__':
    app.run(debug=True)