from pypdf import PdfReader, PdfWriter
import io
import re
import fitz # PyMuPDF

# --- Fonctions de manipulation PDF ---

def insert_pdfs_mem(main_pdf, annexe_pdfs, insertion_point):
    """
    Insère des documents PDF (annexes) dans un document PDF principal en mémoire.
    L'insertion se fait au début de la page spécifiée.
    """
    # F - Fusionner le document principal avec les annexes
    # I - Initialiser les lecteurs et écrivains PDF
    # A - Ajouter les pages dans l'ordre séquentiel
    # M - Manipuler les flux de données en mémoire
    
    main_reader = PdfReader(main_pdf)
    writer = PdfWriter()
    insertion_index = insertion_point - 1

    if not (0 <= insertion_index <= len(main_reader.pages)):
        raise ValueError(f"Le point d'insertion '{insertion_point}' est invalide pour un document de {len(main_reader.pages)} pages.")

    for i in range(insertion_index):
        writer.add_page(main_reader.pages[i])

    for annexe_file in annexe_pdfs:
        try:
            # Vérifier si c'est une image (basé sur l'extension ou le nom)
            # Streamlit UploadedFile a un attribut .name
            filename = annexe_file.name.lower()
            is_image = filename.endswith(('.jpg', '.jpeg', '.png'))

            if is_image:
                # Convertir l'image en PDF avec PyMuPDF
                img_bytes = annexe_file.read()
                # On ouvre l'image
                # On recupere l'extension sans le point
                ext = filename.split('.')[-1]
                with fitz.open(stream=img_bytes, filetype=ext) as img_doc:
                    # On convertit en PDF (bytes)
                    pdf_bytes = img_doc.convert_to_pdf()
                    # On crée un PdfReader à partir des bytes du PDF converti
                    annexe_reader = PdfReader(io.BytesIO(pdf_bytes))
            else:
                # C'est un PDF standard
                annexe_reader = PdfReader(annexe_file)

            for page in annexe_reader.pages:
                writer.add_page(page)

        except Exception as e:
            raise ValueError(f"Impossible de lire/convertir le fichier annexe '{annexe_file.name}'. Erreur: {e}")

    for i in range(insertion_index, len(main_reader.pages)):
        writer.add_page(main_reader.pages[i])

    output_pdf_stream = io.BytesIO()
    writer.write(output_pdf_stream)
    output_pdf_stream.seek(0)
    return output_pdf_stream

def delete_pages_mem(pdf_file, pages_to_delete):
    """
    Supprime des pages d'un document PDF en mémoire.
    pages_to_delete est une liste de numéros de page (commençant à 1).
    """
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
    # Convertir les numéros de page en indices (base 0)
    pages_to_delete_indices = {p - 1 for p in pages_to_delete}

    for i, page in enumerate(reader.pages):
        if i not in pages_to_delete_indices:
            writer.add_page(page)
    
    if len(writer.pages) == len(reader.pages):
        raise ValueError("Aucune des pages spécifiées n'a été trouvée dans le document.")

    output_pdf_stream = io.BytesIO()
    writer.write(output_pdf_stream)
    output_pdf_stream.seek(0)
    return output_pdf_stream

def parse_page_numbers(pages_str, max_pages):
    """
    Analyse une chaîne de numéros de page (ex: "1, 3, 5-7")
    et retourne un ensemble de numéros de page valides.
    """
    pages = set()
    # Supprimer les espaces et diviser par la virgule ou d'autres séparateurs
    parts = re.split(r'[,\s;]+', pages_str.strip())
    
    for part in parts:
        if not part:
            continue
        if '-' in part:
            try:
                start_str, end_str = part.split('-', 1)
                start = int(start_str)
                end = int(end_str)
                if start > end:
                    raise ValueError(f"Intervalle invalide : {start}-{end}")
                for i in range(start, end + 1):
                    if 1 <= i <= max_pages:
                        pages.add(i)
            except ValueError:
                raise ValueError(f"Format d'intervalle invalide : '{part}'")
        else:
            try:
                page_num = int(part)
                if 1 <= page_num <= max_pages:
                    pages.add(page_num)
            except ValueError:
                raise ValueError(f"Numéro de page invalide : '{part}'")
    return sorted(list(pages))

def convert_pdf_to_jpegs_mem(pdf_file):
    """
    Convertit les pages d'un PDF en images JPEG.
    Retourne un tuple (type_resultat, data, nom_fichier_suggéré).
    - type_resultat: 'image' (si 1 page) ou 'zip' (si > 1 page)
    - data: bytes de l'image ou du fichier zip
    - nom_fichier_suggéré: nom pour le téléchargement
    """
    import fitz # PyMuPDF
    import zipfile
    
    # Lire le flux PDF
    # Note: pdf_file est un UploadedFile de streamlit, il se comporte comme un fichier ouvert.
    # On lit les bytes.
    pdf_bytes = pdf_file.read()
    
    # Ouvrir avec fitz
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Impossible d'ouvrir le PDF avec PyMuPDF: {e}")
    
    if len(doc) == 0:
        raise ValueError("Le document PDF est vide.")
        
    # Si une seule page
    if len(doc) == 1:
        page = doc[0]
        # zoom = 2 pour meilleure qualité (dpi ~144 -> 2*72)
        # dpi=300 est mieux. get_pixmap gère dpi ou matrix.
        pix = page.get_pixmap(dpi=300) 
        img_bytes = pix.tobytes("jpg")
        return "image", img_bytes, "page_converted.jpg"
        
    # Si plusieurs pages -> ZIP
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("jpg")
                zip_file.writestr(f"page_{i+1}.jpg", img_bytes)
        
        zip_buffer.seek(0)
        return "zip", zip_buffer.getvalue(), "images_converted.zip"

def convert_pdf_to_word_mem(pdf_file):
    """
    Convertit un PDF en document Word (DOCX).
    Retourne un tuple (bytes_docx, nom_fichier_suggéré).
    """
    import tempfile
    import os
    from pdf2docx import Converter

    # Création d'un fichier temporaire pour le PDF
    # On utilise delete=False pour pouvoir fermer le fichier avant que pdf2docx ne l'ouvre (windows lock)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        # Si c'est un Streamlit UploadedFile, on peut faire getvalue()
        # Sinon read(). On assume UploadedFile ici.
        try:
            content = pdf_file.getvalue()
        except AttributeError:
             # Fallback si ce n'est pas un UploadedFile
            pdf_file.seek(0)
            content = pdf_file.read()
            
        tmp_pdf.write(content)
        tmp_pdf_path = tmp_pdf.name
    
    tmp_docx_path = tmp_pdf_path.replace(".pdf", ".docx")

    try:
        # Conversion
        cv = Converter(tmp_pdf_path)
        cv.convert(tmp_docx_path, start=0, end=None)
        cv.close()

        # Lecture du résultat
        if os.path.exists(tmp_docx_path):
            with open(tmp_docx_path, "rb") as f:
                docx_bytes = f.read()
            return docx_bytes, "document_converted.docx"
        else:
            raise Exception("Le fichier DOCX n'a pas été créé.")

    except Exception as e:
        raise ValueError(f"Erreur lors de la conversion PDF -> Word : {e}")
    finally:
        # Nettoyage
        if os.path.exists(tmp_pdf_path):
            try:
                os.remove(tmp_pdf_path)
            except:
                pass
        if os.path.exists(tmp_docx_path):
            try:
                os.remove(tmp_docx_path)
            except:
                pass