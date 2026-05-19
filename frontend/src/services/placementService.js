import api from '../api/axios';
import { fileService } from './fileService';
import { handleApiError } from '../utils/apiUtils';

export const placementService = {
  getMyPlacements: async () => {
    try {
      const response = await api.get('/placements/me');
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch placements');
    }
  },

  getLogs: async (placementId) => {
    try {
      const response = await api.get(`/placements/${placementId}/logs`);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch activity logs');
    }
  },

  createLog: async (placementId, data) => {
    try {
      const response = await api.post(`/placements/${placementId}/logs`, data);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to create activity log');
    }
  },

  updateLog: async (placementId, logId, data) => {
    try {
      const response = await api.patch(`/placements/${placementId}/logs/${logId}`, data);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to update activity log');
    }
  },

  deleteLog: async (placementId, logId) => {
    try {
      const response = await api.delete(`/placements/${placementId}/logs/${logId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to delete activity log');
    }
  },

  uploadLogAttachment: async (placementId, logId, file) => {
    try {
      return await fileService.uploadSingle(`/placements/${placementId}/logs/${logId}/attachment`, file);
    } catch (error) {
      handleApiError(error, 'Failed to upload attachment');
    }
  },

  enhanceLog: async (placementId, logId) => {
    try {
      const response = await api.post(`/placements/${placementId}/logs/${logId}/enhance`);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to enhance activity log');
    }
  },

  generateReport: async (placementId) => {
    try {
      const response = await api.post(`/placements/${placementId}/report/generate`);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to generate report');
    }
  },

  getReport: async (placementId) => {
    try {
      const response = await api.get(`/placements/${placementId}/report`);
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch report status');
    }
  },
};

export default placementService;
