import logging
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import nltk

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class ATSSimilarityChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.stemmer = PorterStemmer()

    def get_synonyms(self, word: str) -> set:
        synonyms = set([word.lower()])
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
        return synonyms

    def preprocess_text(self, text: str) -> str:
        try:
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            processed = " ".join(self.stemmer.stem(word) for word in text.split())
            logging.debug(f"Processed text: {processed[:1000]}...")
            return processed
        except Exception as e:
            logging.error(f"Error preprocessing text: {str(e)}")
            return text

    def filter_relevant_text(self, text: str, job_desc: str = None) -> str:
        """
        Extracts relevant sections from resumes based on job description.
        """
        relevant_sections = [
            "professional summary", "profile", "summary", "objective", "about me",
            "skills", "technical skills", "core competencies", "experience",
            "projects", "achievements", "qualifications", "training"
        ]

        irrelevant_sections = [
            "education", "personal details", "contact information", "references",
            "interests", "hobbies", "volunteering", "languages", "publications", "awards"
        ]

        key_terms = set()
        if job_desc:
            jd_text = job_desc.lower()
            patterns = [
                r'\b(python|java|c\+\+|sql|aws|azure|tensorflow|pytorch|git|ml|ai|cloud|docker|kubernetes)\b'
            ]
            for pattern in patterns:
                matches = re.findall(pattern, jd_text)
                key_terms.update(matches)

        lines = text.split("\n")
        relevant_text = []
        in_relevant_section = False

        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            if any(section in line_lower for section in relevant_sections):
                in_relevant_section = True
                relevant_text.append(line)
            elif any(section in line_lower for section in irrelevant_sections):
                in_relevant_section = False
            elif in_relevant_section:
                relevant_text.append(line)
            elif key_terms and any(term in line_lower for term in key_terms):
                relevant_text.append(line)

        filtered_text = "\n".join(relevant_text).strip()
        logging.debug(f"Filtered text: {filtered_text[:4000]}...")
        return filtered_text

    def calculate_similarity(self, job_desc: str, resume_text: str) -> float:
        try:
            if not job_desc.strip() or not resume_text.strip():
                raise ValueError("Job description or resume text cannot be empty")

            job_desc_processed = self.preprocess_text(job_desc)
            resume_text_filtered = self.filter_relevant_text(resume_text, job_desc)
            resume_text_processed = self.preprocess_text(resume_text_filtered)

            vectors = self.vectorizer.fit_transform([job_desc_processed, resume_text_processed])
            tfidf_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

            jd_terms = set(job_desc_processed.split())
            resume_terms = set(resume_text_processed.split())
            jd_synonyms = {term: self.get_synonyms(term) for term in jd_terms}

            key_matches = sum(
                1 for jd_term in jd_terms
                if jd_term in resume_terms or any(syn in resume_terms for syn in jd_synonyms[jd_term])
            )
            key_match_ratio = key_matches / len(jd_terms) if jd_terms else 0

            final_score = (tfidf_similarity * 0.25 + key_match_ratio * 0.75) * 100
            return min(round(final_score, 2), 100.0)
        except Exception as e:
            logging.error(f"Error computing similarity: {str(e)}")
            return 0.0


def extract_text_from_pdf(pdf_path, output_folder="output_images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        logging.info("Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=300)
        full_text = ""

        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            image.save(image_path, "PNG")
            logging.info(f"Processing page {i+1}...")
            text = pytesseract.image_to_string(image, config='--psm 6')
            full_text += f"\n--- Page {i+1} ---\n{text}"

        logging.info("Text extraction complete!")
        logging.debug(f"Extracted text: {full_text[:4000]}...")
        return full_text
    except Exception as e:
        logging.error(f"PDF extraction failed: {str(e)}")
        return ""
    finally:
        if os.path.exists(output_folder):
            for file in os.listdir(output_folder):
                os.remove(os.path.join(output_folder, file))
            os.rmdir(output_folder)


def main():
    logging.getLogger().setLevel(logging.INFO)

    pdf_file = "/content/Anshoom_Resume.pdf"
    job_desc = ("**We are seeking a highly motivated Data Analyst with expertise in AI & Machine Learning and a strong foundation in Graphic & UI/UX Design. The ideal candidate will develop and optimize AI/ML models, conduct data analysis using Python, and implement predictive analytics solutions such as cryptocurrency trading bots and customer churn prediction models. They will also design intuitive user experiences, create and manage digital engagement strategies, and collaborate with cross-functional teams to drive innovation. Proficiency in Python, C++, Java, Scikit-learn, TensorFlow, LangChain, Microsoft Azure AI, Figma, and Adobe Suite is essential. The candidate holds a Bachelor’s in Computer Science Engineering with AI (Hons.) from Chandigarh University and certifications including Microsoft Azure AI Associate Engineer. Notable achievements include winning MUN at IIT Roorkee, publishing a book chapter on cryptocurrency trading, and running a YouTube channel with 4.3K+ subscribers. This role is ideal for an individual passionate about AI-driven solutions, data analytics, and impactful design strategies.**")

    extracted_text = extract_text_from_pdf(pdf_file)
    if not extracted_text:
        logging.error("Failed to extract text from PDF. Aborting ATS check.")
        return

    with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    checker = ATSSimilarityChecker()
    score = checker.calculate_similarity(job_desc, extracted_text)
    logging.info(f"ATS Similarity Score: {score}%")


if __name__ == "__main__":
    main()
