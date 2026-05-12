import api from '../api/axios';
import { fileService } from './fileService';

export const profileService = {
  /**
   * Get current student profile details.
   */
  getProfile: async () => {
    const response = await api.get('/profile/me');
    return response.data;
  },

  /**
   * Update CV data (phone, linkedin, cv_url, skills).
   * @param {Object} data - { phone_number, linkedin_url, cv_url, skills: [{ skill_id, level }] }
   */
  updateCVData: async (data) => {
    const response = await api.put('/profile/cv-data', data);
    return response.data;
  },

  /**
   * Upload CV file to S3.
   * @param {File} file
   */
  uploadCV: async (file) => {
    return await fileService.uploadSingle('/profile/student/cv', file);
  },
};

export default profileService;
