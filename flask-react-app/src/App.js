
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');

  const handleSignup = async () => {
    try {
      await axios.post('/signup', { username, password });
      console.log('Signup successful');
    } catch (error) {
      console.error('Signup error:', error.response.data);
    }
  };

  const handleLogin = async () => {
    try {
      await axios.post('/login', { username, password });
      console.log('Login successful');
    } catch (error) {
      console.error('Login error:', error.response.data);
    }
  };

  const handleMarkAttendance = async () => {
    try {
      await axios.post('/mark-attendance', { status });
      console.log('Attendance marked successfully');
    } catch (error) {
      console.error('Attendance marking error:', error.response.data);
    }
  };

  const handleViewAttendance = async () => {
    try {
      const response = await axios.get('/view-attendance');
      console.log('Attendance records:', response.data);
    } catch (error) {
      console.error('View attendance error:', error.response.data);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Attend-In</h1>

      <div style={styles.formContainer}>
        <h2 style={styles.sectionTitle}>Signup</h2>
        <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} style={styles.input} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} style={styles.input} />
        <button onClick={handleSignup} style={styles.button}>Sign Up</button>
      </div>

      <div style={styles.formContainer}>
        <h2 style={styles.sectionTitle}>Login</h2>
        <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} style={styles.input} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} style={styles.input} />
        <button onClick={handleLogin} style={styles.button}>Log In</button>
      </div>

      <div style={styles.formContainer}>
        <h2 style={styles.sectionTitle}>Mark Attendance</h2>
        <select onChange={(e) => setStatus(e.target.value)} style={styles.input}>
          <option value="Present">Present</option>
          <option value="Absent">Absent</option>
        </select>
        <button onClick={handleMarkAttendance} style={styles.button}>Mark Attendance</button>
      </div>

      <div style={styles.formContainer}>
        <h2 style={styles.sectionTitle}>View Attendance</h2>
        <button onClick={handleViewAttendance} style={styles.button}>View Attendance</button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: 'center',
    padding: '20px',
  },
  title: {
    fontSize: '24px',
    marginBottom: '20px',
  },
  formContainer: {
    maxWidth: '400px',
    margin: '0 auto',
    marginBottom: '20px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '5px',
    backgroundColor: '#f9f9f9',
  },
  sectionTitle: {
    fontSize: '18px',
    marginBottom: '10px',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    boxSizing: 'border-box',
  },
  button: {
    backgroundColor: '#4caf50',
    color: 'white',
    padding: '10px',
    cursor: 'pointer',
    width: '100%',
    border: 'none',
    borderRadius: '5px',
  },
};

export default App;
