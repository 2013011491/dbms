from flask import Flask, render_template, redirect, request
import csv


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
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    line_count = 0
    for row in reader:
        if line_count>0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()

    for row in result :
        print(row)
        if id == row[2].strip() :
            return redirect('/student')
    session['id'] = None
    return render_template('error.html', msg="Wrong ID")

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
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    line_count = 0
    for row in reader:
        if line_count>0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()
    if session['id'] == 'admin' :
        return render_template('info.html',stu_data = result)
    return redirect('/')

@app.route('/admin/scontact',methods=["GET",'POST'])
def scon():
    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    line_count = 0
    for row in reader:
        if line_count>0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()

    if session['id']  == 'admin' :
        return render_template('continfo.html',stu_data = result)
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
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result=[]
    for row in reader: 
        result.append(row)    
    read_file.close()
    for row in result : #for already existing sid
        print(row)
        if info[0].strip() == row[0].strip() :
            return render_template('error.html', msg="Already exists Sid")

    for row in result : #for already existing name
        print(row)
        if info[2].strip() == row[2].strip() :
            return render_template('error.html', msg="Already exists name")
    read_file.close()
    append_file = open(filepath,mode='a', encoding='utf-8',newline='')
    appender = csv.writer(append_file)
    appender.writerow(info)

    append_file.close()

    return redirect('/admin/sinfo')

@app.route('/admin/cappend',methods=["POST"])
def admincappend():
    info=request.form.get('info')
    info=info.split(',')
    for i in range(len(info)) :
        info[i]=info[i].strip()
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result=[]
    for row in reader: #for already existing sid
        result.append(row)    
    read_file.close()
    check=0
    for row in result :
        if info[0] == row[0].strip() :
            check=1
            break
    if check == 0 :
        return render_template('error.html', msg="No exists Sid")
    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result=[]
    for row in reader: #for already existing sid
        result.append(row)    
    read_file.close()
    for row in result :
        if info[0] == row[0].strip() :
            return render_template('error.html', msg="Already exists Sid")
    read_file.close()
    append_file = open(filepath,mode='a', encoding='utf-8',newline='')
    appender = csv.writer(append_file)
    appender.writerow(info)

    append_file.close()

    return redirect('/admin/scontact')

@app.route('/<sid>')
def modify(sid) :
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []
    result1=[]

    for row in reader:
        if sid == row[0].strip() :
            for i in range(len(row)) :
                result=row
            break
    read_file.close()
    for i in range(len(result)) :
        result[i] = result[i].strip()

    try :
        filepath = 'Private_Contact\\%s.csv' % result[2]
        read_file = open(filepath,mode='r', encoding='utf-8')
        reader = csv.reader(read_file,delimiter=',')
    
    except :
        result1=[]
    
    else :
        line_count=0
        for row in reader:
            if line_count>0 :
                result1.append(row)
            line_count = line_count +1
        read_file.close()
        
    if session['id'] == 'admin' :
        return render_template('sinfo_modify.html',stu_data=result,stu_data1=result1)
    return redirect('/')

@app.route('/<sid>/contact')
def cmodify(sid) :
    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    for row in reader:
        if sid == row[0] :
            result=row
            break
    read_file.close()
    for i in range(len(result)) :
        result[i] = result[i].strip()
    if session['id']  == 'admin' :
        return render_template('scon_modify.html',stu_data=result)
    return redirect('/')
    
@app.route('/contact/name',methods=["POST"])
def modiname():
    id=request.form.get('id')
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    sid=None
    for row in reader:
        if id == row[2].strip() :
            sid = row[0].strip()
            break
    if sid == None :
        return render_template('error.html',msg="Not exist")
    read_file.close()

    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    for row in reader:
        if sid == row[0].strip() :
            result=row
            break
    read_file.close()
    print(result)
    for i in range(len(result)) :
        result[i] = result[i].strip()
    
    return render_template('scon_modify.html',stu_data=result,sname=id)


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
    temp=[sid,passwd,sname,sex,mid,tid,grade]
    if cancel !=None :
        return redirect("/admin/sinfo")

    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []
    for row in reader:
        result.append(row)
    read_file.close()

    for row in result :
        if sname.strip() == row[2].strip() :
            return render_template("error.html", msg = "already exists name")

    if deli != None :
        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if sid != row[0].strip() :
                writer.writerow(row)
        write_file.close()
        return redirect('/admin/sinfo')
    if modi != None :
        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if sid != row[0].strip() :
                writer.writerow(row)
            else :
                writer.writerow(temp)
        write_file.close()
        return redirect('/admin/sinfo')

@app.route('/<sid>/cmodicomple',methods=["POST"])
def cmodified_info(sid):
    cancel=request.form.get('cancel')
    modi=request.form.get('modi')
    deli=request.form.get('del')
    if cancel !=None :
        return redirect("/admin/scontact")

    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []
    for row in reader:
        result.append(row)
    read_file.close()

    if deli != None :
        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if sid.strip() != row[0].strip() :
                writer.writerow(row)
        write_file.close()
        return redirect('/admin/scontact')
    if modi != None :
        phone=request.form.get('phone')
        email=request.form.get('email')
        temp=[sid,phone,email]

        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if sid.strip() != row[0].strip() :
                writer.writerow(row)
            else :
                writer.writerow(temp)
        write_file.close()
        return redirect('/admin/scontact')

@app.route('/private')
def private() :
    filepath = 'CSV_folder\\students.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []


    for row in reader:
        if session['id'] == row[2].strip() :
            result=row
            break
    read_file.close()
    print(result)
    for i in range(len(result)) :
        result[i] = result[i].strip()
    if session['id'] == 'admin' :
        return redirect('/admin')
    return render_template('privinfo.html',stu_data = result)

