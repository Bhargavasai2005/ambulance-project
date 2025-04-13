import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [nearestAmbulance, setNearestAmbulance] = useState(null);
  const [route, setRoute] = useState(null);
  const [trafficSignals, setTrafficSignals] = useState(null);
  const [hospitalBooking, setHospitalBooking] = useState(null);

  const fetchNearestAmbulance = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/get_nearest_ambulance/', {
        location: [12.9716, 77.5946]
      });
      setNearestAmbulance(response.data);
    } catch (error) {
      console.error('Error fetching nearest ambulance:', error);
    }
  };

  const fetchRoute = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/get_optimized_ambulance_route/', {
        location: [12.9352, 77.6245]
      });
      setRoute(response.data.optimized_route);
    } catch (error) {
      console.error('Error fetching route:', error);
    }
  };

  const fetchTrafficSignals = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/get_traffic_signal_status/');
      setTrafficSignals(response.data.traffic_signals);
    } catch (error) {
      console.error('Error fetching traffic signals:', error);
    }
  };

  const bookHospital = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/book_hospital/', {
        location: [12.9716, 77.5946]
      });
      setHospitalBooking(response.data);
    } catch (error) {
      console.error('Error booking hospital:', error);
    }
  };

  useEffect(() => {
    fetchNearestAmbulance();
    fetchRoute();
    fetchTrafficSignals();
    bookHospital();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Ambulance Dashboard</h1>
      {hospitalBooking && (
        <div>
          <h2>Hospital Booking</h2>
          <p><strong>Message:</strong> {hospitalBooking.message}</p>
          <p><strong>Location:</strong> {hospitalBooking.location.join(', ')}</p>
          <p><strong>Remaining Beds:</strong> {hospitalBooking.remaining_beds}</p>
        </div>
      )}
      {nearestAmbulance && (
        <div>
          <h2>Nearest Ambulance</h2>
          <p><strong>Ambulance:</strong> {nearestAmbulance.nearest_ambulance}</p>
          <p><strong>Location:</strong> {nearestAmbulance.location.join(', ')}</p>
        </div>
      )}
      {route && (
        <div>
          <h2>Optimized Route</h2>
          <p><strong>Ambulance:</strong> {route.ambulance}</p>
          <p><strong>Start:</strong> {route.start.join(', ')}</p>
          <p><strong>Destination:</strong> {route.destination.join(', ')}</p>
        </div>
      )}
      {trafficSignals && (
        <div>
          <h2>Traffic Signals</h2>
          <ul>
            {Object.entries(trafficSignals).map(([id, data]) => (
              <li key={id}>
                {id}: {data.status} (Location: {data.location.join(', ')})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;