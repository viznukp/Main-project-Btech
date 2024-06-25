import json
# from speech_to_text import *

class InputHandeler:
    def __init__(self, gpt_insatance):
        self.gpt = gpt_insatance
        # self.recorder = SpeechRecognizer()

    def ask_gpt(self,query):
        result = self.gpt.ask(query)

        content_dict = json.loads(result.content)
        print(content_dict)
        
        return content_dict



    