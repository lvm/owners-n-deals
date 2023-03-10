import React, { useState, useCallback, useEffect } from 'react';

function TokenRefresh({ props }) {
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(null);

  const refreshAccessToken = useCallback(async () => {
    try {
      const response = await fetch(props.oauthRefreshToken, {method: 'POST'}, props.config.API_TIMEOUT);

      if (!response.ok) { throw new Error(`HTTP ${response.status} - ${response.statusText}`); }
      else { console.log("Token refreshed!"); }

      setError(null);
      setLastRefreshed(new Date());
    } catch (error) {
      setError(error.message);
    }
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (!lastRefreshed || Date.now() - lastRefreshed.getTime() >= 60 * 1000) {
        refreshAccessToken();
      }
    }, 30 * 1000);

    return () => clearInterval(intervalId);
  }, [lastRefreshed, refreshAccessToken]);

  return (
    <div>
      {error && <div>Error obtaining a new HubSpot Token: {error}</div>}
      {lastRefreshed && (
        <div>
          Last refreshed: {lastRefreshed.toString()} 
        </div>
      )}
    </div>
  );
}

export default TokenRefresh;
// import React, { useState, useCallback, useEffect } from 'react';

// function TokenRefresh({ props }) {
//   const [error, setError] = useState(null);

//   const refreshAccessToken = useCallback(async () => {
//     try {
//       const response = await fetch(props.oauthRefreshToken, {method: 'POST'}, props.config.API_TIMEOUT);

//       if (!response.ok) { throw new Error(`HTTP ${response.status} - ${response.statusText}`); }
//       else { console.log("Token refreshed!"); }

//       setError(null);
//     } catch (error) {
//       setError(error.message);
//     }
//   }, []);

//   useEffect(() => {
//     const intervalId = setInterval(() => {
//       refreshAccessToken();
//     }, 60 * 1000);

//     return () => clearInterval(intervalId);
//   }, [refreshAccessToken]);

//   return (
//     <div>
//       {error && <div>Error obtaining a new HubSpot Token: {error}</div>}
//     </div>
//   );
// }

// export default TokenRefresh;