
from zxcvbn import zxcvbn

def analyze_password(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    return score, feedback['warning'], feedback['suggestions']
