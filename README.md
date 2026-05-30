# AI Study Assistant

AI Study Assistant is an AI-powered study tool that helps students learn from their own study materials. Users can upload PDF, DOCX, or PPTX files, ask questions from the uploaded content, generate summaries, and practice quizzes.

The project uses Retrieval-Augmented Generation (RAG) to retrieve relevant content from uploaded documents and generate answers using Groq's Llama model.

## Features

- Upload PDF, DOCX, and PPTX study materials
- Ask questions from uploaded documents
- Generate 2 marks, 5 marks, and 10 marks answers
- Generate key points, quick revision notes, and chapter summaries
- Create MCQs, short questions, viva questions, and mixed quizzes
- Practice interactive MCQs with score calculation
- ChatGPT-style study session interface
- Session-based chat history
- Lightweight embedding approach using scikit-learn HashingVectorizer

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Streamlit | Web application interface |
| Groq API | LLM response generation |
| Llama 3.3 | Answer generation model |
| ChromaDB | Vector database |
| scikit-learn | Lightweight text vectorization |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| python-pptx | PPTX text extraction |
| python-dotenv | Environment variable management |

## RAG Workflow

```text
Upload Document
        |
        v
Extract Text
        |
        v
Split Text into Chunks
        |
        v
Store Chunks in ChromaDB
        |
        v
Retrieve Relevant Context
        |
        v
Send Context to Groq Llama
        |
        v
Generate Answer / Summary / Quiz
Project Structure
AI-Study-Assistant/
│
├── app.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── docs/
    └── AI_Study_Assistant_Screenshots.pdf
Installation
1. Clone the repository
git clone https://github.com/your-username/AI-Study-Assistant.git
2. Go to the project folder
cd AI-Study-Assistant
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
For Windows:

venv\Scripts\activate
For macOS/Linux:

source venv/bin/activate
5. Install dependencies
pip install -r requirements.txt
Environment Setup
Create a .env file in the root folder and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here
Do not upload the .env file to GitHub.

Run the Application
streamlit run app.py
After running the command, open the local URL shown in the terminal.

Screenshots
Project screenshots are available in:

docs/AI_Study_Assistant_Screenshots.pdf
Main Functionalities
Ask Doubts
Users can ask questions from uploaded documents and choose the answer length:

2 marks
5 marks
10 marks
Revision Summary
Users can generate:

Key Points
Quick Revision Notes
Chapter Summary
Practice Quiz
Users can generate:

MCQs
Short Questions
Viva Questions
Mixed Quiz
MCQs are interactive and show the final score after submission.

Supported File Types
PDF
DOCX
PPTX
Security Notes
The following files and folders should not be uploaded to GitHub:

.env
venv/
chroma_db/
__pycache__/
uploads/
These are already included in .gitignore.
```

## Future Improvements

- Persistent chat history across app restarts
- User authentication
- Export summaries and quizzes as PDF
- Support for more file formats
- Better quiz analytics
- Improved document management

## Author

**Spruha Umarani**
