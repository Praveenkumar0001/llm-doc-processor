# LLM Document Processing System

See frontend/ and backend/ folders for instructions. Set your `.env` keys (OpenAI, Pinecone), then:

```bash
# start infra
docker-compose up --build

# backend tests
pytest backend/tests