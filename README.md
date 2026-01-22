# Ed_scan 📄✂️🖼️

**Ed_scan** est une application web moderne et élégante conçue pour simplifier la manipulation de vos documents PDF. Développée avec Python et Streamlit, elle offre une interface intuitive pour fusionner, nettoyer et convertir vos fichiers en toute simplicité.

## ✨ Fonctionnalités

### 1. ⚡ Fusionner (Document & Images)
Assemblez vos documents facilement.
*   **Document Principal** : Chargez votre PDF de base.
*   **Ajouts Flexibles** : Insérez d'autres fichiers PDF **ou des images** (JPG, PNG) directement dans le document. Les images sont automatiquement converties en pages PDF.
*   **Positionnement Précis** : Choisissez exactement à quelle page insérer les nouveaux éléments.

### 2. 🗑️ Supprimer des Pages
Nettoyez vos documents en retirant les pages inutiles.
*   Sélectionnez votre fichier PDF.
*   Indiquez simplement les numéros de pages à supprimer (ex: `1`, `3-5`, `10`).

### 3. 🖼️ PDF vers JPEG
Transformez vos documents en images.
*   Convertit chaque page de votre PDF en image haute résolution.
*   Téléchargement intelligent : Image unique (si 1 page) ou archive ZIP (si plusieurs pages).

## 🛠️ Installation et Lancement

1. **Cloner le projet**
   ```bash
   git clone https://github.com/tkf-data17/ed_scan.git
   cd ed_scan
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   streamlit run main.py
   ```

## 📦 Technologies Utilisées

*   **[Streamlit](https://streamlit.io/)** : Pour l'interface utilisateur interactive.
*   **[pypdf](https://pypi.org/project/pypdf/)** : Pour la manipulation des structures PDF (fusion, suppression).
*   **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)** : Pour le rendu haute qualité et la conversion d'images.

## 🎨 Design

L'application utilise un style CSS personnalisé pour offrir une expérience utilisateur fluide et agréable, avec une mise en page centrée et des composants visuels clairs.

---
*Fait avec ❤️ pour simplifier votre gestion documentaire.*
