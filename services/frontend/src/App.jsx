import React, { Component } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";
import { CSVLink, CSVDownload } from "react-csv";

import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import SearchForm from "./components/SearchForm";
import JobsList from "./components/JobsList";

class App extends Component {
  constructor() {
    super();
    this.state = {
      title: "Custom Job Search",
      jobs: [],
      location: "",
      words: "",
      offset: -1
    };
    this.addUser = this.addUser.bind(this);
    this.handleSearchFormSubmit = this.handleSearchFormSubmit.bind(this);
    this.handleRegisterFormSubmit = this.handleRegisterFormSubmit.bind(this);
    this.handleLoginFormSubmit = this.handleLoginFormSubmit.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
    this.isAuthenticated = this.isAuthenticated.bind(this);
  }

  addUser(data) {
    axios
      .post(`${process.env.REACT_APP_BACKEND_SERVICE}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  }

  handleSearchFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE}/search`;
    data.offset = this.state.offset + 1;
    axios
      .post(url, data)
      .then(res => {
        this.setState({
          jobs: res.data.data.jobs,
          location: res.data.data.location,
          words: res.data.data.words,
          offset: data.offset
        });
      })
      .catch(err => {
        console.log(err);
      });
  }

  handleRegisterFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE}/auth/register`;
    axios
      .post(url, data)
      .then(res => {
        window.localStorage.setItem("authToken", res.data.auth_token);
        setTimeout(
          function() {
            this.getUsers();
            this.createMessage("success", "You have registered successfully.");
          }.bind(this),
          300
        );
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "That user already exists.");
      });
  }

  handleLoginFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE}/auth/login`;
    axios
      .post(url, data)
      .then(res => {
        window.localStorage.setItem("authToken", res.data.auth_token);
        setTimeout(
          function() {
            this.getUsers();
            this.createMessage("success", "You have logged in successfully.");
          }.bind(this),
          300
        );
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "Incorrect email and/or password.");
      });
  }

  logoutUser() {
    window.localStorage.removeItem("authToken");
    this.forceUpdate();
  }

  isAuthenticated() {
    const token = window.localStorage.getItem("authToken");
    if (token) {
      const options = {
        url: `${process.env.REACT_APP_BACKEND_SERVICE}/auth/status`,
        method: "get",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        }
      };
      return axios(options)
        .then(res => {
          return true;
        })
        .catch(err => {
          this.logoutUser();
          return false;
        });
    }
    return false;
  }

  isJobsEmpty() {
    return this.state.jobs.length == 0;
  }

  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
          logoutUser={this.logoutUser}
          isAuthenticated={this.isAuthenticated}
        />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Switch>
                  <Route
                    exact
                    path="/"
                    render={() => (
                      <div>
                        <SearchForm
                          handleSearchFormSubmit={this.handleSearchFormSubmit}
                        />
                        <JobsList jobs={this.state.jobs} />
                        {!this.isJobsEmpty() && (
                          <CSVLink
                            data={this.state.jobs}
                            filename={"searched-jobs.csv"}
                            className="btn btn-primary"
                          >
                            Download Jobs as CSV file
                          </CSVLink>
                        )}
                      </div>
                    )}
                  />
                  <Route
                    exact
                    path="/register"
                    render={() => (
                      <RegisterForm
                        handleRegisterFormSubmit={this.handleRegisterFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    exact
                    path="/login"
                    render={() => (
                      <LoginForm
                        handleLoginFormSubmit={this.handleLoginFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
