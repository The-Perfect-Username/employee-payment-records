import React, { Component } from 'react';
import Employee from './Employee'

class EmployeeReport extends Component {

	constructor(props) {
		super(props);
		this.state = {employee_data: []};
	}

	componentDidMount() {
		fetch("http://localhost:5000/employees")
        .then((response) => response.json())
        .then((data) => {
			this.setState({employee_data: JSON.parse(data)});
		}).catch((err) => {
			console.log(err);
		})
	}

	render() {

        const employees = [];
        
        for (var i in this.state.employee_data) {
			employees.push(<Employee key={i} employee_data={this.state.employee_data[i]} />)	
		}

		return (
			<div className="container" >
				<div id="employee-reports" className="dashboard-content">
					<div className="content-header">
						<h3>
							Employee Reports
						</h3>
					</div>
					{employees}
				</div>
			</div>
		);
	};
}

export default EmployeeReport;