@app.route("/s_contacts")
def s_constacts():
    try :
        filepath = 'Private_Contact\\%s.csv' %(session['id'])
        read_file = open(filepath,mode='r', encoding='utf-8')
        reader = csv.reader(read_file,delimiter=',')
    except :
        write_file = open(filepath,mode='w',newline='', encoding='utf-8')
        writer = csv.writer(write_file)
        temp=['name', 'number', 'email', 'rank']
        writer.writerow(temp)
        write_file.close()
        read_file = open(filepath,mode='r', encoding='utf-8')
        reader = csv.reader(read_file,delimiter=',')
    result = []
    line_count = 0
    for row in reader:
        if line_count >0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()

    return render_template("s_contacts.html", stu_data = result)

@app.route('/<number>/privmodi')
def privmodi(number) :
    filepath = 'Private_Contact\\%s.csv' % session['id'] 
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []
    for row in reader:
        if number == row[1] :
            result=row
            break
    read_file.close()
    for i in range(len(result)) :
        result[i] = result[i].strip()
    if session['id'] == 'admin' :
        return render_template('/admin')
    return render_template('priv_modify.html',stu_data = result)    

@app.route('/<number>/pmodicomple',methods=['POST'])
def pmodicom(number) : 
    cancel=request.form.get('cancel')
    modi=request.form.get('modi')
    deli=request.form.get('del')
    if cancel !=None :
        return redirect("/s_contacts")

    filepath = 'Private_Contact\\%s.csv' % session['id']
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []
    for row in reader:
        result.append(row)
    read_file.close()

    if deli != None :
        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if number.strip() != row[1].strip() :
                writer.writerow(row)
        write_file.close()
        return redirect('/s_contacts')
    if modi != None :
        name=request.form.get('name')
        email=request.form.get('email')
        rank=request.form.get('rank')
        temp=[name,number,email,rank]

        write_file = open(filepath, mode='w', encoding='utf-8',newline='')
        writer = csv.writer(write_file)
        for row in result :
            if number.strip() != row[1].strip() :
                writer.writerow(row)
            else :
                writer.writerow(temp)
        write_file.close()
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
    filepath = 'Private_Contact\\%s.csv' % session['id']
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result=[]
    for row in reader: #for already existing sid
        result.append(row)    
    read_file.close()
    for row in result :
        if info[1] == row[1] :
            return render_template('error.html', msg="Already exists Phonenumber")
    append_file = open(filepath,mode='a', encoding='utf-8',newline='')
    appender = csv.writer(append_file)
    appender.writerow(info)

    append_file.close()

    return redirect('/s_contacts')

@app.route('/sending')
def sending() :
    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    line_count = 0
    for row in reader:
        if line_count>0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()

    try : 
        filepath = 'Private_Contact\\%s.csv' %(session['id'])
        read_file = open(filepath,mode='r', encoding='utf-8')
        reader = csv.reader(read_file,delimiter=',')
    except :
        write_file = open(filepath,mode='w',newline='', encoding='utf-8')
        writer = csv.writer(write_file)
        temp=['name', 'number', 'email', 'rank']
        writer.writerow(temp)
        write_file.close()
        read_file = open(filepath,mode='r', encoding='utf-8')
        reader = csv.reader(read_file,delimiter=',')
    result2 = []
    line_count = 0
    for row in reader:
        if line_count >0 :
            result2.append(row)
        line_count = line_count+1
    read_file.close()

    if session['id'] == 'admin' :
        return redirect('/admin')
    elif session['id'] == None :
        return redirect('/')
    return render_template('sending.html',stu_data=result,stu_data1=result2)

@app.route('/upload',methods = ['POST'])
def fileupload() :
    temp = request.files['file']
    temp.save(temp.filename)

    filepath = '%s' % temp.filename
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    for row in reader:
        result.append(row)
    read_file.close()

    filepath = 'Private_Contact\\%s.csv' % session['id'] 
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result1 = []
    for row in reader:
        result1.append(row)
    read_file.close()

    print(result1)

    newcheck = 1
    for row in result :
        for i in range(len(result1)) :
            if row[1] == result1[i][1] :
                newcheck = 0
                result1[i] = list(row)
                print(result1[i])
                break
        if newcheck == 0 : 
            newcheck = 1
            continue
        else :
            result1.append(row)
    write_file = open(filepath, mode='w', encoding='utf-8',newline='')
    writer = csv.writer(write_file)
    for row in result1 :
        writer.writerow(row)
    write_file.close()
    
    return redirect('/s_contacts')

@app.route('/dom')
def domainN() :
    filepath = 'CSV_folder\\contacts.csv'
    read_file = open(filepath, encoding='utf-8')
    reader = csv.reader(read_file,delimiter=',')
    result = []

    line_count = 0
    for row in reader:
        if line_count>0 :
            result.append(row)
        line_count = line_count+1
    read_file.close()
    domain=[]
    for row in result :
        if row[2] == '' : 
            domain.append(row[2])
            continue
        domain.append((row[2].split('@'))[1])
    temp = list(set(domain))
    tempN = []
    for i in range(len(temp)) :
        tempN.append(domain.count(temp[i]))
    for i in range(len(temp)) :
        temp[i] = [temp[i], tempN[i]]
    if session['id'] =='admin' :
        return render_template("dom.html",stu_data = temp)
    return redirect('/')

if __name__ == "__main__": 
    app.run(debug=True)