from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
app= Flask(__name__)

@app.route('/')
@app.route('/patient')
def showpatient():
    db = sqlite3.connect('covid19.db')
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select 환자.연번, 확진일, 지역, 여행력, 접촉력, 병원ID, 상태 from 환자, 접수 where 접수.연번 = 환자.연번'
    ).fetchall()

    db.close()
    return render_template('patient.html', items=items)

@app.route('/patient/edit/<int:patient_id>/', methods=['GET','POST'])
def editpatient(patient_id):
    if request.method=='POST':
        db = sqlite3.connect("covid19.db")
        db.row_factory = sqlite3.Row
        db.execute(
            ' update 접수 SET'
            ' 상태 = ? '
            ' where 접수.연번 = ?',
            (request.form['patient_name'],patient_id)
        )
        db.execute(
            ' update 환자 SET'
            ' 접촉력 = ? '
            ' where 환자.연번 = ?',
            (request.form['patient_name'],patient_id)
        )
        
        db.commit()
        db.close()
        return redirect(url_for('showpatient'))
    else:
        db = sqlite3.connect("covid19.db")
        db.row_factory = sqlite3.Row
        item = db.execute(
            'select 환자.연번, 확진일, 지역, 여행력, 접촉력, 병원ID, 상태 from 환자, 접수 where 접수.연번 = 환자.연번 and 환자.연번=?',(patient_id,)
        ).fetchone()
        db.close()
        return render_template('editpatient.html', item=item)
if __name__ == '__main__':
    app.debug= True
    app.run(host='127.0.0.1', port=5000)