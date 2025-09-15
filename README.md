# AskMyVideo 🎥🔎

AskMyVideo is an interactive Q&A application built with the **LangChain framework**.  
It allows users to enter a YouTube video URL, extracts its audio, transcribes it into text, and enables intelligent question-answering over the transcript using advanced retrieval and LLM-based reasoning.

---

## 🚀 Features

### 🎧 Audio-to-Text Conversion
- **YoutubeAudioLoader** extracts audio directly from a given YouTube URL.  
- **OpenAI Whisper model** converts the audio into accurate transcripts, handling noise, accents, and multiple languages effectively.

---

### ✂️ Transcript Chunking with Recursive Character Text Splitting
- Long transcripts are split into **smaller overlapping chunks** using LangChain’s `RecursiveCharacterTextSplitter`.  
- This ensures that chunks respect natural language boundaries (e.g., sentences or paragraphs) rather than cutting off mid-thought.  
- ✅ **Advantage**: Preserves semantic meaning in each chunk, making retrieval more accurate when answering context-specific queries.

---

### 🔍 Embeddings with OpenAI Models
- Each chunk is embedded using the **OpenAI Embeddings model** (`text-embedding-3-small`).  
- The embeddings capture semantic meaning, enabling the system to “understand” similarity between chunks and user queries.

---

### 🗄️ Vector Store with FAISS
- The embeddings are stored in **FAISS** (Facebook AI Similarity Search), a highly efficient vector database.  
- ✅ **Advantage**:  
  - Optimized for similarity search at scale.  
  - Extremely fast nearest-neighbor lookups.  
  - Robust handling of large datasets compared to in-memory approaches.  

---

### 🧠 Hybrid Retrieval with Multi-Query Retriever
- Retrieval is not limited to simple similarity search. Instead, a **Multi-Query Retriever** powered by `gpt-3.5-turbo` is used.  
- The retriever reformulates the user’s query into multiple semantically equivalent queries.  
- These queries are run against the FAISS store, pulling in a richer and more diverse set of relevant documents.  
- ✅ **Advantage**: Overcomes limitations of single-query retrieval (which may miss contextually relevant chunks). Increases recall without sacrificing precision.

---

### 🔗 Parallel Chain for Reasoning
- LangChain’s **parallel chain** is used to manage different logic branches in the workflow.  
- Ensures the augmented prompt is enriched with the most relevant contextual information before being sent to the LLM.

---

### 💬 Final Response Generation
- The **OpenAI Chat Model** (`gpt-4o`) receives the augmented prompt and produces a final, coherent, and contextually accurate answer.  
- Combines transcript-based evidence with natural language generation to deliver high-quality responses.


###  Sleak UI with Streamlit
- Interactive UI with custom buttons and progress bar to walk you through each step behind the process.

---

## ⚙️ Tech Stack
- [LangChain](https://www.langchain.com/)  
- [OpenAI Whisper](https://github.com/openai/whisper)  
- [OpenAI GPT-3.5](https://platform.openai.com/docs/models/gpt-3-5)  
- [FAISS](https://faiss.ai/) for vector storage and retrieval  
- [YoutubeAudioLoader](https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.youtube.YoutubeAudioLoader.html)  
- [Streamlit]
---

## 🖥️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/LangChain-RAG-AskMyVideo.git
cd LangChain-RAG-AskMyVideo

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. **Install dependencies**
```bash
pip install -r requirements.txt

4. **Set environment variables**
```bash
OPENAI_API_KEY=your_openai_api_key

5. **Run the app**
```bash
streamlit run app.py


