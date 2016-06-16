type flake8 >/dev/null 2>&1 || { echo >&2 "Flake8 is not installed. Please run \"pip install flake8\" to install "; exit 1; }
flake8 --install-hook
git config flake8.complexity 100
git config flake8.strict true
