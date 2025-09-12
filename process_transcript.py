from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import load_prompt
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel,RunnableLambda,RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents.base import Blob
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from document_handler import DocumentHandler
import streamlit as st
from pathlib import Path
import time

from dotenv import load_dotenv

class ProcessTranscript:
    def process_transcript(url:str,query:str):
        # main entry point
        load_dotenv()
        # RAG pipeline can be divided into 4 broad steps :----------
        # 1. Indexing
        # 2. Retrieval
        # 3. Augmentation - Prompt + Context
        # 4. Generation
        # ------------------------------------------------------------
        
        # define progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        steps = [
            "Loading audio...",
            "Converting audio to text...",
            "Generating embeddings...",
            "Configuring retriever...",
            "Wiring up LLM chain...",
            "Generating response..."
        ]

        # Step 1a - Indexing - Create a transcript from audio file
        status_text.text(steps[0])
        file_path = "transcript_"+str(url[-4:])+".txt"
        if not Path(file_path).is_file():
            transcript = DocumentHandler.generate_transcript(url=url,file_path=file_path)
        else:
            # load saved transcript file
            transcript = DocumentHandler.load_transcript(file_path)
        progress_bar.progress(16)

        # Step 1b - Indexing - text splitting into chunks with appropriate overlap
        status_text.text(steps[1])
        docs = DocumentHandler.create_documents(transcript=transcript)
        progress_bar.progress(32)

        # Step 1c - Indexing -generate embeddings using OpenAI's embedding model
        status_text.text(steps[2])
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # Step 1d - Indexing - store the generated embeddings into a local vector store like FAISS or Chroma
        vector_store = FAISS.from_documents(documents=docs,embedding=embeddings)
        progress_bar.progress(48)

        # Step 2 - Retrieval - create a multi-query retriever to answer ambiguous questions
        status_text.text(steps[3])
        retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k":4})
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        # multi-query retriever automates the process of prompt tuning by using an LLM to
        #  generate multiple queries from different perspectives for a given user input query
        mqr = MultiQueryRetriever.from_llm(retriever=retriever,llm=llm)
        progress_bar.progress(64)

        # Step 3 - Augmentation - create prompt and invoke a parallel chain
        status_text.text(steps[4])
        prompt = load_prompt("PromptTemplate.json")

        # define parallel chain to retrieve relevant docs as context from the retriever
        parallel_chain = RunnableParallel({'question':RunnablePassthrough(),
                                        'context': mqr | RunnableLambda(DocumentHandler.format_docs)})
        progress_bar.progress(80)

        # Step 4 - Generation - define LLM to process the overall query and generate response
        model = ChatOpenAI(name="gpt-4o")
        parser = StrOutputParser()

        # main chain
        status_text.text(steps[5])
        chain = parallel_chain | prompt | model | parser
        result = chain.invoke(query)
        progress_bar.progress(100)

        # remove progress bar and text from screen once response has been generated
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
            
        return result









