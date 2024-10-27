import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [showFormModal, setShowFormModal] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    region: '',
    place: '',
    topic: '',
    question: '',
  });
  const [forms, setForms] = useState([]);
  const [alertMessage, setAlertMessage] = useState('');
  const [isError, setIsError] = useState(false); 
  const navigate = useNavigate();

  const fetchForms = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/accounts/forms/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      });
      setForms(response.data);
    } catch (error) {
      console.log('Failed to fetch forms:', error);
    }
  };

  useEffect(() => {
    fetchForms();
  }, []);

  const handleFormClick = (formId) => {
    navigate(`/form/${formId}`);
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access');

    if (!token) {
      setAlertMessage("User is not authenticated.");
      setIsError(true);
      navigate('/login');
      return;
    }

    try {
      await axios.post('http://127.0.0.1:8000/api/accounts/create-form/', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setAlertMessage("Form submitted successfully!");
      setIsError(false);
      setShowFormModal(false);
      setFormData({ email: '', region: '', place: '', topic: '', question: '' });
      fetchForms();
    } catch (error) {
      console.error("Form submission error:", error.response ? error.response.data : error.message);
      setAlertMessage("Failed to submit form.");
      setIsError(true);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-300">
      {/* Navbar */}
      <div className="navbar bg-base-100">
        <div className="navbar-start">
          <div className="dropdown">
            <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" />
              </svg>
            </div>
            <ul tabIndex={0} className="menu menu-sm dropdown-content bg-base-100 rounded-box mt-3 w-36 p-2 shadow z-[1]">
              <li>
                <button onClick={() => setShowFormModal(true)}>Create New Form</button>
                <button onClick={() => setShowLogoutModal(true)}>Logout</button>
              </li>
            </ul>
          </div>
        </div>
        <div className="navbar-center">
          <button className="btn btn-ghost text-xl">Nutritech Agro</button>
        </div>
      </div>

      {/* Success/Error Alert */}
      {alertMessage && (
        <div role="alert" className={`alert ${isError ? 'alert-error' : 'alert-success'} my-4`}>
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
          <span>{alertMessage}</span>
        </div>
      )}

      {/* Create Form Modal */}
      {showFormModal && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg">Create New Form</h3>
            <form onSubmit={handleFormSubmit} className="space-y-4 mt-4">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
                className="input input-bordered w-full"
                required
              />
              <input
                type="text"
                name="region"
                placeholder="Region"
                value={formData.region}
                onChange={handleInputChange}
                className="input input-bordered w-full"
                required
              />
              <input
                type="text"
                name="place"
                placeholder="Place"
                value={formData.place}
                onChange={handleInputChange}
                className="input input-bordered w-full"
                required
              />
              <select
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                className="select select-bordered w-full"
                required
              >
                <option value="">Select a Topic</option>
                <option value="Engrais solides">Engrais solides</option>
                <option value="Engrais spéciaux hydrosolubles">Engrais spéciaux hydrosolubles</option>
                <option value="Correcteurs de carence">Correcteurs de carence</option>
                <option value="Biostimulants">Biostimulants</option>
              </select>
              <textarea
                name="question"
                placeholder="Enter your question"
                value={formData.question}
                onChange={handleInputChange}
                className="textarea textarea-bordered w-full"
                required
              ></textarea>
              <div className="modal-action">
                <button type="submit" className="btn btn-primary">Submit</button>
                <button type="button" className="btn" onClick={() => setShowFormModal(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Display Forms */}
      <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 bg-gray-300">
        {forms.map((form) => (
          <div
            key={form.id}
            onClick={() => handleFormClick(form.id)}
            className="card w-full bg-blue-50 shadow-md rounded-lg p-4 cursor-pointer"
          >
            <h4 className="font-bold text-gray-700 text-lg text-center">{form.topic}</h4>
            <p className="text-gray-600 text-left mt-2"><strong>Question:</strong> {form.question}</p>
          </div>
        ))}
      </div>

      {/* Logout Confirmation Modal */}
      {showLogoutModal && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg">Logout</h3>
            <p className="py-4">Are you sure you want to log out?</p>
            <div className="modal-action">
              <button className="btn btn-error" onClick={handleLogout}>
                Logout
              </button>
              <button className="btn" onClick={() => setShowLogoutModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
