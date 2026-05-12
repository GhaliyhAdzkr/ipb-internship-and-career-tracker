import api from '../api/axios';
import { fileService } from './fileService';

export const applicationService = {
  /**
   * Initialize a new job application.
   * @param {Object} data - Application data (vacancy_id, documents, etc.)
   */
  apply: async (data) => {
    const response = await api.post('/applications', data);
    return response.data;
  },

  /**
   * Update application status (e.g., to REJECTED or ACCEPTED after LoA).
   * @param {string} applicationId
   * @param {Object} data - { status }
   */
  updateStatus: async (applicationId, data) => {
    const response = await api.patch(`/applications/${applicationId}/status`, data);
    return response.data;
  },

  /**
   * Upload proof of acceptance (Screenshot LoA).
   * @param {string} applicationId
   * @param {File} file
   */
  uploadProof: async (applicationId, file) => {
    return await fileService.uploadSingle(`/applications/${applicationId}/proof`, file);
  },

  /**
   * Get audit logs/history for a specific application.
   * @param {string} applicationId
   */
  getHistory: async (applicationId) => {
    const response = await api.get(`/applications/${applicationId}/history`);
    return response.data;
  },

  /**
   * Get all applications for the current student.
   */
  getMyApplications: async () => {
    const response = await api.get('/applications/my');
    return response.data;
  },
};

export default applicationService;
