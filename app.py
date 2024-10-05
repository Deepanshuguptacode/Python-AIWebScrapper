from flask import Flask, render_template, request
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key='AIzaSyCFXQEmG1WkHeg2ZLhM-UtrDDkSdm8VWUc')

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    scraped_data = None

    if request.method == 'POST':
        # Check if 'url' is in the form data
        if 'url' in request.form:
            url = request.form['url']
            # Scrape data from the provided URL
            scraped_data = scrape_website(url)
            if scraped_data:
                response = get_gemini_response(scraped_data)

        # Check if 'question' is in the form data (when asking a question after scraping)
        elif 'question' in request.form and 'scraped_data' in request.form:
            question = request.form['question']
            scraped_data = request.form['scraped_data']
            response = get_gemini_response(scraped_data + "\n" + question)

    return render_template('index.html', response=response, scraped_data=scraped_data)

def scrape_website(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Extract the text content of the page
        text = soup.get_text()
        return format_text(text)  # Structure the text
    except Exception as e:
        return str(e)

def format_text(text):
    """Format the scraped text to enhance readability."""
    paragraphs = text.split('\n')  # Split text into paragraphs
    structured_text = "\n\n".join([p.strip() for p in paragraphs if p.strip()])  # Remove empty lines
    return structured_text

def get_gemini_response(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([text])
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

