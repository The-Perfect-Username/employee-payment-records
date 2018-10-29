import React, {Component} from 'react';
import { FinancialData } from '../Financial/Financial';

class Employee extends Component {

	constructor(props) {
		super(props);
		this.state = {financial_data: [], show_financial_data: false, show_employee_data: false};
		this.getFinancialData = this.getFinancialData.bind(this);
		this.showFinancialData = this.showFinancialData.bind(this);
		this.showEmployeeData = this.showEmployeeData.bind(this);
	}


	showEmployeeData() {
		this.setState({
			show_employee_data: !this.state.show_employee_data,
			show_financial_data: false,
		});
	}

	showFinancialData(employee_id) {
		this.setState({
			show_financial_data: !this.state.show_financial_data,
			show_employee_data: false
		});
		if (this.state.financial_data.length === 0)
			this.getFinancialData(employee_id);
	}

	getFinancialData(employee_id) {
		fetch(`http://localhost:5000/employees/${employee_id}`,
		{
			method: 'GET',
			headers: {
				'Authorization': `Bearer ${localStorage.getItem('token')}`
			}
		})
		.then((response) => response.json())
		.then((data) => {
			this.setState({financial_data: JSON.parse(data)});
		}).catch((err) => {
			console.log(err);
		})
	}

	render() {
		return (
			<div className="employee">
				<div className="employee-name">
					<span>
						{`${this.props.employee_data.first_name} ${this.props.employee_data.last_name}`}
					</span>
				</div>
				<div className="employee-controls">
					<a onClick={this.showEmployeeData}>
						Employee Information
					</a>
					<a onClick={() => {this.showFinancialData(this.props.employee_data.id)}}>
						Financial Year Records
					</a>
				</div>
				<div className="employee-information">
					{this.state.show_employee_data &&
						<EmployeeData employee_data={this.props.employee_data} />
					}
					{this.state.show_financial_data &&
						<FinancialData financial_data={this.state.financial_data} />
					}
					
				</div>
			</div>
		);
	};
}

function EmployeeData(props) {
	return (
		<div className="employee-data">
			<InformationRow label="ID" value={props.employee_data.id} />
			<InformationRow label="DOB" value={props.employee_data.date_of_birth} />
			<InformationRow label="Terminated" value={props.employee_data.is_terminated === "0" ? "No" : "Yes"} />
			<InformationRow label="Address 1" value={props.employee_data.address1} />
			<InformationRow label="Address 2" value={props.employee_data.address2} />
			<InformationRow label="City" value={props.employee_data.city} />
			<InformationRow label="State" value={props.employee_data.state} />
			<InformationRow label="Postcode" value={props.employee_data.postcode} />
			<InformationRow label="Country" value={props.employee_data.country} />
		</div>
	);
}

function InformationRow(props) {
	return (
		<div className="information-row">
			<div className="label">{props.label}</div>
			<div className="value">{props.value}</div>
		</div>
	)
}

export default Employee;