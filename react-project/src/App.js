import React from 'react';
import {
  WrestlerComponent,
  EventComponent,
  MatchComponent,
  TagTeamComponent,
  TitleComponent,
  VenueComponent,
  PromotionComponent,
  HomePage
} from './components'; // Update the path accordingly

const App = () => {
  return (
    <div className="app">
      <HomePage />
      {/* Use other components as needed */}
    </div>
  );
};

export default App;
