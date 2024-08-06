from dotenv import load_dotenv #install python-dotenv
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import numpy as np
import requests
import faiss  #install faiss-cpu

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key)



##fonction pour la source#####################################################
def get_text(source):    
    response = requests.get(source)
    text = response.text
    return text[:2000]
##############################################################################





##fonction pour diviser le texte en chunks#####################################
def get_chunks(text,chunk_size):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks
##############################################################################





##fonction pour créer l'embedding de chaque chunk##############################
def get_text_embedding(chunk):
    embeddings_batch_response = client.embeddings(
          model="mistral-embed",
          input=chunk
    )
    return embeddings_batch_response.data[0].embedding
##############################################################################





##fonction pour rediger le prompt#############################################
def get_prompt(retrieved_chunk,question):
    prompt = f"""
    Context information is below.
    ---------------------
    {retrieved_chunk}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer:
    """
    return prompt
##############################################################################





##fonction pour generer la reponse############################################
def run_mistral(prompt):
    model = "mistral-large-latest"
    messages = [
        ChatMessage(role="user", content=prompt)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content
#############################################################################




#liste des mots qui permettent d'arreter le chat avec le bot
#quit =["quit", "exit", "bye", "by"]


#test sur une source
#source = 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'



def initialisation(source):
    #source = 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'
    text = get_text(source)
    chunks = get_chunks(text,2048)
    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])

    #load in a vector database
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)
    return (chunks,index)

"""chunks,index= initialisation(source)
while True :
    question = input("You : ")
    if question not in quit :
        question_embeddings = np.array([get_text_embedding(question)])

        #trouver les chunks similaires à la question
        D, I = index.search(question_embeddings, k=2) # distance, index
        retrieved_chunk = [chunks[i] for i in I.tolist()[0]]
        #########################

        prompt = get_prompt(retrieved_chunk, question)
        print("CHATBOT : ",run_mistral(prompt))

    else : break"""