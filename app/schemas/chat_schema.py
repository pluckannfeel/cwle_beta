from pydantic import BaseModel, field_validator
from fastapi import Form, UploadFile
from typing import Optional

class ChatRequest(BaseModel):
    role: str
    user_id: str
    prompt: str
    data: str
    model: str = "bedrock-claude"
    files: Optional[list[UploadFile]] = None
    stream: bool = True

    @classmethod
    def as_form(
        cls,
        role:str = Form(...),
        user_id: str = Form(...),
        prompt: str = Form(...),
        data: str = Form(...),
        model: str = Form("bedrock-claude"),
        files: Optional[list[UploadFile]] = None,
        stream: bool = Form(True)
    ):
        return cls(
            role=role,
            user_id=user_id,
            prompt=prompt,
            data=data,
            model=model,
            files=files,
            stream=stream
        )

    @field_validator('model')
    def validate_model(cls, value):
        allowed_models = ["bedrock-claude", "openai-gpt-4o"]
        if value not in allowed_models:
            raise ValueError(f"Model must be one of {allowed_models}")
        return value

    @field_validator('files')
    def validate_file_type(cls, files):
        if files is None:  # Allow empty files
            return None

        if files:
            allowed_types = ['image/jpeg', 'image/png', 'text/plain', 'application/pdf']
            for file in files:
                content_type = file.content_type
                if content_type not in allowed_types:
                    raise ValueError(f"File type must be one of {allowed_types}. Got {content_type}")
        return files

class ChatResponse(BaseModel):
    results: dict