Run all tests:
pytest -v -s --alluredir=reports/allure-results && allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report

Run tests in parallel (3 workers):
pytest -n 3 -v -s --alluredir=reports/allure-results

Clean reports:
rmdir /s /q reports\allure-results && rmdir /s /q reports\allure-report

Allure Report:
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

nornal run +html report:
pytest -v -s --alluredir=reports/allure-results --html=reports/report.html --self-contained-html


