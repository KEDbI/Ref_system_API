import uvicorn
from fastapi import FastAPI

from app.api.endpoints.ref_system import ref_system_router


app = FastAPI()

app.include_router(ref_system_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app')