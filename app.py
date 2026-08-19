import streamlit as st

from chatbot import get_response


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="NexaAI",
    page_icon="",
    layout="centered",
)


# ==========================================
# Header
# ==========================================

st.title("🤖 NexaAI")
st.caption("Your intelligent AI assistant powered by LangChain & Groq")


# ==========================================
# Initialize Chat History
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# Display Chat History
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":
            st.markdown(message["content"])

        else:
            response = message["content"]

            st.markdown("### Answer")
            st.write(response.answer)

            st.markdown("### Summary")
            st.write(response.summary)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Confidence",
                    f"{response.confidence:.0%}",
                )

            with col2:
                st.write("**Category**")
                st.write(response.category)

            st.write("**Keywords**")
            st.write(", ".join(response.keywords))


# ==========================================
# Clear Chat
# ==========================================

if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ==========================================
# User Input
# ==========================================

question = st.chat_input("Ask NexaAI anything...")


# ==========================================
# Process User Question
# ==========================================

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = get_response(question)

        st.markdown("### Answer")
        st.write(response.answer)

        st.markdown("### Summary")
        st.write(response.summary)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Confidence",
                f"{response.confidence:.0%}",
            )

        with col2:
            st.write("**Category**")
            st.write(response.category)

        st.write("**Keywords**")
        st.write(", ".join(response.keywords))

    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )