import React from 'react';

const TableTr = ({ item }) => {
    if (!item) { return '' }
    else {
        return (
        <tr key={item.id} className="border-b dark:border-neutral-500">
            <td className="whitespace-nowrap px-6 py-4">{item.id}</td>
            <td className="whitespace-nowrap px-6 py-4">{item.properties.dealname}</td>
            <td className="whitespace-nowrap px-6 py-4">{item.properties.amount}</td>
            <td className="whitespace-nowrap px-6 py-4">{item.properties.closedate}</td>
        </tr>
        );
    }
};

export default TableTr;