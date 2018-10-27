import React from 'react';

export function FinancialData(props) {
	const elements = [];
	for (let i in props.financial_data) {
		elements.push(<FinancialDataRow key={i} financial_data={props.financial_data[i]} />)
	}
	return (
		<div className="financial-data">
			<table>
				<thead>
					<tr>
						<th>Date</th>
						<th>Gross</th>
						<th>Tax</th>
					</tr>
				</thead>
				<tbody>
					{elements}
				</tbody>
			</table>
		</div>
	);
}

export function FinancialDataRow(props) {
	return (
		<tr>
			<td>{props.financial_data.date}</td>
			<td>{parseFloat(props.financial_data.gross).toFixed(2)}</td>
			<td>{parseFloat(props.financial_data.tax).toFixed(2)}</td>
		</tr>
	)
}