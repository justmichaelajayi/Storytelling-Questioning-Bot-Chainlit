from langchain import PromptTemplate, LLMChain
from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI
import os
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import os
from langchain.tools import ShellTool
from langchain.tools import YouTubeSearchTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
import os
from chainlit.types import AskFileResponse
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
import os
import openai


os.environ['OPENAI_API_KEY'] = "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"
OpenAI.api_key = "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"


template = """Question: {question}
Answer: Let's think step by step."""


@cl.langchain_factory(use_async=True)
def factory():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=ChatOpenAI(
        temperature=0, streaming=True))
    return llm_chain


def get_gpt_output(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "you are an writer that is obsessed with storytelling and will never stop talking about it"},
            {"role": "user", "content": user_message}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response


@cl.on_message
async def main(message: str):
    await cl.Message(content=f"{get_gpt_output(message)['choices'][0]['message']['content']}",).send()


#! pip install youtube_search
tool = YouTubeSearchTool()

tools = [
    Tool(
        name="Search",
        func=tool.run,
        description="useful for when you need to give links to youtube videos. Remember to put https://youtube.com/ in front of every link to complete it",
    )
]


agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent.run('Whats a good vido on the topic of dialogue')