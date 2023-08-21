import streamlit as st
from langchain.llms import OpenAI

css = """
<style>
    *{
        margin: 0;
        padding: 0;
        border: 0;
    }
    input.st-bd,input.st-bn,input.st-bv,input.st-ce,input.st-ck{
        border-radius: 10px;
            height: 46px;
    }
    .css-1sdqqxz.e1f1d6gn1{
        display: flex;
        height: 20px;
        align-items: center;
    }
    .css-ocqkz7.e1f1d6gn3{
        border: 1px solid black;
        text-align: center;
        justify-content: center;
        height: 50px;
        align-items: stretch;
        background: rgb(240, 242, 246);
        position: fixed;
        width: 60%;
        bottom: 100px;
        z-index: 999;
    }
    div.st-bd,div.st-be,div.st-bw{
        border: 0;
    }
    .css-j5r0tf.e1f1d6gn1{
        display: flex;
        align-items: center;
    }
    button.css-7ym5gk.ef3psqc11{
        border: 0;
        color: white;
        background: rgba(0, 0, 0,0.1);
        transition: all,1s;
    }
    button.css-7ym5gk.ef3psqc11:hover{
        border: 0;
        color: white;
        background: rgba(25,195,125,0.5);
    }
    button p{
        border: 0;
        color: white;
    }
    div.row-widget.stButton{
        text-align: end;
    padding-right: 20px;
    }
    .user-bubble {
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 8px;
        margin: 10px 0;
        width: 70%;
        text-align: right;
        float: right;
    }
    .chatbot-bubble {
        background-color: #E5E5EA;
        border-radius: 10px;
        padding: 8px;
        margin: 10px 0;
        width: 70%;
        text-align: left;
        float: left;
    }
    @media only screen and (max-width: 600px) {
    .css-ocqkz7.e1f1d6gn3{
        width: 90%;
    }
    input.st-bd,input.st-bn,input.st-bv,input.st-ce,input.st-ck{
        width: 70%;
    }
    button.css-7ym5gk.ef3psqc11{
        margin-top: 15px;
        background: rgba(25,195,125,0.5);
    }
}
</style>
"""

st.title('DialogDyno - Your AI Chatbot')

openai_api_key = st.sidebar.text_input('OpenAI API Key')


def generate_response(input_text, conversation_history):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    conversation = "\n".join(conversation_history +
                             [f'You: {input_text}', 'DialogDyno:'])
    return llm(conversation)


def main():
    st.markdown(css, unsafe_allow_html=True)

    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    col1, col2 = st.columns([4, 1])

    with col1:
        text = st.text_input("", placeholder='Enter prompt')
    with col2:
        submitted = st.button("➤")

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    elif submitted and openai_api_key.startswith('sk-') and text.strip() != '':
        response = generate_response(
            text, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append(f'You: {text}')
        st.session_state['conversation_history'].append(
            f'DialogDyno: {response}')
        # Create an empty element
        typing_message = st.empty()

        # Simulate typing...
        typing_message.text("DialogDyno is typing...")

        # Simulate response
        response = ""

        # Update the typing message with the response
        typing_message.text(response)

    if len(st.session_state['conversation_history']) > 0:
        for item in st.session_state['conversation_history']:
            if item.startswith('You:'):
                st.markdown(
                    f'<div class="user-bubble">{item[4:]}</div>', unsafe_allow_html=True)
            elif item.startswith('DialogDyno:'):
                st.markdown(
                    f'<div class="chatbot-bubble">{item[11:]}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
