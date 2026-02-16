import streamlit as st
from pypdf import PdfReader
from utils import insert_pdfs_mem, delete_pages_mem, parse_page_numbers, convert_pdf_to_jpegs_mem, convert_pdf_to_word_mem, extract_pages_to_pdf_mem, extract_pages_to_images_mem
from style import load_css

# --- Fonctions d'affichage des onglets ---

def fusion_tab():
    st.markdown("<h2 style='text-align: center; color: #333;'>Fusionner des Documents PDF</h2>", unsafe_allow_html=True)
    
    # Structure de grille pour centrer le contenu (1/3 largeur)
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # --- Card 1: Document Principal ---
        st.markdown('<div class="card-label">⬆️ Document Principal</div>', unsafe_allow_html=True)
        main_doc = st.file_uploader("Choisissez le fichier principal", type="pdf", key="inserer_main", label_visibility="collapsed")
        if main_doc:
            try:
                 main_doc.seek(0)
                 reader = PdfReader(main_doc)
                 st.caption(f"✅ {len(reader.pages)} pages détectées")
            except Exception as e:
                 st.error(f"Erreur lecture PDF: {e}")

        st.markdown("---") # Séparateur visuel léger

        # --- Card 2: Document Annexe ---
        st.markdown('<div class="card-label">📄 Document à Ajouter</div>', unsafe_allow_html=True)
        annexe_docs = st.file_uploader("Choisissez le(s) fichier(s) à ajouter", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True, key="inserer_annexes", label_visibility="collapsed")
        
        st.markdown("---") 

        # --- Card 3: Position ---
        st.markdown('<div class="card-label">Numéro de la page où insérer</div>', unsafe_allow_html=True)
        # Calcul max page
        max_page = 1
        if main_doc:
            try:
                max_page = len(PdfReader(main_doc).pages) + 1
            except:
                pass
                
        insertion_page = st.number_input("Position", min_value=1, max_value=max_page if main_doc else 1000, value=1, label_visibility="collapsed")
        st.caption("Le document à ajouter sera inséré à cette position")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Bouton d'action ---
        if st.button("Fusionner les Documents", key="btn_fusion"):
            if not main_doc or not annexe_docs:
                st.warning("Veuillez sélectionner un document principal et au moins une annexe.")
            else:
                with st.spinner("Fusion en cours..."):
                    try:
                        final_pdf = insert_pdfs_mem(main_doc, annexe_docs, insertion_page)
                        st.success("Documents fusionnés avec succès !")
                        st.download_button(
                            label="📥 Télécharger le résultat",
                            data=final_pdf.getvalue(),
                            file_name="fusion_edscan.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Une erreur est survenue : {e}")

def suppr_tab():
    st.markdown("<h2 style='text-align: center; color: #333;'>Supprimer des Pages</h2>", unsafe_allow_html=True)

    # Structure de grille pour centrer (1/3 largeur)
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown('<div class="card-label">📄 Document à Modifier</div>', unsafe_allow_html=True)
        delete_doc = st.file_uploader("Choisissez le fichier", type="pdf", key="suppr_doc", label_visibility="collapsed")
        
        num_pages_del = 0
        if delete_doc:
            try:
                delete_doc.seek(0)
                num_pages_del = len(PdfReader(delete_doc).pages)
                st.caption(f"✅ {num_pages_del} pages détectées")
            except Exception as e:
                st.error(f"Erreur lecture PDF: {e}")

        st.markdown("---")

        st.markdown('<div class="card-label">Pages à supprimer (ex: 1, 3-5)</div>', unsafe_allow_html=True)
        pages_str = st.text_input("Pages", label_visibility="collapsed", placeholder="Exemple: 1, 2, 5-7")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Supprimer les Pages", key="btn_suppr"):
            if not delete_doc or not pages_str:
                st.warning("Veuillez charger un document et indiquer les pages à supprimer.")
            else:
                with st.spinner("Traitement..."):
                    try:
                        pages_to_del = parse_page_numbers(pages_str, num_pages_del)
                        if not pages_to_del:
                            st.warning("Aucune page valide sélectionnée.")
                        else:
                            final_del = delete_pages_mem(delete_doc, pages_to_del)
                            st.success(f"Pages {pages_to_del} supprimées !")
                            st.download_button(
                                label="📥 Télécharger le résultat",
                                data=final_del.getvalue(),
                                file_name="suppression_edscan.pdf",
                                mime="application/pdf"
                            )
                    except Exception as e:
                        st.error(f"Erreur : {e}")

