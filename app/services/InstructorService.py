from typing import Dict, List, Type
import os
from dotenv import load_dotenv
import logging
import instructor
from pydantic import BaseModel
from openai import AsyncOpenAI
import base64

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

class InstructorService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.aclient = instructor.apatch(AsyncOpenAI(api_key=OPENAI_KEY))
        return cls._instance


    async def completion_with_image_path(
        self,
        prompt: str,
        image_path: str,
        instructor_model: Type[BaseModel],
        max_retries: int = 5,
    ) -> Type[BaseModel]:
        """
        Most of you are likely familiar with tool calling with GPT4.

        This is just that but instead of passing a JSON string, we
        pass a Pydantic model, and it returns that Pydantic model.

        In addition, we can add retry mechanisms. This is all thanks to
        Jason Liu and his instructor package. Definitely recommend
        checking it out!

        https://github.com/jxnl/instructor

        Args:
        - messages: List[Dict[str, str]]: The messages to send to the model
        - instructor_model: Type[BaseModel]: The Pydantic model to return
        - max_retries: int: The maximum number of retries to attempt

        Returns:
        - Type[BaseModel]: The Pydantic model
        """
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode()

        messages = [
            {"role": "user", 
             "content": [
                {
                    "type": "text", 
                    "text": prompt
                },
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]}
        ]

        logging.info(f"Sending messages to the model:\n{messages}")

        task = self.aclient.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_model=instructor_model,
            temperature=0.0,
            seed=69,
            max_retries=max_retries,
        )

        model = await task
        logging.info(f"Received completion from the model:\n{str(model)}")
        return model

    async def completion_with_base64_image_string(
        self,
        prompt: str,
        image_base64: str,
        instructor_model: Type[BaseModel],
        max_retries: int = 5,
    ) -> Type[BaseModel]:
        messages = [
            {"role": "user", 
             "content": [
                {
                    "type": "text", 
                    "text": prompt
                },
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]}
        ]

        logging.info(f"Sending messages to the model:\n{messages}")

        task = self.aclient.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_model=instructor_model,
            temperature=0.0,
            seed=69,
            max_retries=max_retries,
        )

        model = await task
        logging.info(f"Received completion from the model:\n{str(model)}")
        return model

    async def completion(
        self,
        prompt: str,
        instructor_model: Type[BaseModel],
        max_retries: int = 5,
    ) -> Type[BaseModel]:
        
        logging.info(f"Sending message to the model:\n{prompt}")

        task = self.aclient.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_model=instructor_model,
            temperature=0.0,
            seed=69,
            max_retries=max_retries,
        )

        model = await task
        logging.info(f"Received completion from the model:\n{str(model)}")
        return model
