import React, { useEffect, useState } from 'react';
import { getWrestler } from '../services/api'; // Update the path as needed


const WrestlerDetails = () => {
  const [wrestlerData, setWrestlerData] = useState(null);
  const wrestlerId = 350; // Replace with the desired wrestler ID

  useEffect(() => {
    const fetchWrestlerData = async () => {
      try {
        const data = await getWrestler(wrestlerId);
        setWrestlerData(data);
      } catch (error) {
        console.error('Error fetching wrestler data:', error.message);
      }
    };

    fetchWrestlerData();
  }, [wrestlerId]);

  // Display wrestlerData in your component

  return (
    <div>
      {wrestlerData ? (
        <div>
          <h2>{wrestlerData.name}</h2>
          <p>Site ID: {wrestlerData.site_id}</p>
          <p>Ring Names:</p>
          {wrestlerData.img_src && (
            <img src={wrestlerData.img_src} alt={wrestlerData.name} />
          )}
        </div>
      ) : (
        <p>Loading wrestler data...</p>
      )}
    </div>
  );
};

export default WrestlerDetails;
