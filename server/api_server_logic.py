import json
from queue import Queue


class logic:

    def __init__(self):
        self.queue_to_calculate = Queue()
        self.list_of_answers = []
        """
        self.queue_to_calculate.put(
            {'sex': ['male'], 'city': ['Chaohu City, Hefei City'], 'province': ['Anhui'],
             'country': ['China'], 'age': ['80']})
        self.queue_to_calculate.put(
            {'sex': ['female'], 'city': ['Chaohu City, Hefei City'], 'province': ['Anhui'],
             'country': ['Italy'], 'age': ['30']})
        """
    def add_question(self, question, username):
        print("Added question", question)
        self.queue_to_calculate.put(question)
        question["user"] = username

    def get_top_question(self):
        question = self.queue_to_calculate.get()
        print("There is only :", self.queue_to_calculate.qsize())
        return question

    def add_answer(self, answer):
        print("Add answer :\n", answer)
        self.list_of_answers.append(answer)

    def get_all_answers(self):
        print("Get all answers :\n", self.list_of_answers)
        return self.list_of_answers

    def check_if_empty(self):
        if self.queue_to_calculate.empty():
            return True
        return False

