<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="readme_src/little_blood.png" alt="Logo" width="80" height="80">
  </a>

<h2 align="center">My blood</h2>

  <p align="center">
    Web application for personal blood giving in a form of log book with possibility to check the current blood giving actions (e.g. away blood giving)
    <br />
    <br />
    <br />

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


### Built With

* [![Python][Python.org]][Python-url]
* [![Flask][Flask-badge]][Flask-url]
* [![PostgreSQL][PostgreSQL.org]][PostgreSQL-url]
* ![HTML]
* ![CSS]
* ![JS]
* [![Celery][Celery]][Celery-url]
* [![Redis][Redis.io]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Whole project is based on Python and Postgres database.

* **Python**
  * It is best to work within Python virtual environments - if you do NOT know how to setup a virtual environment, here is a [link](https://docs.python.org/3/library/venv.html) 😊
  * All prerequisite libraries used in Python are listed in [`requirements.txt`](https://github.com/mattix1710/app-sec-app/blob/main/requirements.txt) file.
    
    They are also listed below:

<center>

| Library              | Version       |
|----------------------|---------------|
| Python               | 3.12          |
| Flask                | 3.0.0         |
| psycopg              | 3.1.13        |
| psycopg[binary,pool] | 3.1.13, 3.2.0 |
| Flask-SQLAlchemy     | 3.1.1         |
| Flask-Session        | 0.5.0         |
| Flask-Bootstrap      | 3.3.7.1       |
| Flask-WTF            | 1.2.1         |
| Flask-Mail           | 0.9.1         |
| email-validator      | 2.1.0.post1   |
| bcrypt               | 4.0.1         |
| pycryptodome         | 3.19.0        |
| celery               | 5.3.6         |
| gevent               | 23.9.1        |
| redis                | 5.0.1         |

</center>

* **PostgreSQL**
  * e.g. running as *Docker container* - for this project [the official image](https://hub.docker.com/_/postgres) (provided by Docker) was chosen:

    [![postgres][Postgres-badge]][Postgres-docker-url] [![postgres-image-tag][Postgres-tag-badge]][Postgres-tag-url]

* **Redis** server
  * e.g. running as *Docker container* - for this project [the official image](https://hub.docker.com/_/redis) (provided by Docker) was chosen:
  
    [![redis][Redis-badge]][Redis-docker-url] [![redis-image-tag][Redis-tag-badge]][Redis-tag-url]

### Installation

🚧🚧🚧
> TODO: Installation description

1. Clone this repository and move to the project directory
2. Rename `template.env` to `.env` and add your data (ex: `mv template.env .env`)
    - MAIL_ADDRESS -- The email that will send password reset tokens
    - MAIL_PASSWORD -- The password for the email account
    - MAIL_SERVER -- The SMTP server address
    - MAIL_PORT -- The SMTP server port
3. Build the Docker Compose images
```
docker compose up --build
```
4. Access the server on `localhost:5000`.

You can terminate the application via the command line. After that you'll need to run `docker compose down`.

To restart the application you can run `docker compose up` without the **build** parameter.

#### Dockering Postgres

1. After installing [Docker Desktop](https://www.docker.com/get-started/) (e.g. on Windows) it is possible to run the app in the terminal:
```
docker run --name <container_name> -p 5432:5432 -e POSTGRES_PASSWORD=<password> -d <image_name>
```
* Where:
   * `container_name` - chosen container name, e.g. *postgres-db*
   * `password` - password used for logging into the server
   * `image_name` - source image used for creation of a container, e.g. postgres:11.22-bullseye
   * `-p` - flag used for port binding between host and working container
* ❕If there wasn't any image locally, docker app will download necessary files

2. After creating the container, the user can connect to the container via terminal:
```
docker exec -it <container_name> bash
```

3. In the internal terminal there is a possibility to connect to the database:
```
psql -h localhost -U <user_name>
```
* Default user is the superuser: **postgres**

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Starting the app
1. Run **Postgres** database server
   1. As Docker container via Desktop app:
      1. Proceed to `Containers` bookmark and click on `Run` button
   2. As Docker container via terminal:
      1. Run the following command:
          ```
          docker start <container_name>
          ```
2. Run **Redis** server
   1. As Docker container via Desktop app:
      1. Proceed to `Containers` bookmark and click on `Run` button
   2. As Docker container via terminal:
      1. Run the following command:
          ```
          docker start <container_name>
          ```
3. Run **Celery** handler
   1. As python application:
      ```
      python -m celery -A website_app worker -l info -P gevent
      ```
      1. `-l info` - run in verbose mode (display all logs)
      2. `-P gevent` - adding gevent pool for concurrency
4. Run **Flask** app
   1. Proceed to its main folder location
   2. Run the following command:
        ```
        flask --app website_app run --debug
        ```
        1. `--debug` option is optional - can be used for debug purposes (ALSO: allows to insert changes while running the server)

<!-- ROADMAP -->
## Roadmap

- [x] Create login/register forms
  - [x] Allow user authentication
  - [x] Create relational database in Postgres environment
- [x] Create users profile site
    - [ ] Add view of gave blood status
    - [ ] Add view for local blood giving actions
- [x] Connect to Postgres database
  - [x] Create SQL Alchemy connection
  - [ ] Create database models
- [x] Add concurrency for heavy tasks
  - [x] Implement Celery handler

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

No license chosen at the time of creating this repository!
<!-- Distributed under the MIT License. See `LICENSE.txt` for more information. -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Flask structure template](https://github.com/miguelgrinberg/flasky/tree/master)
* [Gitmoji - guide for commit messages](https://gitmoji.dev)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/tree/master)
* [Blood drop image](https://www.creativefabrica.com/pl/product/blood-donor-day-heart-and-blood-drop-22/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[PostgreSQL-url]: https://www.postgresql.org

[Flask-badge]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[PostgreSQL.org]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[HTML]: 	https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white
[CSS]: https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white
[JS]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black

[Celery]: https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4
[Celery-url]: https://docs.celeryq.dev/en/stable/
[Redis.io]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io

<!-- BADGES -->

[Postgres-badge]: https://img.shields.io/badge/image-postgres-blue
[Postgres-docker-url]: https://hub.docker.com/_/postgres

[Postgres-tag-badge]: https://img.shields.io/badge/TAG-11.22--bullseye-green
[Postgres-tag-url]: https://hub.docker.com/layers/library/postgres/11.22-bullseye/images/sha256-b3de7d483937f2df1106398290b35c1bc0ecc7508e2d4a2d72ae7a42c41a4b90?context=explore

[Redis-badge]: https://img.shields.io/badge/image-redis-blue
[Redis-docker-url]: https://hub.docker.com/_/redis

[Redis-tag-badge]: https://img.shields.io/badge/TAG-7.2.3-green
[Redis-tag-url]: https://hub.docker.com/layers/library/redis/7.2.3/images/sha256-d4c84914b872521e215f77d8845914c2268a96b0e35bacd5691e1f5e1f88b500?context=explore