
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Ensure the session has a place to store answers
    if "answers" not in session:
        session["answers"] = {}

    # Validate the answer (for simplicity, we just check if it's non-empty)
    if not answer:
        return False, "Answer cannot be empty."

    # Store the answer in the session
    session["answers"][current_question_id] = answer
    # print("@@@@@", session["answers"])
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        current_question_id = 0
    if current_question_id == len(PYTHON_QUESTION_LIST):
        return None, current_question_id

    next_ques = PYTHON_QUESTION_LIST[current_question_id]["question_text"] + f"\n\nOptions are:\n&bull; {'\n&bull; '.join(PYTHON_QUESTION_LIST[current_question_id]['options'])}"
    return next_ques, current_question_id +1



def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    correct_anss = 0
    total_ques = len(PYTHON_QUESTION_LIST)

    for id, ques in enumerate(PYTHON_QUESTION_LIST):
        correct_ans = ques['answer']
        user_ans = session["answers"].get(id+1)
        if user_ans == correct_ans:
            correct_anss += 1
    return f"Quiz Completed! Your score is {correct_anss}/{total_ques}"
    # return "dummy result"
