from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from calculate_reorder_quantity_func import create_inventory_task
from pydantic import BaseModel
app = FastAPI()

# Add CORS middleware to allow requests from any origin with any method (you can customize as needed)
origins = ["*"]  # Allow requests from any origin
# Add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class ReorderQuantityRequest(BaseModel):
    current_inventory: int
    historic_data: int
    forecast: int  

@app.post("/calculate-reorder-quantity")
async def calculate_reorder_quantity(request:ReorderQuantityRequest):
    res = create_inventory_task(request.current_inventory, 
                                            request.historic_data, 
                                            request.forecast)
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
