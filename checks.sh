PYTHONPATH="$PYTHONPATH:$(pwd)qleet/"

python -m mypy --install-types --non-interactive qleet/ --config-file=tests/_config/mypy.ini
python -m black qleet tests
python -m pytest tests/
python -m pylint --rcfile tests/_config/.pylintrc --fail-under=10.0 qleet
