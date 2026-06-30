from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from pypdf import PdfReader
import docx2txt
import io

load_dotenv(override=True)

app = Flask(__name__)
client = OpenAI()

def extract_text(uploaded_file):
    filename = uploaded_file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    
    elif filename.endswith(".docx"):
        # docx2txt needs a file path or file-like object that supports seek
        file_bytes = io.BytesIO(uploaded_file.read())
        return docx2txt.process(file_bytes)
    
    elif filename.endswith(".doc"):
        # .doc (legacy binary format) isn't supported by docx2txt; flag it
        return None
    
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

@app.route("/", methods=["GET", "POST"])
def process_documents():
    if request.method == "POST":
        job_description = request.form.get("jobDescription")
        uploaded_file = request.files.get("resume")

        resume_text = extract_text(uploaded_file)

        if resume_text is None:
            return jsonify({"error": "Legacy .doc files aren't supported - please uploade .pdf or .docs"}), 400
        
        if not resume_text.strip():
            return jsonify({"error": "Couldn't extract any text from the resume"}), 400
        
        prompt = f"""You are a career advisor. Compare the following resume against the job description and provide:

Respond ONLY with valid JSON (no markdown fences, no preamble) in exactly this shape:
{{
  "score": <integer 0-100>,
  "summary": "<one sentence overall verdict>",
  "strengths": ["<strength 1>", "<strength 2>", "..."],
  "gaps": ["<gap 1>", "<gap 2>", "..."],
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "..."]
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            result_json = json.loads(response.choices[0].message.content)
            return jsonify(result_json)
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)