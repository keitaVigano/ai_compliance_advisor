import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class ComplianceAgent:
    def __init__(self):
        """
        Initialize the ComplianceAgent with the Gemini API.
        """
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        genai.configure(api_key=os.getenv("GEMINIKEY"))
        self.prompt_template = """
        Answer the following question using only the provided documents as context.
        If no useful information is found in the documents, state that no relevant data was found.

        Question: {question}

        Documents:
        {context}

        Answer:
        """

    def generate_response(self, question, documents):
        """
        Generate a structured response based on the retrieved documents.

        :param question: The user question as a string.
        :param documents: List of documents retrieved by the QueryAgent.
        :return: The generated answer as a string.
        """
        context = "\n\n".join([doc for doc in documents])
        prompt = self.prompt_template.format(question=question, context=context)

        response = self.model.generate_content(
            prompt
        ).text

        return response
