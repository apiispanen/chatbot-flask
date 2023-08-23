from typing import List, Optional, Dict
from pydantic import BaseModel

class MultipleChoiceQuestion(BaseModel):
    question_number: int
    question: str
    correct_answer: str
    wrong_answers: List[str]
    answer_reason: Optional[str] = None

class QuizLayout(BaseModel):
    quiz_title: str = "Quiz"
    questions: List[MultipleChoiceQuestion]

schema = QuizLayout.schema()

# print({'message':schema})





