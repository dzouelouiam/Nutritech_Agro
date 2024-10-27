import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  // Here we’re checking if the user is authenticated by looking for a token in localStorage
  const isAuthenticated = localStorage.getItem('access');

  // If the user is not authenticated, redirect them to the login page
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, render the protected component
  return children;
};

export default ProtectedRoute;
