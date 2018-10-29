import React, { Component } from 'react';
import {FinancialData} from '../Financial/Financial';

export default class PaysReport extends Component {

    constructor() {
        super();
        this.state = {"financial_data": []};
    }

    componentDidMount() {
        // TODO: Make it so a user can retrieve other employee payment records
        fetch(`http://localhost:5000/payments?employee_id=1`,
        {
			method: 'GET',
			headers: {
				'Authorization': `Bearer ${localStorage.getItem('token')}`
			}
		})
        .then((response) => response.json())
        .then((data) => {
            this.setState({'financial_data': JSON.parse(data)});
        })
        .catch((err) => {
            console.error(err);
        })
    }

    render() {
        return (
            <div className="container">
                <div id="pays-report" className="dashboard-content">
                    <div className="content-header">
						<h3>
							Payment Reports
						</h3>
					</div>
                    <div className="financial-information">
                        {<FinancialData financial_data={this.state.financial_data} />}
                    </div>
                </div>
            </div>
        );
    }
}