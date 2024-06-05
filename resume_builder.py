from flask import Flask, request, render_template, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_resume(data):
    pdf = PDF()
    pdf.add_page()

    # Personal Details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, data['name'], 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Email: {data['email']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Phone: {data['phone']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Address: {data['address']}", 0, 1, 'L')

    pdf.ln(10)

    # Education
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Education', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, data['degree'], 0, 1, 'L')
    pdf.cell(0, 10, f"{data['university']}, {data['education_years']}", 0, 1, 'L')

    pdf.ln(10)

    # Experience
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Experience', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, data['job_title'], 0, 1, 'L')
    pdf.cell(0, 10, f"{data['company']}, {data['job_years']}", 0, 1, 'L')
    pdf.multi_cell(0, 10, data['job_description'])

    pdf.ln(10)

    # Skills
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Skills', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, data['skills'])

    pdf.ln(10)

    # Additional Information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Additional Information', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f"Certifications: {data['certifications']}")
    pdf.multi_cell(0, 10, f"Languages: {data['languages']}")
    pdf.multi_cell(0, 10, f"Hobbies: {data['hobbies']}")

    pdf.ln(10)

    # Save the PDF
    resume_path = 'resume.pdf'
    pdf.output(resume_path)
    return resume_path

@app.route('/')
def form():
    return render_template('resume_builder.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'address': request.form['address'],
        'degree': request.form['degree'],
        'university': request.form['university'],
        'education_years': request.form['education_years'],
        'job_title': request.form['job_title'],
        'company': request.form['company'],
        'job_years': request.form['job_years'],
        'job_description': request.form['job_description'],
        'skills': request.form['skills'],
        'certifications': request.form.get('certifications', ''),
        'languages': request.form.get('languages', ''),
        'hobbies': request.form.get('hobbies', '')
    }

    resume_path = create_resume(data)
    return send_file(resume_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
