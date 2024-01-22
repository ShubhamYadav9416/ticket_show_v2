# CINEPASS
## Ticket-show-app v2

A platform for admin to add diffrent movies in theaters and user can book ticket. 


### Features :

- Proper Authentication with Token Based Authentication - JWT

- Dynamic Pricing for ticket price.

- caching & cache expiry where required to increase the API performance.

#### ADMIN Features:

- One Admin is created when database is created.

- Admin can add movies and theater and alloacte them in many to many functionality with CRUD

- Admin can export csv file with details about theaters rating, booking, etc.

#### Normal USER Features:

- User can register and login and Use forget password functionality.

- User can book multiple tickets and manage them.

- User can rate Theater

- User can search for shows, venue, location.

- User can filter with rating.

#### BACKEND Features

- send daily reminders to user about movies and hto make bookings running every day..

- send a report as an email or PDF summarizing engagement for the month.

### Technologies Used : 

- VueJS - Used for User Interface 

- Flask RestFul API - Used to develop the RESTful API for the app

- Jinja2 - Used for rendering templates for sending emails

- Bootstrap - Used for HTML and CSS styling

- SQLite - Used for data storage

- Flask SQLAlchemy - Used as an ORM (Object-Relational Mapping) tool to interact with the database

- Flask Celery - Used for asynchronous background jobs at the backend.

- Flask Caching - Used for caching API outputs and increasing performance.

- Redis - Used as an in-memory database for the API cache and as a message broker for celery.


## Getting Started

### Prerequisites

- Python 3.x
- pip


### Installation

1. Clone the repo.

```
git clone https://github.com/ShubhamYadav9416/Ticket_show_app.git
```

2. Navigate to the root folder of the application.

3. Open two separate terminals and execute the following commands in each:

- To install Redis and run(after running each line close the terminal and run next line new terminal.)
  
```
Install flatpak: pip insatll flatpak
add flatpak repo: sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
Install RedisInsight using flatpak: flatpak install flathub com.redis.RedisInsight
REDIS SERVER : flatpak run com.redis.RedisInsight
```

-To install and run Mailhog

```
Install go: sudo apt-get -y install golang-go
install MailHog Using go: go install github.com/mailhog/MailHog@latest
MAILHOG : ~/go/bin/MailHog
```

4. Navigate to the backend folder and open three separate terminals. Execute the following commands in each:
   
- To run flask app(run virtual environment and pip install all dependencies)
  
```
BACKEND : python main.py
```

-To run celery

```
WORKERS : celery -A main:cel_app worker -l info
```

-To run celery beat

```
BEATS : celery -A main:cel_app beat --max-interval 1 -l info
```

5. Navigate to the frontend folder.

In the terminal, execute the following command:

```
npm run serve
```


### Contributing

Contributions are always welcome !!

If you would like to contribute to the project, please fork the repository and make a pull request.



### Support my work 
Do ⭐ the repository, if it inspired you, gave you ideas for your own portfolio or helped you in any way.


