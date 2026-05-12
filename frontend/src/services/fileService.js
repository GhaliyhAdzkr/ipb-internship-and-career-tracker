import api from '../api/axios';

/**
 * Shared File Service for robust uploads
 */
export const fileService = {
  /**
   * Upload a single file with validation and error handling
   * @param {string} endpoint - API endpoint
   * @param {File} file - File object
   * @param {string} fieldName - Form field name (default: 'file')
   * @param {object} additionalData - Extra form fields
   * @returns {Promise<any>}
   */
  uploadSingle: async (endpoint, file, fieldName = 'file', additionalData = {}) => {
    // 1. Validation (Max 10MB)
    const MAX_SIZE = 10 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      throw new Error(`File "${file.name}" terlalu besar. Maksimal 10MB.`);
    }

    // 2. Prepare FormData
    const formData = new FormData();
    formData.append(fieldName, file);
    
    Object.keys(additionalData).forEach(key => {
      formData.append(key, additionalData[key]);
    });

    // 3. Upload with Retry Logic (Simple 3x retry)
    let retries = 0;
    const maxRetries = 2;

    const attemptUpload = async () => {
      try {
        const response = await api.post(endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          // timeout: 30000, // 30s timeout for large files
        });
        return response.data;
      } catch (error) {
        if (retries < maxRetries && (!error.response || error.response.status >= 500)) {
          retries++;
          console.warn(`Upload failed, retrying (${retries}/${maxRetries})...`);
          await new Promise(resolve => setTimeout(resolve, 1000 * retries)); // Exponential backoff
          return attemptUpload();
        }
        throw error;
      }
    };

    return attemptUpload();
  },

  /**
   * Upload multiple files in a batched/sequential manner to minimize errors
   * @param {string} endpoint - API endpoint
   * @param {File[]} files - Array of files
   * @returns {Promise<any[]>}
   */
  uploadBatch: async (endpoint, files, fieldName = 'file') => {
    const results = [];
    const errors = [];

    // Process sequentially to avoid overwhelming connection/server
    for (const file of files) {
      try {
        const res = await fileService.uploadSingle(endpoint, file, fieldName);
        results.push(res);
      } catch (err) {
        console.error(`Batch upload failed for ${file.name}:`, err);
        errors.push({ file: file.name, error: err.message });
      }
    }

    if (errors.length > 0 && results.length === 0) {
      throw new Error(`Gagal mengunggah semua file: ${errors.map(e => e.error).join(', ')}`);
    }

    return { results, errors };
  }
};
