import asyncio
import boto3
from langchain_aws import ChatBedrock
from app.services.llm.base import BaseLLMProvider  # Import the base class
from typing import List
from loguru import logger
from langchain.schema import BaseMessage
from app.config.settings import settings

# chat history db
from app.models.chat_history import ChatHistory


class BedrockLLMProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "anthropic.claude-3-haiku-20240307-v1:0"):
        bedrock_client = boto3.client('bedrock-runtime',
                                      aws_access_key_id=settings.ACCESS_KEY_ID_AWS,
                                      aws_secret_access_key=settings.SECRET_ACCESS_KEY_AWS,)

        self.model = ChatBedrock(
            client=bedrock_client,
            model_id=model_name,
            #    aws_access_key_id=settings.ACCESS_KEY_ID_AWS,
            #    aws_secret_access_key=settings.SECRET_ACCESS_KEY_AWS,
            region_name=settings.REGION_AWS,
            temperature=0.5,
            max_tokens=4096,
            streaming=False
        )

    # original
    # def generate_stream_response(self, messages: List[BaseMessage]):
    #     response = self.model.stream(messages)
    #     for chunk in response:
    #         if chunk.content is not None:
    #             yield chunk.content

    # modified to save chat history
    async def generate_stream_response(self, messages: List[BaseMessage], model_name: str, prompt: str, role: str, user_id: str):
        """
        Stream the AI response while saving chunks in real-time.
        """
        chat_record = await ChatHistory.create(  # ✅ Save chat entry immediately (empty response)
            user_id=user_id,
            # role="user",
            role=role,
            model_name=model_name,
            prompt=prompt,
            response=""
        )

        full_response = ""  # ✅ Collect the full response

        def sync_stream():
            """ Helper function to stream responses in a synchronous way """
            for chunk in self.model.stream(messages):  # ✅ Sync generator
                if chunk.content:
                    yield chunk.content

        async for chunk in self._async_stream(sync_stream):
            full_response += chunk
            yield chunk  # ✅ Send chunk to frontend

            # ✅ Update the database after each chunk (real-time logging)
            await ChatHistory.filter(id=chat_record.id).update(response=full_response, role=chat_record.role)

        logger.info(
            f"Chat updated successfully in real-time: {full_response[:50]}...")

    async def _async_stream(self, sync_generator):
        """
        Converts a synchronous generator to an asynchronous generator.
        """
        for chunk in await asyncio.to_thread(lambda: list(sync_generator())):
            yield chunk

    def generate_response(self, messages: List[BaseMessage]) -> str:
        response = self.model.invoke(messages)
        return response.content

    def get_model_name(self) -> str:
        return f"bedrock-{self.model.model_name}"  # Return the model name
