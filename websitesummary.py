import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

class WebsiteSummarizer:
    def __init__(self, url: str):
        self.url = url
        load_dotenv()  # Load .env file
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in .env file.")

        self.client = OpenAI(api_key=self.api_key)
        self.title = ""
        self.text = ""

    def fetch_and_parse_website(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Error fetching the website: {e}")
            return False

        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string.strip() if soup.title else "No title found"

        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)
        return True

    def prompts(self):
        system = (
            "You are an intelligent summarizer. Summarize the provided webpage content "
            "into 5 concise sentences. Remove navigation, labels, or irrelevant text. "
            "Present the summary in proper paragraph format with a clear heading."
        )
        return system

    def summarize(self):
        if not self.text:
            print("⚠️ No text found to summarize.")
            return

        messages = [
            {"role": "system", "content": self.prompts()},
            {"role": "user", "content": self.text}
        ]

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Change to gpt-4 if needed
                messages=messages
            )
            print("\n✅ Summary:\n")
            print(completion.choices[0].message.content)
        except OpenAIError as e:
            print(f"❌ Error while calling OpenAI API: {e}")

def main():
    url = "https://www.example.pk/"
    summarizer = WebsiteSummarizer(url)
    if summarizer.fetch_and_parse_website():
        print(f"\n🌐 Title: {summarizer.title}")
        summarizer.summarize()

if __name__ == "__main__":
    main()
