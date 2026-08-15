import React, { useState, useEffect } from 'react';
import api from './api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Overview / PR stats
  const [stats, setStats] = useState(null);

  // Workout state
  const [sessions, setSessions] = useState([]);
  const [editingSessionId, setEditingSessionId] = useState(null); // Track if editing an existing session
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');
  const [exercises, setExercises] = useState([
    { name: 'Bench Press', sets: 3, reps: 10, weight: 60 }
  ]);

  // Fetch past sessions
  const fetchSessions = async () => {
    try {
      const res = await api.get('sessions/');
      setSessions(res.data);
    } catch (err) {
      console.error('Failed to load workouts:', err);
    }
  };

  // Fetch summary & PR stats
  const fetchStats = async () => {
    try {
      const res = await api.get('sessions/summary_stats/');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  useEffect(() => {
    if (token) {
      fetchSessions();
      fetchStats();
    }
  }, [token]);

  // Handle Login & Registration
  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    const endpoint = isRegisterMode ? 'register/' : 'login/';
    try {
      const res = await api.post(endpoint, { username, password });
      const userToken = res.data.token;
      localStorage.setItem('token', userToken);
      setToken(userToken);
      setUsername('');
      setPassword('');
    } catch (err) {
      const msg = err.response?.data?.error || 'Authentication failed. Please check your credentials.';
      alert(msg);
    }
  };

  // Handle Logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken('');
    setSessions([]);
    setStats(null);
    cancelEdit();
  };

  // Exercise row management
  const addExerciseRow = () => {
    setExercises([...exercises, { name: '', sets: 3, reps: 10, weight: 0 }]);
  };

  const updateExercise = (index, field, value) => {
    const updated = [...exercises];
    updated[index][field] = value;
    setExercises(updated);
  };

  const removeExerciseRow = (index) => {
    setExercises(exercises.filter((_, i) => i !== index));
  };

  // Cancel edit mode and reset the form
  const cancelEdit = () => {
    setEditingSessionId(null);
    setDate(new Date().toISOString().split('T')[0]);
    setNotes('');
    setExercises([{ name: 'Bench Press', sets: 3, reps: 10, weight: 60 }]);
  };

  // Load an existing session into the form for editing
  const startEditSession = (session) => {
    setEditingSessionId(session.id);
    setDate(session.date);
    setNotes(session.notes || '');
    setExercises(
      session.exercises.length > 0
        ? session.exercises.map((ex) => ({
            name: ex.name,
            sets: ex.sets,
            reps: ex.reps,
            weight: ex.weight
          }))
        : [{ name: '', sets: 3, reps: 10, weight: 0 }]
    );
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Save Workout (Handles both POST for new sessions and PUT for edits)
  const handleSaveWorkout = async (e) => {
    e.preventDefault();
    try {
      if (editingSessionId) {
        // Update existing session
        await api.put(`sessions/${editingSessionId}/`, { date, notes, exercises });
      } else {
        // Create new session
        await api.post('sessions/', { date, notes, exercises });
      }
      cancelEdit();
      fetchSessions();
      fetchStats();
    } catch (err) {
      alert('Failed to save workout session.');
    }
  };

  // Delete Workout Session
  const handleDeleteSession = async (id) => {
    if (window.confirm('Are you sure you want to delete this workout session?')) {
      try {
        await api.delete(`sessions/${id}/`);
        if (editingSessionId === id) {
          cancelEdit();
        }
        fetchSessions();
        fetchStats();
      } catch (err) {
        alert('Failed to delete workout session.');
      }
    }
  };

  // 1. Authentication Screen
  if (!token) {
    return (
      <div style={{ maxWidth: '400px', margin: '4rem auto', fontFamily: 'sans-serif', padding: '2rem', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>{isRegisterMode ? 'Sign Up' : 'Gym Logger - Login'}</h2>
        <form onSubmit={handleAuthSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ padding: '8px' }}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ padding: '8px' }}
          />
          <button type="submit" style={{ padding: '10px', cursor: 'pointer', background: '#007bff', color: '#fff', border: 'none', borderRadius: '4px' }}>
            {isRegisterMode ? 'Create Account' : 'Log In'}
          </button>
        </form>
        <p style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.9rem' }}>
          {isRegisterMode ? 'Already have an account? ' : "Don't have an account? "}
          <button
            type="button"
            onClick={() => setIsRegisterMode(!isRegisterMode)}
            style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}
          >
            {isRegisterMode ? 'Log In here' : 'Sign Up here'}
          </button>
        </p>
      </div>
    );
  }

  // 2. Main Dashboard
  return (
    <div style={{ maxWidth: '700px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>🏋️ Gym / Workout Logger</h2>
        <button onClick={handleLogout} style={{ padding: '6px 12px', cursor: 'pointer' }}>Logout</button>
      </div>

      {/* OVERVIEW / PR SECTION */}
      {stats && (
        <div style={{ background: '#eef2f7', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>📊 Your Overview</h3>
          <p style={{ margin: '0.25rem 0' }}><strong>Total Workouts Logged:</strong> {stats.total_workouts}</p>

          <h4 style={{ margin: '0.75rem 0 0.25rem 0' }}>🏆 Personal Records (Max Weight):</h4>
          {stats.personal_records && stats.personal_records.length > 0 ? (
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
              {stats.personal_records.map((pr, index) => (
                <div
                  key={index}
                  style={{
                    background: '#fff',
                    border: '1px solid #ccd0d5',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    fontSize: '0.9rem'
                  }}
                >
                  <strong>{pr.name}:</strong> {pr.max_weight} kg
                </div>
              ))}
            </div>
          ) : (
            <p style={{ fontSize: '0.9rem', color: '#666' }}>No PRs recorded yet. Add some exercises!</p>
          )}
        </div>
      )}

      {/* CREATE / EDIT WORKOUT FORM */}
      <form
        onSubmit={handleSaveWorkout}
        style={{
          border: editingSessionId ? '2px solid #ffc107' : '1px solid #ddd',
          padding: '1.5rem',
          borderRadius: '8px',
          marginTop: '1.5rem',
          backgroundColor: editingSessionId ? '#fffdf6' : '#fff'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>{editingSessionId ? '✏️ Edit Workout Session' : '➕ Log New Session'}</h3>
          {editingSessionId && (
            <button
              type="button"
              onClick={cancelEdit}
              style={{ background: '#6c757d', color: '#fff', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
            >
              Cancel Edit
            </button>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Date: </label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Notes: </label>
          <input
            type="text"
            placeholder="e.g. Chest & Triceps day"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            style={{ width: '80%', padding: '6px' }}
          />
        </div>

        <h4>Exercises</h4>
        {exercises.map((ex, idx) => (
          <div key={idx} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <input
              type="text"
              placeholder="Exercise name"
              value={ex.name}
              onChange={(e) => updateExercise(idx, 'name', e.target.value)}
              required
              style={{ flex: 2, padding: '4px' }}
            />
            <input
              type="number"
              placeholder="Sets"
              value={ex.sets}
              onChange={(e) => updateExercise(idx, 'sets', Number(e.target.value))}
              required
              style={{ width: '60px', padding: '4px' }}
            />
            <input
              type="number"
              placeholder="Reps"
              value={ex.reps}
              onChange={(e) => updateExercise(idx, 'reps', Number(e.target.value))}
              required
              style={{ width: '60px', padding: '4px' }}
            />
            <input
              type="number"
              step="0.5"
              placeholder="Weight (kg)"
              value={ex.weight}
              onChange={(e) => updateExercise(idx, 'weight', Number(e.target.value))}
              required
              style={{ width: '80px', padding: '4px' }}
            />
            {exercises.length > 1 && (
              <button type="button" onClick={() => removeExerciseRow(idx)} style={{ color: 'red' }}>✕</button>
            )}
          </div>
        ))}

        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
          <button type="button" onClick={addExerciseRow}>+ Add Exercise</button>
          <button
            type="submit"
            style={{
              background: editingSessionId ? '#ffc107' : '#28a745',
              color: editingSessionId ? '#000' : '#fff',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            {editingSessionId ? 'Update Workout Session' : 'Save Workout Session'}
          </button>
        </div>
      </form>

      {/* PAST SESSIONS LIST */}
      <h3 style={{ marginTop: '2.5rem' }}>Past Workout Sessions</h3>
      {sessions.length === 0 ? (
        <p>No workouts recorded yet.</p>
      ) : (
        sessions.map((s) => (
          <div
            key={s.id}
            style={{
              background: '#f8f9fa',
              padding: '1rem',
              margin: '1rem 0',
              borderRadius: '6px',
              borderLeft: editingSessionId === s.id ? '4px solid #ffc107' : '4px solid #007bff'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>📅 {s.date}</strong> — <em>{s.notes || 'No notes'}</em>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={() => startEditSession(s)}
                  style={{ background: '#007bff', color: '#fff', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteSession(s.id)}
                  style={{ background: '#dc3545', color: '#fff', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </div>
            </div>
            <ul style={{ marginTop: '0.5rem' }}>
              {s.exercises.map((ex, i) => (
                <li key={i}>
                  <strong>{ex.name}</strong>: {ex.sets} sets × {ex.reps} reps @ {ex.weight} kg
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}

export default App;