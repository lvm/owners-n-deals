import React from 'react';
import Form from '../components/Deals/Form';
import TokenRefresh from '../components/TokenRefresh';
import config from '../config/config';
import "../App.css";


const App = () => {

  const props = {
    "dealsEndpoint": window.__APP_DATA__.dealsEndpoint,
    "oauthRefreshToken": window.__APP_DATA__.oauthRefreshToken,
    "config": config,
  }

  return (
    <div>
      <Form props={props} />
      <TokenRefresh props={props} />
    </div>
  );
}


export default App;