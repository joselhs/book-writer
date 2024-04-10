import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain


class MainCharacterChain:

    PROMPT = """
    Se te provee el resumé de una persona.
    Describe el perfil de esa persona en unas pocas frases e incluye el nombre de esa persona.
    Si su resumé está en inglés, traducelo al castellano.
    
    Resume: {text}
    Perfil:"""
    
    def __init__(self):
        self.llm = ChatOpenAI()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )

        self.chain.verbose = True


    def load_resume(self, file_name):
        folder = './docs'
        file_path = os.path.join(folder, file_name)
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()

        return docs



    def run(self, file_name):
        # Load Resume
        docs = self.load_resume(file_name)
        resume = '\n\n'.join([doc.page_content for doc in docs])
        # Generate a Summary
        return self.chain.invoke(resume)
        