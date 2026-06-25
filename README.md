# Smart-Cart AI Diet Agent

An intelligent, stateless web application built to help users plan optimized, macro-targeted meals based on live local grocery market prices and accurate nutritional data. 

The app calculates precise ingredient portions to meet a specified protein target while strictly staying within a defined financial budget (INR), calculating costs based on real-world upfront commercial packet sizes.

---

## Features

* **Stateless Optimization Architecture:** Zero user tracking, no databases, and absolute privacy. Every request builds a fresh context loop.
* **Dynamic Meal Scoping:** Supports customized meal planning across **Breakfast, Lunch, Dinner, and Snacks**.
* **Real-World Costing Engine:** Budgets expenditure based on minimum retail pack sizes (e.g., pricing a full 200g paneer packet or 1kg flour pack rather than theoretical linear grams).
* **Culinary Blueprint Generation:** Returns exact preparation weights, financial checkout metrics, and streamlined cooking steps using the latest AI models.

---

## Tech Stack

* **Frontend:** Streamlit (Python-based interactive UI)
* **Backend API:** FastAPI (High-performance async Python framework)
* **AI Engine:** Google GenAI SDK (`gemini-3.5-flash`)
* **Package Management:** Python Virtual Environments (`venv`)

---

## Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Bhavana-Krishnan/Smart_Cart_AI_Agent.git](https://github.com/Bhavana-Krishnan/Smart_Cart_AI_Agent.git)
cd Smart_Cart_AI_Agent
