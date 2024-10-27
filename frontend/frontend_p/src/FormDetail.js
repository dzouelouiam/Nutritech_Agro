import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const FormDetail = () => {
  const { id } = useParams();
  const [form, setForm] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    region: '',
    place: '',
    topic: '',
    question: '',
  });
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false); // Track success/error for alerts
  const navigate = useNavigate();

  useEffect(() => {
    const fetchForm = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/accounts/form/${id}/`);
        setForm(response.data);
        setFormData(response.data);
      } catch (error) {
        setMessage('Failed to fetch form');
        setIsError(true);
      }
    };

    const fetchComments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/accounts/form/${id}/comments/`);
        setComments(response.data);
      } catch (error) {
        setMessage('Failed to fetch comments');
        setIsError(true);
      }
    };

    fetchForm();
    fetchComments();
  }, [id]);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleEdit = async () => {
    try {
      await axios.put(`http://127.0.0.1:8000/api/accounts/form/${id}/`, formData);
      setMessage("Form updated successfully!");
      setIsError(false);
      setEditMode(false);
      setForm(formData);
    } catch (error) {
      setMessage("Failed to update form.");
      setIsError(true);
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/accounts/form/${id}/`);
      setMessage("Form deleted successfully!");
      setIsError(false);
      navigate('/'); // Redirect to home after deletion
    } catch (error) {
      setMessage("Failed to delete form.");
      setIsError(true);
    }
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) {
      setMessage("Please enter a comment.");
      setIsError(true);
      return;
    }

    try {
      const response = await axios.post(`http://127.0.0.1:8000/api/accounts/form/${id}/comments/`, {
        text: newComment,
      });
      setComments([...comments, response.data]);
      setNewComment('');
      setMessage("Comment added successfully!");
      setIsError(false);
    } catch (error) {
      setMessage("Failed to add comment.");
      setIsError(true);
    }
  };

  const handleHomeNavigation = () => {
    navigate('/home'); 
  };

  if (!form) {
    return <div>Loading form data...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-300">
      {/* Navbar */}
      <div className="navbar bg-base-100">
        <div className="navbar-start">
          <button onClick={handleHomeNavigation} className="btn btn-ghost text-lg">Nutritech Agro</button>
        </div>
        <div className="navbar-center">
          <button className="btn btn-ghost normal-case text-xl">Form Details</button>
        </div>
      </div>

      {/* Alert Message */}
      {message && (
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
          <span>{message}</span>
        </div>
      )}

      {/* Main Content */}
      <div className="flex items-center justify-center p-6">
        <div className="card w-full max-w-lg bg-white shadow-lg rounded-lg p-6 mt-10">
          {editMode ? (
            <div>
              <h2 className="text-xl font-bold text-center mb-4">Edit Form</h2>
              <input
                type="text"
                name="topic"
                placeholder="Topic"
                value={formData.topic}
                onChange={handleInputChange}
                className="input input-bordered w-full mb-4"
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
                className="input input-bordered w-full mb-4"
              />
              <input
                type="text"
                name="region"
                placeholder="Region"
                value={formData.region}
                onChange={handleInputChange}
                className="input input-bordered w-full mb-4"
              />
              <input
                type="text"
                name="place"
                placeholder="Place"
                value={formData.place}
                onChange={handleInputChange}
                className="input input-bordered w-full mb-4"
              />
              <textarea
                name="question"
                placeholder="Question"
                value={formData.question}
                onChange={handleInputChange}
                className="textarea textarea-bordered w-full mb-4"
              ></textarea>
              <button className="btn btn-primary w-full mb-2" onClick={handleEdit}>Save</button>
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-bold text-center mb-4">{form.topic}</h2>
              <p className="text-gray-600"><strong>Email:</strong> {form.email}</p>
              <p className="text-gray-600"><strong>Region:</strong> {form.region}</p>
              <p className="text-gray-600"><strong>Place:</strong> {form.place}</p>
              <p className="text-gray-600"><strong>Question:</strong> {form.question}</p>
            </div>
          )}

          {/* Edit/Delete Buttons */}
          <div className="flex mt-4 space-x-2 justify-center">
            {!editMode ? (
              <>
                <button className="btn btn-warning" onClick={() => setEditMode(true)}>Edit</button>
                <button className="btn btn-error" onClick={handleDelete}>Delete</button>
              </>
            ) : (
              <button className="btn btn-secondary" onClick={() => setEditMode(false)}>Cancel</button>
            )}
            <button className="btn btn-secondary" onClick={() => navigate(-1)}>Back</button>
          </div>

          {/* Comments Section */}
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-4">Commentaires et Conseils</h3>
            
            {/* List of comments */}
            <div className="space-y-4 max-h-40 overflow-y-auto">
              {comments.map((comment, index) => (
                <div key={index} className="bg-gray-100 p-3 rounded-lg shadow-sm">
                  <p className="text-gray-700">{comment.text}</p>
                  <p className="text-gray-500 text-xs text-right">Posté le {new Date(comment.created_at).toLocaleString()}</p>
                </div>
              ))}
            </div>

            {/* Add new comment */}
            <div className="mt-4">
              <textarea
                placeholder="Laissez un commentaire ou un conseil..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                className="textarea textarea-bordered w-full"
              ></textarea>
              <button onClick={handleAddComment} className="btn btn-primary w-full mt-2">Ajouter un commentaire</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FormDetail;
