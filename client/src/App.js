import React, { Component } from 'react';
import EmployeeReport from './Components/Employee/EmployeeReport';
import Login from './Components/Login/Login';
import ProtectedRoute from './Components/Authentication/ProtectedRoute';
import PaysReport from './Components/PaysReport/PaysReport';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

class App extends Component {

	render() {
		return (
			<div>
				{localStorage.getItem('token') &&
					<Header />
				}
				<main>
					<BrowserRouter>
						<Switch>
							<ProtectedRoute exact path='/' component={() => <div><EmployeeReport/><PaysReport/></div>} />
							<Route exact path='/login' component={Login} />
						</Switch>
					</BrowserRouter>
				</main>
			</div>
		);
	}
}

function Header() {
	return (
		<header>
            <div className="header-controls">
                <div>Logged in as <span id="username">{localStorage.getItem("username")}</span></div>
                <div>
                    <a id="logout" onClick={() => {
						localStorage.removeItem("username");
						localStorage.removeItem("token");
						window.location.replace("http://localhost:3000/login");
					}}>Logout</a>
                </div>
            </div>
        </header>
	);
}




export default App;
