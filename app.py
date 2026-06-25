# app.py
import streamlit as st
import requests

# Set up clean, responsive page layout
st.set_page_config(page_title="Smart-Cart AI Agent", page_icon="🥗", layout="centered")

st.title("🥗 Smart-Cart AI Diet Agent")
st.subheader("Plan optimal meals based on real market rates")
st.markdown("---")

# Sidebar inputs for a clean user interface
st.sidebar.header("🎯 Target Constraints")
budget = st.sidebar.slider("Maximum Budget (INR)", min_value=30, max_value=1000, value=200, step=10)
protein_target = st.sidebar.slider("Minimum Protein (Grams)", min_value=10, max_value=100, value=25, step=5)

# 🌟 Add a meal type dropdown selection
meal_type = st.sidebar.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

st.markdown(f"### What do you want to eat for {meal_type.lower()}?")
user_ingredients = st.text_input(
    label="Mention your base ingredients:",
    value="chana and wheat flour" if meal_type in ["Lunch", "Dinner"] else "paneer and muesli",
    placeholder="e.g., chicken and rice, paneer and wheat flour, eggs..."
)

# 🌟 Dynamically pass the meal_type into the prompt string
constructed_prompt = f"Plan a {meal_type.lower()} using {user_ingredients}. I need at least {protein_target}g of protein, but my budget is strictly {budget} INR max."
st.markdown("#### Preview of the agent's instructions:")
st.caption(f'"{constructed_prompt}"')

st.markdown("---")

# Execution trigger button
if st.button("🚀 Let Agent Plan Meal", type="primary"):
    with st.spinner("🧠 Agent is searching market prices and calculating nutritional profiles..."):
        try:
            # Pings your running local FastAPI backend endpoint
            backend_url = "http://127.0.0.1:8000/plan"
            payload = {"prompt": constructed_prompt}
            
            response = requests.post(backend_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                agent_text = result.get("agent_response", "No response text received.")
                
                st.success("✅ Optimization Complete!")
                
                # Render the markdown recipe cleanly with beautiful spacing
                # st.markdown("### 📋 Your Optimized Meal Plan")
                st.markdown(agent_text)
                
            else:
                st.error(f"❌ Backend Error (Status Code: {response.status_code})")
                st.json(response.json())
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to FastAPI server. Make sure your backend is running on `http://127.0.0.1:8000` via Uvicorn!")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {str(e)}")

st.markdown("---")
st.caption("Powered by FastAPI + Gemini 2.5 Flash Lite + Streamlit Architecture.")