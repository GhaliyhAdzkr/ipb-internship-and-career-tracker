import api from '../api/axios';

export const adminService = {
  // Master Data: Departemen
  getDepartments: async () => {
    const response = await api.get('/admin/departments');
    return response.data;
  },
  createDepartment: async (data) => {
    const response = await api.post('/admin/departments', data);
    return response.data;
  },
  updateDepartment: async (id, data) => {
    const response = await api.patch(`/admin/departments/${id}`, data);
    return response.data;
  },
  deleteDepartment: async (id) => {
    const response = await api.delete(`/admin/departments/${id}`);
    return response.data;
  },

  // Master Data: Keahlian
  getSkills: async () => {
    const response = await api.get('/admin/skills');
    return response.data;
  },
  createSkill: async (data) => {
    const response = await api.post('/admin/skills', data);
    return response.data;
  },
  updateSkill: async (id, data) => {
    const response = await api.patch(`/admin/skills/${id}`, data);
    return response.data;
  },
  deleteSkill: async (id) => {
    const response = await api.delete(`/admin/skills/${id}`);
    return response.data;
  },

  // Master Data: Perusahaan
  getCompanies: async () => {
    const response = await api.get('/admin/companies');
    return response.data;
  },
  createCompany: async (data) => {
    const response = await api.post('/admin/companies', data);
    return response.data;
  },
  updateCompany: async (id, data) => {
    const response = await api.patch(`/admin/companies/${id}`, data);
    return response.data;
  },
  deleteCompany: async (id) => {
    const response = await api.delete(`/admin/companies/${id}`);
    return response.data;
  },
  uploadCompanyLogo: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/admin/companies/upload-logo', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Manajemen Lowongan: Otoritas Admin
  createVacancy: async (data) => {
    const response = await api.post('/vacancies', data);
    return response.data;
  },
  updateVacancy: async (id, data) => {
    const response = await api.put(`/vacancies/${id}`, data);
    return response.data;
  },
  deleteVacancy: async (id) => {
    const response = await api.delete(`/vacancies/${id}`);
    return response.data;
  },

  // Manajemen User
  getStudents: async () => {
    const response = await api.get('/admin/users', { params: { role: 'STUDENT' } });
    return response.data;
  },
  toggleUserActive: async (userId) => {
    const response = await api.patch(`/admin/users/${userId}/toggle-active`);
    return response.data;
  },

  // Verifikasi Lamaran
  getPendingVerifications: async () => {
    const response = await api.get('/admin/applications/pending-verification');
    return response.data;
  },
  verifyApplication: async (applicationId, data) => {
    const response = await api.post(`/admin/applications/${applicationId}/verify`, data);
    return response.data;
  },
  rejectApplication: async (applicationId, data) => {
    const response = await api.post(`/admin/applications/${applicationId}/reject-proof`, data);
    return response.data;
  },
  
  // Placement
  getPlacements: async () => {
    const response = await api.get('/admin/placements');
    return response.data;
  }
};

export default adminService;
