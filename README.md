# BlogBEE

A simple Blog Website which uses the Django Framework.



## Run Locally

1. To install my Project and Run it on your local machine, follow the stated instruction.
Make sure that your computer is has python3 installed (preferably a 3.10.x version)

2. Set an virtual environment in a desired directory on your local computer. 
To install a virtual environment on your local machine, follow the link provided below.

3. Activate Virtual Environment, and clone the repository.

```bash
  git clone https://github.com/sm-wyBme/BlogBEE.git
```
Move into the project directory
```bash
  cd BlogBEE
```
4. Install the dependencies on the requirements.txt file.

```bash
  pip install -r requirements.txt
```

5. The following commands are required to run the Project.

```bash
  python manage.py makemigrations
  python manage.py migrate
```
The above commands are required to make migrations(changes) into the database. This creates an sqlite3 database when run for the first time.

6. Create a superuser. This user will have admin proviledges on the application.

```bash
  python manage.py createsuperuser
```

7. Run the project locally using the following command. The website will be hosted on port 8000.
```bash
  python manage.py runserver
```


## Features

- Register a user
- Customise a blog
- Customise your profile
- Write your heart out
- Email Authentication for Forgot Password  


## Demo

Landing Page           |  Register A User
:-------------------------:|:-------------------------:
![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/home.png) | ![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/register.png) 
Write A Blog           |  View a Blog
![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/writeBlog.png) |   ![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/blog.png)  
Customise Profile |  Customise Profile
![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/profile.png) | ![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/crop.png) 


<!-- 
Welcome to BlogBEE

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/home.png)

Register a user

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/register.png)

Write a Blog

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/writeBlog.png)

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/blog.png)


Customise your Profile

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/profile.png)

![App Screenshot](https://github.com/sm-wyBme/BlogApp/blob/master/Screenshots/crop.png)
 -->


## Acknowledgements

This Project would not have been possible without proper research and proper guidance.

The best help one could ask for in this project, is the Offical Django documentation which in itself is a treasure trove.

Many a times I was confused about certain functionalities, and as beginner my greatest nightmares were bugs. This Websites takes inspirations from credible sources such as StackOverFlow, which helped a lot while debugging and understanding certain concepts.

The subreddit r/django was of great help too.




## Authors

- [@sm_wyBme](https://github.com/sm-wyBme)
