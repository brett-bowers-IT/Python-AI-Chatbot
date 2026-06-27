from openai import OpenAI
import json

client = OpenAI(api_key = "OPENAI_API_KEY") # INSERT OPENAI API KEY

with open(r"C:\Users\Brett\Python\AI Chatbot\user_profile.json", "r") as file:
    user_profile = json.load(file)

with open(r"C:\Users\Brett\Python\AI Chatbot\memory.json", "r") as file:
    messages = json.load(file)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:

    user_input = input("You: ")

    # COMMAND /exit
    if user_input.lower() == "/exit":
        break

    # COMMAND /clear
    if user_input.lower() == "/clear":
        messages = []

        with open(r"C:\Users\Brett\Python\AI Chatbot\memory.json", "w") as file:
            json.dump(messages, file)

        print("Memory Cleared.")
        continue
   
    # COMMAND /remember name = Brett
    if user_input.lower().startswith("/remember"):
        fact = user_input[10:]
        key, value = fact.split("=")
        user_profile[key.strip()] = value.strip()

        with open(r"C:\Users\Brett\Python\AI Chatbot\user_profile.json", "w") as file:
            json.dump(user_profile, file, indent=4)

        print("Memory Saved")
        continue

    # COMMAND /profile
    if user_input.lower() == "/profile":
        print(user_profile)
        continue
    
    messages.append({"role": "user", "content": user_input})

    profile_context = f"""
    User Profile:
    {json.dumps(user_profile, indent=2)}
    """
    conversation = [
        {
            "role": "system",
            "content": profile_context
        }
    ] + messages

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # API CALL
    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = conversation
    )
    
    bot_reply = response.choices[0].message.content

    print("Bot:", bot_reply)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # MEMORY MANAGEMENT
    messages.append({"role": "assistant", "content": bot_reply})
    if len(messages) > 20:
        messages[:] = messages[-20:]

    with open(r"C:\Users\Brett\Python\AI Chatbot\memory.json", "w") as file:
        json.dump(messages, file, indent=4)


   
   
   
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
# Framework:
# import open AI tools so Python can use
# Create connection client to OpenAI API
# Create infinite loop until manually stopped
# Wait for user input
# API call. Send message -> Wait for response
# AI Model Selection
# Conversation Messages, Message Structure, Role Type
# Extract first AI response text

# Add Basic Memory:
# Store chat, isolate every request
# input → memory → API → response → memory → loop

# Load Memory on startup using JSON file
# Open, Read, Convert to Python, Save memory after each message,
# Write, Convert Python objects to JSON, Make file readable/formatted
# PROBLEM: Messages grows forever, TOKEN LIMITS & COSTS, needs to be managed via memory limit aka "Sliding Window Memory"
# SOLUTION: Keep only the newest 20 messages
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
#PHASE 1: Sliding Window Memory
#PHASE 2: Special Commands /clear /save /exit
#PHASE 3: Long term memory extraction (remember important facts permanently)



