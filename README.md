## General info
Tax Forms script
	
## Technologies
Project is created with:
* requests
* bs4
* pylint
## Getting Started
Python Version - 3.7
Install project:
* mkdir tax_script - "tax_script" for example
* cd tax_script
* python -m venv myvenv - create virtual environment
* venv/Scripts/activate - for Windows
* source venv/bin/activate - for Linux
* git clone "repository"
* pip install -r requirements - installing all packages for project
* cd iris_gov_parse - open repository
## Script execution
the names of the forms that we want to get information about are separated by a space. 
Next, we see information about the received forms in json format. Enter the name of the desired date and the range of years
* python main.py Form1 Form2 Form3 - form name separated by space
