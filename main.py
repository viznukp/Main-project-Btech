from ide import *
from trained_model_test import*
from input_handler import *

def main():
    print("here 1")
    gpt = GPT()
    print("here 2")
    input_handler = InputHandeler(gpt)
    print("here 3")
    editor = Editor()
    print("here 4")
    editor.init(input_handler)
    

if __name__ == "__main__":
    main()
