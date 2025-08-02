#!/bin/bash
# delete and recreate index
echo "Cleaning up Pinecone index..."
pinecone delete-index --name documents
pinecone create-index --name documents --dimension 1536
echo "Done."