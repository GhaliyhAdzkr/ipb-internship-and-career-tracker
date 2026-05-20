import api from '../api/axios';

const buildVacancyParams = ({ page = 1, perPage = 9, query, location, type, paymentType, industry }) => {
  const params = {
    page,
    per_page: perPage,
  };

  if (query) params.query = query;
  if (location) params.location = location;
  if (type) params.type = type;
  if (paymentType) params.payment_type = paymentType;
  if (industry) params.industry = industry;

  return params;
};

export const vacancyService = {
  getVacancies: async ({ page = 1, perPage = 9, query, location, type, paymentType, industry } = {}) => {
    const hasFilters = Boolean(query || location || type || paymentType || industry);
    const params = buildVacancyParams({ page, perPage, query, location, type, paymentType, industry });
    const endpoint = hasFilters ? '/vacancies/search' : '/vacancies';
    const response = await api.get(endpoint, { params });
    return response.data;
  },

  getVacancy: async (vacancyId) => {
    const response = await api.get(`/vacancies/${vacancyId}`);
    return response.data;
  },

  addToWishlist: async (vacancyId, notes = null) => {
    const response = await api.post('/wishlist', {
      vacancy_id: vacancyId,
      notes,
    });
    return response.data;
  },
  getWishlist: async ({ page = 1, perPage = 20 } = {}) => {
    const response = await api.get('/wishlist', { params: { page, per_page: perPage } });
    return response.data;
  },
  deleteWishlist: async (wishlistId) => {
    const response = await api.delete(`/wishlist/${wishlistId}`);
    return response.data;
  },
  getJobMatch: async (vacancyId) => {
    const response = await api.get(`/job-matching/${vacancyId}`);
    return response.data;
  },
  getJobMatches: async ({ page = 1, perPage = 10, minMatch = 0 } = {}) => {
    const response = await api.get('/job-matching', {
      params: { page, per_page: perPage, min_match: minMatch },
    });
    return response.data;
  },
  getIndustries: async () => {
    const response = await api.get('/vacancies/industries');
    return response.data;
  },
};

export default vacancyService;
