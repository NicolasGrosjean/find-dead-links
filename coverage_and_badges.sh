python -m pytest tests/ -v --cov=find_dead_links --cov-report=xml --junitxml=./report.xml
genbadge tests -i ./report.xml -s -o ./badges/tests.svg
genbadge coverage -i ./coverage.xml -s -o ./badges/coverage.svg
