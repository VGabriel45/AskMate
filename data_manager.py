import csv
import os
import operator

data_headers = ['id', 'submission_time', 'view_number',
                'vote_number', 'title', 'message', 'image']
data_headers_answers = ['id', 'submission_time',
                        'vote_number', 'question_id', 'message', 'image']


def get_data(filename, data_id=None):

    csv_dict_list = []
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_dict_list.append(row)

    if data_id is not None:
        for dictionary in csv_dict_list:
            if dictionary['id'] == str(data_id):

                return dictionary

    return csv_dict_list


def reverse_list(my_list):
    return reversed(my_list)


def add_in_csv(filename, new_data, fieldnames):

    with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames)
        csv_writer.writerow(new_data)
    return 'Submitted successful'


def update_on_csv(filename, question_id, update_dict, fieldnames):

    list_of_all = get_data(filename)

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames)
        csv_writer.writeheader()
        for row in list_of_all:
            if row['id'] == question_id:
                row = update_dict
            csv_writer.writerow(row)

    return "update succesfull"


def delete_on_csv(filename, delete_id, fieldnames):

    list_of_all = get_data(filename)

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames)
        csv_writer.writeheader()
        for row in range(len(list_of_all)-1):
            if list_of_all[row]['id'] == delete_id:
                del list_of_all[row]
            csv_writer.writerow(list_of_all[row])
    return "delete succesfull"


def find_question(filename, id):
    questions_list = get_data(filename)
    for question in questions_list:
        if question['id'] == str(id):
            return question


def find_answers(filename, id):
    answers_list = []
    answers = get_data(filename)
    for answer in answers:
        if answer['question_id'] == str(id):
            answers_list.append(answer)
    return answers_list


def generate_id():
    max_id = 0
    for row in get_data('question.csv'):
        if int(row['id']) > max_id:
            max_id = int(row['id'])
    return max_id + 1


def sort_csv(filename, key, direction):
    data = get_data(filename)
    return sorted(data, key=lambda i: i[key], reverse=direction)



