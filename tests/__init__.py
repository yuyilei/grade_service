from service import app
from .test_grade_api import test_grade_api

if __name__ == '__main__':
    test_grade_api(app)
