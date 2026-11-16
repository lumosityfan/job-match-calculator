# Job Match Calculator

Upload your resume, paste in a job description, and get back a **match score from 0 to 100**, with a one-line verdict, your strengths for the role, your gaps, and concrete suggestions to improve your fit.

## Demo

> 🚧 **A screenshot of the results card is coming soon.**

## Features

- Accepts **PDF**, **DOCX** and plain-text resumes. Legacy `.doc` files are rejected with a clear error message.
- Sends the resume and job description to an OpenAI model and requests **structured JSON** (`score`, `summary`, `strengths`, `gaps`, `suggestions`), which is rendered as a result card.
- Handles empty files, unreadable resumes and API errors with friendly messages instead of crashing.
- Responsive Bootstrap UI with a loading state.

## Tech stack

Python · Flask · OpenAI API (`gpt-4o-mini`) · pypdf · docx2txt · vanilla JavaScript · Bootstrap

## Getting started

**Prerequisites:** Python 3.10+ and an [OpenAI API key](https://platform.openai.com/api-keys).

```bash
git clone https://github.com/lumosityfan/job-match-calculator.git
cd job-match-calculator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

echo "OPENAI_API_KEY=your-key-here" > .env
python app.py
```

Open <http://localhost:5000>, upload a resume, paste a job description and click submit.

## How it works

1. `static/app.js` posts the resume file and job description as form data to `/`.
2. `app.py` extracts the resume text (`pypdf` for PDF, `docx2txt` for DOCX).
3. A prompt asks the model to act as a career advisor and reply **only** with JSON in a fixed shape (`response_format={"type": "json_object"}`).
4. The JSON is returned to the browser and rendered as a result card.

## Also available as a serverless API

The same idea runs in production as an AWS Lambda on my [resume site](https://www.jeffxieresumewebsite.com). It adds job-posting URL support (including Ashby job boards), blocks requests to private or internal addresses, and applies per-IP rate limiting. The infrastructure is in [cloud-resume-challenge-backend](https://github.com/lumosityfan/cloud-resume-challenge-backend).

## Roadmap

- [ ] Add a `requirements.txt`
- [ ] Add tests for text extraction and response handling
- [ ] Support job-posting URLs in this standalone version
- [ ] Add a `LICENSE`
