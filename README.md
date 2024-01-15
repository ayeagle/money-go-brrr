# money-go-brrr

Script ecosystem for trading on various signals.

Script is run once a day before opening if trading is allowed that day.

Ensure python3.11.4 is installed

1. Navigate to where you want your project to live e.g.
   (Optional)

```shell
cd desktop && mkdir projects && cd projects
```

2. Clone the repo

```shell
git clone git@github.com:ayeagle/money-go-brrr.git
```

3. Open project

```shell
cd money-go-brrr
```

May need to use "python3" instead of "python" for following commands depending on setup

4. Create new venv for script development

```shell
python -m venv money_venv
```

5. Activate venv

```shell
source money_venv/bin/activate
```

6. Install dependencies for venv

```shell
pip install -r requirements.txt
```

7. Create .env for api keys

```shell
python script_setup.py
```

8. Create working branch

```shell
git branch main_wip
```

```shell
git checkout main_wip
```

9. Run to get started

```shell
python script_controller.py help
```

<strong>Available script run modes:</strong>

<p>
<code style="color: green">test</code> [default] => runs script in paper trading, skipping certain account checks<br>
<code style="color: green">full_test</code> => runs script in paper trading, including account checks<br>
<code style="color: green">prod</code> => runs script with real trading account<br>
<code style="color: green">prod_dangerous</code> => runs script with real money and trading authorization<br>
<code style="color: green">download</code> => runs script with paper creds and initiates a download of the data<br>
<code style="color: green">help</code> => shows the help command<br>
</p>

To end virtual env session

```shell
deactivate
```

Hehe
