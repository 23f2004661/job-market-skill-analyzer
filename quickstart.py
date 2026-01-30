import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import base64
from bs4 import BeautifulSoup
import unicodedata
import re
from google import genai
from dotenv import load_dotenv
import httpx
from collections import Counter

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

POSITIVE_KEYWORDS = [
    "job",
    "internship",
    "intern",
    "opportunity",
    "hiring",
    "apply",
    "opening",
    "role",
    "position",
    "full-time",
    "full time",
    "paid internship",
    "work based learning",
    "wbl",
    "roles",
    "genai",
    "mlops",
    "ai/ml",
    "data science",
    "data scientist",
    "data science intern",
    "data engineer",
    "machine learning",
    "ml engineer",
    "ai engineer",
    "generative ai",
    "genai",
    "llm",
    "analytics",
    "research intern"
]

NEGATIVE_KEYWORDS = [
    "scam",
    "beware",
    "session",
    "workshop",
    "webinar",
    "talk",
    "bootcamp",
    "learn",
    "training",
    "invitation to",
    "congratulations",
    "next steps",
    "selection",
    "orientation"
]

SKILL_KEYWORDS = {
    # Programming
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql", "postgresql", "mysql"],
    "javascript": ["javascript"],

    # Data / AI
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "data science": ["data science"],
    "statistics": ["statistics", "probability"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "image processing"],

    # GenAI / LLM
    "llm": ["llm", "large language model"],
    "genai": ["generative ai", "genai"],
    "rag": ["rag", "retrieval augmented generation"],
    "prompt engineering": ["prompt engineering"],
    "fine-tuning": ["fine tuning", "finetuning", "peft"],

    # Frameworks
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "huggingface": ["huggingface"],
    "langchain": ["langchain"],

    # Backend / Infra
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
    "aws": ["aws"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "microservices": ["microservices"],

    # Systems
    "data structures": ["data structures", "dsa"],
    "algorithms": ["algorithms"],
    "system design": ["system design", "lld", "hld"],

    # DevOps / MLOps
    "mlops": ["mlops"],
    "llmops": ["llmops"],
    "ci/cd": ["ci/cd"]
}


def normalize_text_strong(text):
    # Normalize unicode (– → -, fancy quotes → normal)
    text = unicodedata.normalize("NFKD", text)

    # Lowercase
    text = text.lower()

    # Replace all dashes with standard dash
    text = re.sub(r"[‐-‒–—―]", "-", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def is_job_or_internship_subject(subject):
    s = normalize_text_strong(subject)

    # Hard reject
    if any(neg in s for neg in NEGATIVE_KEYWORDS):
        return False

    # Soft accept
    if any(pos in s for pos in POSITIVE_KEYWORDS):
        return True

    return False

def extract_href_strings(a_tags):
    hrefs = []
    for tag in a_tags:
        href = tag.get("href")
        if href:
            hrefs.append(href)
    return hrefs

def extract_google_doc_links(hrefs):
    return [
        url for url in hrefs
        if "docs.google.com/document" in url and "/pub" in url
    ]

def extract_doc_content(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        doc_content = soup.get_text(separator="\n")
        return doc_content
    except httpx.HTTPError as e:
        print(f"Error fetching document content from {url}: {e}")
        return "Did not get the document content."

def clean_jd_text(text):
    # Remove Google Docs boilerplate
    boilerplate = [
        "Published using Google Docs",
        "Report abuse",
        "Learn more",
        "Updated automatically every"
    ]
    for b in boilerplate:
        text = text.replace(b, "")

    # Remove non-breaking spaces
    text = text.replace("\xa0", " ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_skills_from_text(text):
    text = text.lower()
    found = set()

    for skill, variants in SKILL_KEYWORDS.items():
        for v in variants:
            if v in text:
                found.add(skill)
                break

    return list(found)

def get_llm_respponse(skill_summary):
    prompt = f"""You are analyzing job market demand based on a frequency analysis of skills extracted from recent job descriptions.

Each skill has a count indicating how often it appeared across roles.

Your task:
1. Identify which skills a student should START working on now to be prepared for future job descriptions.
2. Group skills into:
   - Core foundational skills (must-have)
   - Cross-role / production skills (high leverage)
   - Emerging / future-facing skills
3. Recommend a clear learning priority order.
4. Explain briefly WHY each group matters for employability.
5. Focus on preparation for future job descriptions, not just current ones.

Important rules:
- Do NOT invent new skills.
- Base all reasoning only on the provided data.
- Be concise, practical, and actionable.

Skill frequency data:
{json.dumps(skill_summary, indent=2)}
"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}], 
    }
    r = httpx.post("https://aipipe.org/openrouter/v1/chat/completions",json = data, headers = headers, timeout=httpx.Timeout(300.0))
    answer = r.json()['choices'][0]['message']['content']
    return answer

final_list_to_send_to_genai_raw = []
final_list = []

def main():
    """extracts the jd from each mail of the iic inbox and then process it to get the skill summary and finally get llm response
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"], q="from:iic@study.iitm.ac.in").execute()
        )
        print(f"This is the Estimated result size: {results.get('resultSizeEstimate')}")
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print("Messages:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            headers = msg["payload"]["headers"]

            for header in headers:
                if header["name"] == "Subject":
                    # print(f'  Subject: {header["value"]}')
                    subject = header["value"]
                    if is_job_or_internship_subject(subject):
                        print(f'Message ID: {message["id"]}')
                        print(f'  Subject: {subject}')
                        parts = msg.get("payload").get("parts", [])
                        for part in parts:
                            if part.get("mimeType") == "text/html":
                                data = part.get("body").get("data")
                                html = base64.urlsafe_b64decode(data).decode("utf-8")
                                soup = BeautifulSoup(html, "html.parser")
                                links = soup.find_all("a", href=True)
                                hrefs = extract_href_strings(links)
                                url = extract_google_doc_links(hrefs)
                                if url:
                                    doc_content = extract_doc_content(url[0])
                                    final_list_to_send_to_genai_raw.append({
                                        "subject": subject,
                                        "url": url[0],
                                        "content": doc_content
                                    })
        
        skill_counter = Counter()
        for item in final_list_to_send_to_genai_raw:
            cleaned_content = clean_jd_text(item["content"])
            skills = extract_skills_from_text(cleaned_content)
            skill_counter.update(skills)
        
        skill_summary = [
            {"skill": skill, "count": count}
            for skill, count in skill_counter.most_common()
        ]

        print("\nSkill Summary:")
        print(json.dumps(skill_summary, indent=2))
        final_output = get_llm_respponse(skill_summary)
        print("\nFinal LLM Output:")
        print(final_output)
        
                                    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
