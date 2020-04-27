from flask import Flask, render_template, request, redirect, url_for
import data_manager
import csv

app = Flask(__name__)


@app.route("/")
def hello():
    tabel_header_questions = data_manager.DATA_HEADER_QUESTIONS
    questions_list = data_manager.get_data()
    return render_template('all_questions.html', questions_list=questions_list,
                           tabel_header_questions=tabel_header_questions)


@app.route("/add_new_question", methods=["GET", "POST"])
def add_question():
    print(data_manager.generate_id())
    if request.method == 'POST':
        new_question = {
            'id': data_manager.generate_id(),
            'submission_time': 0,  # trebuie adaugat ceasul
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('title'),
            'message': request.form.get("message"),
            'image': request.form.get('image')

        }
        data_manager.add_in_csv(new_question)
        return redirect('/')
    return render_template('add_new_question.html')


@app.route('/question/<id>', methods=['GET', 'POST'])
def show_question(id):
    if request.method == "GET":
        question = data_manager.find_question(id)
        return render_template('question.html', question=question)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    questions_list = data_manager.get_data()
    question_1 = data_manager.find_question(question_id)

    if request.method == 'POST':
        question = {
            'id': question_id,
            # trebuie modificat cu data, ex:questions_list[int('submission_time')]
            'submission_time': 0,
            # trebuie modificat cu data, ex:questions_list[int('submission_time')]
            'view_number': 0,
            # trebuie modificat cu data, ex:questions_list[int('submission_time')]
            'vote_number': 0,
            'title': request.form.get('title'),
            'message': request.form.get("message"),
            'image': request.form.get('image')
        }
        data_manager.update_on_csv(question_id, question)
        return redirect('/')

    return render_template('edit.html', id=question_id, question=question_1)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_on_csv(question_id)
    return redirect('/')

#
# @app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
# def new_answer(question_id):


if __name__ == "__main__":
    app.run(
        debug=True
    )
