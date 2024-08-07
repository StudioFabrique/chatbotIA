from flask import Flask,  render_template, request, session, redirect, url_for
from flask_session import Session #install Flask-Session
from bot import initialisation_lien, initialisation_pdf, get_text_embedding, get_prompt, run_mistral
import numpy as np
import faiss

app = Flask(__name__)

# Configuration de Flask-Session pour utiliser le système de fichiers car session normal ne supporte pas plus que 4000bytes?
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'ksksk'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Initialiser Flask-Session
Session(app)


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/getSource', methods = ["POST"])
def source():
    sourceDic = request.get_json()
    source = sourceDic['source']  
    chunks,index = initialisation_lien(str(source))

    #index de faiss ne peut pas etre sous format json
    indexJson= {
        'd' : index.d,
        'ntotal' : index.ntotal,
        'vectors' : index.reconstruct_n(0, index.ntotal).tolist()
    }

    session['data']= {'chunks' : chunks, 'index': indexJson}
    return "Source ajoutée!"

@app.route('/upload', methods = ["POST"])
def upload():
    if 'file' not in request.files : 
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '' : 
        return redirect(url_for('home'))
    if file and fichier_autorise(file.filename):
        chunks,index = initialisation_pdf(file)
        #index de faiss ne peut pas etre sous format json
        indexJson= {
            'd' : index.d,
            'ntotal' : index.ntotal,
            'vectors' : index.reconstruct_n(0, index.ntotal).tolist()
        }

        session['data']= {'chunks' : chunks, 'index': indexJson}
        return "Source ajoutée!"
    return redirect(url_for('home'))

def fichier_autorise(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/get', methods = ["POST"])
def chat():
    message = request.get_json(['message'])
    retour = str(message)
    return get_reponse(retour)

def get_reponse(question) :
    question_embeddings = np.array([get_text_embedding(question)])

    chunks = session['data']['chunks']
    indexJson = session['data']['index']
    index = faiss.IndexFlatL2(indexJson['d'])
    index.add(np.array(indexJson['vectors']))

    #trouver les chunks similaires à la question
    D, I = index.search(question_embeddings, k=2) # distance, index
    retrieved_chunk = [chunks[i] for i in I.tolist()[0]]

    prompt = get_prompt(retrieved_chunk, question)
    return run_mistral(prompt)

if __name__ == "__main__": 
    app.run(debug=True)
