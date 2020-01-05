# Custom Job Search

[Custom Job Search](https://custom-job-search.herokuapp.com/) is a web application to search for jobs. It aims to **minimize the browse time on job search sites as much as possible**. The backend service is written by **Flask (Python)**, and the frontend service is written by **React JS (JavaScript)**.

## Demo

![Custom Job Search Demo](demo/demo.gif)

## Prerequisites

1. Create [Docker ID](https://hub.docker.com/signup)
2. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
3. Run & Login [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Run The Application

1. ```(custom-job-search)$ export REACT_APP_BACKEND_SERVICE=http://localhost:3007  # you can change the port number what you want in docker-compose.yml```
2. ```(custom-job-search)$ docker-compose up -d```

## Test The Application

1. ```(custom-job-search)$ docker-compose exec backend pytest "project/tests" -p no:warnings --cov="project"```
2. ```(custom-job-search)$ docker-compose exec frontend react-scripts test --coverage```

## Task Lists

- [x] Implemented the application and separated the backend and frontend services as microservices.
- [x] Tested each component.
- [x] Dockerized the application.
- [x] Deployed the application to [Heroku](https://custom-job-search.herokuapp.com/).
- [x] Searched jobs on [Indeed](https://www.indeed.com/). Will add more job search sites.
- [ ] Integrated the search functionality with logined users.
- [ ] Set up Continuous Integration / Continuous Deployment (CI/CD).
- [ ] Deployed the application to Amazon Web Services (AWS).

## Study Materials That I Used To Develop The Application
- [Flask](http://flask.palletsprojects.com/en/1.1.x/)
- [React JS](https://reactjs.org/)
- [Docker](https://www.docker.com/)
- [Heroku](https://heroku.com/)
- [Testdriven](https://testdriven.io/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
