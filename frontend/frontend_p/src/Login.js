import React, { useState } from 'react'; 
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const backgroundImageUrl = 'https://source.unsplash.com/5gGcn2PRrtc';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false); // State to determine error or success
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/accounts/login/', {
        email,
        password,
      });
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      setMessage("Login successful");
      setIsError(false);
      navigate('/home');
    } catch (error) {
      setMessage('Login failed');
      setIsError(true);
    }
  };

  return (
    <div className="min-h-screen flex flex-col" 
      style={{
        backgroundImage: `url(${backgroundImageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}
    >
      {/* Navbar */}
      <nav className="bg-white bg-opacity-90 p-4 shadow-md fixed top-0 left-0 w-full z-10">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">
            Nutritech Agro
          </h1>
          <a 
           href="/signup" 
            className="text-white bg-blue-600 hover:bg-blue-700 font-semibold py-2 px-4 rounded-full shadow-md transition duration-200 ease-in-out transform hover:scale-105"
          >
            Sign Up
          </a>
        </div>
      </nav>

      {/* Login Card */}
      <div className="flex items-center justify-center flex-grow mt-16">
        <div className="card w-full max-w-md bg-white bg-opacity-80 shadow-xl rounded-lg p-8">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-700">Welcome Back!</h2>
            <p className="text-gray-500">Log in to continue</p>
          </div>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="form-control">
              <label className="label">
                <span className="label-text">Email</span>
              </label>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input input-bordered w-full"
                required
              />
            </div>
            <div className="form-control">
              <label className="label">
                <span className="label-text">Password</span>
              </label>
              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input input-bordered w-full"
                required
              />
            </div>
            
            {/* Message Alerts */}
            {message && (
              <div role="alert" className={`alert ${isError ? 'alert-error' : 'alert-success'} mt-2`}>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 shrink-0 stroke-current"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d={isError
                      ? "M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                      : "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"}
                  />
                </svg>
                <span>{message}</span>
              </div>
            )}

            <div className="form-control mt-6">
              <button type="submit" className="btn btn-primary w-full">
                Log In
              </button>
            </div>
          </form>
          
          <p className="text-center text-sm text-gray-500 mt-6">
            Don't have an account? <a href="/signup" className="text-blue-600">Sign Up</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
