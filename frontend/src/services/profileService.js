import api from '../api/axios';
import { fileService } from './fileService';

export const profileService = {
  /**
   * Ambil detail profil Student saat ini
   */
  getProfile: async () => {
    const response = await api.get('/profile/me');
    return response.data;
  },

  /**
   * Perbarui data CV: nomor telepon, LinkedIn, URL CV, dan keahlian
   * @param {Object} data: Objek berisi phone_number, linkedin_url, cv_url, keahlian
   */
  updateCVData: async (data) => {
    const response = await api.put('/profile/cv-data', data);
    return response.data;
  },

  /**
   * Upload file CV ke S3
   * @param {File} file
   */
  uploadCV: async (file) => {
    return await fileService.uploadSingle('/profile/student/cv', file);
  },
};

export default profileService;
