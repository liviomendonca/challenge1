# Python Challenge - Continuous Learning

Develop an interactive chatbot that not only answers questions but also learns and adapts based on user interactions. The chatbot should store relevant information on a specific topic only when the user provides accurate information (it should not accept false corrections) or when it relates to preferences, such as favoring a more formal tone.


## Files 
### `main.py`

This file contains a Groq chatbot using RAG (Retrieval-Augmented Generation) approach.
It also prints some of the agent's "chain of thought" in the terminal.


### `no_rag_chatbot.py`

This is a simpler Groq chatbot. This version doesn't rely on RAG or agents.
This was the first version, kept for comparison purposes.


### `rag.py`

This file create the vector database used in RAG approach and save it in `/chroma` folder. I included pre-built vector database files for faster initialization, but you can regenerate them with the same data (`shrek_script.md`) or create a new one for any subject of your choice.
The files in `/data` folder are split, embedded and saved in the vector database. Note that only `.md` files are accepted by default, but this is configurable in the `load_documents()` function:

```python
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents
```


## How-to

### API key

To use the chatbot, generate an API key at [Groq](https://groq.com/) and save it in a `.env` file.

Both `main.py` and `no_rag_chatbot.py` handle API key like this:

```python
dotenv.load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
```

### Commands

Use Docker to get it up and running right away!

```bash
docker build -t chatbot .
docker run -p 8501:8501 my-streamlit-app
```

Or you can run it locally:
```bash
# install python dependencies
pip install -r requirements.txt

# [optional] update/generate vector database
python rag.py

# run the app with streamlit
streamlit run main.py
```


### Tunning

RAG can be tunned by adjusting the `split_text()` function in `rag.py` file:

```python
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True,
    )

```
