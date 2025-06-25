Project Overview: Automated Metadata Extraction App

Objective : The project aims to automatically extract structured metadata (such as title, summary, keywords, keyphrases, language, etc.) from unstructured documents including PDFs, DOCX files, and images. It leverages Google Cloud Vision API for OCR, YAKE for keyword extraction, and spaCy + pyTextRank for NLP to make document understanding faster and smarter.


Feature	Description :

Multi-format Input	: Supports PDFs, DOCX, and image files (JPG, PNG, etc.)
OCR Integration     : Uses Google Cloud Vision API to extract text from images or scanned PDFs
Keyword Extraction	: Uses YAKE to extract top keywords and keyphrases
Metadata Generation : Extracts title, summary, keywords, language, word count, and timestamp
Language Detection	: Identifies the document's language using langdetect
Summary Extraction	: Uses spaCy's TextRank to produce concise summaries
Title Detection     : Combines heuristics and NLP (noun/proper noun-rich short lines) to extract meaningful titles
Streamlit UI	      : Provides a clean web interface to upload files, view full text, and download metadata
Download Metadata   : Gives option to user to download the metadata in "json" format


Tools & Technologies Used :

Technology	              Purpose

Streamlit	                Web interface for the app
Google Cloud Vision	      OCR to extract text from images and scanned PDFs
spaCy + pyTextRank	      NLP for sentence parsing, summarization, and title detection
YAKE	                    Lightweight unsupervised keyword extractor
langdetect	              Detects document language
PyPDF2, python-docx	      Parsing PDF and DOCX files
pdf2image + Pillow	      Converting PDF pages to images for OCR fallback
wordninja	                Splits long concatenated words (e.g., metadataextractor)


Why This Design?

1.>OCR Fallback Logic-
Many PDFs have embedded images with no selectable text. We first try native PDF text extraction. If it fails, we convert pages to images and apply Vision OCR.

2.>Heuristic Title Extraction-
Certificates or reports often have all-caps titles. A rule-based filter extracts such lines, and spaCy acts as a fallback for general cases.



Strategies which were changed during developement:

1.>Removed Hugging Face / OpenAI APIs
These APIs required authentication, quota management, and billing, making them unsuitable for free/community deployment. Instead, we opted for fully open-source NLP (spaCy, YAKE) that works offline and integrates well with local and cloud setups.
    
2.>Dropped NLTK
NLTK caused path-related errors and required downloading corpora, which were problematic in deployment (e.g., punkt_tab errors). Replaced by spaCy for better and faster NLP.



Limitations:

*Relies on Google Cloud Vision API (credentials must be available).

*Summarization depends on the quality of extracted OCR/text.

*Not optimized for handwriting or multilingual documents.


How to Run the APP :



To Run the app (metadata_gen_app.py) locally, use:

streamlit run metadata_gen_app.py  # This will automatically run the web app on browser

NOTE: Before running the app , install the required dependencies using:

!pip install streamlit pyngrok google-cloud-vision pdf2image pillow python-docx langdetect wordninja yake spacy pytextrank PyPDF2
!apt-get install -y poppler-utils
!python -m spacy download en_core_web_sm



To Run the app (metadata_gen_app.py) on Google Colab :

- First download the app file metadata_gen_app.py in your system
  
- Then on Colab , run the file "script.ipynb" , in this file after installing all the dependencies and setting up "ngrok" token it will prompt you to upload the code file , then you must upload the downloaded "metadata_gen_app.py" ,
  then on runnning the next cell , it will prompt a public_url (eg.- "https://b961-35-247-107-213.ngrok-free.app") , just tap on the url and user will be redirected to the Web App




    
 
