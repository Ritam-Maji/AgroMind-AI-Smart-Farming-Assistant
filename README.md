# 🌾 AgroMind AI — Intelligent Smart Farming Assistant

AgroMind AI is an AI-powered smart farming assistant designed to help farmers make intelligent, data-driven agricultural decisions using deep learning, weather analytics, and predictive AI.

The platform combines plant disease detection, crop and fertilizer recommendation, weather-based advisory, yield prediction, and real-time farming assistance with secure payment integration for seamless farmer and customer transactions from nearby fertilizer shop into a single software-only ecosystem.

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

# 📸 Screenshots
## 🏠 Dashboard
<img width="2487" height="1350" alt="Screenshot 2026-05-26 125431" src="https://github.com/user-attachments/assets/bb7fb57f-b56d-4ba5-8bf4-aa328498c01f" />
## 📷 Disease Detection

<img width="2435" height="1287" alt="Screenshot 2026-05-26 125913" src="https://github.com/user-attachments/assets/b8500fbc-30f3-46d4-99b9-42c06226ff12" />
## 🌦️ Weather Intelligence

<img width="2404" height="1350" alt="Screenshot 2026-05-26 130224" src="https://github.com/user-attachments/assets/fb1af386-8db7-4952-9b17-2ff65b646c59" />
## 🧪 Fertilizer Advisor

<img width="2413" height="1348" alt="Screenshot 2026-05-26 130125" src="https://github.com/user-attachments/assets/aedcd2a9-e765-4bba-9aad-56f2b8a344ae" />
## 💳 Stripe Payment Integration

<img width="2374" height="1253" alt="Screenshot 2026-05-26 131109" src="https://github.com/user-attachments/assets/a4f13620-bb9a-424f-8e51-da60cbffd10b" />
## 📈 Yield Prediction

<img width="2395" height="916" alt="Screenshot 2026-05-26 130659" src="https://github.com/user-attachments/assets/1ffefb92-9cf9-4e6c-b237-a1e011f552bd" />
## 🗣️ AgroMind Voice Assistant

<img width="2375" height="1338" alt="Screenshot 2026-05-26 191646" src="https://github.com/user-attachments/assets/c1bd124e-37c1-4662-be22-0841d8e469e2" />

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
