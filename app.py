from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from pathlib import Path
import os
from hausse_prix import arrondir_prix

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier sélectionné'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'})
    
    try:
        df = pd.read_excel(file, dtype=str)
        temp_path = os.path.join(UPLOAD_FOLDER, 'temp.xlsx')
        file.seek(0)
        file.save(temp_path)
        return jsonify({'columns': df.columns.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/process', methods=['POST'])
def process():
    try:
        colonne_prix = request.form['colonne_prix']
        pourcentage = float(request.form['pourcentage'])
        colonnes_a_garder = request.form.getlist('colonnes_a_garder[]')
        
        # Lire le fichier temporaire
        temp_path = os.path.join(UPLOAD_FOLDER, 'temp.xlsx')
        df = pd.read_excel(temp_path, dtype=str)
        
        # Garder uniquement les colonnes sélectionnées
        colonnes_finales = list(set(colonnes_a_garder + [colonne_prix]))  # Assure que la colonne prix est incluse
        df = df[colonnes_finales]
        
        # Convertir uniquement la colonne des prix en numérique
        df[colonne_prix] = pd.to_numeric(df[colonne_prix], errors='coerce')
        
        # Calculer les nouveaux prix
        prix_avec_marge = df[colonne_prix] * (1 + pourcentage/100)
        df['Nouveau prix'] = prix_avec_marge.apply(arrondir_prix)
        df['Différence'] = df['Nouveau prix'] - df[colonne_prix]
        
        # Sauvegarder en CSV
        output_file = 'prix_modifies.csv'
        df.to_csv(
            os.path.join(UPLOAD_FOLDER, output_file),
            index=False,
            sep=';',
            float_format='%.2f',
            encoding='utf-8-sig'
        )
        
        # Nettoyer le fichier temporaire
        os.remove(temp_path)
        
        return send_file(
            os.path.join(UPLOAD_FOLDER, output_file),
            mimetype='text/csv',
            as_attachment=True,
            download_name='prix_modifies.csv'
        )
        
    except Exception as e:
        return f'Erreur: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)