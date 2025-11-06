from pydantic import BaseModel, Field

class RoastRequest(BaseModel):
    """Request model for the roasting API."""
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="Name to be roasted. Must be between 2 and 50 characters."
    )

class RoastResponse(BaseModel):
    """Response model for the roasting API."""
    roast: str