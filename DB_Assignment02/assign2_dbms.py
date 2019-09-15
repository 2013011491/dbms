from flask import Flask, render_template, redirect, request
import csv
import psycopg2 as pg
import psycopg2.extras

db_connect = {
        'host': '127.0.0.1',
        'port': '5432',
        'user': 'postgres',
        'dbname': 'postgres',
        'password':'0000'
    }
con_str = "host={host} user={user} dbname={dbname} password={password} port={port}".format(**db_connect)

app = Flask(__name__)

session = {'id': None}

@app.route("/")
def index():
    session['id'] = None
    return render_template("index.html")

@app.route("/contacts")
def constacts():
    if session['id'] == 'admin' :
        return render_template("contacts.html")
    else :
        return redirect("/")



@app.route("/logout",methods=["GET","POST"])
def logout():
    session['id']=None
    return redirect("/")

@app.route('/login',methods=["POST"])
def login():
    id=request.form.get('id')

    session['id'] = id
    if(id == 'admin'):
        return redirect('/admin')

    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT sname FROM students WHERE sname='{id}'"
    cur.execute(sql)
    rows = cur.fetchall()
    if(len(rows) == 0):
        conn.close()
        session['id'] = None
        return render_template('error.html', msg="Wrong ID")
    conn.close()
    return redirect('/student')
    
@app.route('/admin',methods=["GET","POST"])
def admin():
    if session['id'] == 'admin' :
        return render_template('admin.html')
    else :
        return redirect('/')

@app.route('/student',methods=["GET",'POST'])
def student():
    if session['id'] == 'admin' :
        return redirect('/admin')
    elif session['id'] != None :
        return render_template('student.html',id = session['id'])
    else :
        return redirect('/')

@app.route('/admin/sinfo',methods=["GET",'POST'])
def sinfo():
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql="SELECT * FROM students"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    if session['id'] == 'admin' :
        return render_template('info.html',stu_data = rows)
    return redirect('/')

@app.route('/admin/scontact',methods=["GET",'POST'])
def scon():
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql="SELECT * FROM contacts"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    if session['id']  == 'admin' :
        return render_template('continfo.html',stu_data = rows)
    return redirect('/')

@app.route('/sappend')
def sappend():
    if session['id'] == 'admin' : 
        return render_template('sappend.html')
    return redirect('/')

@app.route('/cappend')
def cappend():
    if session['id'] == 'admin' :
        return render_template('cappend.html')
    return redirect('/')

@app.route('/admin/append',methods=["POST"])
def adminappend():
    info=request.form.get('info')
    info=info.split(',')
    for i in range(len(info)) :
        info[i]=info[i].strip()
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"INSERT INTO students VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}','{info[4]}','{info[5]}','{info[6]}')"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect('/admin/sinfo')

@app.route('/admin/cappend',methods=["POST"])
def admincappend():
    info=request.form.get('info')
    info=info.split(',')
    for i in range(len(info)) :
        info[i]=info[i].strip()
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"INSERT INTO contacts VALUES('{info[0]}','{info[1]}','{info[2]}')"
    cur.execute(sql)
    conn.commit()
    conn.close()

    return redirect('/admin/scontact')

@app.route('/<sid>')
def modify(sid) :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT * FROM students WHERE sid = '{sid}'"
    cur.execute(sql)
    rows=cur.fetchall()
    conn.close()
    try :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"SELECT * FROM { rows[0][2] }"  
        cur.execute(sql)      
    except :
        result1=[]
    else :
        result1=cur.fetchall()    
    conn.close()
    if session['id'] == 'admin' :
        return render_template('sinfo_modify.html',stu_data=rows[0],stu_data1=result1)
    return redirect('/')

@app.route('/<sid>/contact')
def cmodify(sid) :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT * FROM contacts WHERE sid = '{sid}'"
    cur.execute(sql)
    rows=cur.fetchall()
    conn.close()
    
    if session['id']  == 'admin' :
        return render_template('scon_modify.html',stu_data=rows[0])
    return redirect('/')
    
@app.route('/contact/name',methods=["POST"])
def modiname():
    id=request.form.get('id')
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT c.sid, c.phone, c.email FROM students s, contacts c WHERE s.sname = '{id}' AND c.sid = s.sid"
    cur.execute(sql)
    rows=cur.fetchall()
    conn.close()
   
    return render_template('scon_modify.html',stu_data=rows[0],sname=id)


@app.route('/<sid>/complete',methods=["POST"])
def modified_info(sid):
    cancel=request.form.get('cancel')
    modi=request.form.get('modi')
    deli=request.form.get('del')
    passwd=request.form.get('passwd')
    sname=request.form.get('sname')
    sex=request.form.get('sex')
    mid=request.form.get('mid')
    tid=request.form.get('tid')
    grade=request.form.get('grade')

    if cancel !=None :
        return redirect("/admin/sinfo")

    if deli != None :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"DELETE FROM students WHERE sid = '{sid}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        
        return redirect('/admin/sinfo')

    if modi != None :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"UPDATE students SET password ='{passwd}', sname='{sname}', sex='{sex}', major_id={mid},tutor_id='{tid}',grade={grade} WHERE sid = '{sid}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect('/admin/sinfo')

