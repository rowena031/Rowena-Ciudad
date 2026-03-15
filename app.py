from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

students = [
    {"id": 1, "name": "John", "grade": 10, "section": "Zechariah"}
]

# UI Template
html_ui = """
<!DOCTYPE html>
<html>
<head>
<title>Student Manager</title>
<style>
body{
font-family: Arial;
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;
padding:30px;
}

.container{
background:white;
color:black;
padding:20px;
border-radius:10px;
width:500px;
margin:auto;
}

input{
padding:8px;
margin:5px;
}

button{
padding:8px 12px;
margin:5px;
border:none;
background:#667eea;
color:white;
border-radius:5px;
cursor:pointer;
}

table{
margin:auto;
margin-top:20px;
border-collapse:collapse;
}

td,th{
padding:8px;
border:1px solid #ddd;
}
</style>
</head>

<body>

<h1>🎓 Student CRUD Dashboard</h1>

<div class="container">

<h3>Add Student</h3>

<input id="name" placeholder="Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<br>

<button onclick="addStudent()">Add Student</button>

<h3>Students</h3>

<table id="studentTable">
<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Actions</th>
</tr>
</table>

</div>

<script>

function loadStudents(){
fetch('/students')
.then(res=>res.json())
.then(data=>{
let table=document.getElementById("studentTable")
table.innerHTML=`<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Actions</th>
</tr>`

data.forEach(s=>{
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
})
}

function addStudent(){

let name=document.getElementById("name").value
let grade=document.getElementById("grade").value
let section=document.getElementById("section").value

fetch('/students',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
name:name,
grade:grade,
section:section
})
})
.then(res=>res.json())
.then(()=>{
loadStudents()
})
}

function deleteStudent(id){

fetch('/students/'+id,{
method:'DELETE'
})
.then(()=>{
loadStudents()
})

}

loadStudents()

</script>

</body>
</html>
"""

# UI
@app.route('/')
def home():
    return render_template_string(html_ui)


# READ
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


# CREATE
@app.route('/students', methods=['POST'])
def add_student():

    data=request.get_json()

    new_id=len(students)+1

    student={
    "id":new_id,
    "name":data["name"],
    "grade":data["grade"],
    "section":data["section"]
    }

    students.append(student)

    return jsonify(student)


# UPDATE
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):

    data=request.get_json()

    for student in students:
        if student["id"]==id:
            student["name"]=data["name"]
            student["grade"]=data["grade"]
            student["section"]=data["section"]
            return jsonify(student)

    return jsonify({"error":"Student not found"}),404


# DELETE
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    global students

    students=[s for s in students if s["id"]!=id]

    return jsonify({"message":"Student deleted"})


if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
