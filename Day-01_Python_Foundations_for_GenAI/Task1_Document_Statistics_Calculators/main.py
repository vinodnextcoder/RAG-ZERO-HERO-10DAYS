import os

def calculate_document_statistics(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print("Document Content:")
        # print(content)
        line_count = 0
        total_word_count = 0
        total_char_count = 0
        total_sentense_splitby_dot = 0
        total_sentense_splitby_exclamation = 0
        total_sentense_splitby_question = 0
        # Total sentences (split by ., !, ?)
        for line in content.split('\n'):
            for chr in line:
                total_char_count += 1
            # print(line)
            line_count += 1
            word_count = line.split(' ')
            # print(word_count)
            total_word_count += len(word_count)
            sentense_splitby_dot = line.split('.')
            sentense_splitby_exclamation = line.split('!')
            sentense_splitby_question = line.split('?')
            total_sentense_splitby_dot += len(sentense_splitby_dot) - 1
            total_sentense_splitby_exclamation += len(sentense_splitby_exclamation) - 1
            total_sentense_splitby_question += len(sentense_splitby_question) - 1

            
            print(f"Line {line_count} has {len(word_count)} words.")
        print("\nDocument Statistics:")
        print(f"Total Lines: {line_count}")
        print(f"Total Words: {total_word_count}")
        print(f"Total Characters: {total_char_count}")
        print(f"Total Sentences (by '.'): {total_sentense_splitby_dot}")
        print(f"Total Sentences (by '!'): {total_sentense_splitby_exclamation}")
        print(f"Total Sentences (by '?'): {total_sentense_splitby_question}")
        total_sentences = (total_sentense_splitby_dot + 
                           total_sentense_splitby_exclamation + 
                           total_sentense_splitby_question)
        print(f"Total Sentences: {total_sentences}")



calculate_document_statistics("./sample.txt")