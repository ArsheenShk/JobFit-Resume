from geminiAPI import*
from OCR import*


def extract_pdf_text(pdf_docs):
    """Extract text from uploaded PDFs."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to get interview tips using the Gemini API
def get_interview_tips_with_gemini(job_title, job_description, resume_text):
    prompt = f"""
    Based on the job title '{job_title}' and the following job description:
    {job_description}
    
    and the provided resume content:
    {resume_text}
    
    1. Generate a list of common interview questions typically asked for this role, including both behavioral and technical questions.
    3. Include a few technical questions relevant to the job requirements mentioned in the description, along with brief answers or explanations.
    4.Offer additional interview preparation tips for the candidate, such as key topics to study, important skills to highlight, and strategies to handle tricky questions.
    5. Also provide few online websites to study and practice for the same.
    """
    # Call the angel function from geminiAPI to get the generated response
    interview_tips = angel(prompt)
    return interview_tips

def main():
    """Main Streamlit app function."""
    
    st.set_page_config(page_title="JobFit Resume")
    st.header("Job Fit Resume Enhancement")

    # Upload PDF file
    pdf_docs = st.file_uploader("Upload your Resume PDF File", type=["pdf"], accept_multiple_files=False)

    # Job title and description input
    job_title = st.text_input("Enter your Job Title")
    job_description = st.text_area("Enter the Job Description")

    # Process button for resume enhancement
    if pdf_docs and st.button("Enhance Resume"):
        # Extract text from the uploaded resume
        raw_text = extract_pdf_text([pdf_docs])
        # Ensure both fields are filled before generating suggestions
        if job_title and job_description:
            query = f"Analyze the provided resume {raw_text} and compare it with the given job title: {job_title} and job description: {job_description}. Identify and list the shortcomings in the current resume content, particularly in relation to the job description. Then, suggest specific keywords that are relevant to the job title and job description, as well as improvements to enhance the resume's effectiveness without changing their existing experiences and skills. Finally, rewrite the resume content by incorporating the recommended keywords and enhancements to optimize it for the desired role."
            with st.spinner("Generating suggestions..."):
                result = angel(query)
                st.success("Resume processed successfully!")
            st.subheader("Resume Enhancement Suggestions")
            st.write(result)
        else:
            st.warning("Please provide both Job Title and Job Description for accurate suggestions.")
    
    # Button to trigger interview preparation tips generation
    if pdf_docs and st.button("Get Interview Preparation Tips"):
        # Ensure both fields are filled
        if job_title and job_description:
            # Extract text from the uploaded resume
            resume_text = extract_pdf_text([pdf_docs])
            # Generate interview tips using Gemini API
            tips = get_interview_tips_with_gemini(job_title, job_description, resume_text)
            # Display the generated tips
            st.subheader("Interview Preparation Tips")
            st.write(tips)
        else:
            st.warning("Please provide both Job Title and Job Description.")
            
if __name__ == "__main__":
    main()


