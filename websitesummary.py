#pip install -r requirements.txt
#pip freeze > requirements.txt
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
from openai import OpenAI
class Website:
    def __init__(self,url):
        self.url = url
        load_dotenv()
        response = requests.get(url)
        soup =BeautifulSoup(response.content,"html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
    def prompts(self):
        system="""You are an intellegent Summarizer you should summrarize the provided text to 5 sentences
        remove the navigation and text you think is used as lable for html text Give it in proper paragraph heading formate """
        user=""""""
        return system,user
    def summarize(self,text):
         systemprompt,userpromt =self.prompts()
         messages = [{"role":"system","content":systemprompt},
                    {
            "role": "user",
            "content": text ,
        },]
         from openai import OpenAI

         client = OpenAI()

         completion = client.chat.completions.create(
         model="gpt-4o-mini",
         messages=messages
         )
         print( completion.choices[0].message.content)

ed = Website("https://www.example.pk/")
# print(ed.title)
# print(ed.text)
text =ed.text
ed.summarize(text)