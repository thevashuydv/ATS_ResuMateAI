from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def get_gemini_response(input_prompt, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    try:
        if uploaded_file:
            images = pdf2image.convert_from_bytes(
                uploaded_file.read(),
                poppler_path=None  # Remove the Windows-specific path for cloud deployment
            )
            first_page = images[0]
            return first_page
        else:
            raise FileNotFoundError("No file uploaded")
    except Exception as e:
        st.error(f"Error processing PDF: Please make sure you've uploaded a valid PDF file")
        raise e



st.set_page_config(page_title="ATS expert")
st.header("ATS System")
input_text = st.text_area("Job Description", key = "input")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully!!")

submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage Match")
submit2 = st.button("Suggest Better Keywords")  # New button

input_prompt1 = """
You are an experienced HR professional with technical expertise in one or more of the following domains: Data Science, Full Stack Development, Big Data Engineering, DevOps, or Data Analysis.

Your task is to carefully review the provided resume in relation to the given job description for one of the above-mentioned roles.

Please provide a professional evaluation that includes:
1. **Overall Fit** – An assessment of how well the candidate’s profile aligns with the job requirements.
2. **Strengths** – Key qualifications, skills, or experiences that support the candidate’s suitability for the role.
3. **Weaknesses / Gaps** – Areas where the candidate falls short or may need improvement based on the job description.

Ensure your feedback is concise, insightful, and framed from a recruitment perspective.
"""

input_prompt2 = """
You are an ATS optimization expert. Your task is to analyze the resume and suggest better keyword alternatives to improve the ATS score.

Please analyze the resume and provide a list of word replacements in the following format:
1. Current Word -> Recommended Word (Reason for change)

For example:
- "Managed" -> "Led" (More impactful leadership term)
- "Used" -> "Implemented" (More professional and technical)

Focus on:
- Technical skills and tools
- Action verbs
- Industry-specific terminology
- Job titles and roles

Provide only the most impactful 5-7 word replacements that would significantly improve the ATS score.
"""

input_prompt3 = """
You are an expert ATS (Applicant Tracking System) evaluator with in-depth knowledge in at least one of the following domains: Data Science, Full Stack Development, Big Data Engineering, DevOps, or Data Analysis, as well as a strong understanding of how ATS systems function.

Your task is to analyze the given resume against the provided job description and generate a compatibility score out of 100.

Please structure your response in the following format:
1. **Score (out of 100)** – Based on how well the resume matches the job description.
2. **Missing Keywords/Skills** – List any important keywords, skills, or qualifications from the job description that are missing in the resume.
3. **Final Thoughts** – Provide a brief analysis or recommendation based on your evaluation.

Ensure the assessment is concise, accurate, and insightful.
"""




if submit1:
    if uploaded_file is not None:
        pdf_image = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_image, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload first")

elif submit2:  # New condition
    if uploaded_file is not None:
        pdf_image = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_image, input_text)
        st.subheader("Suggested Keyword Improvements")
        st.write(response)
    else:
        st.write("Please upload first")

elif submit3:
    if uploaded_file is not None:
        pdf_image = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_image, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload first")

        
