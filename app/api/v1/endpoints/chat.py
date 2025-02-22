#AI MODEL CHAT (bedrock claude, open ai)
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.utils.response_handler import ResponseHandler
from app.services.llm.factory import LLMFactory
from loguru import logger
from app.services.prompts.chat import prepare_chat_prompt
from app.services.prompts.assistant import prepare_assistant_prompt

# chat history db
from app.models.chat_history import ChatHistory


router = APIRouter()

@router.post("", response_model=ChatResponse)
async def create_chat(
    request: ChatRequest = Depends(ChatRequest.as_form),
):
    try:
        provider_id = request.model
        llm_provider = LLMFactory.get_provider(provider_id)
        
        if request.data:
            messages = prepare_assistant_prompt(request.prompt, request.data)
        else:
            messages = prepare_chat_prompt(request.prompt, request.files)

        
        if request.stream:
            return StreamingResponse(
                llm_provider.generate_stream_response(messages, request.model, request.prompt, request.role, request.user_id),
                media_type='text/event-stream'
            )

        ai_response = llm_provider.generate_response(messages)

        # ✅ Save chat history when NOT streaming
        await ChatHistory.create(
            role=request.role,
            user_id=request.user_id,
            model_name=provider_id,
            prompt=request.prompt,
            response=ai_response
        )
        logger.info("Chat saved successfully")

        return ResponseHandler.success_response(
            data={"response": ai_response},
            message="Chat processed successfully",
            code=200
        )
    except ValueError as ve:
        logger.error(f"Error in chat endpoint: {str(ve)}")
        return ResponseHandler.error_response(
            message=str(ve),
            code=400
        )
    except Exception as e:
        return ResponseHandler.error_response(
            message=str(e),
            code=500
        )
    
@router.get("/history", response_model=dict)
async def get_chat_history(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(10, description="Number of records to fetch"),
    model_name: str = Query(None, description="Filter by model name")
):
    """
    Retrieves chat history for a specific user.

    Args:
        user_id (str): ID of the user whose chat history is being fetched.
        limit (int): Number of records to retrieve (default: 10).
        model_name (str, optional): Filter by AI model name.

    Returns:
        dict: List of chat history records.
    """
    try:
        query = ChatHistory.filter(user_id=user_id).order_by("created_at").limit(limit)  # ✅ Fixed Query

        if model_name:
            query = query.filter(model_name=model_name)

        history = await query

        if not history:  # ✅ Handle case where no history exists
            return ResponseHandler.success_response(
                data=[],
                message="No chat history found for this user.",
                code=200
            )

        return ResponseHandler.success_response(
            data=[{
                "id": str(chat.id),
                "user_id": str(chat.user_id),
                "role": chat.role,
                "model": chat.model_name,
                "prompt": chat.prompt,
                "response": chat.response,
                "created_at": chat.created_at.isoformat()
            } for chat in history],
            message="Chat history retrieved successfully",
            code=200
        )
    except Exception as e:
        return ResponseHandler.error_response(
            message=f"Error retrieving chat history: {str(e)}",
            code=500
        )