@app.route('/<sid>/cmodicomple',methods=["POST"])
def cmodified_info(sid):
    cancel=request.form.get('cancel')
    modi=request.form.get('modi')
    deli=request.form.get('del')
    if cancel !=None :
        return redirect("/admin/scontact")

    if deli != None :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"DELETE FROM contacts WHERE sid = '{sid}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect('/admin/scontact')

    if modi != None :
        phone=request.form.get('phone')
        email=request.form.get('email')
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"UPDATE contacts SET phone ='{phone}', email ='{email}' WHERE sid = '{sid}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect('/admin/scontact')

@app.route('/private')
def private() :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT * FROM students WHERE sname = '{session['id']}'"
    cur.execute(sql)
    rows=cur.fetchall()
    conn.close()
    print(sql)
    
    if session['id'] == 'admin' :
        return redirect('/admin')
    if session['id'] == None :
        return redirect('/')
    return render_template('privinfo.html',stu_data = rows[0])

@app.route("/s_contacts")
def s_constacts():
    try :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"SELECT * FROM {session['id']}"
        cur.execute(sql)

    except :
        conn.close()
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"CREATE TABLE {session['id']} (name char(15), phone char(15), email varchar, rank char(15), UNIQUE(phone)) "
        cur.execute(sql)
        conn.commit()
        conn.close()
        rows=[]

    else : 
        rows = cur.fetchall()
        conn.close()
    if session['id'] == 'admin' :
        return redirect('/admin')
    elif session['id'] == None :
        return redirect('/')
    return render_template("s_contacts.html", stu_data = rows)

@app.route('/<number>/privmodi')
def privmodi(number) :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT * FROM {session['id']} WHERE phone = '{number}'"
    cur.execute(sql)
    rows=cur.fetchall()
    conn.close()
    if session['id'] == 'admin' :
        return render_template('/admin')
    if session['id'] == None :
        return redirect('/')
    return render_template('priv_modify.html',stu_data = rows[0])    

@app.route('/<number>/pmodicomple',methods=['POST'])
def pmodicom(number) : 
    cancel=request.form.get('cancel')
    modi=request.form.get('modi')
    deli=request.form.get('del')
    if cancel !=None :
        return redirect("/s_contacts")

    if deli != None :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"DELETE FROM {session['id']} WHERE phone = '{number}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect('/s_contacts')

    if modi != None :
        name=request.form.get('name')
        email=request.form.get('email')
        rank=request.form.get('rank')

        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"UPDATE {session['id']} SET name ='{name}', email ='{email}', rank = '{rank}' WHERE phone = '{number}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect('/s_contacts')

@app.route('/pappend',methods=['POST'])
def pappend() :
    return render_template('pappend.html',name=session['id'])

@app.route('/<name>/pappend',methods=["POST"])
def pripappend(name):
    info=request.form.get('info')
    info=info.split(',')
    for i in range(len(info)) :
        info[i]=info[i].strip()
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"INSERT INTO {session['id']} VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}')"
    cur.execute(sql)
    conn.commit()
    conn.close()

    return redirect('/s_contacts')

@app.route('/sending')
def sending() :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"SELECT * FROM contacts"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    try :
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"SELECT * FROM {session['id']}"
        cur.execute(sql)

    except :
        conn.close()
        conn = pg.connect(con_str)
        cur=conn.cursor()
        sql=f"CREATE TABLE {session['id']} (name char(15), phone char(15), email varchar, rank char(15), UNIQUE(phone)) "
        cur.execute(sql)
        conn.commit()
        conn.close()
        result=[]

    else : 
        result = cur.fetchall()
        conn.close()
    
    if session['id'] == 'admin' :
        return redirect('/admin')
    elif session['id'] == None :
        return redirect('/')
    return render_template('sending.html',stu_data=rows,stu_data1=result)

@app.route('/upload',methods = ['POST'])
def fileupload() :
    temp = request.files['file']
    temp.save(temp.filename)

    filepath = '%s' % temp.filename #COPY 가 안됨
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result=[]
    for row in reader :
        result.append(row)

    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql=f"CREATE TABLE temp_contact (name char(15), phone char(15), email varchar, rank char(15), UNIQUE(phone)) "
    cur.execute(sql)
    conn.commit()

    for row in result :
        sql=f"INSERT INTO temp_contact VALUES('{row[0]}','{row[1]}','{row[2]}','{row[3]}')"
        cur.execute(sql)
        conn.commit()

    sql=f"UPDATE {session['id']} SET name=T.name, phone=T.phone, email=T.email, rank=T.rank FROM temp_contact T WHERE {session['id']}.phone = T.phone"
    cur.execute(sql)
    conn.commit()

    sql=f"INSERT INTO {session['id']} (SELECT * FROM temp_contact T WHERE T.phone not in (SELECT phone FROM {session['id']}))"
    cur.execute(sql)
    conn.commit()

    sql="DROP TABLE temp_contact"
    cur.execute(sql)
    conn.commit()
    conn.close()
    
    return redirect('/s_contacts')

@app.route('/dom')
def domainN() :
    conn = pg.connect(con_str)
    cur=conn.cursor()
    sql="SELECT domain, count(*) FROM (SELECT SPLIT_PART(email,'@',2) as domain FROM contacts) AS simple GROUP BY domain "
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    if session['id'] =='admin' :
        return render_template("dom.html",stu_data = rows)
    return redirect('/')

if __name__ == "__main__": 
    app.run(debug=True)