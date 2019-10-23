"""
Reference: https://github.com/deepmipt/DeepPavlov/blob/master/docs/features/models/squad.rst
Full DeepPavlov docs: http://docs.deeppavlov.ai/en/master/
"""
from deeppavlov import build_model, configs


class BertSquad:
    def __init__(self, download=False):
        self.model = build_model(configs.squad.squad, download=download)

    def ask_question(self, document, question):
        if not isinstance(document, list):
            document = [document]

        if not isinstance(question, list):
            question = [question]

        answer = self.model(document, question)
        return answer

    def qa_session(self, document):
        while True:
            question_text = input("('exit' to quit) Question: ")
            if question_text.lower() == 'exit':
                break

            answer = self.ask_question(document, question_text)
            print(answer)
