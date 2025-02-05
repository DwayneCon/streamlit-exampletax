import streamlit as st
import openai

# Set up the layout
st.set_page_config(page_title="ChatGPT UI", layout="centered")

# Custom CSS to hide the label and create a scrollable container
custom_css = """
<style>
.stTextInput > div:first-child > label {
    display: none;
}
.scrollable-container {
    height: 400px;
    overflow-y: scroll;
}
.small-header {
    font-size: 24px;
    margin-top: -15px;
        margin-bottom: 15px;
}
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Set up OpenAI API
openai.api_key = ["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"]

# Function to get response from OpenAI API
def get_openai_response(user_input, message_history):
    # Convert message history to the format required by the API
    api_messages = [{"role": msg.split(': ')[0].lower(), "content": msg.split(': ')[1]} for msg in message_history]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=api_messages,
        max_tokens=200,
        temperature=0.1,
        n=1,
        stream=False
    )
    return response.choices[0].message['content']
st.image("https://camo.githubusercontent.com/59ef0255241368b37cddc9a9f13b0a943a864a7ab6ff6bd57e2641c41cf8c014/68747470733a2f2f6d656469612e646973636f72646170702e6e65742f6174746163686d656e74732f3939393134343535333535363734363235302f313037343835303832323639343930383031342f7275766e65745f61695f726f626f745f6170705f69636f6e5f5f41695f7374796c655f5f6d696e696d616c6973745f36346130306636342d666131342d346234302d383532612d3932623931613433393537302e706e67",  width=150)
col1, col2 = st.columns((2, 1))
col1.title("GPT Tax Bot (v0.0.1)")
col1.markdown("<div class='small-header'>Chat with a GPT-4 powered tax advisor bot!</div>", unsafe_allow_html=True)

# Store messages
system_message = "System: You're a GPT tax advisor bot (v0.0.1). Your job is to help prepare a tax return by asking questions, then preparing a final tax document. Make sure you only respond with one question at a time."
initial_prompt = "Assistant: Hello! I'm your friendly GPT tax advisor bot (v0.0.1). You can ask for help, more details, or a summary at any time. Let's get started! Where are you located?"

# Initialize messages in session_state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [system_message, initial_prompt]

# Display all previous messages in a scrollable container
with col1.container() as scrollable_container:
    with st.markdown('<div class="scrollable-container">', unsafe_allow_html=True):
        for message in st.session_state.messages:
            st.markdown(f'<p>{message}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input field at the bottom of the window
with col1:
 
    st.write("Your message:")

    # Use a form to handle input field and Send button
    with st.form(key="message_form"):
        user_input = st.text_input("Type your message here...", value="", key="user_input")
        submit_button = st.form_submit_button("Send")



# Get response from OpenAI API and display it
if submit_button:
    user_message = f"User: {user_input}"
    st.session_state.messages.append(user_message)
    response = get_openai_response(user_input, st.session_state.messages)
    bot_message = f"Assistant: {response}"
    st.session_state.messages.append(bot_message)

    # Clear input after sending the message and rerun the app
    st.experimental_rerun()

    col1.markdown('<div style="size:9px">Built by <a href="https://twitter.com/ruv">@rUv</a> | USE AT YOUR OWN RISK</div>', unsafe_allow_html=True)

