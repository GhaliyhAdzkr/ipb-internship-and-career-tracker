import api from '../api/axios';

export const documentService = {
  listDocuments: async () => {
    const response = await api.get('/document-requests');
    return response.data;
  },

  requestDocument: async (payload) => {
    // Payload: { document_type, purpose, reference_vacancy_id? }
    const response = await api.post('/document-requests', payload);
    return response.data;
  },

  getDocument: async (documentId) => {
    const response = await api.get(`/document-requests/${documentId}`);
    return response.data;
  },
};

export default documentService;
