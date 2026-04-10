import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import PyPDF2
import os
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()
st.title("AI Resume Analyzer")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
class resume(BaseModel):
    topics: List[str] = Field(description="List of topics")
    review: str = Field(description="Review of the resume")
    match: int = Field(description="Match percentage")
with st.sidebar:
    selected_option = st.selectbox("Select job description", ["Ai developer 1", "Data scientist 2", " software engineer"])
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

extracted_text = ""
if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()
prompts="""
your a Hr assistant 
your provide job description and a resume of candidate
analyze the resume and job description and provide match percentage and topics  on which candidate should be tested and review of the resume
the resume of candidate is:
{resume}
the job description is:
{job_description}

"""
jd_ai="""Job Title: AI Developer
Job Summary
We are seeking a highly skilled AI Developer to design, develop, and deploy innovative AI models and software solutions. You will be responsible for transforming data science prototypes into production-ready systems, optimizing machine learning models for performance, and integrating AI capabilities into our core products.

Key Responsibilities
Model Development: Design and train machine learning (ML) and deep learning models using frameworks like PyTorch or TensorFlow.

Systems Integration: Build APIs and microservices to integrate AI models into web or mobile applications.

Data Pipeline Engineering: Develop and maintain scalable data pipelines to clean, preprocess, and augment data for training.

Optimization: Fine-tune models for latency, memory usage, and accuracy, especially for edge or cloud deployment.

Research & Innovation: Stay current with the latest AI trends (e.g., LLMs, RAG, Stable Diffusion) and implement state-of-the-art techniques.

Required Technical Skills
Programming: Proficiency in Python (essential), C++, or Java.

AI/ML Frameworks: Extensive experience with PyTorch, TensorFlow, or Scikit-Learn.

Generative AI: Familiarity with LLM orchestration tools like LangChain, LlamaIndex, or OpenAI API.

Data Handling: Strong SQL skills and experience with Vector Databases (e.g., Pinecone, Milvus, Weaviate).

Deployment: Experience with Docker, Kubernetes, and cloud platforms like AWS, GCP, or Azure.

Preferred Qualifications
Degree in Computer Science, Data Science, or a related field.

Proven track record of deploying at least one AI-driven product to production.

Understanding of MLOps principles (versioning models, CI/CD for ML)"""
jd_data_scientist = """
When creating a Job Description for a Data Scientist, you need to differentiate it from your previous AI Developer JD. While the AI Developer focuses on building and deploying systems, the Data Scientist focuses on finding insights, testing hypotheses, and statistical validation.

Here is a demo JD, followed by a critical breakdown of why these specific sections matter.

Job Title: Data Scientist
Job Summary
We are looking for a Data Scientist to join our team and turn data into actionable insights. You will be responsible for exploring large datasets, designing statistical experiments, and building predictive models that drive business decisions. The ideal candidate is a curious problem-solver who can communicate complex mathematical findings to non-technical stakeholders.

Key Responsibilities
Data Exploration: Perform deep-dive Analysis (EDA) on structured and unstructured data to identify hidden trends and patterns.

Statistical Modeling: Design and implement statistical models and machine learning algorithms (Regression, Clustering, Time-series forecasting).

A/B Testing: Design experiments to test product changes and use hypothesis testing to validate results.

Data Storytelling: Create compelling visualizations and reports that translate data into business strategy.

Collaboration: Work closely with the AI Engineering team to transition validated models into production environments.

Required Technical Skills
Statistics: Strong foundation in probability, hypothesis testing, and statistical significance.

Programming: Mastery of Python (Pandas, NumPy, Statsmodels) or R.

Data Manipulation: Advanced SQL for extracting and joining data from complex warehouses.

Visualization: Experience with PowerBI, Tableau, or libraries like Matplotlib/Seaborn.

ML Libraries: Proficiency in Scikit-Learn and XGBoost/LightGBM.

Preferred Qualifications
Experience with Big Data tools (PySpark, Hadoop).

Knowledge of Bayesian statistics or Causal Inference.

Strong domain knowledge in [Industry, e.g., Fintech, Healthcare, or E-commerce].

"""
jd_software_engineer = """
For a Software Engineer, the focus shifts away from data insights or model training and pivots toward architecture, scalability, and code quality. This role is about building the "skeleton and muscles" that allow the AI or data models to function in the real world.

Job Title: Software Engineer
Job Summary
We are looking for a Software Engineer to design, build, and maintain robust, scalable software applications. You will be responsible for the full software development lifecycle—from conceptualizing features to deploying code and monitoring performance. You should be a problem-solver who writes clean, maintainable code and understands how to build systems that can handle thousands of concurrent users.

Key Responsibilities
System Design: Architect scalable backend services and APIs that are efficient and secure.

Feature Development: Implement end-to-end features using modern frameworks and best practices.

Code Quality: Participate in rigorous code reviews, write unit and integration tests, and maintain documentation.

Performance Optimization: Identify bottlenecks in the application and optimize for speed and resource usage.

Collaboration: Work with AI Developers and Data Scientists to integrate complex logic into user-facing products.

Required Technical Skills
Programming: Mastery of at least one core language: Python, Java, Go, or C#.

Web Frameworks: Experience with FastAPI, Django, Spring Boot, or Node.js.

Database Management: Proficiency in SQL (PostgreSQL/MySQL) and familiarity with NoSQL (MongoDB/Redis).

DevOps & Infrastructure: Experience with Docker, CI/CD pipelines, and cloud services (AWS/Azure/GCP).

Frontend (Optional but Preferred): Basic understanding of React, Vue, or Angular for full-stack collaboration.

Preferred Qualifications
Experience with microservices architecture and message brokers (Kafka/RabbitMQ).

Solid understanding of Data Structures and Algorithms.

Familiarity with Agile methodologies and Scrum.

"""
prompt_template = PromptTemplate.from_template(prompts)
if selected_option == "Ai developer 1":
    job_description = jd_ai
elif selected_option == "Data scientist 2":
    job_description = jd_data_scientist
elif selected_option == " software engineer":
    job_description = jd_software_engineer
else:
    job_description = ""

chain = prompt_template | llm.with_structured_output(resume)
result = chain.invoke({"resume": extracted_text, "job_description": job_description})
st.write("match of job description:")
st.write(result.match)
st.write("Topics you should focus on for interview:")
for i in result.topics:
    st.write(i)
st.write("Review:")
st.write(result.review)
