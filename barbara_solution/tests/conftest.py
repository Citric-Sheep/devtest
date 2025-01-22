import pytest
from barbara_solution.main import create_app, db


@pytest.fixture
def app():
    """
    Provide a Flask app instance to pytest-flask by calling create_app().
    """
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
