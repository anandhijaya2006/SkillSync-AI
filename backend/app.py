from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)

CORS(app)


# =========================
# HOME
# =========================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SkillSync AI Backend is running!"
    })


# =========================
# LOGIN API
# =========================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    # Demo login
    if email == "test@gmail.com" and password == "123456":

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "name": "Test User",
                "email": email
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    }), 401


# =========================
# RESUME ANALYSIS API
# =========================

@app.route("/api/resume/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "message": "No resume uploaded"
        }), 400

    resume = request.files["resume"]

    if resume.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a resume"
        }), 400

    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Please upload a PDF resume"
        }), 400

    try:

        # Read PDF
        reader = PdfReader(resume)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + " "

        resume_text = resume_text.lower()


        # Skills
        skill_list = [
            "python",
            "java",
            "javascript",
            "react",
            "html",
            "css",
            "sql",
            "node.js",
            "machine learning",
            "data science",
            "c++",
            "git",
            "docker",
            "aws"
        ]


        # Detect skills
        detected_skills = []

        for skill in skill_list:

            if skill.lower() in resume_text:
                detected_skills.append(skill)


        # Score
        total_skills = len(skill_list)
        found_skills = len(detected_skills)

        if total_skills > 0:
            score = int(
                (found_skills / total_skills) * 100
            )
        else:
            score = 0


        score = max(0, min(score, 100))


        # Skill gaps
        skill_gaps = total_skills - found_skills


        return jsonify({
            "success": True,
            "score": score,
            "skills": detected_skills,
            "skillGaps": skill_gaps,
            "message": "Resume analyzed successfully"
        })


    except Exception as error:

        print("Resume Error:", error)

        return jsonify({
            "success": False,
            "message": "Unable to read the resume PDF"
        }), 500


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )