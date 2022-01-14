## SociaBook - A Social Media Application

A social media handle where users can post comments, send text & audio messages and maintain a follower list as well as who follows. The users can like, comment and share posts too. 

## Features

### User Authentication
<ul>
  <li>The user can Sign In, Sign Up, Logout.</li>
  <li>The user can recover password if forgot.</li>
</ul>

### Feed
<ul>
  <li>The user can view the post.</li>
  <li>The user can like, comment and share the post.</li>
</ul>

### Social
<ul>
  <li>The user can post pictures.</li>
  <li>The user can search, follow and unfollow other users.</li>
  <li>The user can see the followers and following list of other users.</li>
</ul>

### Profile
<ul>
  <li>The user can change their profile details.</li>
  <li>The user can change their password.</li>
  <li>The user can edit and delete their post.</li>
</ul>

### Messaging
<ul>
  <li>The user can see whether his friend is online or offline.</li>
  <li>The user can see the last seen of the friend.</li>
  <li>The user can send & receive text and multimedia messages.</li>
  <li>The user can see the time and date of the messages.</li>
</ul>


## Setup

Cloning the Repository
```
$ git clone https://github.com/Rishabh7896/SociaBook
$ cd SociaBook
```

Creating Virtual Environment
```
$ python -m venv myenv
```

Activating the Environment
```
$ myenv\Scripts\activate
```

Installing Dependencies
```
$ pip install -r requirements.txt
```

Migrating the project
```
$ python manage.py makemigration
$ python manage.py migrate
```

Runing the project on your local machine
```
$ python manage.py runserver
```

## User Login
Open <a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a> on your browser.
```
username: abhi
password: abhi
```

## Admin Login

Open <a href="http://127.0.0.1:8000/admin">http://127.0.0.1:8000/admin</a> on your browser.
```
username: admin
password: admin
```
