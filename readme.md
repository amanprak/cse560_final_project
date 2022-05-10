# SETUP Database-

1. Open postgres using below command

> sudo -i -u postgres

2. Find the Convenient SQL Script and Import the Database with normalized tables and preprocessed data using below command

> psql -h localhost -d ecom -U postgres -f databaseSQLScript.sql 

3. Database Successfully Imported

# RUN E-COMM WEBAPP

1.	Open VS code and open the project directory.
2.	Click on main.py and click on the top left to run the code.
 
3.	A terminal will pop in the below just run the below command to install all the requirements.

pip install -r requirement.txt
or
pip3 install -r requirement.txt

4.	After installing all the requirements, if you used pip just write in the terminal the below code:
python main.py
If you used pip3 while installing all the requirements, then use the below code in the terminal:
python3 main.py

5.	Click ctrl + left mouse on the link (http://127.0.0.1:5000/ ) to redirect to the website.