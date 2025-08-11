<h1 style="
    color: white;
    font-family: Arial, sans-serif;
    font-size: 48px;
    text-decoration: underline;
    font-weight: normal;
    align: center;
">
    UnifyU
</h1>

<h4 align="center">A web portal for student services.</h4>

---

# Installation

In order to clone the repository paste the below given link in your github
```sh
https://github.com/izack05/UnifyU_project_Group07.git 
```

>now open a terminal in github by pressing 
for windows --> ctrl + shift + `
for mac --> control + `

>in the cmd/terminal type the below commands in order to:
1. create a virtual environment
2. activate the virtual environment
3. install the required libraries for the project
4. 

(copy and paste each command one by one)

for windows:
```sh
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

for mac:
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

> afterwards, in your project folder scope create a new file names sk.py and set a variable secret_key = "what i provide in discord"
---

# Running the project
> in order to run the project
- open cmd in vscode
- type in the below command
```sh
python ./app.py
```

--- 
# Important instructions
1. make sure to implement the below codes in your html files body tag
```sh
{% extends "layout/base.html" %}
{% block content %}
{% endblock %} 
```
where you place your actual html things between the block content and endblock tags

2. in app.py under route decorators please put these login required decorators 
```sh
@app.route('/url')    # can be your route
@login_required
def function():   # can be your function
  pass
```