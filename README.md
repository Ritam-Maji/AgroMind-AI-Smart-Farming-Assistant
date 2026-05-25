# 🌾 AgroMind AI — Intelligent Smart Farming Assistant

AgroMind AI is an AI-powered smart farming assistant designed to help farmers make intelligent, data-driven agricultural decisions using deep learning, weather analytics, and predictive AI.

The platform combines plant disease detection, crop and fertilizer recommendation, weather-based advisory, yield prediction, and real-time farming assistance into a single software-only ecosystem.

---

## 🚀 Features

### 📷 AI-Powered Plant Disease Detection
- Upload crop/leaf images
- Detect diseases using fine-tuned ResNet CNN model
- Confidence score prediction
- Explainable AI with highlighted infected regions (Grad-CAM)

### 🌦️ Smart Weather Intelligence
- 7-day weather forecasting
- Weather-based farming alerts
- Rain, heatwave, and humidity risk notifications

### 🌱 Crop & Fertilizer Recommendation
- Soil-aware crop suggestions
- Fertilizer planning system
- Modes:
  - Low-Cost Farming
  - Organic Farming
  - High-Yield Farming

### 📈 Yield Prediction System
- Predict expected crop yield
- Risk assessment based on:
  - Weather
  - Disease impact
  - Soil conditions

### 🧠 Daily Farming Advisor
Generates intelligent daily farming action plans such as:
- Irrigation timing
- Spraying recommendations
- Fertilizer scheduling

### 🗣️ Voice Assistant Support
- Voice-based interaction
- Multilingual support (English, Hindi, Bengali)

### 🗺️ Nearby Fertilizer Shop Finder
- Map-based nearby shop discovery
- OpenStreetMap integration
- Smart fertilizer suggestions

### 💳 Stripe Payment Integration
Integrated Stripe payment gateway for:
- Premium advisory subscriptions
- AI consultation services
- Marketplace/fertilizer purchases
- Secure online payments

---

# 🏗️ System Architecture

```bash
Frontend (Streamlit)
        ↓
FastAPI Backend
        ↓
AI/ML Models (PyTorch)
        ↓
SQLite / MongoDB
        ↓
External APIs
(Weather + Maps + Stripe)
```

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- FastAPI
- Python

## Machine Learning
- PyTorch
- Scikit-learn
- OpenCV
- NumPy
- Pandas

## APIs & Services
- OpenWeatherMap API
- OpenStreetMap API
- Stripe Payment Gateway

## Database
- SQLite
- MongoDB

---

# 🧠 AI Models Used

| Module | Model |
|--------|------|
| Disease Detection | ResNet50 (Transfer Learning) |
| Yield Prediction | Random Forest |
| Fertilizer Recommendation | Random Forest |
| Explainable AI | Grad-CAM |

---

# 📂 Project Structure

```bash
AgroMind-AI/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── routes/
│   └── services/
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── assets/
│
├── ml_models/
│   ├── disease_detection/
│   ├── yield_prediction/
│   └── fertilizer_recommendation/
│
├── datasets/
├── notebooks/
├── payments/
│   └── stripe/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/AgroMind-AI.git
cd AgroMind-AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux/Mac
```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

## Start Backend

```bash
uvicorn app:app --reload
```

## Start Frontend

```bash
streamlit run app.py
```

---

# 💳 Stripe Payment Setup

## Install Stripe SDK

```bash
pip install stripe
```

## Add Stripe Keys

Create `.env` file:

```env
STRIPE_SECRET_KEY=your_secret_key
STRIPE_PUBLIC_KEY=your_public_key
```

## Example Stripe Payment Intent

```python
import stripe

stripe.api_key = "YOUR_SECRET_KEY"

payment_intent = stripe.PaymentIntent.create(
    amount=5000,
    currency="inr",
)
```

---

# 📊 Dataset

Recommended dataset:
- PlantVillage Dataset
- Custom crop disease datasets from Kaggle

---

# 🔒 Future Enhancements

- AI chatbot for farmers
- Satellite imagery analysis
- Market price prediction
- Smart farming analytics dashboard
- Government scheme recommendation engine

---

# 🌍 Real-World Impact

AgroMind AI aims to:
- Reduce crop loss
- Improve agricultural productivity
- Support sustainable farming
- Provide accessible AI tools for farmers

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Developed by Ritam Maji

---

# ⭐ Support

If you like this project, give it a ⭐ on GitHub!
