PYTHONPATH="$PYTHONPATH:$(pwd)qleet/"

python -m mypy --install-types --non-interactive qleet/ --config-file=tests/_config/mypy.ini
python -m black qleet tests
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m pytest tests/
python -m pylint --rcfile tests/_config/.pylintrc --fail-under=10.0 qleet
