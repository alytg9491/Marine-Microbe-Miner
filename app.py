import streamlit as st
from Bio import Entrez

# 1. Page Configuration (Makes it look like a real website)
st.set_page_config(page_title="Marine Microbe Miner", page_icon="🧬")
st.title("🌊 Marine Microbe Genome Miner")
st.markdown("""
This tool fetches genomic data from the **NCBI Nucleotide database**. 
It is designed to assist in bioprospecting for marine microbial secondary metabolites.
""")

# 2. User Input Area
st.subheader("Search the Global Genomic Database")
species = st.text_input("Enter Marine Species Name (e.g., Salinispora tropica):", "")

# 3. The Logic (Fetching from NCBI)
if st.button("Search & Fetch DNA"):
    if species:
        # REQUIRED: Tell NCBI who is accessing their data
        Entrez.email = "your-email@example.com" 
        
        try:
            with st.spinner(f"Scanning NCBI archives for {species}..."):
                # Search for 'complete genome' to get the best quality data
                search_term = f"{species}[Organism] AND complete genome[Title]"
                search_handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=1)
                search_results = Entrez.read(search_handle)
                search_handle.close()

                if search_results["IdList"]:
                    genome_id = search_results["IdList"][0]
                    st.success(f"✅ Success! Genome found. NCBI Accession ID: {genome_id}")
                    
                    # Fetch the actual DNA sequence in FASTA format
                    fetch_handle = Entrez.efetch(db="nucleotide", id=genome_id, rettype="fasta", retmode="text")
                    fasta_data = fetch_handle.read()
                    fetch_handle.close()

                    # 4. Display a "Science Preview" for your resume demo
                    st.subheader("Genetic Sequence Preview (First 1,000 Base Pairs):")
                    st.code(fasta_data[:1000] + "...", language="text")
                    
                    # 5. Add a Download Button (Very professional feature)
                    st.download_button(
                        label="Download Full Genome for Analysis",
                        data=fasta_data,
                        file_name=f"{species.replace(' ', '_')}_genome.fasta",
                        mime="text/plain"
                    )
                else:
                    st.warning("⚠️ No complete genome found. Try a different species name.")
                
        except Exception as e:
            st.error(f"Error connecting to NCBI: {e}")
    else:
        st.info("Please enter a species name to begin the search.")

# Footer for your resume
st.divider()
st.caption("Developed for UC San Diego (Scripps Institution of Oceanograph) Undergraduate Admissions Portfolio.")
