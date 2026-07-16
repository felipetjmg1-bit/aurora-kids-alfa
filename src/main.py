import uvicorn
import os
import sys

# Adiciona o diretório atual ao path para evitar erros de importação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
