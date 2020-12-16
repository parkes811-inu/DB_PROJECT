from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app= Flask(__name__)
@app.route('/')
@app.route('/homepage', methods=['GET','POST'])
def showhome():
    db = sqlite3.connect('covid19.db')
    #db.row_factory = sqlite3.Row
    c=db.cursor()
    db.row_factory=lambda cursor, row:row[0]

    items = db.execute(
        'select count(*) from 환자'
    ).fetchall()
    items2 = db.execute(
        'select count(*) from 접수 where 상태="퇴원"'
     ).fetchall()
    items3 = db.execute(
        'select count(*) from 접수 where 상태="사망"'
    ).fetchall()
    db.close()
    return render_template('homepage.html', items=items, items2=items2, items3=items3)

@app.route('/patient', methods=['GET','POST'])
def showpatient():
    if request.method=='POST':
        #if request.form:
        print('11')
        # db = sqlite3.connect("covid19.db")
        # db.row_factory = sqlite3.Row
        # cursor = db.cursor()
        # cursor.execute(
        #     'delete from 환자 where 환자.연번=?',(patient_id, )
        # )
        # db.commit()
        # db.close()

    db = sqlite3.connect('covid19.db')
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select 환자.연번, 확진일, 지역, 여행력, 접촉력, 병원ID, 상태 from 환자, 접수 where 접수.연번 = 환자.연번'
    ).fetchall()
    db.close()

    return render_template('patient.html', items=items)
@app.route('/hospital')
def showhospital():
    

    db = sqlite3.connect('covid19.db')
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select 병원ID, 병원이름, 입원환자, 최대입원환자, 전화번호 from 병원'
    ).fetchall()


    db.close()
    return render_template('hospital.html', items=items)    

@app.route('/patient/edit/<int:patient_id>/', methods=['GET','POST'])
def editpatient(patient_id):
    if request.method=='POST':
        db = sqlite3.connect("covid19.db")
        db.row_factory = sqlite3.Row
        if request.form['patient_name'] != 'NULL':
            db.execute(
                ' update 접수 SET'
                ' 상태 = ? '
                ' where 접수.연번 = ?',
                (request.form['patient_name'],patient_id)
        )
        if request.form['patient_name1'] != 'NULL':
            db.execute(
                ' update 환자 SET'
                ' 접촉력 = ? '
                ' where 환자.연번 = ?',
                (request.form['patient_name1'],patient_id)
        )
        if request.form['patient_name2'] != 'NULL':
            db.execute(
                ' update 환자 SET'
                ' 여행력 = ? '
                ' where 환자.연번 = ?',
                (request.form['patient_name2'],patient_id)
        )
        if request.form['patient_name3'] != 'NULL':
            db.execute(
                ' update 환자 SET'
                ' 지역 = ? '
                ' where 환자.연번 = ?',
                (request.form['patient_name3'],patient_id)
        )
        if request.form['patient_name4'] != 'NULL':
            db.execute(
                ' update 환자 SET'
                ' 확진일 = ? '
                ' where 환자.연번 = ?',
                (request.form['patient_name4'],patient_id)
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

@app.route('/delete/<int:patient_id>')
def delete(patient_id):
    db = sqlite3.connect("covid19.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(
        'delete from 환자 where 환자.연번=?',(patient_id, )
    )
    db.commit()
    db.close()
    
    return redirect(url_for('showpatient'))

if __name__ == '__main__':
    app.debug= True
    app.run(host='127.0.0.1', port=7000)