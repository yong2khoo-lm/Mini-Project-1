# Step 1 - Create your environment

`conda create --name env1`
`conda activate env1`

# Step 2 - Install requirement

`pip install -r requirements.txt`

# Step 3 - Setup Database

`python manage.py makemigrations`
`python manage.py migrate`

# Step 4 - Start the app

`python manage.py runserver`
