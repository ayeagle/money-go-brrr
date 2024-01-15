# money-go-brrr

Script ecosystem for trading on SPY signals.

Script is run once a day before opening if trading is allowed that day.


Ensure python3.11.4 is installed


clone the repo

navigate to repo

may need to use "python3" instead of "python" for following commands depending on setup

Create new venv for script development
$ ```python -m venv money_venv```

$ ```shell source money_venv/bin/activate```

Install dependencies for venv
$ 
```shell
pip install -r requirements.txt
```

Create working branch
$ ```shell
git branch main_wip
```
$ ```shell
git checkout main_wip
```

Run to get started
$ ```shell
python script_controller.py help
```


To end virtual env session
$ ```shell
deactivate
```


Hehe