# 🧮 Budget Planner App

A modular, planner-grade budgeting tool built with **Streamlit**, **Plotly**, and **Python**. Designed for financial educators, planners, and DIY budgeters, this app helps users visualize monthly spending, track savings goals, and receive dynamic Planner’s Notes based on their financial behavior.

---

## 🚀 Features

- **CSV Upload + Manual Entry**: Combine uploaded expenses with on-the-fly manual inputs.
- **Clean Modular Design**: Split into simulation, visuals, and notes for scalability and clarity.
- **Interactive Visuals**: Pie and bar charts powered by Plotly for intuitive category analysis.
- **Planner’s Notes Engine**: Generates personalized insights based on income, spending, and goals.
- **Streamlit UI**: Responsive layout with sidebar inputs and metric cards.

---

## 🧩 Modular Structure

| Module               | Description                                           |
|----------------------|-------------------------------------------------------|
| `budget_simulator.py` | Loads, cleans, and summarizes expense data            |
| `budget_visuals.py`   | Generates interactive Plotly charts                   |
| `budget_notes.py`     | Produces dynamic Planner’s Notes based on behavior    |
| `app.py`              | Streamlit interface tying everything together         |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/budget-planner-app.git
cd budget-planner-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
