import os
import streamlit as st
import PyPDF2
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def read_pdf(file):
    """Reads a PDF file and extracts text."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def create_question_generation_message(pdf_content):
    """Generates a message to create questions from PDF content."""
    messages = [
        SystemMessage(
            content="""You are a question generator. I will provide you with content from a PDF file, and your task is to generate a list of thoughtful, content-related questions from the text. Generate questions that cover key points, concepts, and data from the PDF. Ensure the questions are clear and relevant to the content."""
        ),
        HumanMessage(content=pdf_content)
    ]
    return messages

def extract_questions(response_text):
    """Extracts questions from the response."""
    return response_text.split("\n") if response_text else None

def main():
    st.title("PDF Question Generator")

    st.write("Upload a PDF file to generate questions from its content.")

    pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

    if pdf_file is not None:
        pdf_content = read_pdf(pdf_file)

        if pdf_content:
            st.subheader("Extracted PDF Content:")
            st.write(pdf_content[:1000])  # Show first 1000 characters of content

            if st.button("Generate Questions"):
                messages = create_question_generation_message(pdf_content)

                with st.spinner("Generating questions..."):
                    response = llm.invoke(messages).content.strip()

                questions = extract_questions(response)

                # Filter out empty or whitespace-only questions
                questions = [q.strip() for q in questions if q.strip()]

                if questions:
                    st.subheader("Generated Questions:")
                    for question in questions:
                        st.write(question)  # Display questions without numbering
                else:
                    st.warning("No questions were generated.")
        else:
            st.warning("Failed to read or extract content from the PDF.")

if __name__ == "__main__":
    main()
