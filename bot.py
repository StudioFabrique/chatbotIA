#entrainement du model mistral pour répondre à des questions selon une source donnée 

from dotenv import load_dotenv 
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import numpy as np
import requests
import faiss 

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key)



##fonction pour transformer la source en texte ###############################
#source est un lien vers un site
def get_text(source):    
    response = requests.get(source)
    text = response.text
    return text[:2000]
    #return text[:1000] (si le texte est long pour que les tests soient plus rapide)
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





#initialiser les chunks et les embeddings du texte de la source##############
#exemple de source : 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'

def initialisation_lien(source):
    text = get_text(source)
    chunks = get_chunks(text,2048)
    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])

    #load in a vector database
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)
    return (chunks,index)
############################################################################