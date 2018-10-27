import React, { Component } from 'react';

class LoginForm extends Component {

    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(e) {
        e.preventDefault();

        let form = e.target;
        let username = form.elements['username'].value;
        let password = form.elements['password'].value;

        if (!username) {
            let errorMessage = document.getElementById('error-message');
            errorMessage.textContent = "Please enter a username";
            return;
        }

        fetch('http://localhost:5000/login', {
            method: "POST",
            headers: {
                'Accept': 'application/json;charset=UTF-8',
                'Content-Type': 'application/json;charset=UTF-8',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        }).then((response) => {
            
            if (response.status === 401) {
                let errorMessage = document.getElementById('error-message');
                errorMessage.textContent = "Incorrect username/password combination";
            } 
            
            if (response.status === 403) {
                let errorMessage = document.getElementById('error-message');
                errorMessage.textContent = "Account is locked";
            }

            if (!response.ok) {
                throw new Error("An unkown error occured");
            }

            return response.json();
            
        }).then((data) => {
            let payload_data = JSON.parse(data);
            
            if (!('token' in payload_data)) {
                throw new Error("Token not found in payload");
            }
            
            if (!('username' in payload_data)) {
                throw new Error("Username not found in payload");
            }

            let token = payload_data.token;
            let username = payload_data.username;

            localStorage.setItem("token", token);
            localStorage.setItem("username", username)

            window.location.replace("http://localhost:3000")

        }).catch(function(error){
            console.error(error);
        })
    }

    render() {
        return (
            <form id="login-form" action="/login" method="post" onSubmit={this.handleSubmit}>
                <h2>Login</h2>
                <div className="form-group">
                    <label>Username</label>
                    <input className="form-control" name="username" />
                </div>
                <div className="form-group">
                    <label>Password</label>
                    <input className="form-control" name="password" />
                </div>
                <div className="form-group form-footer">
                    <button>Login</button>
                </div>
                <div id="error-message"></div>
            </form>
        )
    }
}

export default LoginForm;