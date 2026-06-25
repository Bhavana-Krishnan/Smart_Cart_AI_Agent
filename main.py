# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# Import our custom tools
import tools

app = FastAPI(
    title="Smart-Cart AI Agent",
    description="An autonomous AI agent managing meal planning constraints",
    version="1.0.0"
)

# Initialize GenAI Client (Make sure GEMINI_API_KEY is set in your venv terminal!)
client = genai.Client()

# Define what our API input looks like using Pydantic
class PlanRequest(BaseModel):
    prompt: str  # Example: "Plan a high protein breakfast with ragi and paneer under 150 INR"

# Mapping tool names to their actual python functions
AVAILABLE_TOOLS = {
    "search_market_price": tools.search_market_price,
    "get_nutrition_profile": tools.get_nutrition_profile,
    "calculate_live_cart": tools.calculate_live_cart
}


SYSTEM_INSTRUCTION = """
You are an elite, autonomous Smart-Cart AI Diet Agent and Culinary Expert. Your goal is to plan a highly optimized meal (breakfast, lunch, dinner, or snack) within a user's budget and protein targets based on their request.

CRITICAL WORKFLOW:
1. Identify the requested ingredients and the specific meal type requested (e.g., lunch, dinner).
2. Call `get_nutrition_profile` for each ingredient to fetch cooked/prepared protein metrics per 100g.
3. Call `search_market_price` to check current Bangalore market rates.
4. Calculate the exact weights needed to hit the protein target without exceeding the budget.

CRITICAL REAL-WORLD COSTING RULE:
When calculating the final "Total Cost", you must calculate based on full commercial pack sizes, NOT just the grams eaten. 
If the user consumes 10g of paneer, you must budget the cost for a full 200g packet (approx ₹76). 
If they consume 50g of flour, budget a full 1kg packet (approx ₹60). 
Label this clearly in the final summary as "Upfront Cart Cost".

OUTPUT FORMAT REQUIREMENTS:
You must present the final layout in a beautiful, user-friendly recipe format appropriate for that meal type. Structure your response exactly like this:

### 🥗 Your Optimized Meal Plan
*Provide a 1-sentence encouraging summary of the culinary dish.*

#### 🛒 Ingredients & Preparation Weights
* **[Ingredient Name]**: [X]g ([Y]g protein) — *Specify if this weight is dry/raw or cooked/prepared.*

#### 📊 Financial & Macro Summary
* **Total Protein:** [X]g / [Target]g
* **Total Cost:** ₹[X] (Budget: ₹[Target])

#### 🍳 Quick Culinary Instructions
*Provide a brief, step-by-step preparation guide on how the user should combine these calculated weights into a delicious, edible meal suitable for the requested meal type (e.g., how to simmer a lunch curry, prep a dinner stir-fry, or assemble a snack bowl).*
"""


@app.post("/plan")
def run_agent(request: PlanRequest):
    try:
        registered_tools = [tools.search_market_price, tools.get_nutrition_profile, tools.calculate_live_cart]
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=registered_tools,
            temperature=0.1
        )
        
        # Create an official managed chat session
        chat = client.chats.create(
            model='gemini-2.5-flash',
            config=config
        )
        
        # Send the initial goal to start the chat session
        response = chat.send_message(request.prompt)
        
        # The Agent Loop: Run while Gemini requests tools
        max_steps = 5
        steps = 0
        
        while response.function_calls and steps < max_steps:
            steps += 1
            print(f"\n🤖 [Step {steps}] Agent requested tool execution...")
            tool_responses = []
            
            for call in response.function_calls:
                tool_name = call.name
                tool_args = call.args
                print(f"👉 Executing {tool_name} locally with args: {tool_args}")
                
                if tool_name in AVAILABLE_TOOLS:
                    # Run our python tool
                    executed_result = AVAILABLE_TOOLS[tool_name](**tool_args)
                    
                    # Package the result using the explicit Part function
                    tool_responses.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response=executed_result
                        )
                    )
                else:
                    print(f"⚠️ Tool {tool_name} not found.")
            
            # Send the tool responses back into the active chat session context
            response = chat.send_message(tool_responses)
            
        return {
            "status": "success",
            "agent_response": response.text
        }

    except Exception as e:
        print(f"❌ Error encountered: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))