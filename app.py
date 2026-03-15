dashboard = """
<!DOCTYPE html>
<html>
<head>
<title>Student Manager</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family:Arial;
background:linear-gradient(135deg,#9CAF88,#7A9D76);
color:white;
text-align:center;
padding:30px;
}

.container{
background:rgba(255,255,255,0.15);
backdrop-filter: blur(10px);
padding:25px;
border-radius:15px;
width:700px;
margin:auto;
box-shadow:0 10px 25px rgba(0,0,0,0.2);
}

input{
padding:10px;
margin:5px;
border-radius:6px;
border:none;
outline:none;
}

button{
padding:10px 16px;
margin:5px;
border:none;
border-radius:6px;
cursor:pointer;
font-weight:bold;
transition:0.2s;
}

.add-btn{
background:#4CAF50;
color:white;
}

.edit-btn{
background:#FFC107;
color:black;
}

.delete-btn{
background:#E53935;
color:white;
}

button:hover{
transform:scale(1.05);
}

table{
width:100%;
margin-top:20px;
border-collapse:collapse;
background:rgba(255,255,255,0.05);
}

th,td{
padding:12px;
border-bottom:1px solid rgba(255,255,255,0.3);
}

</style>

</head>

<body>

<h1>🌿 Student Manager</h1>

<div class="container">

<h3>Add / Edit Student</h3>

<input id="studentId" placeholder="ID for update">
<input id="name" placeholder="Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<br>

<button class="add-btn" onclick="addStudent()">➕ Add</button>
<button class="edit-btn" onclick="updateStudent()">✏️ Update</button>

<h3>Students</h3>

<table id="table"></table>

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

table.innerHTML=`
<tr>
<th>ID</th>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Action</th>
</tr>
`

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
<button class="edit-btn" onclick="editStudent(${s.id}, '${s.name}', '${s.grade}', '${s.section}')">✏️ Edit</button>
<button class="delete-btn" onclick="deleteStudent(${s.id})">🗑 Delete</button>
</td>
</tr>
`

})

drawChart(names,grades)

})

}

function editStudent(id,name,grade,section){

document.getElementById("studentId").value=id
document.getElementById("name").value=name
document.getElementById("grade").value=grade
document.getElementById("section").value=section

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
})
.then(()=>loadStudents())

}

function updateStudent(){

let id=document.getElementById("studentId").value

fetch('/students/'+id,{
method:'PUT',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
name:document.getElementById("name").value,
grade:document.getElementById("grade").value,
section:document.getElementById("section").value
})
})
.then(()=>loadStudents())

}

function deleteStudent(id){

fetch('/students/'+id,{
method:'DELETE'
})
.then(()=>loadStudents())

}

function drawChart(names,grades){

if(chart) chart.destroy()

chart=new Chart(document.getElementById('chart'),{
type:'bar',
data:{
labels:names,
datasets:[{
label:'Grade Level',
data:grades
}]
}
})

}

loadStudents()

</script>

</body>
</html>
"""
