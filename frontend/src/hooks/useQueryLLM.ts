import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

export const useQueryLLM = () => {
  return useMutation(async (query: string) => {
    const res = await axios.post('/api/query', { query });
    return res.data;
  });
};