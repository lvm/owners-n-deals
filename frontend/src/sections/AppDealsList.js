import React, { useState, useEffect } from 'react';
import Table from '../components/Deals/Table';
import TokenRefresh from '../components/TokenRefresh';
import fetchApi from '../utils/http';
import config from '../config/config';
import "../App.css";

const App = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const dealsEndpoint = window.__APP_DATA__.dealsEndpoint;
  const tokenRefreshProps = {
    "oauthRefreshToken": window.__APP_DATA__.oauthRefreshToken,
    "config": config,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const newData = await fetchApi(dealsEndpoint, {method: 'GET'}, config.API_TIMEOUT);
        setData([...data, ...newData.results]);
      } catch (error) {
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
  <div className="flex flex-col">
    <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div className="inline-block min-w-full py-2 sm:px-6 lg:px-8">
        <div className="overflow-hidden">
          {loading && <p>Loading...</p>}
          {error && <p>Error fetching data.</p>}
          {!loading && !error && <Table items={data} />}
        </div>
      </div>
    </div>
    <TokenRefresh props={tokenRefreshProps} />
  </div>
  );
};


export default App;