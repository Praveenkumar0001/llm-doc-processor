#!/bin/bash
for f in ./documents/*; do
  curl -F "file=@$f" http://localhost:8000/documents/pdf
done