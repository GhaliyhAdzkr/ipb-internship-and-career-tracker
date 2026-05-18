import api from '../api/axios';

/**
 * Service File bersama untuk upload yang tangguh
 */
export const fileService = {
  /**
   * Upload file tunggal dengan validasi dan penanganan error
   * @param {string} endpoint: Endpoint API
   * @param {File} file: Objek File
   * @param {string} fieldName: Nama field form (default: 'file')
   * @param {object} additionalData: Data form tambahan
   * @returns {Promise<any>}
   */
  uploadSingle: async (endpoint, file, fieldName = 'file', additionalData = {}) => {
    // 1. Validasi: Maksimal 10MB
    const MAX_SIZE = 10 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      throw new Error(`File "${file.name}" terlalu besar. Maksimal 10MB.`);
    }

    // 2. Siapkan FormData
    const formData = new FormData();
    formData.append(fieldName, file);
    
    Object.keys(additionalData).forEach(key => {
      formData.append(key, additionalData[key]);
    });

    // 3. Upload dengan Logika Retry: Simple 3 kali percobaan
    let retries = 0;
    const maxRetries = 2;

    const attemptUpload = async () => {
      try {
        const response = await api.post(endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          // timeout: 30000, // Timeout 30 detik untuk file besar
        });
        return response.data;
      } catch (error) {
        if (retries < maxRetries && (!error.response || error.response.status >= 500)) {
          retries++;
          console.warn(`Upload failed, retrying (${retries}/${maxRetries})...`);
          await new Promise(resolve => setTimeout(resolve, 1000 * retries)); // Backoff eksponensial
          return attemptUpload();
        }
        throw error;
      }
    };

    return attemptUpload();
  },

  /**
   * Upload beberapa file secara berurutan untuk meminimalkan error
   * @param {string} endpoint: Endpoint API
   * @param {File[]} files: Array dari File
   * @returns {Promise<any[]>}
   */
  uploadBatch: async (endpoint, files, fieldName = 'file') => {
    const results = [];
    const errors = [];

    // Proses secara berurutan untuk menghindari beban berlebih pada koneksi atau server
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
