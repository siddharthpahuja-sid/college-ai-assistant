from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = text_splitter.split_text(text)

    return chunks
