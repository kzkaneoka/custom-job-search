import React, { Component } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";
import Modal from "react-modal";

import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import UserStatus from "./components/UserStatus";
import Message from "./components/Message";
import SearchForm from "./components/SearchForm";

const modalStyles = {
  content: {
    top: "0",
    left: "0",
    right: "0",
    bottom: "0",
    border: 0,
    background: "transparent"
  }
};

Modal.setAppElement(document.getElementById("root"));

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      title: "Template",
      messageType: null,
      messageText: null,
      showModal: false
    };
    this.addUser = this.addUser.bind(this);
    this.handleRegisterFormSubmit = this.handleRegisterFormSubmit.bind(this);
    this.handleLoginFormSubmit = this.handleLoginFormSubmit.bind(this);
    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
    this.handleSearchFormSubmit = this.handleSearchFormSubmit.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
    this.isAuthenticated = this.isAuthenticated.bind(this);
    this.removeMessage = this.removeMessage.bind(this);
    this.removeUser = this.removeUser.bind(this);
  }
  componentDidMount() {
    this.getUsers();
    this.createMessage();
  }
  addUser(data) {
    axios
      .post(`${process.env.REACT_APP_BACKEND_SERVICE}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
        this.handleCloseModal();
        this.createMessage("success", "User added.");
      })
      .catch(err => {
        console.log(err);
        this.handleCloseModal();
        this.createMessage("danger", "That user already exists.");
      });
  }
  createMessage(type, text) {
    this.setState({
      messageType: type,
      messageText: text
    });
    setTimeout(() => {
      this.removeMessage();
    }, 3000);
  }
  getUsers() {
    axios
      .get(`${process.env.REACT_APP_BACKEND_SERVICE}/users`)
      .then(res => {
        this.setState({ users: res.data.data.users });
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
  handleOpenModal() {
    this.setState({ showModal: true });
  }
  handleCloseModal() {
    this.setState({ showModal: false });
  }
  handleSearchFormSubmit(data) {
    const url = `${process.env.REACT_APP_BACKEND_SERVICE}/search`;
    axios
      .post(url, data)
      .then(res => {
        console.log(res.data);
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
  removeMessage() {
    this.setState({
      messageType: null,
      messageText: null
    });
  }
  removeUser(user_id) {
    axios
      .delete(`${process.env.REACT_APP_BACKEND_SERVICE}/users/${user_id}`)
      .then(res => {
        this.getUsers();
        this.createMessage("success", "User removed.");
      })
      .catch(err => {
        console.log(err);
        this.createMessage("danger", "Something went wrong.");
      });
  }
  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
          logoutUser={this.logoutUser}
          isAuthenticated={this.isAuthenticated}
        />
        {this.state.messageType && this.state.messageText && (
          <Message
            messageType={this.state.messageType}
            messageText={this.state.messageText}
            removeMessage={this.removeMessage}
          />
        )}
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
                      <SearchForm
                        handleSearchFormSubmit={this.handleSearchFormSubmit}
                      />
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
