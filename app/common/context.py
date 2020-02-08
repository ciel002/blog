from app.model.setting import Config
from manager import app


@app.app_context_processor
def my_context_processor():
    return dict(
        web_config=Config.get_config(),
    )