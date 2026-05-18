export const handleApiError = (error, customMessage) => {
  const detail = error.response?.data?.detail;
  let message = 'An unexpected error occurred';

  if (typeof detail === 'string') {
    message = detail;
  } else if (Array.isArray(detail) && detail[0]?.msg) {
    message = detail[0].msg;
  } else if (customMessage) {
    message = customMessage;
  }

  const err = new Error(message);
  err.status = error.response?.status;
  err.originalError = error;
  throw err;
};
