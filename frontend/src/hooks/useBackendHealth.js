import { useEffect } from 'react';
import toast from 'react-hot-toast';
import api from '../api/axios';

const TOAST_ID = 'backend-health';

// Lacak status gangguan saat ini pada lingkup modul: menghindari closure usang di dalam
// interceptor dan memastikan sistem bekerja bahkan sebelum komponen React dipasang.
const isDownRef = { current: false };

// Daftarkan interceptor sekali pada saat impor modul: sebelum rendering React terjadi.
// Ini memastikan interceptor aktif sebelum React Query mengirimkan request pertama.
api.interceptors.response.use(
  (response) => {
    if (isDownRef.current) {
      isDownRef.current = false;
      toast.dismiss(TOAST_ID);
      toast.success('Server kembali tersedia.', { duration: 3000 });
    }
    return response;
  },
  (error) => {
    const isNetworkError = !error.response;
    const isServerError = error.response?.status >= 500;

    if ((isNetworkError || isServerError) && !isDownRef.current) {
      // Tampilkan sekali saja per gangguan: bukan pada setiap request yang gagal
      isDownRef.current = true;
      toast.error('Server sedang tidak dapat dijangkau.', {
        id: TOAST_ID,
        duration: Infinity,
      });
    } else if (!isNetworkError && !isServerError && isDownRef.current) {
      // Status 4xx berarti backend aktif: bersihkan alert gangguan
      isDownRef.current = false;
      toast.dismiss(TOAST_ID);
    }

    return Promise.reject(error);
  }
);

/**
 * Memasang event listener online atau offline pada browser
 * Interceptor axios di atas menangani kegagalan spesifik backend
 * dan terdaftar pada saat pemuatan modul: tidak bergantung pada lifecycle React.
 */
export function useBackendHealth() {
  useEffect(() => {
    const onOffline = () => {
      if (!isDownRef.current) {
        isDownRef.current = true;
        toast.error('Tidak ada koneksi internet.', {
          id: TOAST_ID,
          duration: Infinity,
        });
      }
    };

    const onOnline = () => {
      isDownRef.current = false;
      toast.dismiss(TOAST_ID);
      toast.success('Koneksi internet kembali.', { duration: 3000 });
    };

    window.addEventListener('offline', onOffline);
    window.addEventListener('online', onOnline);
    return () => {
      window.removeEventListener('offline', onOffline);
      window.removeEventListener('online', onOnline);
    };
  }, []);
}
