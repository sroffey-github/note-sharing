from flask import Flask, redirect, render_template, request, session, flash, redirect, url_for
from dotenv import load_dotenv
import os, config

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if session.get('logged_in'):
            note = request.form['note']
            username = session['username']
            if config.create_note(note, username):
                pass
            else:
                flash('Error, Unable to create note!')
                return render_template('index.html', data=config.get_notes())
        else:
            username = request.form['username']
            password = request.form['password']
            if config.auth(username, password):
                session['logged_in']= True
                session['username'] = username
                return render_template('index.html', data=config.get_notes())
            else:
                flash('Error, Access Denied')
                return render_template('index.html')
    else:
        return render_template('index.html')
    
@app.route('/delete/<noteid>')
def delete(noteid):
    if config.delete_note(noteid):
        flash('Success, note removed')
        return redirect(url_for('index', data=config.get_notes()))
    else:
        flash('Error, note coud not be removed')
        return redirect(url_for('index', data=config.get_notes()))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    config.init()
    app.run(debug=True)