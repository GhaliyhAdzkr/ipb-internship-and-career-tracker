import api from '../api/axios';

export const adminService = {
  // Master Data: Departments
  getDepartments: async () => {
    const response = await api.get('/admin/departments');
    return response.data;
  },
  createDepartment: async (data) => {
    const response = await api.post('/admin/departments', data);
    return response.data;
  },

  // Master Data: Skills
  getSkills: async () => {
    const response = await api.get('/admin/skills');
    return response.data;
  },
  createSkill: async (data) => {
    const response = await api.post('/admin/skills', data);
    return response.data;
  },

  // Master Data: Companies
  getCompanies: async () => {
    const response = await api.get('/admin/companies');
    return response.data;
  },
  createCompany: async (data) => {
    const response = await api.post('/admin/companies', data);
    return response.data;
  },

  // User Management
  toggleUserActive: async (userId) => {
    const response = await api.patch(`/admin/users/${userId}/toggle-active`);
    return response.data;
  },

  // Application Verification
  getPendingVerifications: async () => {
    const response = await api.get('/admin/applications/pending');
    return response.data;
  },
  verifyApplication: async (applicationId, data) => {
    const response = await api.post(`/admin/applications/${applicationId}/verify`, data);
    return response.data;
  },
  rejectApplication: async (applicationId, data) => {
    const response = await api.post(`/admin/applications/${applicationId}/reject`, data);
    return response.data;
  },
};

export default adminService;
