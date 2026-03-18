import streamlit as st, os
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
# from langchain.chains import LLMChain
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper
from langchain_community.tools import TavilySearchResults
# from langchain_core.runnables.history import RunnableWithMessageHistory

st.title("Blog Content Writer AI")

st.sidebar.header("Additional options to make your blog specific")

# st.sidebar.markdown("---")
wikipedia_search_bool = st.sidebar.toggle("Search Wikipedia", value=False)
chat_model = st.sidebar.selectbox("Select Model",
                             options=["meta-llama/llama-4-maverick-17b-128e-instruct",
                                        "gemma2-9b-it","llama-3.3-70b-versatile",
                                        "llama3-70b-8192"])
import os
groq_api_key = os.getenv("GROQ_API_KEY")
#os.environ["SERPAPI_API_KEY"] = "62859c2f1cc309ae78353573a674417d79953f29c27d9bcddfd41456af3a1bc3"
#os.environ["TAVILY_API_KEY"] = "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"
tavily_search = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,)

params = {
    "engine": "google",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
history = StreamlitChatMessageHistory(key="chat_messages")

keyword = st.sidebar.text_input("Please enter a keyword")
word_limit = st.sidebar.text_input("Please enter the word limit", value=500)
specific_instructions = st.sidebar.text_input("Please enter any specific instructions for the writer")

wikipedia = WikipediaAPIWrapper(top_k_results=5)

query = st.text_input('Enter Your Topic for the blog : ') 
submit_button = st.button("Submit")
st.markdown("----")
st.header("Conversation")
chat_holder = st.empty()

if submit_button and query:

    with st.spinner("Researching Internet for the information"):
        if wikipedia_search_bool:
            try:
                wikipedia_context = wikipedia.run(query)
            except Exception as e:
                wikipedia_context = "No good Wikipedia Search Result was found"
        else:
            wikipedia_context = ""
            search_results = tavily_search.invoke({"query":query})
            for result in search_results:
                wikipedia_context += f"url: {result['url']}, content: {result['content']}"

        search_content = search.run(query)
        if keyword:
            template='''You are a blog content writer who write based on the topic asked by the user.
    
                You will use this as the data source to create the blogs:
                Wikipedia Sources: {wikipedia_context},
                Internet Sources:{search},
                Information related to keyword : {keyword_content}
                
                you will follow any specific instruction if mentioned:

                Specific instruction:{specific_instructions}

                Make it {words_limit} long
                '''
            keyword_search_content = search.run(keyword)
        else:
            keyword = None
            keyword_search_content = None
            template = '''You are a blog content writer who write based on the topic asked by the user 

            You will use this as the data source to create the blogs:
            Wikipedia Sources: {wikipedia_context},
            Internet Sources:{search},

            you will follow any specific instruction if mentioned:

            Specific instruction:{specific_instructions}

            Make it {words_limit} long
            
            '''
        # rephrase_template = PromptTemplate(
        #     input_variables =["input", "word_limit", "specific_instructions"],
        #     template = """
        #     Make {input} upto {word_limit} words long and
        #     you will follow any specific instruction if mentioned:

        #     Specific instruction:{specific_instructions}
        #     """)
        blog_template = ChatPromptTemplate([
            ("system", template),
            MessagesPlaceholder("chat_messages"),
            ("user", "{topic}")
            
        ])

        blog_chain = blog_template| ChatGroq(model=chat_model)

    # rephrase_chain = rephrase_template | ChatGroq(model=chat_model)
    with st.spinner("Generating Answer"):
        config = {"configurable": {"session_id": "any"}}
        history.add_user_message(query)
        blog_answer = blog_chain.invoke(
            input = {
                    "topic":query,
                    "wikipedia_context":wikipedia_context,
                    "search":search_content,
                    "keyword":keyword,
                    "keyword_content":keyword_search_content,
                    "chat_messages":history.messages,
                    "words_limit":word_limit,
                    "specific_instructions": specific_instructions
                    }, 
                    config=config) 
        # blog = rephrase_chain.invoke(
        #     {
        #         "input":blog_answer,
                
        #     })
        history.add_ai_message(blog_answer)

with chat_holder.container(height=750):
    for message in history.messages:
        if message.type == "human":
            with st.chat_message("user"): st.markdown(message.content)
        else:
            with st.chat_message("ai"): st.markdown(message.content)
