from flask import Flask

app = Flask(__name__)

from blueprints.TextBlockWorker import text_block_bp
from blueprints.QuestionWorker import question_bp
from blueprints.QuestionProcessorWorker import question_processor_bp
from blueprints.QuestionAnswerWorker import question_answer_bp
from blueprints.QADeliveryWorker import qa_delivery_bp

app.register_blueprint(text_block_bp,url_prefix="/text_block")
app.register_blueprint(question_bp,url_prefix="/question")
app.register_blueprint(question_processor_bp,url_prefix="/question_processor")
app.register_blueprint(question_answer_bp,url_prefix="/question_answer")
app.register_blueprint(qa_delivery_bp,url_prefix="/qa_delivery")

if __name__ == '__main__':
    app.run()