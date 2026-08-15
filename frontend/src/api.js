import axios from 'axios';

const getBaseUrl = () => {
  let url = process.env.REACT_APP_API_URL || 'https://gym-tracker-api-3jl4.onrender.com/api';
  // Strip trailing slashes so endpoints format reliably as `${baseURL}/endpoint/`
  return url.replace(/\/+$/, '');
};

const API = axios.create({
  baseURL: getBaseUrl(),
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const loginUser = (username, password) => {
  return API.post('/login/', { username, password });
};

export const registerUser = (username, password, email = '') => {
  return API.post('/register/', { username, password, email });
};

export const fetchWorkouts = () => {
  return API.get('/workouts/');
};

export const createWorkout = (workoutData) => {
  return API.post('/workouts/', workoutData);
};

export const fetchExercises = () => {
  return API.get('/exercises/');
};

export const fetchPersonalRecords = () => {
  return API.get('/analytics/personal-records/');
};

export default API;