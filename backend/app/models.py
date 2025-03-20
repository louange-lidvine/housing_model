from pydantic import BaseModel

class HouseData(BaseModel):
    Area: int
    Bedrooms: int
    Bathrooms: int
    Floors: int
    YearBuilt: int
    Location: str
    Condition: str
    Garage: str