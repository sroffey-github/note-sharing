from flask import Flask, render_template, request, flash, redirect, url_for, session
import config, uuid, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form['submitBtn'] == "Add":

            date = str(datetime.datetime.now().strftime('%d/%m/%Y'))
            user = 'spencer' # session['user']
            note = request.form['note']
            if config.add_user(date, user, note):
                return render_template('index.html', data=config.get_data())
            else:
                flash('Error Adding Note!')
                return render_template('index.html', data=config.get_data())

        elif request.form['submitBtn'] == "Save":
            id_ = request.form['editid']
            date = request.form['editdate']
            user = request.form['edituser']
            note = request.form['editnote']
            if config.edit_user(id_, date, user, note):
                return render_template('index.html', data=config.get_data())
            else:
                flash('Error Editing Note Data!')
                return render_template('index.html', data=config.get_data())

        else:
            return render_template('index.html', data=config.get_data())
    else:
        return render_template('index.html', data=config.get_data())

@app.route('/delete/<id_>')
def delete(id_):
    if config.delete_user(id_):
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    config.init()
    app.run(debug=True)