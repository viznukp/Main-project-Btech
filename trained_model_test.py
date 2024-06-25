from openai import OpenAI

class GPT():
  def __init__(self):
    self.client = OpenAI(api_key='***********************************')
    self.model = "ft:gpt-3.5-turbo-0125:personal::******" #4
    self.messages=[
      {"role": "system", "content": "you are a ntuaral language interpreting chatbot. The following are some actions that you have to do. You will get a pice of string that asks to do something. Interpret the string provide a json output. use the following keys in the json. the json alway contain the key \"command\". if the query is about selecting or higlighting lines \"commmand = select_line\", if the qery is about generating code \"command = code\", if the query is about general questions or to explain code or algorithms \"command = text\". Here's the list of output jason structures. The rest of the values of command is given in there. {'command':'code', 'content': The user query might be asking to generate code then fill the asked code here, 'description':description about the code}, {command:'text', content:answers to users queries which might not require any code outputs}, {command:'select_line', start_line:starting line number for the selection, end_line: ending line number for selection}, {command:'copy'}, {command:'paste'}, {command: 'cut'}, {command: 'save', filename:if user specified the filename then provide it here else don't} , {command:'goto', line_number:the line number to which the user wants to move the cursor, direction: if the user specified to go to the end of line set direction to 'end'. if user wants to go to the starting of the line set position to 'start'}, {command:'run'}, {command:'debug'}, {command:'new_line'}, {command:'scroll', direction: this attribute takes two values, either 'up' or 'down' depending on the direction in which the user wants to scroll}. use exactly the given attribute names as keys according to the type of query. The output json must follow one of the given jason structures. If the query says \"updated state of code\", that means it is giving you the latest version of the code present in the editor now. So when asked to make changes in the code refer to the latest code.)"}
    ]

  def ask(self, query):
    new_query = {"role": "user", "content": query}
    self.messages.append(new_query)
    print(self.messages)
    completion = self.client.chat.completions.create(
      messages=self.messages,
      model= self.model,
      temperature=0
    )

    print("\n\n")
    print (completion.choices[0].message)
    print("\n\n")
    self.messages.append(completion.choices[0].message)
    return completion.choices[0].message
# print(completion.choices[0].message)