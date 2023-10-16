import React, { useState } from 'react';

function App() {
  const [bikeNumber, setBikeNumber] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create the JSON payload
    const payload = {
      line_items: [
        {
          "properties": [
            {
              name: 'Bike Number',
              value: bikeNumber,
            },
          ],
        },
      ],
    };

    // Send the JSON payload to your Flask backend
    fetch('/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Response from Flask backend:', data);
      })
      .catch((error) => {
        console.error('Error sending data to Flask backend:', error);
      });
  };

  return (
    <div className="App">
      <h1>Enter Bike Number</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Bike Number"
          value={bikeNumber}
          onChange={(e) => setBikeNumber(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
