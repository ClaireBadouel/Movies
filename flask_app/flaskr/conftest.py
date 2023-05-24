import os
import tempfile

import pytest
from flaskr.__init__ import create_app
from flaskr.db import get_db, init_db


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client