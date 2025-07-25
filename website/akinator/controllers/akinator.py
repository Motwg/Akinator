from typing import NewType
from sklearn.feature_selection import chi2
from sklearn.impute import SimpleImputer

import numpy as np
import pandas as pd

Priori = NewType('Priori', tuple[np.ndarray, np.ndarray])
Posterior = NewType('Posterior', tuple[np.ndarray, np.ndarray])

np.set_printoptions(formatter={'float': lambda x: '{0:0.3f}'.format(x)})

questions = {
    0: 'Is your character fictional',
    1: 'Is your character yellow',
    2: 'Is your character bald',
    3: 'Is your character a man',
    4: 'Is your character short',
    5: 'Is your character blonde'
}

characters = {
    0: {'name': 'Homer Simpson', 'answers': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0.25}},
    1: {'name': 'SpongeBob', 'answers': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0.75, 5: 0.25}},
    2: {'name': 'Sandy Cheeks', 'answers': {0: 1, 1: 0, 2: 0, 3: 0, 5: 0}},
    3: {'name': 'Kermit the Frog', 'answers': {1: 0, 2: 1, 3: 0.75, 4: 0.25, 5: 0}},
    4: {'name': 'Elvis Presley', 'answers': {0: 0, 1: 0.1, 2: 0, 3: 1, 4: 0.25, 5: 0}},
    5: {'name': 'Donald Trump', 'answers': {0: 0, 1: 0.25, 2: 0.1, 3: 1, 4: 0, 5: 1}},
}

# Prior
p_character = 1. / len(characters)
p_not_character = 1. - p_character


def supported_characters() -> list[str]:
    return [character['name'] for character in characters.values()]


# Depreciated
def calculate_answer_probability_for_character(character, question, answer):
    return (max(1 - abs(answer - character_answer(character, question)), 0.01),
            max(np.mean([1 - abs(answer - character_answer(not_character, question))
                         for not_character in characters
                         if not_character['name'] != character['name']]), 0.01))


# Depreciated
def calculate_character_probability(character, questions_so_far, answers_so_far):
    # Likelihood
    p_answers_given_character = 1.
    p_answers_given_not_character = 1.
    for question, answer in zip(questions_so_far, answers_so_far):
        p, not_p = calculate_answer_probability_for_character(character, question, answer)
        p_answers_given_character *= p
        p_answers_given_not_character *= not_p

    # Evidence
    p_answers = p_character * p_answers_given_character + p_not_character * p_answers_given_not_character

    # Bayes Theorem
    p_character_given_answers = (p_character * p_answers_given_character) / p_answers

    return p_character_given_answers


# Depreciated
def character_answer(character, question):
    if question in character['answers']:
        return character['answers'][question]
    return 0.5


# Depreciated
def calculate_probabilities(questions_so_far, answers_so_far):
    probabilities = []
    for character in characters.values():
        probabilities.append({
            'name': character['name'],
            'probability': calculate_character_probability(character, questions_so_far, answers_so_far)
        })

    return probabilities


def get_answer_for_characters(question) -> np.ndarray:
    return np.array([char['answers'].get(question, 0.5) for char in characters.values()], dtype=float)


def count_entropy(p_yes: np.ndarray, p_no: None | np.ndarray = None) -> np.ndarray:
    entropy = p_yes * np.log2(p_yes)
    if isinstance(p_no, np.ndarray):
        entropy += p_no * np.log2(p_no)
    return -entropy


def calculate_posterior(priori: Priori, characters_answer: np.ndarray, user_answer: float) -> Posterior:
    differs = np.abs(characters_answer - user_answer)
    not_differs = np.tile(differs, (len(differs), 1))
    print('Priori: ', priori)
    np.fill_diagonal(not_differs, np.nan)
    not_differs = np.nanmean(not_differs, axis=1)

    p_till_answer_given_characters = np.clip(1 - differs, 0.01, None) * priori[0]
    p_till_answer_given_not_characters = np.clip(1 - not_differs, 0.01, None) * priori[1]

    return Posterior((p_till_answer_given_characters, p_till_answer_given_not_characters))


def bayes(posterior: Posterior) -> np.ndarray:
    return posterior[0] / (posterior[0] + posterior[1])


def get_all_answers_matrix(characters: dict[int, dict[str, str | dict[int, float]]]):
    return pd.DataFrame(map(lambda v: v['answers'], characters.values()), dtype=float).to_numpy()


def get_best_features(characters):
    answers = get_all_answers_matrix(characters)
    impute = SimpleImputer(missing_values=np.nan, strategy='mean')
    answers = impute.fit_transform(answers)

    # asked_questions = set()
    # asked_questions.add(question)
    # print('Left questions: ', lq := set(all_questions.keys()).difference(asked_questions))
    # answers = answers[:, list(lq)]
    # print('masked', answers)
    f_class, _ = chi2(answers, np.arange(answers.shape[0]))
    print('Chi2: ', f_class)
    return f_class


if __name__ == '__main__':
    answers = {0: 1, 1: 1, 2: 0.75, 3: 1, 4: 0, 5: 0}
    all_questions = questions

    p_chars = np.ones(len(characters)) / len(characters)
    p_not_chars = np.ones(len(characters)) - p_chars
    priori = Priori((p_chars, p_not_chars))
    for question, answer in answers.items():
        chars_answer = get_answer_for_characters(question)
        posterior_y, posterior_n = calculate_posterior(priori, chars_answer, answer)

        priori = Posterior((posterior_y, posterior_n))
        print('Bayes: ', b := bayes(priori), np.max(b), np.argmax(b), np.sum(b))

