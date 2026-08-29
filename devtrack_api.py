from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. JSON Dataset containing 10 records relevant to the DevTrack domain
projects = [
    {"id": 1, "title": "Volunteer Management System", "tech": ".NET / C#", "status": "In Progress"},
    {"id": 2, "title": "Synthetic Voice Detection", "tech": "Python", "status": "Training"},
    {"id": 3, "title": "Student Engagement Analytics", "tech": "Computer Vision", "status": "Planning"},
    {"id": 4, "title": "GPA Race Mobile Game", "tech": "Kotlin", "status": "Completed"},
    {"id": 5, "title": "Fresh Basket Grocers Ledger", "tech": "Python", "status": "Completed"},
    {"id": 6, "title": "Pet Adoption Center", "tech": "Java", "status": "Completed"},
    {"id": 7, "title": "Mini Mood Tracker", "tech": "C# Windows Forms", "status": "Completed"},
    {"id": 8, "title": "Network Packet Tracer Simulation", "tech": "Cisco", "status": "Completed"},
    {"id": 9, "title": "Student Exchange App", "tech": "Android / XML", "status": "In Progress"},
    {"id": 10, "title": "Bengaluru Cares Web Portal", "tech": "HTML/CSS/MongoDB", "status": "Planning"}
]

# GET: Retrieve all records
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify({"data": projects, "status": "success"})

# GET: Retrieve a single record by ID
@app.route('/api/projects/<int:proj_id>', methods=['GET'])
def get_project(proj_id):
    for proj in projects:
        if proj['id'] == proj_id:
            return jsonify({"data": proj, "status": "success"})
    return jsonify({"error": f"Project with ID {proj_id} not found"}), 404

# POST: Add a new record
@app.route('/api/projects', methods=['POST'])
def add_project():
    new_project = request.get_json(silent=True)

    # Basic request validation
    if not new_project or not isinstance(new_project, dict):
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    required_fields = ['title', 'tech', 'status']
    missing = [f for f in required_fields if not new_project.get(f)]
    if missing:
        return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400

    new_project['id'] = len(projects) + 1
    projects.append(new_project)
    return jsonify({"message": "Record added successfully", "data": new_project}), 201

# PUT: Update an existing record
@app.route('/api/projects/<int:proj_id>', methods=['PUT'])
def update_project(proj_id):
    update_data = request.get_json(silent=True)

    if not update_data or not isinstance(update_data, dict):
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    for proj in projects:
        if proj['id'] == proj_id:
            proj.update(update_data)
            return jsonify({"message": f"Record {proj_id} updated", "data": proj})
    return jsonify({"error": f"Project with ID {proj_id} not found"}), 404

# DELETE: Remove a record
@app.route('/api/projects/<int:proj_id>', methods=['DELETE'])
def delete_project(proj_id):
    global projects
    if not any(p['id'] == proj_id for p in projects):
        return jsonify({"error": f"Project with ID {proj_id} not found"}), 404
    projects = [p for p in projects if p['id'] != proj_id]
    return jsonify({"message": f"Record {proj_id} deleted successfully"})

if __name__ == '__main__':
    # Runs the server locally on port 5000
    app.run(debug=True, port=5000)