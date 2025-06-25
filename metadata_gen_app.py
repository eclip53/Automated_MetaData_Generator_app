#Streamlit Metadata Extraction App (Vision OCR + YAKE + spaCy)


# To run the app on the system first install all the dependencies using :
"""!pip install streamlit pyngrok google-cloud-vision pdf2image pillow python-docx langdetect wordninja yake spacy pytextrank PyPDF2
!apt-get install -y poppler-utils  # for pdf2image
!python -m spacy download en_core_web_sm"""

# Importing essential modeules/libraries and packages

import os
import io
import json
import re
from datetime import datetime
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
from pdf2image import convert_from_bytes
from google.cloud import vision
import langdetect
import wordninja
import yake
import streamlit as st
import spacy
import pytextrank

# Load spaCy model with TextRank
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

# Setting Up Cloud Vision API Key
GOOGLE_APPLICATION_CREDENTIALS = """
{
  "type": "service_account",
  "project_id": "fabled-cocoa-463611-h2",
  "private_key_id": "f84a318bb4b2d31828e88ac0e3e78fe308aadd20",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7U277/CGnEuRA\\nkGhili7GsdfdhuG/u21hXf9c2hTFPi4fi6Hu8onAzDPUo73BYhrV32fmQUbB4sae\\nybHCKnwGsdcuVGIs0rBzUq7KFdq/4XdyAUqDvofRx19SMJGBj1MuHztU6YYn4hEj\\nAFH+kri+qTPY0zmSJHaRkxakb5VPvo8ahV8O7+741MmtA7PpUusrg4Nj7zaKR5w5\\n8hMfnGQdcaomwQbqvfZSwnT4fRj/aBRMsm9jEOpAzVHB9YAvmbCANr+3cVikUsxe\\nSh40DRJQlsPRS718DFkkXZFf+vksy++1vgKv0kq43VbG9azbjkSSLzWTWPTFn3TW\\nJW6sF1zPAgMBAAECggEADxm7sZ5yjAhO1BGQCJp4rNW7RAVSf2U5fQbZxf9iez/2\\n8d4MsLlmd18+sl58tnEVHraCpqIOdSS1xCkYJkHMe7GsWfS9cUWOqc05f9rhJmSj\\nf1IxUotyYWvD+Fkn8Zy/JNGps7+ba+2iWgL1mSL0t5HmNw1X77r2v+duhNTl4Wak\\nvJCxCqcLlaurmTM4BfksEA99uor+k6/lIR7eC+tr3iiQN9I1ALNpU6bfyTusNFyA\\nrOx++oeHfhIOWBdkJmFTnBgeZtzmUxjZaSLIIjdK+q2pz0ZWdjGUXjFI4vr2gChs\\n8eblrLvJCLVCPYTKxVedJtiR3UfMIj+eWdfmnJa9mQKBgQDpGHCKbHkinKT6cWI9\\nxp/sFEvdEI7XQpotSCVzq0F8nbjfClv0HKT8gC0pvIW7zQwFjFblEngTwiB0Hqwz\\natfD65/EJcZrM7fnmbJH3ROn1CDftBr5SKgM+03AWVp0DVVgojBU/9fYBF3mTAoU\\nSZ99evZR3j8gdi7K9nqaXHXnxQKBgQDNu6byzo5WSIyXnDcJ0vo6GbXXwCDKVm8g\\nTCwfx6FrhFpU9A7HjimMA+cqX/8MLKfkO9GJ4KLRqyHrJnkdlQ1rzxdGDH4MBD7+\\nc3dbmPPVezfLKViccKPMPn8q5r/ZPSvIxe615QRL0YJyPENvX/Rf84XOJrOEEBHm\\nhRaf9BPngwKBgQCcSsXTGu6SNaQtRO9Raqf6XJWNkbelQEQujoyGJVNQolS+QKzt\\nXnOF1s/xhzXIebFQ2wu8pwiafvTRx2tBQqeP96J1m7qSUOhDw3uV0feG9aZhONtJ\\nQN1lbu9wRLlwzSvtEnMD21Q3xJ3NeDjd54uoUFVvCW0ccAHqFyCX9d0c3QKBgQCj\\n+bwf7Ohf9yUvtc/cYa8VXeak1rqL6wZZfLzye3+6HVyON5QME9Aji/zUtnynLHSI\\nofDp7wR3DupS7XA9Vs7CreXD7DMOyteWoVtxw2AdOD+JCyRYVCMJqIpdHFuu/2WF\\nedVAXw/kilFpUYUCIT26uHNek1Qjn1dVH6Cfzr+KlwKBgANO6ZesCq05FOTogTTF\\nbnrWhMm/U1d8i5PLLW1Tj44HWEY8PAK6xSmAIsKe6nMrkItIVD3K64Jhh/pjjyOr\\nEUH162oClsHG5CTYjRuqAqFlZCbePMnWBBTeMOWtsn9sY6pVuRwzgIAgfXKtgpLO\\nMrqgCAM/808pFFiCR2VaUOP/\\n-----END PRIVATE KEY-----\\n",
  "client_email": "vision-access@fabled-cocoa-463611-h2.iam.gserviceaccount.com",
  "client_id": "111486156180014007001",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vision-access%40fabled-cocoa-463611-h2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
with open("/tmp/gcp_key.json", "w") as f:
    json.dump(json.loads(GOOGLE_APPLICATION_CREDENTIALS), f)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_key.json"

# Initialize Vision API client
vision_client = vision.ImageAnnotatorClient()


#Cleans and normalizes OCR-extracted text for better readability and downstream processing.
def clean_ocr_text(text):
    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"(?:[A-Z]\s*){3,}", line):
            fixed = " ".join(line.split())
            cleaned_lines.append(fixed)
            continue
        line = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', line)
        line = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', line)
        line = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', line)
        tokens = []
        for word in line.split():
            if re.match(r"https?://\S+", word) or re.match(r"www\.\S+", word) or re.match(r"^[\w\.-]+@[\w\.-]+$", word):
                tokens.append(word)
            elif len(word) > 14:
                tokens.extend(wordninja.split(word))
            else:
                tokens.append(word)
        line = re.sub(r'\s{2,}', ' ', " ".join(tokens))
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


# Extract text from an image using Google Cloud Vision OCR.
def extract_text_from_image(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    image = vision.Image(content=image_bytes)
    response = vision_client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")
    return response.full_text_annotation.text


# Extract text from a PDF file using PyPDF2 or OCR fallback if needed.
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
        if text.strip():
            return text
        raise ValueError("No text found")
    except:
        file.seek(0)
        images = convert_from_bytes(file.read())
        return "\n".join([extract_text_from_image(img) for img in images])
    

# Extract text from a DOCX (Word) file.
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs)


# Route uploaded file to the appropriate text extraction function based on its type.
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type.startswith("image/"):
        return extract_text_from_image(Image.open(uploaded_file))
    else:
        raise ValueError("Unsupported file type")
    
    

# Generate a document title using uppercase headers or spaCy noun-based sentences.
def extract_title(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # 1. Prioritize clean all-caps lines near top
    for line in lines[:10]:
        if line.isupper() and 2 <= len(line.split()) <= 8:
            return line  # Keep all caps 

    # 2. Use spaCy to find best candidate sentence
    doc = nlp(text)
    for sent in doc.sents:
        s = sent.text.strip()
        if 3 <= len(s.split()) <= 12 and any(tok.pos_ in {"NOUN", "PROPN"} for tok in sent):
            return s

    # 3. Fallback
    return "Untitled Document"



# Generate a short summary using spaCy TextRank algorithm.
def extract_summary(text, num_sentences=3):
    doc = nlp(text)
    summary = " ".join([str(sent) for sent in doc._.textrank.summary(limit_sentences=num_sentences)])
    return summary if summary else "No summary available"



# Generate metadata including title, summary, keywords, and language from the given text.
def generate_metadata(text, filename="unknown.txt"):
    kw_extractor = yake.KeywordExtractor(top=20, stopwords=None)
    keyword_results = kw_extractor.extract_keywords(text)

    keyword_list = [kw for kw, _ in keyword_results if len(kw.split()) == 1][:10]
    keyphrase_list = [kw for kw, _ in keyword_results if len(kw.split()) > 1][:10]

    try:
        language = langdetect.detect(text)
    except:
        language = "unknown"

    title = extract_title(text)
    summary = extract_summary(text)
    word_count = len(re.findall(r"\w+", text))

    return {
        "filename": filename,
        "title": title,
        "summary": summary,
        "keywords": keyword_list,
        "keyphrases": keyphrase_list,
        "language": language,
        "word_count": word_count,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }




# Streamlit UI
st.set_page_config(page_title="Automated Meta Data Generator", layout="wide")
st.title("Automated Metadata Generator (Vision OCR + YAKE + spaCy)")

uploaded_file = st.file_uploader("Upload a PDF, DOCX, or Image", type=["pdf", "docx", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("Extracting content..."):
        try:
            raw_text = extract_text(uploaded_file)
            cleaned_text = clean_ocr_text(raw_text)
            metadata = generate_metadata(cleaned_text, filename=uploaded_file.name)

            tab1, tab2 = st.tabs(["Extracted Text", "Metadata"])
            with tab1:
                st.text_area("Full Text", cleaned_text, height=300)
            with tab2:
                st.json(metadata)

            st.download_button(
                label="Download Metadata as JSON",
                data=json.dumps(metadata, indent=4),
                file_name="metadata.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f" Error: {str(e)}")
