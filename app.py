from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

students = [
    {"name": "John", "grade": 10, "section": "Zechariah"}
]

html_ui = """
<!DOCTYPE html>
<html>
<head>
<title>Student API</title>
<style>
body{
    font-family: Arial;
    background: linear-gradient(135deg,#4facfe,#00f2fe);
    color:white;
    text-align:center;
    padding:40px;
}
.card{
    background:white;
    color:black;
    padding:20px;
    border-radius:10px;
    width:320px;
    margin:auto;
}
button{
    padding:10px;
    border:none;
    border-radius:5px;
    background:#4facfe;
    color:white;
    cursor:pointer;
}
</style>
</head>
<body>

<h1>🎓 Student Flask API</h1>
<p>Welcome to your API dashboard</p>

<div class="card">
<h3>Available Endpoints</h3>
<p>/students</p>
<p>/student?name=John</p>
<p>POST /add_student</p>
</div>

<br>

<button onclick="loadStudents()">Load Students</button>

<script>
function loadStudents(){
fetch('/students')
.then(res=>res.json())
.then(data=>{
alert(JSON.stringify(data,null,2))
})
}
</script>

</body>
</html>
"""

# Home page
@app.route('/')
def home():
    return render_template_string(html_ui)


# Get all students
@app.route('/students')
def get_students():
    return jsonify(students)


# Search student
@app.route('/student')
def get_student():
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "Please provide ?name="}), 400

    for student in students:
        if student["name"].lower() == name.lower():
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


# Add student
@app.route('/add_student', methods=["POST"])
def add_student():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if "name" not in data or "grade" not in data or "section" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_student = {
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
