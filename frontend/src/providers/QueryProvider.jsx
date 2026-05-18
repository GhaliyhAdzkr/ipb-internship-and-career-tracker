import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useBackendHealth } from '../hooks/useBackendHealth';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1000 * 60 * 5, // Waktu stale 5 menit
    },
  },
});

export const QueryProvider = ({ children }) => {
  useBackendHealth();
  return (
    <QueryClientProvider client={queryClient}>
      <Toaster
        position="top-right"
        toastOptions={{
          className: 'font-jakarta text-sm font-bold',
          duration: 4000,
          style: {
            borderRadius: '10px',
            boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
          },
        }}
      />
      {children}
    </QueryClientProvider>
  );
};
