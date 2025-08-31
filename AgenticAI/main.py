from fastapi import FastAPI
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory

# Initialize FastAPI app
app = FastAPI(title="Conversation History API")

# LangChain memory to store conversations
memory = ConversationBufferMemory(return_messages=True)

# Request/Response models
class Message(BaseModel):
    sender: str
    text: str

class ConversationResponse(BaseModel):
    history: list

@app.post("/send_message", response_model=ConversationResponse)
def send_message(msg: Message):
    """
    Store a message in the conversation history.
    """
    memory.chat_memory.add_user_message(f"{msg.sender}: {msg.text}")
    return {"history": [m.content for m in memory.chat_memory.messages]}

@app.get("/history", response_model=ConversationResponse)
def get_history():
    """
    Retrieve the entire conversation history.
    """
    return {"history": [m.content for m in memory.chat_memory.messages]}

@app.post("/clear")
def clear_history():
    """
    Clear the conversation history.
    """
    memory.clear()
    return {"status": "cleared"}
