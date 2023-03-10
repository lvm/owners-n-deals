import React, { useState } from 'react';
import fetchApi from '../../utils/http';

function Form({ props }) {
    const [amount, setAmount] = useState('');
    const [closedate, setClosedate] = useState('');
    const [dealname, setDealname] = useState('');
    const [dealstage, setDealstage] = useState('');
    const [hubspot_owner_id, setHubspot_owner_id] = useState('');
    const [pipeline, setPipeline] = useState('');
    const [isSent, setIsSent] = useState(false);
    const [error, setError] = useState('');
  
    const handleSubmit = async (event) => {
      event.preventDefault();
  
      try {
        const response = await fetchApi(
            props.dealsEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  amount,
                  closedate,
                  dealname,
                  dealstage,
                  hubspot_owner_id,
                  pipeline,
                }),
            }, 
            props.config.API_TIMEOUT
        );
        setIsSent(true);
        setError('');
      } catch (error) {
        console.log(error);
        setIsSent(false);
        setError('Failed to submit form');
      }
    };

    return (
      <>
        {isSent && <p>Form sent successfully!</p>}
        {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="amount">Amount</label>
          <input
            id="amount"
            type="text"
            value={amount}
            className="form-control" 
            onChange={(event) => setAmount(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="closedate">Close Date</label>
          <input
            id="closedate"
            type="date"
            value={closedate}
            className="form-control"
            onChange={(event) => setClosedate(`${event.target.value}T23:59:59.000Z`)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dealname">Deal Name</label>
          <input
            id="dealname"
            type="text"
            value={dealname}
            className="form-control"
            onChange={(event) => setDealname(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dealstage">Deal Stage</label>
          <input
            id="dealstage"
            type="text"
            value={dealstage}
            className="form-control"
            onChange={(event) => setDealstage(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="hubspot_owner_id">HubSpot Owner ID</label>
          <input
            id="hubspot_owner_id"
            type="text"
            value={hubspot_owner_id}
            className="form-control"
            onChange={(event) => setHubspot_owner_id(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="pipeline">Pipeline</label>
          <input
            id="pipeline"
            type="text"
            value={pipeline}
            className="form-control"
            onChange={(event) => setPipeline(event.target.value)}
          />
        </div>

        <button className="btn btn-dark" type="submit">Submit</button>
      </form>
      </>
    );
  }
  

export default Form;