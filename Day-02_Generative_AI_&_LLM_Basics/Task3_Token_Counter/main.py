# pip install tiktoken

import tiktoken

def show_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")  # Tokenizer for GPT-4/4o/5
    
    tokens = enc.encode(text)

    print(f"Input Text: {text}")
    print(f"Token Count: {len(tokens)}")
    print("\nTokens:")
    for t in tokens:
        print(f"{t} --> {enc.decode([t])}")

# Example
show_tokens("Hello world")
show_tokens("RAG system")