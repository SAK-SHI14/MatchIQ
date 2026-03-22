import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper for multipart/form-data
const apiUploadClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const api = {
  // Jobs
  listJobs: () => apiClient.get('/jobs/'),
  // Job Uploads
  uploadJD: (data) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('text', data.text);
    formData.append('skills', data.skills);
    return apiUploadClient.post('/upload/jd', formData);
  },
  
  // Resume Uploads
  uploadResume: (jobId, file) => {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('file', file);
    return apiUploadClient.post('/upload/resume', formData);
  },

  // Match Results
  getRankings: (jobId) => apiClient.get(`/match/${jobId}`),

  // Analysis
  getSkillGaps: (candidateId) => apiClient.get(`/gaps/${candidateId}`),

  // Interviews
  getInterviewQuestions: (candidateId) => apiClient.get(`/interview/${candidateId}`),
};
