from flask_login import current_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import flask
from werkzeug.exceptions import abort
from credit import db

from credit.db  import get_db
from credit.auth import login_required
bp = Blueprint('credit', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():   
    if request.method == 'POST':          
        age = request.form['age']
        credit = request.form['credit']        
        db = get_db()
        error = None 
          
        if not age:
            error = 'Age is required.'
        if not credit:
            error = 'Credit is required.'        

        age=int(age)
        credit=float(credit)
        if age > 18 and credit < 100.000:
            status = 'Approved'
            error = None
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'INSERT INTO ticket (stage, fk_user_id, credit)'
                    ' VALUES (?, ?, ?)',
                    (status, g.user['id'], credit)
                )
                db.commit()

            return redirect(url_for('credit.ticket'))
        else:
            status = 'Denied'
            error = None

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'INSERT INTO ticket (stage, fk_user_id, credit)'
                    ' VALUES (?, ?, ?)',
                    (status, g.user['id'], credit)
                )
                db.commit()

            return redirect(url_for('credit.ticket'))

    return render_template('credit/index.html')

@bp.route("/consultar")
@login_required
def consultar():
    if request.method == 'POST':     
        num = request.form['num_ticket']
        db = get_db()
        error = None
        if error is not None:
            flash(error)
        else:           
            stage = db.execute(
                'SELECT stage FROM ticket WHERE ticket_id = ?',
                (num,)  
            ).fetchall()
        return render_template('credit/consultar.html')

@bp.route("/ticket")
@login_required
def ticket():
    user = g.user['id']
    db = get_db()
    error = None
    if error is not None:
        flash(error)
    else:             
        ticket_info = db.execute(
            'SELECT p.ticket_id, stage, username FROM ticket p JOIN user u ON p.fk_user_id = u.id WHERE p.fk_user_id = ?',
            (user,)
         ).fetchall()

    return render_template('credit/ticket.html', ticket=ticket_info)
