from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate



load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history = [])
print(chat)
conversation = ConversationChain(
    llm=llm, verbose=True, memory=ConversationBufferMemory()
)


def get_gemini_response(question):
    try:
        #response = model.generate_content(question)
        response = chat.send_message(question, stream = True)
        print(response)
        #return response

        text_response = ''
        if isinstance(response.text, str):
            text_response = response.text
        else:
            text_response = ' '.join(part for part in response.text.parts)  # assuming response.text.parts is a list of strings

        # Limit the response to 300 words
        words = text_response.split()
        if len(words) > 100:
            text_response = ' '.join(words[:100]) + '... (response truncated)'

        return {'status': 1, 'response': text_response}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 0, 'response': f"An error occurred: {e}"}

'''conversation.predict(input="Hi there, my name is Asif!")
conversation.predict(input="how are you doing?")
conversation.predict(input="who are you?")
conversation.predict(input="what is my name?")
conversation.predict(input="define rocket in 15 words?")
conversation.predict(input="who is president of india")'''

