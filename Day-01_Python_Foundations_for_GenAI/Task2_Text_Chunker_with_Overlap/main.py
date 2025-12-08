import os

def chunk_with_overlap(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print("Document Content:")

        for line in content.split('\n'):
            line_length = len(line)
            # print(f"Processing line of length {line_length}: {line}")
            chunk_size = 10
            overlap_size = 3
            start = 0
            chunk_count = 0
            chunk_text = ""
            chunk_id = 0
            chunk_text = []
            while start < line_length:
                end = min(start + chunk_size, line_length)
                chunk = line[start:end]
                chunk_count += 1
                # chunk_text.append(chunk)
                # print(f"Chunk {chunk_count}: {chunk}")
                if end == line_length:
                    break
                start += (chunk_size - overlap_size)
                chunk_text.append({
                    'chunk_id': chunk_id,
                    'text': chunk,
                    'start_pos': start,
                    'end_pos': end,
                    'word_count': len(chunk.split())
                })
            # print(chunk_count)
            print(chunk_text)


chunk_with_overlap("./sample.txt")