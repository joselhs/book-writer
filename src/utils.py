from langchain.chains import LLMChain
from langchain_openai.chat_models import ChatOpenAI


class BaseStructureChain():

    PROMPT = ''

    def __init__(self) -> None:
        self.llm = ChatOpenAI(temperature=0.3)

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True


class BaseEventChain:
    
    PROMPT = ''

    def __init__(self) -> None:

        self.llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo-16k')

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True

