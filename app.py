from flask import Flask, jsonify, request, render_template_string, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"
DB = "students.db"

# -----------------------------
# DATABASE
# -----------------------------
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

# -----------------------------
# LOGIN PAGE
# -----------------------------
login_page = """
<h2>Login</h2>
<form method="POST">
Username: <input name="username"><br><br>
Password: <input name="password" type="password"><br><br>
<button>Login</button>
</form>
"""

# -----------------------------
# DASHBOARD
# -----------------------------
dashboard = """
<!DOCTYPE html>
<html>
<head>
<title>Student Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>

<h2>Student Dashboard</h2>

<input id="search" placeholder="Search..." onkeyup="searchStudent()">

<h3>Add / Update</h3>
<input id="id" placeholder="ID">
<input id="name" placeholder="Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<br><br>
<button onclick="addStudent()">Add</button>
<button onclick="updateStudent()">Update</button>

<h3>Students</h3>
<table border="1" id="table"></table>

<h3>Chart</h3>
<canvas id="chart"></canvas>

<script>

let students=[]
let chart

function loadStudents(){
    fetch('/students')
    .then(res=>res.json())
    .then(data=>{
        students=data
        drawTable(data)

        let names=data.map(s=>s.name)
        let grades=data.map(s=>s.grade)

        drawChart(names,grades)
    })
}

function drawTable(data){
    let table=document.getElementById("table")

    table.innerHTML=`
    <tr>
    <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Action</th>
    </tr>
    `

    data.forEach(s=>{
        table.innerHTML+=`
        <tr>
        <td>${s.id}</td>
        <td>${s.name}</td>
        <td>${s.grade}</td>
        <td>${s.section}</td>
        <td>
        <button onclick="fillForm(${s.id},'${s.name}','${s.grade}','${s.section}')">Edit</button>
        <button onclick="deleteStudent(${s.id})">Delete</button>
        </td>
        </tr>
        `
    })
}

function fillForm(id,name,grade,section){
    document.getElementById("id").value=id
    document.getElementById("name").value=name
    document.getElementById("grade").value=grade
    document.getElementById("section").value=section
}

function searchStudent(){
    let q=document.getElementById("search").value.toLowerCase()
    let filtered=students.filter(s=>s.name.toLowerCase().includes(q))
    drawTable(filtered)
}

function drawChart(names,grades){
    if(chart) chart.destroy()

    chart=new Chart(document.getElementById("chart"),{
        type:"bar",
        data:{
            labels:names,
            datasets:[{
                label:"Grades",
                data:grades
            }]
        }
    })
}

function addStudent(){
    fetch("/students",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            name:document.getElementById("name").value,
            grade:document.getElementById("grade").value,
            section:document.getElementById("section").value
        })
    }).then(()=>loadStudents())
}

function updateStudent(){
    let id=document.getElementById("id").value

    fetch("/students/"+id,{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            name:document.getElementById("name").value,
            grade:document.getElementById("grade").value,
            section:document.getElementById("section").value
        })
    }).then(()=>loadStudents())
}

function deleteStudent(id){
    fetch("/students/"+id,{
        method:"DELETE"
    }).then(()=>loadStudents())
}

loadStudents()

</script>

</body>
</html>
"""

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")

    return render_template_string(login_page)


@app.route("/dashboard")
def dashboard_page():
    if "user" not in session:
        return redirect("/")
    return render_template_string(dashboard)


# -----------------------------
# API
# -----------------------------
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    conn.close()

    students = [{"id":r[0],"name":r[1],"grade":r[2],"section":r[3]} for r in rows]
    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students(name,grade,section) VALUES(?,?,?)",
        (data["name"], data["grade"], data["section"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"added"})


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "UPDATE students SET name=?, grade=?, section=? WHERE id=?",
        (data["name"], data["grade"], data["section"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"updated"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message":"deleted"})


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
