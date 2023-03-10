import React from 'react';
import TableTr from './TableTr';

const Table = ({ items }) => {
  return (
    <table className="table">
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Deal Name</th>
                <th scope="col">Amount</th>
                <th scope="col">Close Date</th>
            </tr>
        </thead>
        <tbody>
            {items.map(item => (<TableTr key={item.id} item={item} />))}
        </tbody>
    </table>
  );
};

export default Table;