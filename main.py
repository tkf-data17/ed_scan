import streamlit as st
from pypdf import PdfReader
from utils import insert_pdfs_mem, delete_pages_mem, parse_page_numbers, convert_pdf_to_jpegs_mem
from style import load_css

# --- Fonctions d'affichage des onglets ---

def fusion_tab():
    st.markdown("<h2 style='text-align: center; color: #333;'>Fusionner des Documents PDF</h2>", unsafe_allow_html=True)
    
    # Structure de grille pour centrer le contenu (1/3 largeur)
    col_left, col_center, col_right = st.columns([1, 1, 1])

    with col_center:
        # --- Card 1: Document Principal ---
        st.markdown('<div class="card-label">⬆️ Document Principal</div>', unsafe_allow_html=True)
        main_doc = st.file_uploader("Choisissez le fichier principal", type="pdf", key="inserer_main", label_visibility="collapsed")
        if main_doc:
            try:
                 reader = PdfReader(main_doc)
                 st.caption(f"✅ {len(reader.pages)} pages détectées")
            except:
                 st.error("Erreur lecture PDF")

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
    col_left, col_center, col_right = st.columns([1, 1, 1])

    with col_center:
        st.markdown('<div class="card-label">📄 Document à Modifier</div>', unsafe_allow_html=True)
        delete_doc = st.file_uploader("Choisissez le fichier", type="pdf", key="suppr_doc", label_visibility="collapsed")
        
        num_pages_del = 0
        if delete_doc:
            try:
                num_pages_del = len(PdfReader(delete_doc).pages)
                st.caption(f"✅ {num_pages_del} pages détectées")
            except:
                st.error("Erreur lecture PDF")

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
    st.markdown("<h2 style='text-align: center; color: #333;'>Convertir PDF en Image(s)</h2>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_center:
        st.markdown('<div class="card-label">📄 Document à Convertir</div>', unsafe_allow_html=True)
        convert_doc = st.file_uploader("Choisissez le fichier PDF", type="pdf", key="convert_doc", label_visibility="collapsed")
        
        if convert_doc:
             st.caption("✅ Document chargé. Prêt à être converti.")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Convertir en images", key="btn_convert"):
            if not convert_doc:
                st.warning("Veuillez charger un document PDF.")
            else:
                with st.spinner("Conversion en cours..."):
                    try:
                        # Reset pointer just in case
                        convert_doc.seek(0)
                        res_type, res_data, res_name = convert_pdf_to_jpegs_mem(convert_doc)
                        
                        st.success("Conversion réussie !")
                        
                        mime_type = "image/jpeg" if res_type == "image" else "application/zip"
                        label_btn = "📥 Télécharger l'image" if res_type == "image" else "📥 Télécharger fichier compressé"
                        
                        st.download_button(
                            label=label_btn,
                            data=res_data,
                            file_name=res_name,
                            mime=mime_type
                        )
                    except Exception as e:
                        st.error(f"Erreur lors de la conversion : {e}")

# --- Main Application ---

def main():
    # --- Configuration de la page ---
    st.set_page_config(page_title="Ed_scan - Editeur PDF", layout="wide")

    # --- Chargement du CSS personnalisé ---
    load_css()
    
    # --- Contenu Principal avec Onglets ---
    tab_fusion, tab_suppr, tab_convert = st.tabs(["⚡ Fusionner", "🗑️ Supprimer Pages", "🖼️ PDF to JPEG"])

    with tab_fusion:
        fusion_tab()

    with tab_suppr:
        suppr_tab()
    
    with tab_convert:
        convert_tab()

if __name__ == "__main__":
    main()
