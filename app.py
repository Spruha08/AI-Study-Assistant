import streamlit as st
from utils import (
    extract_text_from_file,
    split_text_into_chunks,
    create_vector_store,
    answer_question,
    generate_summary,
    generate_quiz,
    generate_interactive_mcqs,
)

st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f5ef;
        color: #1f2933;
    }

    section[data-testid="stSidebar"] {
        background-color: #ece7da;
        border-right: 1px solid #d8d3c4;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #243b53;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #52616b;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .status-box, .turn-box, .answer-box {
        background-color: #fbfaf7;
        border: 1px solid #d8d3c4;
        border-radius: 8px;
        padding: 14px;
        margin: 14px 0;
    }

    .turn-box {
        background-color: #eef3f7;
    }

    .answer-box {
        background-color: #fbfaf7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    if "chats" not in st.session_state:
        st.session_state.chats = {}

    if not st.session_state.chats:
        st.session_state.chats["chat_1"] = create_chat_data()

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = "chat_1"


def create_chat_data():
    return {
        "title": "New Study Session",
        "turns": [],
        "vector_store": None,
        "document_ready": False,
        "file_names": [],
        "current_mcqs": [],
        "quiz_result": "",
    }


def get_current_chat():
    chat = st.session_state.chats[st.session_state.current_chat_id]

    if "turns" not in chat:
        chat["turns"] = []
    if "current_mcqs" not in chat:
        chat["current_mcqs"] = []
    if "quiz_result" not in chat:
        chat["quiz_result"] = ""

    return chat


def create_new_chat():
    chat_number = len(st.session_state.chats) + 1
    chat_id = f"chat_{chat_number}"
    st.session_state.chats[chat_id] = create_chat_data()
    st.session_state.current_chat_id = chat_id


def update_chat_title(user_message):
    chat = get_current_chat()

    if chat["title"] == "New Study Session":
        title = user_message.strip()[:35]

        if len(user_message.strip()) > 35:
            title += "..."

        chat["title"] = title if title else "Study Session"


def add_follow_up(answer):
    return (
        answer
        + "\n\n---\n"
        + "Would you like help with another doubt, a revision summary, or a practice quiz?"
    )


def add_turn(user_action, assistant_response, mcqs=None):
    chat = get_current_chat()
    chat["turns"].append(
        {
            "user_action": user_action,
            "assistant_response": assistant_response,
            "mcqs": mcqs or [],
            "quiz_result": "",
        }
    )


def show_previous_turns(chat):
    for turn_index, turn in enumerate(chat["turns"]):
        st.markdown("### What would you like to do next?")
        st.markdown(
            f'<div class="turn-box"><strong>You:</strong><br>{turn["user_action"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("### Response")
        st.markdown(
            f'<div class="answer-box">{turn["assistant_response"]}</div>',
            unsafe_allow_html=True,
        )

        if turn.get("mcqs"):
            show_mcq_quiz(chat, turn, turn_index)

        st.divider()


def show_mcq_quiz(chat, turn, turn_index):
    st.subheader("Interactive MCQ Quiz")

    user_answers = {}

    for index, mcq in enumerate(turn["mcqs"], start=1):
        st.markdown(f"**Q{index}. {mcq['question']}**")

        options = []
        for option_key, option_text in mcq["options"].items():
            options.append(f"{option_key}. {option_text}")

        selected_option = st.radio(
            "Choose your answer",
            options,
            key=f"{st.session_state.current_chat_id}_turn_{turn_index}_mcq_{index}",
        )

        user_answers[index] = selected_option[0]

    if not turn.get("quiz_result"):
        if st.button("Submit Quiz", key=f"submit_quiz_{turn_index}"):
            score = 0
            total = len(turn["mcqs"])
            result_lines = []

            for index, mcq in enumerate(turn["mcqs"], start=1):
                correct_answer = mcq["answer"]
                selected_answer = user_answers[index]

                if selected_answer == correct_answer:
                    score += 1
                    result_lines.append(f"Q{index}: Correct. Answer: {correct_answer}")
                else:
                    result_lines.append(
                        f"Q{index}: Wrong. Your answer: {selected_answer}, Correct answer: {correct_answer}"
                    )

            turn["quiz_result"] = (
                f"Your score is {score}/{total}.\n\n"
                + "\n".join(result_lines)
                + "\n\nWould you like to try another quiz or ask a doubt from this document?"
            )

            st.rerun()

    if turn.get("quiz_result"):
        st.success("Quiz submitted successfully.")
        st.markdown("### Quiz Result")
        st.write(turn["quiz_result"])


initialize_session_state()

with st.sidebar:
    st.markdown("## AI Study Assistant")
    st.caption("Your study sessions")

    if st.button("+ New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    st.divider()
    st.markdown("### Chat History")

    for chat_id, chat_data in st.session_state.chats.items():
        if st.button(chat_data["title"], key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

chat = get_current_chat()

st.markdown('<div class="main-title">Study Session</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload your notes, ask doubts, generate summaries, and practice questions.</div>',
    unsafe_allow_html=True,
)

if chat["document_ready"]:
    st.markdown(
        '<div class="status-box">Document ready. You can continue your study session.</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="status-box">Attach your study material to begin.</div>',
        unsafe_allow_html=True,
    )

if not chat["document_ready"]:
    uploaded_files = st.file_uploader(
        "Attach study material",
        type=["pdf", "docx", "pptx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        full_text = ""
        file_names = []

        for file in uploaded_files:
            file_names.append(file.name)
            file_text = extract_text_from_file(file)
            full_text += file_text + "\n"

        chunks = split_text_into_chunks(full_text)

        if st.button("Process Document"):
            with st.spinner("Reading and preparing your study material..."):
                collection_name = st.session_state.current_chat_id
                vector_store = create_vector_store(chunks, collection_name)

                chat["vector_store"] = vector_store
                chat["document_ready"] = True
                chat["file_names"] = file_names

                ready_message = (
                    f"Your document is ready. I created {len(chunks)} study chunks from your uploaded material.\n\n"
                    "You can ask doubts, generate revision notes, or practice with quizzes."
                )

                add_turn("Processed uploaded study material.", ready_message)

            st.success("Document processed successfully.")
            st.rerun()

if chat["file_names"]:
    with st.expander("Attached files"):
        for file_name in chat["file_names"]:
            st.write(file_name)

if chat["document_ready"]:
    st.divider()

    show_previous_turns(chat)

    st.markdown("### What would you like to do next?")

    study_mode = st.selectbox(
        "Study mode",
        ["Ask Doubt", "Revision Summary", "Practice Quiz"],
    )

    if study_mode == "Ask Doubt":
        marks = st.selectbox(
            "Answer length",
            ["2 marks", "5 marks", "10 marks"],
        )

        user_input = st.text_input("Ask a question from your uploaded document")

        if st.button("Send"):
            if not user_input.strip():
                st.warning("Please enter a question.")
            else:
                user_action = f"Ask Doubt ({marks}): {user_input}"
                update_chat_title(user_input)

                with st.spinner("Thinking..."):
                    answer = answer_question(
                        chat["vector_store"],
                        user_input,
                        marks,
                    )

                add_turn(user_action, add_follow_up(answer))
                st.rerun()

    elif study_mode == "Revision Summary":
        summary_type = st.selectbox(
            "Summary type",
            ["Key Points", "Quick Revision Notes", "Chapter Summary"],
        )

        if st.button("Generate Summary"):
            user_action = f"Generate a {summary_type.lower()} from my uploaded document."
            update_chat_title(user_action)

            with st.spinner("Preparing summary..."):
                summary = generate_summary(
                    chat["vector_store"],
                    summary_type,
                )

            add_turn(user_action, add_follow_up(summary))
            st.rerun()

    elif study_mode == "Practice Quiz":
        st.write("How many questions do you want to generate?")

        number_of_questions = st.number_input(
            "Number of questions",
            min_value=1,
            max_value=30,
            value=10,
            step=1,
        )

        quiz_type = st.selectbox(
            "Quiz type",
            ["MCQs", "Short Questions", "Viva Questions", "Mixed Quiz"],
        )

        if st.button("Generate Quiz"):
            user_action = f"Generate {number_of_questions} {quiz_type.lower()} from my uploaded document."
            update_chat_title(user_action)

            if quiz_type == "MCQs":
                with st.spinner("Creating interactive MCQs..."):
                    mcqs = generate_interactive_mcqs(
                        chat["vector_store"],
                        number_of_questions,
                    )

                if mcqs:
                    quiz_message = (
                        "I created an interactive MCQ quiz for you. "
                        "Select your answers below and submit the quiz when you are ready."
                    )
                    add_turn(user_action, quiz_message, mcqs)
                else:
                    quiz_message = (
                        "I could not create interactive MCQs from this document. "
                        "Try fewer questions or use another quiz type."
                    )
                    add_turn(user_action, quiz_message)

            else:
                with st.spinner("Creating practice questions..."):
                    quiz = generate_quiz(
                        chat["vector_store"],
                        quiz_type,
                        number_of_questions,
                    )

                add_turn(user_action, add_follow_up(quiz))

            st.rerun()
