# Shopping Ingredients 
    When user provides list of ingredients, application will show a receipe and missing ingredients for the reciepe. 
    If user likes the receipe and shopping list, application will provide list of shopping items and cost of the shopping list.

# Project Structure & Dependencies:
    [GIT Repo](https://github.com/vsakamuri/shopping-ingredient-app/).
    source code is present in src folder
    unit tests are in test folder
    project dependencies are in Pipfile. No need to install below dependencies. pipenv helps us with the same. 
        - Pillow - to display images on UI
        - pyinstaller - to create executable
        - python-decouple - to handle environment variables.
        - pipenv - create virtual running environment

    project need a .env file with is not included in the repo. please contact me so that I can provide the file. add the file under root directory.

# Developer Setup: 

* Install Python version 3.9 or update your python version in Pipfile. Python version should be > 3.5

* Add Python and Python Script folders to home path

* Download the code from GitHub

* Get the .env from app owner and add it to root folder

* Open the project root folder in command prompt 

* Run following command to create virtual running environment
>    python -m pip install pipenv

* Run following command to install dependencies in virtual environment
>    pipenv install --dev

* To run the application without creating executable 
>    pipenv run python src/shopping_app.py

* To run unit tests
>    pipenv run python -m unittest discover -s test -p "test_*.py"

* Run following command to create executable. It will create executable (shopping_app.exe) in dist folder. You can double click on the executable to run the application. 
>    pipenv run pyinstaller --onefile  src/shopping_app.py

 

