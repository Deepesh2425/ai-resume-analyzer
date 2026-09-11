import os
from flask import Flask, render_template, request, jsonify
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


# Skills that our analyzer can detect
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "bootstrap",
    "react",
    "node.js",
    "node",
    "express",
    "mongodb",
    "mysql",
    "sql",
    "git",
    "github",
    "flask",
    "django",
    "fastapi",
    "numpy",
    "pandas",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "rest api",
    "api"
]


# Extract text from uploaded PDF
def extract_text_from_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Detect technical skills from text
def detect_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


# Calculate resume and job description similarity
def calculate_similarity(resume_text, job_description):

    documents = [
        resume_text.lower(),
        job_description.lower()
    ]

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# Detect resume sections
def detect_sections(text):

    text = text.lower()

    sections = {
        "summary": ["summary", "profile", "objective"],
        "education": ["education", "qualification"],
        "experience": ["experience", "work experience"],
        "skills": ["skills", "technical skills"],
        "projects": ["projects", "project"],
        "certifications": ["certification", "certifications"],
        "contact": ["email", "phone", "contact"]
    }

    found_sections = []

    for section, keywords in sections.items():

        for keyword in keywords:

            if keyword in text:

                found_sections.append(section)

                break

    return sorted(set(found_sections))


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Analyze resume
@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # Check resume
        if "resume" not in request.files:

            return jsonify({
                "error": "Please upload your resume PDF."
            }), 400


        resume_file = request.files["resume"]


        if resume_file.filename == "":

            return jsonify({
                "error": "Please select a resume."
            }), 400


        if not resume_file.filename.lower().endswith(".pdf"):

            return jsonify({
                "error": "Only PDF files are supported."
            }), 400


        # Get job description
        job_description = request.form.get(
            "job_description",
            ""
        ).strip()


        if not job_description:

            return jsonify({
                "error": "Please enter the job description."
            }), 400


        # Extract resume text
        resume_text = extract_text_from_pdf(
            resume_file
        )


        if not resume_text.strip():

            return jsonify({
                "error": "Could not read text from this PDF."
            }), 400


        # Detect skills
        resume_skills = detect_skills(
            resume_text
        )

        job_skills = detect_skills(
            job_description
        )


        # Find missing skills
        missing_skills = [
            skill
            for skill in job_skills
            if skill not in resume_skills
        ]


        # Calculate score
        score = calculate_similarity(
            resume_text,
            job_description
        )


        # Detect sections
        sections = detect_sections(
            resume_text
        )


        # Suggestions
        suggestions = []


        if "projects" not in sections:

            suggestions.append(
                "Add a Projects section to your resume."
            )


        if "skills" not in sections:

            suggestions.append(
                "Add a clear Technical Skills section."
            )


        if missing_skills:

            suggestions.append(
                "Consider adding or learning: "
                + ", ".join(missing_skills)
            )


        if not suggestions:

            suggestions.append(
                "Your resume looks good. "
                "Keep it updated according to the job description."
            )


        # Final result
        result = {

            "score": score,

            "word_count": len(
                resume_text.split()
            ),

            "skills": resume_skills,

            "skill_count": len(
                resume_skills
            ),

            "job_skills": job_skills,

            "missing_skills": missing_skills,

            "sections": sections,

            "suggestions": suggestions
        }


        return jsonify(result)


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Start application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
