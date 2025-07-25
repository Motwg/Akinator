import random

from flask import (
    Blueprint, render_template, request, send_from_directory, current_app
)

from ..controllers.akinator import calculate_probabilities, questions, supported_characters
from ..utils import set_menu
from ..blueprints.auth import manage_cookie_policy

bp = Blueprint('bl_home', __name__)


questions_so_far = []
answers_so_far = []


@bp.route('/', methods=('GET',))
def index():
    global questions_so_far, answers_so_far
    mc = set_menu('home')
    template = 'home/index.html'

    question = request.args.get('question')
    answer = request.args.get('answer')
    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))

    probabilities = calculate_probabilities(questions_so_far, answers_so_far)
    for q, a in zip(questions_so_far, answers_so_far):
        print(q, a)
    print("probabilities", probabilities)

    questions_left = list(set(questions.keys()) - set(questions_so_far))
    if len(questions_left) == 0:
        result = sorted(probabilities, key=lambda p: p['probability'], reverse=True)[0]
        questions_so_far = []
        answers_so_far = []
        return render_template(
            template,
            mc=mc,
            result=result['name'],
            character_names=supported_characters()
        )
    else:
        next_question = random.choice(questions_left)
        print(next_question, questions[next_question])
        return render_template(
            template,
            mc=mc,
            question=next_question,
            question_text=questions[next_question],
            character_names=supported_characters()
        )


@bp.route('/about', methods=('GET', 'POST'))
@manage_cookie_policy
def about():
    mc = set_menu('about')
    bar = create_plot()
    return render_template('home/about.html', mc=mc, plot=bar)


@bp.route('/privacy-notice', methods=('GET', 'POST'))
def privacy():
    mc = set_menu('')
    return render_template('home/privacy-notice.html', mc=mc)


@bp.route('/terms-of-service', methods=('GET', 'POST'))
def terms_of_service():
    mc = set_menu('')
    return render_template('home/terms-of-service.html', mc=mc)


# MANAGE sitemap and robots calls
# These files are usually in root, but for Flask projects must
# be in the static folder
@bp.route('/robots.txt')
@bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():
    generator = np.random.default_rng(42)
    n = 40
    x = np.linspace(0, 1, n)
    y = generator.random(n)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
