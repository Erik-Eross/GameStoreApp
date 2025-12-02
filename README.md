**Game Store Web Application**
A cloud-integrated game store web application built with Flask, Google Cloud SQL, MongoDB Atlas, and Google Cloud Functions.

This project demonstrates a modern cloud-based architecture suitable for enterprise-level applications.

**User Authentication**  
- Register, Login, Logout  
- Password hashing (Werkzeug)  
- Session-based authentication  

- Game Catalogue (Cloud SQL)
- Games stored in MySQL (Cloud SQL)
- Thumbnail images saved locally
- Modern catalogue UI

**Game Detail Page** 
- Large thumbnail
- Title, platform, description
- Price + Buy Now button
- Reviews pulled from MongoDB Atlas  
- Logged-in users can add reviews  

### ✔ Reviews (MongoDB Atlas)  
MongoDB is used to store dynamic user-generated reviews.

**Cloud Function Purpose**
featured-games: Loads featured game data from Google Cloud Storage,
top-reviews: Returns the latest reviews from MongoDB,
mesh-service:	Aggregates both functions into a single REST API.

Flask now calls one endpoint for simplicity and performance.

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
```
