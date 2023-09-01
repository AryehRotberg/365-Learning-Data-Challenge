import pandas as pd
import streamlit as st

from langchain.agents import AgentType
from langchain.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI

from openai.error import RateLimitError
from langchain.schema.output_parser import OutputParserException

from langchain.agents.openai_functions_agent import base
from langchain.tools.python import tool


df = pd.read_csv('data/processed/ml_dataset.csv')

st.set_page_config(page_title='Ask ChatGPT',
                   layout='wide',
                   page_icon='🤖')

st.title('Ask ChatGPT 🤖')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

if 'messages' not in st.session_state or st.sidebar.button('Clear conversation history'):
    st.session_state['messages'] = [{'role': 'assistant', 'content': 'How can I help you?'}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt := st.chat_input(placeholder='What is the data about?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    if not openai_api_key:
        st.info('Please add your OpenAI API key to continue.')
        st.stop()
    
    try:
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613', openai_api_key=openai_api_key, streaming=True)

        pandas_df_agent = create_pandas_dataframe_agent(llm,
                                                        df,
                                                        agent_type=AgentType.OPENAI_FUNCTIONS,
                                                        handle_parsing_errors=True,
                                                        verbose=True)

        with st.chat_message('assistant'):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({'role': 'assistant', 'content': response})
            st.write(response)
    
    except RateLimitError:
        st.info('Your account is not active, please check your billing details on our website.')
        st.stop()
    
    except OutputParserException as e:
        st.error('Oops! Apparently there was a problem with json parsing. Please rewrite your prompt.')
