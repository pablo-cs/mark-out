import React, { useEffect, useState } from 'react';
import { getMatch } from '../services/api'; // Update the path as needed


const MatchDetails = () => {
  const [matchData, setMatchData] = useState(null);
  const matchId = 350; // Replace with the desired match ID

  useEffect(() => {
    const fetchMatchData = async () => {
      try {
        const data = await getMatch(matchId);
        setMatchData(data);
      } catch (error) {
        console.error('Error fetching match data:', error.message);
      }
    };

    fetchMatchData();
  }, [matchId]);

  // Display matchData in your component

  return (
    <div>
      {matchData ? (
        <div>
          <h2>{matchData.name}</h2>
          <p>Site ID: {matchData.site_id}</p>
          <p>Date: {matchData.date}</p>
          {matchData.img_src && (
            <img src={matchData.img_src} alt={matchData.name} />
          )}
        </div>
      ) : (
        <p>Loading match data...</p>
      )}
    </div>
  );
};

export default MatchDetails;
