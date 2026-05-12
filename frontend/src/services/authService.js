import api from '../api/axios';
import { fileService } from './fileService';

export const authService = {
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  register: async (userData) => {
    const response = await api.post('/auth/register/student', userData);
    return response.data;
  },
  requestPasswordReset: async (email) => {
    const response = await api.post('/auth/password/reset-request', { email });
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
  logout: async (refresh_token) => {
    const response = await api.post('/auth/logout', { refresh_token });
    return response.data;
  },
  verifyEmail: async (token) => {
    const response = await api.post(`/auth/verify-email?token=${token}`);
    return response.data;
  },
  updateProfile: async (data) => {
    const response = await api.put('/auth/profile', data);
    return response.data;
  },
  uploadAvatar: async (file) => {
    return await fileService.uploadSingle('/auth/profile/avatar', file);
  },
  getDepartments: async () => {
    const response = await api.get('/auth/departments');
    return response.data;
  },
};
