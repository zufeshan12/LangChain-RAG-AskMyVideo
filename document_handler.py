from langchain_core.documents import Document
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentHandler:
    # save page-content from returned Document object into a text file
    def save_transcript(documents:str,file_path:str):
        with open(file_path,'w',encoding='UTF-8') as txt_file:
            txt_file.write(documents + '\n')
    # load saved transcript from local to bypass speech-to-text conversion process
    def load_transcript(file_path:str):
    # load txt file and reconstruct Document object from it
        with open(file_path,'r',encoding='utf-8') as f:
            text = f.read()
        return text
    # generate transcript from youtube video url
    def generate_transcript(url:str,file_path:str):
        #["https://www.youtube.com/watch?v=hmtuvNfytjM&t=25s"]
        # directory to save audio files
        save_dir = "Downloads/Youtube"
        # convert audio into transcript, OpenAIWhisperParser expects a Blob object
        # also urls must be a list to avoid TypeError
        
        blob_loader = YoutubeAudioLoader(urls=[url],save_dir=save_dir)
        base_blob_parser = OpenAIWhisperParser()
        loader = GenericLoader(blob_loader=blob_loader,blob_parser=base_blob_parser)

        docs = loader.load() #gives a list of Document objects wth metadata and page-content
        transcript = "".join([doc.page_content for doc in docs])
        DocumentHandler.save_transcript(transcript,file_path)
        return transcript

    def create_documents(transcript:str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap = 100)
        docs = text_splitter.create_documents([transcript]) #from_text
        return docs

    def format_docs(docs:list[Document]):
        return "\n\n".join([doc.page_content for doc in docs])


