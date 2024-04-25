import math
import numpy as np

def read_doc(doc_file):
    dictionary = {}
    word_id = 0
    with open(doc_file, 'r') as f:
        for line in f:
            words = line.strip().split()
            for word in words:
                if word not in dictionary and word.isalpha():
                    word = word.lower()
                    dictionary[word] = word_id
                    word_id += 1
    return dictionary

def generate_inverted_index(doc_file, dictionary):
    inverted_index = {word: [] for word in dictionary} #Initialize each word as an empty list
    with open(doc_file, 'r') as f:
        for line_id, line in enumerate(f, start=1): 
            words = line.strip().split()
            common_words = set(words) & set(dictionary.keys())  #Find common words in a current line that are also in the dictionary
            for word in common_words:
                if line_id not in inverted_index[word]:
                    inverted_index[word].append(line_id)
    return inverted_index

def generate_document_vector(line_id, inverted_index, dictionary, doc_file):
    doc_vector = [0] * len(dictionary) #Creates a list of 0s for the length of the dictionary
    doc_words = []
    with open(doc_file, 'r') as f:
        for line_num, line in enumerate(f, start=1): #Iterate through each line in a file while keeping track of the line number
            if line_num == line_id:
                doc_words = line.strip().split()
                break
    total_words = len(doc_words)
    for word, doc_list in inverted_index.items():
        if line_id in doc_list:
            word_count = doc_words.count(word)
            doc_vector[dictionary[word]] = word_count / total_words #Term frequency (numb of times a word appears in doc / total words in doc )
    return doc_vector

def generate_query_vector(query, dictionary):
    query_vector = [0] * len(dictionary)
    for word in query.split():
        if word in dictionary:
            query_vector[dictionary[word]] = 1
    return query_vector

def calc_angle(vector_1, vector_2): 
    norm_x = np.linalg.norm(vector_1)
    norm_y = np.linalg.norm(vector_2)
    cos_theta = np.dot(vector_1, vector_2) / (norm_x * norm_y)
    theta = math.degrees(math.acos(cos_theta)) #Angle between 2 vectors in degrees, smaller the angle, the more relevant it is...
    return theta 

def doc_search(doc_file, query_file):
    dictionary = read_doc(doc_file)
    inverted_index = generate_inverted_index(doc_file, dictionary)
    print(f"Words in dictionary: {len(dictionary)}")
    
    with open(query_file, 'r') as f:
        for query in f:
            query = query.strip()
            print(f"Query: {query}")
            query_vector = generate_query_vector(query, dictionary)

            relevant_docs = [] #Doc IDs relevant to each query
            for word in query.split():
                if word in dictionary:
                    doc_list = inverted_index[word]
                    if not relevant_docs:
                        relevant_docs = doc_list
                    else:
                        relevant_docs = [doc for doc in relevant_docs if doc in doc_list]
            print(f"Relevant documents: {' '.join(map(str, relevant_docs))}")

            if relevant_docs:
                doc_angles = []
                for doc_id in relevant_docs:
                    doc_vector = generate_document_vector(doc_id, inverted_index, dictionary, doc_file)
                    angle = calc_angle(query_vector, doc_vector)
                    doc_angles.append((doc_id, angle))

                doc_angles.sort(key=lambda x: x[1]) #Organizes angles from most relevant to least relevant...
                for doc_id, angle in doc_angles:
                    print(f"{doc_id} {angle:.2f}")

# Below I've ran tests for the sets in CM1208testcases. To test difference sets, the path can be changed ...
doc_search("CM1208testcases/set3/docs.txt", "CM1208testcases/set3/queries.txt")




