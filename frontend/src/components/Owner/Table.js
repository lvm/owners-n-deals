import React from 'react';
import TableTr from './TableTr';

const Table = ({ items }) => {
  return (
    <table className="table">
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
            </tr>
        </thead>
        <tbody>
            {items.map(item => (<TableTr key={item.id} item={item} />))}
        </tbody>
    </table>
  );
};

export default Table;