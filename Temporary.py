from fastapi import FastAPI, Body
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Initialize FastAPI app
app = FastAPI(title="Ollama Conversational History Service")

# Memory to store conversation
memory = ConversationBufferMemory()

# Use Ollama local model (make sure Ollama is installed and running)
llm = ChatOllama(model="llama2")   # you can change to "mistral", "codellama", etc.

# Conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

@app.post("/chat/")
async def chat(user_input: str = Body(..., embed=True)):
    """
    Accepts user input, stores conversation in memory,
    and returns AI response along with history.
    """
    response = conversation.run(user_input)
    return {
        "user_input": user_input,
        "ai_response": response,
        "history": memory.load_memory_variables({})["history"]
    }

@app.get("/history/")
async def get_history():
    """
    Retrieves complete conversational history.
    """
    return {"history": memory.load_memory_variables({})["history"]}

@app.post("/reset/")
async def reset_history():
    """
    Clears the conversation history.
    """
    global memory, conversation
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    return {"message": "History reset successfully"}
