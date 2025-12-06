from flask import Flask, render_template, session, request, redirect, url_for
from db_scripts import get_question_after, get_quieses
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'


def start_quiz(quiz_id):
    try:
        session['quiz'] = int(quiz_id)
    except (TypeError, ValueError):
        session['quiz'] = -1
    session['last_question'] = 0
    session['score'] = 0
    session['total'] = 0


def end_quiz():
    session.clear()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        quizzes = get_quieses()
        return render_template('index.html', quizzes=quizzes)
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))


@app.route('/test', methods=['GET', 'POST'])
def test():
    # ensure quiz started
    if not ('quiz' in session) or int(session.get('quiz', -1)) < 0:
        return redirect(url_for('index'))

    # POST: user answered current question
    if request.method == 'POST':
        selected = request.form.get('answer')
        correct = request.form.get('correct')
        # increase total asked
        session['total'] = session.get('total', 0) + 1
        if selected and correct and selected == correct:
            session['score'] = session.get('score', 0) + 1
        # advance last_question to the current question id
        cur_qc_id = session.get('current_qc_id', 0)
        session['last_question'] = int(cur_qc_id)
        # after processing, redirect to GET to load next question
        return redirect(url_for('test'))

    # GET: fetch next question
    result = get_question_after(session.get('last_question', 0), session.get('quiz', 1))

    if not result:
        return redirect(url_for('result'))

    # result: (quiz_content.id, question, answer, wrong1, wrong2, wrong3)
    qc_id, q_text, correct, w1, w2, w3 = result
    options = [correct, w1, w2, w3]
    shuffle(options)

    # store current question id so POST can advance
    session['current_qc_id'] = qc_id

    return render_template(
        'test.html',
        question=q_text,
        options=options,
        correct=correct,
        score=session.get('score', 0),
        total=session.get('total', 0),
        quiz_id=session.get('quiz')
    )


@app.route('/result')
def result():
    score = session.get('score', 0)
    total = session.get('total', 0)
    end_quiz()
    return render_template('result.html', score=score, total=total)


if __name__ == '__main__':
    app.run(debug=True)