def convert_tab():
    st.markdown("<h2 style='text-align: center; color: #333;'>Convertir PDF</h2>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('<div class="card-label">📄 Document à Convertir</div>', unsafe_allow_html=True)
        convert_doc = st.file_uploader("Choisissez le fichier PDF", type="pdf", key="convert_doc", label_visibility="collapsed")
        
        if convert_doc:
             st.caption("✅ Document chargé. Prêt à être converti.")
        
        st.markdown("---")
        st.markdown('<div class="card-label">Format de sortie</div>', unsafe_allow_html=True)
        format_choice = st.radio("Format", ["Image (JPEG)", "Word (DOCX)"], horizontal=True, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Convertir", key="btn_convert"):
            if not convert_doc:
                st.warning("Veuillez charger un document PDF.")
            else:
                with st.spinner("Conversion en cours..."):
                    try:
                        # Reset pointer just in case
                        convert_doc.seek(0)
                        
                        if format_choice == "Image (JPEG)":
                            res_type, res_data, res_name = convert_pdf_to_jpegs_mem(convert_doc)
                            
                            mime_type = "image/jpeg" if res_type == "image" else "application/zip"
                            label_btn = "📥 Télécharger l'image" if res_type == "image" else "📥 Télécharger fichier compressé"
                            
                        else: # Word
                            res_data, res_name = convert_pdf_to_word_mem(convert_doc)
                            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            label_btn = "📥 Télécharger Word"

                        st.success("Conversion réussie !")
                        st.download_button(
                            label=label_btn,
                            data=res_data,
                            file_name=res_name,
                            mime=mime_type
                        )
                    except Exception as e:
                        st.error(f"Erreur lors de la conversion : {e}")


def extract_tab():
    st.markdown("<h2 style='text-align: center; color: #333;'>Extraire des Pages</h2>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown('<div class="card-label">📄 Document Source</div>', unsafe_allow_html=True)
        extract_doc = st.file_uploader("Choisissez le fichier PDF", type="pdf", key="extract_doc", label_visibility="collapsed")
        
        num_pages_total = 0
        if extract_doc:
            try:
                extract_doc.seek(0)
                reader = PdfReader(extract_doc)
                num_pages_total = len(reader.pages)
                st.caption(f"✅ {num_pages_total} pages détectées")
            except Exception as e:
                st.error(f"Erreur lecture PDF: {e}")
        
        st.markdown("---")
        
        st.markdown('<div class="card-label">Pages à extraire (ex: 1, 3-5)</div>', unsafe_allow_html=True)
        pages_str = st.text_input("Pages", key="extract_pages_input", label_visibility="collapsed", placeholder="Exemple: 1, 3-5", help="Entrez les numéros de pages séparés par des virgules ou des tirets.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="card-label">Format de sortie</div>', unsafe_allow_html=True)
        output_format = st.radio("Format", ["PDF", "Images (JPEG)"], horizontal=True, key="extract_format", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Extraire les Pages", key="btn_extract"):
            if not extract_doc or not pages_str:
                st.warning("Veuillez charger un fichier PDF et indiquer les pages à extraire.")
            else:
                with st.spinner("Extraction en cours..."):
                    try:
                        # Reset pointer
                        extract_doc.seek(0)
                        
                        pages_to_extract = parse_page_numbers(pages_str, num_pages_total)
                        
                        if not pages_to_extract:
                            st.warning("Aucune page valide sélectionnée.")
                        else:
                            if output_format == "PDF":
                                res_pdf = extract_pages_to_pdf_mem(extract_doc, pages_to_extract)
                                st.success("Extraction réussie !")
                                st.download_button(
                                    label="📥 Télécharger PDF",
                                    data=res_pdf.getvalue(),
                                    file_name="pages_extraites.pdf",
                                    mime="application/pdf"
                                )
                            else:
                                type_res, data_res, name_res = extract_pages_to_images_mem(extract_doc, pages_to_extract)
                                mime = "image/jpeg" if type_res == "image" else "application/zip"
                                st.success("Extraction réussie !")
                                st.download_button(
                                    label=f"📥 Télécharger {name_res}",
                                    data=data_res,
                                    file_name=name_res,
                                    mime=mime
                                )
                    except Exception as e:
                        st.error(f"Une erreur est survenue : {e}")

# --- Main Application ---

def main():
    # --- Configuration de la page ---
    st.set_page_config(page_title="Ed_scan - Editeur PDF", layout="wide")

    # --- Chargement du CSS personnalisé ---
    load_css()
    
    # --- Contenu Principal avec Onglets ---
    tab_fusion, tab_suppr, tab_convert, tab_extract = st.tabs(["⚡ Fusionner", "🗑️ Supprimer Pages", "🔄 Convertir Document", "📑 Extraire Pages"])

    with tab_fusion:
        fusion_tab()

    with tab_suppr:
        suppr_tab()
    
    
    with tab_convert:
        convert_tab()

    with tab_extract:
        extract_tab()

if __name__ == "__main__":
    main()
