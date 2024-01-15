# money-go-brrr

Script ecosystem for trading on SPY signals.

Script is run once a day before opening if trading is allowed that day.

Ensure python3.11.4 is installed

clone the repo

navigate to repo

may need to use "python3" instead of "python" for following commands depending on setup

Create new venv for script development

```shell
python -m venv money_venv
```

Activate venv

```shell
source money_venv/bin/activate
```

Install dependencies for venv

```shell
pip install -r requirements.txt
```

Create working branch

```shell
git branch main_wip
```

```shell
git checkout main_wip
```

Create .env for api keys

```shell
python script_setup.py
```

Run to get started

```shell
python script_controller.py help
```

'''
Available script run modes:
... {green('test')} [default] => runs script in paper trading, skipping certain account checks
... {green('full_test')} => runs script in paper trading, including account checks
... {green('prod')} => runs script with real trading account
... {green('prod_dangerous')} => runs script with real money and trading authorization
... {green('download')} => runs script with paper creds and initials a download of the data
... {green('help')} => shows help command
\033[0m
'''

To end virtual env session

```shell
deactivate
```

Hehe
