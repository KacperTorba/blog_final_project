from flask import render_template, request, flash, redirect, url_for
from blog import app
from .models import Entry, db
from .forms import EntryForm



@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    
    return render_template("homepage.html",all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
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