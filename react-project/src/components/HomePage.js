import React from 'react';

const HomePage = () => {
  return (
    <div className="home-page">
      <header>
        <h1>Mark Out V1</h1>
      </header>
      <main>
        <section>
          <h2>About Us</h2>
          <p>Search for any wrestler, match, promotion, venue, or event.</p>
        </section>
        <section>
          <h2>Services</h2>
          <p> This app pulls from The Internet Wrestling Database (http://www.profightdb.com/) to obtain up to date match information..</p>
        </section>
        {/* Add more sections as needed */}
      </main>
      <footer>
        <p>&copy; 2024 Your Company Name</p>
      </footer>
    </div>
  );
};

export default HomePage;
