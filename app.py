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