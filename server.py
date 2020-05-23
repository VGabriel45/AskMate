from flask import Flask, render_template, request, redirect, flash
import data_manager
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def latest_questions():
    data = data_manager.get_latest_questions()
    return render_template('list.html', data=data)


@app.route("/list", methods=['GET', 'POST'])
def list_questions():
    sort_by = ''
    direction = ''
    if request.method == "POST":
        sort_by = request.form.get('sort')
        direction = request.form.get('direction')
        data = data_manager.sort_csv(sort_by, direction)
    else:
        data = data_manager.get_data()
    return render_template('list.html', data=data, sort_by=sort_by, direction=direction, searching=True)


@app.route('/searched', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_by = request.form.get('search-question')
        data = data_manager.search_questions(search_by)
    return render_template('searched-questions.html', data=data, search_by=search_by)


@app.route('/question/<question_id>', methods=['POST', 'GET'])
def display_question(question_id):
    if request.method == 'GET':
        data_manager.view_up_answer(question_id)
    question_comments = data_manager.get_question_comment(question_id)
    questions = data_manager.find_question(question_id)
    answers = data_manager.find_question_answer(question_id)
    comments = data_manager.get_comments()
    question_tags = data_manager.get_question_tags(question_id)
    return render_template('question.html', questions=questions, answers=answers, question_comments=question_comments, comments=comments, question_id=question_id, question_tags=question_tags)


@app.route('/add-question', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        submission_time = datetime.now().date()
        view_number = 0
        vote_number = 0
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.add_question_in_csv(submission_time, view_number, vote_number, title, message, image)
        return redirect('/list')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    questions = data_manager.find_question(question_id)
    if request.method == 'POST':
        submission_time = datetime.now().date()
        vote_number = 0
        message = request.form.get('message')
        question_id = question_id
        image = request.form.get('image')
        data_manager.add_answer_in_csv(submission_time, vote_number, message, question_id, image)
        return redirect('/question/' + str(question_id))
    return render_template('add-answer.html', questions=questions)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_question_comment(question_id):
    questions = data_manager.find_question(question_id)
    if request.method == 'POST':
        submission_time = datetime.now().date()
        message = request.form.get('message')
        data_manager.add_comment_for_question(question_id, message, submission_time)
        return redirect('/question/' + str(question_id))
    return render_template('add_comment.html', questions=questions)


@app.route('/question/<question_id>/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_answer_comment(question_id, answer_id):
    answers = data_manager.find_answers(answer_id)
    if request.method == 'POST':
        submission_time = datetime.now().date()
        message = request.form.get('message')
        data_manager.add_comment_for_answer(answer_id, message, submission_time)
        return redirect('/question/' + question_id)
    return render_template('add_comment_answer.html', answers=answers, question_id=question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_on_csv(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    questions = data_manager.find_question(question_id)
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.update_question_on_csv(title, message, image, question_id)
        return redirect('/question/' + str(question_id))
    return render_template('edit.html', questions=questions)


@app.route('/question/<question_id>/answer/<answer_id>/edit', methods=['POST', 'GET'])
def edit_answer(question_id, answer_id):
    answers = data_manager.find_answers(answer_id)
    if request.method == 'POST':
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.update_answer_on_csv(message, image, answer_id)
        return redirect('/question/' + question_id)
    return render_template('edit-answer.html', answers=answers, question_id=question_id)


@app.route('/question/<question_id>/answer/<answer_id>/comment/<comment_id>/edit', methods=['POST', 'GET'])
def edit_comment_for_answer(question_id, answer_id, comment_id):
    answers = data_manager.find_answers(answer_id)
    comments = data_manager.get_comment_by_id(comment_id)
    if request.method == 'POST':
        data_manager.edit_comment_count(comment_id)
        message = request.form.get('message')
        data_manager.update_comment_on_csv(message, comment_id)
        return redirect('/question/' + question_id)
    return render_template('edit-answer-comment.html', answers=answers, question_id=question_id, comments=comments, answer_id=answer_id)


@app.route('/question/<question_id>/comment/<comment_id>/edit', methods=['POST', 'GET'])
def edit_comment_for_question(question_id, comment_id):
    comments = data_manager.get_comment_by_id(comment_id)
    if request.method == 'POST':
        data_manager.edit_comment_count(comment_id)
        message = request.form.get('message')
        data_manager.update_comment_on_csv(message, comment_id)
        return redirect('/question/' + question_id)
    return render_template('edit-question-comment.html',  question_id=question_id, comments=comments)


@app.route('/question/<question_id>/answer/<answer_id>/delete')
def delete_answer(question_id, answer_id):
    data_manager.delete_answer_on_csv(answer_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/answer/<answer_id>/comment/<comment_id>/delete')
def delete_answer_comment(question_id, answer_id, comment_id):
    data_manager.delete_comment_on_csv(comment_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/comment/<comment_id>/delete')
def delete_question_comment(question_id, comment_id):
    data_manager.delete_comment_on_csv(comment_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag_on_csv(tag_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-tag', methods=['POST', 'GET'])
def add_question_tag(question_id):
    if request.method == 'POST':
        name = request.form.get('tag-name')
        try:
            data_manager.add_tag_in_csv(name)
            tag_id = data_manager.get_tag_id(name)
            data_manager.add_tag_in_question_tag(question_id, tag_id['id'])
            return redirect('/question/' + str(question_id))
        except:
            flash('Tag already in use')
            return redirect(request.referrer)
    return render_template('add-tag.html', question_id=question_id)


@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    data_manager.vote_up_question(question_id)
    return redirect(request.referrer)


@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    data_manager.vote_down_question(question_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    data_manager.vote_up_answer(answer_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_down")
def A_vote_down(answer_id):
    data_manager.vote_down_answer(answer_id)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(
        debug=True
    )
