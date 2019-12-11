import React, { Component } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";

import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import UserStatus from "./components/UserStatus";

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      title: "Template"
    };
    this.addUser = this.addUser.bind(this);
    this.handleLoginFormSubmit = this.handleLoginFormSubmit.bind(this);
    this.handleRegisterFormSubmit = this.handleRegisterFormSubmit.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
    this.isAuthenticated = this.isAuthenticated.bind(this);
  }
  componentDidMount() {
    this.getUsers();
  }
  addUser(data) {
    axios
      .post(`${process.env.REACT_APP_BACKEND_SERVICE_URL}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  }
  getUsers() {
    axios
      .get(`${process.env.REACT_APP_BACKEND_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data.data.users });
      })
      .catch(err => {
        console.log(err);
      });
  }
  handleLoginFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE_URL}/auth/login`;
    axios
      .post(url, data)
      .then(res => {
        window.localStorage.setItem("authToken", res.data.auth_token);
        setTimeout(
          function() {
            this.getUsers();
          }.bind(this),
          300
        );
      })
      .catch(err => {
        console.log(err);
      });
  }
  handleRegisterFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE_URL}/auth/register`;
    axios
      .post(url, data)
      .then(res => {
        window.localStorage.setItem("authToken", res.data.auth_token);
        setTimeout(
          function() {
            this.getUsers();
          }.bind(this),
          300
        );
      })
      .catch(err => {
        console.log(err);
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
        url: `${process.env.REACT_APP_BACKEND_SERVICE_URL}/auth/status`,
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
                        <h1 className="title is-1">Users</h1>
                        <hr />
                        <br />
                        <AddUser addUser={this.addUser} />
                        <br />
                        <br />
                        <UsersList users={this.state.users} />
                      </div>
                    )}
                  />
                  <Route exact path="/about" component={About} />
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
                  <Route
                    exact
                    path="/status"
                    render={() => (
                      <UserStatus isAuthenticated={this.isAuthenticated} />
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
