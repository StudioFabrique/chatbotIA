from flask import Flask,  render_template, request, session
from flask_session import Session 
from bot import initialisation_lien, get_text_embedding, get_prompt, run_mistral
import numpy as np
import faiss

app = Flask(__name__)

# Configuration de Flask-Session pour utiliser le système de fichiers car session normal n'a pas beaucoup de mémoire?
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'ksksk'

# Initialiser Flask-Session
Session(app)

#page initiale
@app.route('/')
def home():
    return render_template('base.html')




#fait l'analyse de la source
@app.route('/getSource', methods = ["POST"])
def source():
    sourceDic = request.get_json() #reçoit la source du frontend
    source = sourceDic['source']  
    chunks,index = initialisation_lien(str(source))

    #index de faiss ne peut pas se transformer direct en format json
    indexJson= {
        'd' : index.d,
        'ntotal' : index.ntotal,
        'vectors' : index.reconstruct_n(0, index.ntotal).tolist()
    }

    #session pour sauvegarder l'index et les chunks pour les utiliser pour le chat
    session['data']= {'chunks' : chunks, 'index': indexJson}
    return "Source ajoutée!"




#reponsable du chat
@app.route('/get', methods = ["POST"])
def chat():
    message = request.get_json(['message']) #reçoit le message de l'utilisateur du frontend
    retour = str(message)
    return get_reponse(retour)

#cherche ce qui est similaire à la question dans le texte et renvoie la réponse
def get_reponse(question) :
    question_embeddings = np.array([get_text_embedding(question)])

    #recuperer chunks et index de l'etape de l'analyse de la source
    chunks = session['data']['chunks'] 
    indexJson = session['data']['index']
    index = faiss.IndexFlatL2(indexJson['d'])
    index.add(np.array(indexJson['vectors']))

    #trouver les chunks similaires à la question
    D, I = index.search(question_embeddings, k=2) # distance, index
    retrieved_chunk = [chunks[i] for i in I.tolist()[0]] #les chunks du texte similaire à la question

    #generer la reponse
    prompt = get_prompt(retrieved_chunk, question)
    return run_mistral(prompt)




if __name__ == "__main__": 
    app.run(debug=True)
