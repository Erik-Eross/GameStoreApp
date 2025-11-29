**Game Store Web Application**
A cloud-integrated game store web application built with Flask, Google Cloud SQL, MongoDB Atlas, and Google Cloud Functions.

This project demonstrates a modern cloud-based architecture suitable for enterprise-level applications.


**Features:**
- User Authentication (Register, Login, Logout).

- Secure password hashing (Werkzeug).

- Session-based authentication.

- MySQL (Google Cloud SQL).

- Game titles, platforms, prices, descriptions.

- Reviews (using MongoDB linked to individual games).

- Cloud Functions Integration.


**Cloud Function Purpose**
featured-games: Loads featured game data from Google Cloud Storage,
top-reviews: Returns the latest reviews from MongoDB,
mesh-service: Aggregates both functions into a single REST API.

Flask now calls one endpoint for simplicity and performance.


**Architecture Overview**

Flask (Python) – Web framework,

Google Cloud SQL (MySQL) – Relational data,

MongoDB Atlas – Review storage,

Google Cloud Functions – Serverless logic,

Google Cloud Storage – Featured games JSON,

Tailwind CSS – Frontend styling.


**In-Depth Diagram of the Architecture**

```
                +---------------------------+
                |     Mesh Service API      |
                |       (Cloud Function)    |
                +-------------+-------------+
                              |
                +-------------+-------------+
                |                           |
    +------------------------+   +------------------------+
    |    featured-games      |   |      top-reviews       |
    |    Cloud Function      |   |     Cloud Function     |
    +------------------------+   +------------------------+

                      ↓ Combined JSON

                +---------------------------+
                |         Flask App         |
                |   User Auth, Templates    |
                +-------------+-------------+
                              |
                +-------------+-------------+
                |      Google Cloud SQL     |
                +---------------------------+
                |       MongoDB Atlas       |
                +---------------------------+
```


**Project Structure**

```
GameStoreApp/
    main.py
    mongoDBTest.py
    requirements.txt
    .gitignore
    app.yaml
    cloud_functions/
        featured-games/
        mesh-service/
        top-reviews/
    templates/
        404.html
        about.html
        base.html
        game_detail.html
        home.html
        login.html
        register.html
        submitted_account.html
    static/
        css/custom.css
        img/image_placeholder.png
```
