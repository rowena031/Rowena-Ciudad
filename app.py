from flask import Flask, jsonify, request, render_template_string, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"
DB = "students.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade INTEGER,
        section TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# LOGIN PAGE
login_page = """
<html>
<head>
<title>Login</title>

<style>
body{
font-family:Arial;
background:linear-gradient(135deg,#141e30,#243b55);
display:flex;
justify-content:center;
align-items:center;
height:100vh;
color:white;
}

.box{
background:rgba(255,255,255,0.1);
padding:40px;
border-radius:10px;
text-align:center;
}

input{
padding:10px;
margin:10px;
border:none;
border-radius:5px;
}

button{
padding:10px 20px;
border:none;
background:#00c6ff;
color:white;
border-radius:5px;
cursor:pointer;
}
</style>
</head>

<body>

<div class="box">

<h2>Admin Login</h2>

<form method="POST">

<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>

<button>Login</button>

</form>

</div>

</body>
</html>
"""


# DASHBOARD
dashboard = """
<!DOCTYPE html>
<html>
<head>
<title>Student Manager</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family:Arial;
background:linear-gradient(135deg,#141e30,#243b55);
color:white;
text-align:center;
padding:30px;
}

.container{
background:rgba(255,255,255,0.1);
padding:25px;
border-radius:15px;
width:700px;
margin:auto;
}

input{
padding:10px;
margin:5px;
border-radius:5px;
border:none;
}

button{
padding:10px 15px;
margin:5px;
border:none;
border-radius:5px;
background:#00c6ff;
color:white;
cursor:pointer;
}

table{
width:100%;
margin-top:20px;
border-collapse:collapse;
}

th,td{
padding:10px;
border-bottom:1px solid rgba(255,255,255,0.2);
}

</style>

</head>

<body>

<h1>🎓 Student Manager</h1>

<div class="container">

<h3>Add Student</h3>

<input id="name" placeholder="Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<br>

<button onclick="addStudent()">Add</button>

<h3>Students</h3>

<table id="table">
<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>
</table>

<h3>Student Grade Chart</h3>

<canvas id="chart"></canvas>

</div>


<script>

let chart

function loadStudents(){

fetch('/students')
.then(res=>res.json())
.then(data=>{

let table=document.getElementById("table")

table.innerHTML=`<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>`

let names=[]
let grades=[]

data.forEach(s=>{

names.push(s.name)
grades.push(s.grade)

table.innerHTML+=`
<tr>
<td>${s.id}</td>
<td>${s.name}</td>
<td>${s.grade}</td>
<td>${s.section}</td>
<td>
<button onclick="deleteStudent(${s.id})">Delete</button>
</td>
</tr>`

})

drawChart(names,grades)

})
}


function drawChart(names,grades){

if(chart) chart.destroy()

chart=new Chart(document.getElementById('chart'),{
type:'bar',
data:{
labels:names,
datasets:[{
label:'Grades',
data:grades
}]
}
})

}


function addStudent(){

fetch('/students',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
name:document.getElementById("name").value,
grade:document.getElementById("grade").value,
section:document.getElementById("section").value
})
}).then(()=>loadStudents())

}


function deleteStudent(id){

fetch('/students/'+id,{
method:'DELETE'
}).then(()=>loadStudents())

}

loadStudents()

</script>

</body>
</html>
"""


# LOGIN ROUTE
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")

    return login_page


@app.route("/dashboard")
def home():

    if "user" not in session:
        return redirect("/")

    return render_template_string(dashboard)


# CRUD API
@app.route("/students", methods=["GET"])
def get_students():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    conn.close()

    students=[{"id":r[0],"name":r[1],"grade":r[2],"section":r[3]} for r in rows]

    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():

    data=request.get_json()

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute(
        "INSERT INTO students(name,grade,section) VALUES(?,?,?)",
        (data["name"],data["grade"],data["section"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"added"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message":"deleted"})


if __name__ == "__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
