from pypdf import PdfReader, PdfWriter
import io
import re

# --- Fonctions de manipulation PDF ---

def insert_pdfs_mem(main_pdf, annexe_pdfs, insertion_point):
    """
    Insère des documents PDF (annexes) dans un document PDF principal en mémoire.
    L'insertion se fait au début de la page spécifiée.
    """
    main_reader = PdfReader(main_pdf)
    writer = PdfWriter()
    insertion_index = insertion_point - 1

    if not (0 <= insertion_index <= len(main_reader.pages)):
        raise ValueError(f"Le point d'insertion '{insertion_point}' est invalide pour un document de {len(main_reader.pages)} pages.")

    for i in range(insertion_index):
        writer.add_page(main_reader.pages[i])

    for annexe_pdf in annexe_pdfs:
        try:
            annexe_reader = PdfReader(annexe_pdf)
            for page in annexe_reader.pages:
                writer.add_page(page)
        except Exception as e:
            raise ValueError(f"Impossible de lire l'un des fichiers annexes. Erreur: {e}")

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