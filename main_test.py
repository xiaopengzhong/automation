# @File   : .py
# @Time   : 2023/7/14 0:37
# @Author :
# @Software: PyCharm
import os

import pytest

if __name__ == '__main__':
    pytest.main(['test_case/api_tests/test_businessRule.py', '-s', '--alluredir=tmp/report', '--clean-alluredir'])
    os.system("allure generate ./tmp/report -o ./report/html --clean")
    os.system("allure serve -p 60001 ./tmp/report")

