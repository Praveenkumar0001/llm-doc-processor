// frontend/src/pages/api/query.ts

import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Allow only POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { query } = req.body;

  if (!query || typeof query !== 'string') {
    return res.status(400).json({ error: 'Missing or invalid "query" in request body.' });
  }

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  if (!backendUrl) {
    console.error('❌ NEXT_PUBLIC_BACKEND_URL is not defined.');
    return res.status(500).json({ error: 'Backend URL is not configured.' });
  }

  try {
    const backendRes = await axios.post(`${backendUrl}/query`, { query });
    return res.status(200).json(backendRes.data);
  } catch (err: any) {
    console.error('❌ Error talking to backend:', err.message || err);
    return res.status(502).json({
      error: 'Bad Gateway',
      details: err.message || 'Unknown error'
    });
  }
}
