from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class CountrySchema(BaseModel):
    nume_tara: str = Field(..., regex=r"^[A-Za-z\s\-]+$", description="Country name must only contain letters, spaces, or hyphens")
    latitudine: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90")
    longitudine: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180")

class CitySchema(BaseModel):
    id_tara: str = Field(..., regex=r"^[0-9a-fA-F]{24}$", description="Country ID must be a valid MongoDB ObjectId")
    nume_oras: str = Field(..., regex=r"^[A-Za-z\s\-]+$", description="City name must only contain letters, spaces, or hyphens")
    latitudine: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90")
    longitudine: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180")

class TemperatureSchema(BaseModel):
    id_oras: str = Field(..., regex=r"^[0-9a-fA-F]{24}$", description="City ID must be a valid MongoDB ObjectId")
    valoare: float = Field(..., ge=-100, le=100, description="Temperature value must be between -100 and 100")
