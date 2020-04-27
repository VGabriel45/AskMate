import csv
import os

ANSWER_PATH = os.getenv(
    'ANSWER_PATH') if 'ANSWER_PATH' in os.environ else 'answer.csv'
QUESTIONS_PATH = os.getenv(
    'QUESTIONS_PATH') if 'QUESTIONS_PATH' in os.environ else 'question.csv'

DATA_HEADER_ANSWER = ['id', 'submission_time',
                      'vote_number', 'question_id', 'message', 'image']
DATA_HEADER_QUESTIONS = ['id', 'submission_time',
                         'view_number', 'vote_number', 'title', 'message', 'image']


def get_data(data_id=None):

    csv_dict_list = []
    with open('question.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_dict_list.append(row)

    if data_id is not None:
        for dictionary in csv_dict_list:
            if dictionary['id'] == str(data_id):

                return dictionary

    return csv_dict_list


def find_question(id):
    questions_list = get_data()
    for question in questions_list:
        if question['id'] == id:
            return question


def add_in_csv(new_data):

    with open('question.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER_QUESTIONS)
        csv_writer.writerow(new_data)
    return 'Submitted successful'


def update_on_csv(question_id, update_dict):

    list_of_all = get_data()

    with open('question.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER_QUESTIONS)
        csv_writer.writeheader()
        for row in list_of_all:
            if row['id'] == question_id:
                row = update_dict
            csv_writer.writerow(row)

    return "update succesfull"


def delete_on_csv(delete_id):

    list_of_all = get_data()

    with open('question.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER_QUESTIONS)
        csv_writer.writeheader()
        for row in range(len(list_of_all)-1):
            if list_of_all[row]['id'] == delete_id:
                del list_of_all[row]
            csv_writer.writerow(list_of_all[row])
    return "delete succesfull"


def generate_id():
    max_id = 0
    for row in get_data():
        if int(row['id']) > max_id:
            max_id = int(row['id'])
    return max_id + 1
