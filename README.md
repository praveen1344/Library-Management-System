# Library-Management-System
LMS

1. Clone Project
2. Ensure you have installed Python3, pip and vitualenv
3. Ensure Python3 is added to the PATH variable
4. Navigate into Server and run the following commands
    - python3 -m venv venv
    - source venv/bin/activate
5. Once the virtual environment is activate within the given folder, run the following command
    - pip install -r requirements.txt
6. Run Mysql DB instance locally or in a Docker container exposing port 3306
7. Run the following commands in MySQL(terminal):
    - UPDATE mysql.user SET Password = PASSWORD(‘your_password’) WHERE User = ‘your_user’;
    - FLUSH PRIVILEGES;
    - CREATE DATABASE test_db; Note: Ensure there is no existing DB by that name
6. If all dependencies are installed successfully in step 5, run 'flask run'
7. Server should be up and table is added to the 'test_db' database
