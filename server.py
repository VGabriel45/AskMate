from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/list")
def list_questions():
    headers = data_manager.data_headers
    data = data_manager.reverse_list(data_manager.get_data('question.csv'))
    return render_template('list.html', data = data,headers = headers)

@app.route('/question/<question_id>', methods=['POST', 'GET'])
def display_question(question_id):
    headers = data_manager.data_headers
    question = data_manager.find_question('question.csv',question_id)
    answer = data_manager.find_answers('answer.csv',question_id)
    answers = data_manager.get_data('answer.csv')
    return render_template('question.html',question=question,answer = answer, answers=answers, headers = headers)

@app.route('/add-question', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = '0'
        view_number = '0'
        vote_number = 0
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        new_question = {'id':id ,'submission_time':submission_time, 'view_number':view_number,
                        'vote_number':vote_number,'title':title, 'message':message,'image': image}
        data_manager.add_in_csv('question.csv',new_question,data_manager.data_headers)
        return redirect('/list')
    return render_template('add-question.html')

@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    question = data_manager.find_question('question.csv', question_id)
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = '0'
        vote_number = 0
        message = request.form.get('message')
        question_id = question['id']
        image = request.form.get('image')
        new_answer = {'id':id ,'submission_time':submission_time,
                        'vote_number':vote_number,'question_id': question_id, 'message':message, 'image': image}
        data_manager.add_in_csv('answer.csv',new_answer,data_manager.data_headers_answers)
        return redirect('/question/' + str(question_id))
    return render_template('add-answer.html', question = question)

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_on_csv('question.csv',question_id,data_manager.data_headers)
    return redirect('/list')

@app.route('/question/<question_id>/edit', methods=['POST','GET'])
def edit_question(question_id):
    question = data_manager.find_question('question.csv',question_id)
    if request.method == 'POST':
        id = question_id
        submission_time = '0'
        view_number = '0'
        vote_number = 0
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        update_question = {'id':id ,'submission_time':submission_time, 'view_number':view_number,
                        'vote_number':vote_number,'title':title, 'message':message,'image': image}
        data_manager.update_on_csv('question.csv',question_id, update_question,data_manager.data_headers)
        return redirect('/list')
    return render_template('edit.html', question = question)

@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_on_csv('answer.csv',answer_id,data_manager.data_headers_answers)
    return redirect(request.referrer)


# @app.route('/question/<question_id>/vote_up')
# def vote_up(question_id):
#     vote = int(question['vote_number'])
#     question = data_manager.find_question('question.csv',question_id)
#     id = question_id
#     submission_time = question['submission_time']
#     view_number = question['view_number']
#     vote_number = str(vote + 1)
#     title = question['title']
#     message = question['message']
#     image = question['image']
#     update_question = {'id':id ,'submission_time':submission_time, 'view_number':view_number,
#                     'vote_number':vote_number,'title':title, 'message':message,'image': image}
#     data_manager.update_on_csv('question.csv',question_id, update_question,data_manager.data_headers)
#     return redirect(request.referrer)

@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    file_data = data_manager.find_question('question.csv', question_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) + 1)
    data_manager.update_on_csv('question.csv', question_id, file_data, data_manager.data_headers)
    return redirect(request.referrer)

@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    file_data = data_manager.find_question('question.csv', question_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) - 1)
    data_manager.update_on_csv('question.csv', question_id, file_data, data_manager.data_headers)
    return redirect(request.referrer)

@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    file_data = data_manager.find_question('answer.csv', answer_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) + 1)
    data_manager.update_on_csv('answer.csv', answer_id, file_data, data_manager.data_headers_answers)
    return redirect(request.referrer)

@app.route("/answer/<answer_id>/vote_down")
def A_vote_down(answer_id):
    file_data = data_manager.find_question('answer.csv', answer_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) - 1)
    data_manager.update_on_csv('answer.csv', answer_id, file_data, data_manager.data_headers_answers)
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(
        debug=True
    )
