import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { query } = req.body;
  const backendRes = await axios.post(process.env.BACKEND_URL + '/query', { query });
  res.status(200).json(backendRes.data);
}