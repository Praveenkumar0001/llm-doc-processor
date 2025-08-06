// frontend/src/hooks/useQueryLLM.ts
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

export const useQueryLLM = () => {
  return useMutation({
    // mutationFn takes your variables (here: query string) and returns a promise
    mutationFn: async (query: string) => {
      const res = await axios.post('/api/query', { query });
      return res.data;
    },
    // Optional: you can type the generics explicitly
    // <TData = any, TError = Error, TVariables = string>
  });
};
