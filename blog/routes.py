from flask import render_template, request, flash, redirect, url_for, session
from blog import app
from .models import Entry, db
from .forms import EntryForm, LoginForm
import functools


def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions


@app.route('/')
def index():    
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())    
    return render_template("homepage.html",all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def add_edit_entry(entry_id=None):
    errors = None
    form = EntryForm()
    flag = 1
    
    if entry_id == None and request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
               title = form.title.data,
               body = form.body.data,
               is_published = form.is_published.data
           )
            db.session.add(entry)
            db.session.commit()
            
            if form.is_published.data:
                flash(f'Post was successfully add.')
            else:
                flash(f'Post was successfully add but not published.')
                
            return redirect(url_for('index'))
            
        else:
            errors = form.errors
            flash(f'Error: {errors}')              
    
    elif entry_id:        
        flag = 0
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()                
                
                return redirect(url_for('index'))
        
            else:
                errors = form.errors
                flash(f'Error: {errors}')            
                        
    return render_template("entry_form.html", form=form, errors=errors, flag = flag)


@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
           
   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    first = Entry.query.filter_by(id=entry_id).first()
    print(first)
    
    if not first:
        flash('Error')
        return redirect(url_for('index'))
    
    db.session.delete(first)
    db.session.commit()
     
    return redirect(url_for('index'))