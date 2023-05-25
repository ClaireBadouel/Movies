import pytest
from movies_package import create_app
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(__file__), "helpers"))


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client
