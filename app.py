from flask import Flask, jsonify, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
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


html = """
<!DOCTYPE html>
<html>
<head>
<title>Student Manager Pro</title>

<style>

body{
font-family: Arial;
background: linear-gradient(135deg,#141e30,#243b55);
color:white;
text-align:center;
padding:30px;
}

.container{
backdrop-filter: blur(10px);
background: rgba(255,255,255,0.1);
border-radius:15px;
padding:25px;
width:650px;
margin:auto;
}

input{
padding:10px;
margin:5px;
border:none;
border-radius:5px;
}

button{
padding:10px 15px;
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

.stat{
margin:10px;
font-size:18px;
}

</style>
</head>

<body>

<h1>🎓 Student Manager Pro</h1>

<div class="container">

<div class="stat">
Total Students: <span id="count">0</span>
</div>

<input id="search" placeholder="Search student..." onkeyup="searchStudent()">

<h3>Add / Update Student</h3>

<input id="id" placeholder="ID (for update)">
<input id="name" placeholder="Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<br>

<button onclick="addStudent()">Add</button>
<button onclick="updateStudent()">Update</button>

<table id="table">

<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>

</table>

</div>


<script>

let allStudents=[]

function loadStudents(){

fetch('/students')
.then(res=>res.json())
.then(data=>{

allStudents=data

document.getElementById("count").innerText=data.length

let table=document.getElementById("table")

table.innerHTML=`<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>`

data.forEach(s=>{
table.innerHTML+=`
<tr>
<td>${s.id}</td>
<td>${s.name}</td>
<td>${s.grade}</td>
<td>${s.section}</td>
<td>
<button onclick="fill(${s.id},'${s.name}',${s.grade},'${s.section}')">Edit</button>
<button onclick="deleteStudent(${s.id})">Delete</button>
</td>
</tr>`
})

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

function updateStudent(){

let id=document.getElementById("id").value

fetch('/students/'+id,{
method:'PUT',
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

function fill(id,name,grade,section){

document.getElementById("id").value=id
document.getElementById("name").value=name
document.getElementById("grade").value=grade
document.getElementById("section").value=section

}

function searchStudent(){

let q=document.getElementById("search").value.toLowerCase()

let filtered=allStudents.filter(s=>s.name.toLowerCase().includes(q))

let table=document.getElementById("table")

table.innerHTML=`<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>`

filtered.forEach(s=>{
table.innerHTML+=`
<tr>
<td>${s.id}</td>
<td>${s.name}</td>
<td>${s.grade}</td>
<td>${s.section}</td>
<td>
<button onclick="fill(${s.id},'${s.name}',${s.grade},'${s.section}')">Edit</button>
<button onclick="deleteStudent(${s.id})">Delete</button>
</td>
</tr>`
})

}

loadStudents()

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(html)


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

    return jsonify({"message":"Student added"})


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data=request.get_json()

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute(
        "UPDATE students SET name=?, grade=?, section=? WHERE id=?",
        (data["name"],data["grade"],data["section"],id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Updated"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message":"Deleted"})


if __name__ == "__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
