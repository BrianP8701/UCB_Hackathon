import cv2
import asyncio
from pydantic import BaseModel, Field
from typing import List

from app.services.InstructorService import InstructorService


instructor = InstructorService()


class Colors(BaseModel):
    colors: List[str] = Field(..., description="List the most common and main colors in the image")
    

response = asyncio.run(instructor.completion(
    "What are the main colors in this image", 
    "/Users/brianprzezdziecki/Desktop/Things I Use/Dreamscape.jpeg",  # Moved image_path here
    Colors  # Moved instructor_model here
    )
)

print(response)
