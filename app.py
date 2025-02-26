from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import difflib

app = Flask(__name__)

# Base URLs for documentation
CDP_DOCS = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Custom headers to bypass restrictions
def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

# Function to find closest matching section
def find_best_match(query, headers):
    header_texts = [header.get_text().strip().lower() for header in headers]
    best_match = difflib.get_close_matches(query.lower(), header_texts, n=1, cutoff=0.6)
    if best_match:
        for header in headers:
            if header.get_text().strip().lower() == best_match[0]:
                return header
    return None

# Function to fetch relevant documentation content
def fetch_cdp_info(cdp, query):
    if cdp not in CDP_DOCS:
        return "CDP not supported."
    
    url = CDP_DOCS[cdp]
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code == 403:
            return f"Access to {cdp} documentation is restricted. Please visit {url} manually."
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract relevant sections
        headers = soup.find_all(['h2', 'h3', 'h4'])
        best_header = find_best_match(query, headers)
        
        relevant_text = ""
        if best_header:
            relevant_text += best_header.get_text().strip() + "\n\n"
            sibling = best_header.find_next_siblings()
            for sib in sibling:
                if sib.name in ['h2', 'h3']:
                    break
                relevant_text += sib.get_text().strip() + "\n\n"
        
        if not relevant_text:
            return f"No direct match found in {cdp} documentation. Try refining your query or visit {url}."
    
    except requests.exceptions.RequestException as e:
        relevant_text = f"Failed to retrieve documentation. Error: {str(e)}"
    
    return relevant_text.strip()

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '').strip().lower()
    
    matched_cdp = None
    for cdp in CDP_DOCS.keys():
        if cdp in question:
            matched_cdp = cdp
            break
    
    if matched_cdp:
        answer = fetch_cdp_info(matched_cdp, question)
    else:
        answer = "I couldn't identify the CDP. Please specify Segment, mParticle, Lytics, or Zeotap."
    
    return jsonify({"answer": answer, "question": question})

if __name__ == '__main__':
    app.run(debug=True)
