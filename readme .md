# 💊 MediScan AI: Medicine & Tablet Identifier

MediScan AI is an intelligent medical assistance and pharmaceutical awareness web application built with **Python**, **Streamlit**, and **Google Gemini Flash**. 

Users can upload an image or capture a live webcam photo of any medicine, tablet blister pack, capsule, or prescription bottle. The application leverages Google Gemini Flash's high-speed multimodal vision capabilities to detect the medication and provide comprehensive clinical details—including its **purpose**, **therapeutic benefits**, **harmful facts & side effects**, **contraindications**, and **safe usage instructions**.

---

## 🌟 Key Features

- **Multimodal Image Recognition**: Accepts image uploads (`JPG`, `JPEG`, `PNG`, `WEBP`) or live camera captures.
- **Detailed Clinical Breakdown**:
  - **Medicine Identification**: Generic compound, brand names, drug class, and dosage form.
  - **Purpose & Indications**: Exactly what illness, condition, or symptoms the medicine is prescribed for.
  - **Therapeutic Benefits**: How the medicine functions in the body and expected health relief.
  - **Harmful Facts & Warnings**: Common side effects, critical adverse reactions, contraindications (pregnancy, renal/hepatic issues), and harmful drug/food interactions.
  - **Usage & Storage Guidelines**: Proper administration tips and safe storage conditions.
- **Multilingual Support**: Supports reports in English, Urdu (اردو), Spanish, Hindi, Arabic, and French.
- **Downloadable Reports**: Export generated medicine safety reports directly as Markdown (`.md`).
- **Flexible SDK Support**: Compatible with both modern `google-genai` and legacy `google-generativeai`.
- **Integrated Medical Safety Disclaimer**: Prominently guides users to verify all information with certified healthcare professionals.

---

## 📁 Project Structure

```text
mediscan-ai/
│
├── app.py                # Main Streamlit web application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation and deployment guide
└── .streamlit/           # Optional local secrets folder
    └── secrets.toml      # Local API key storage (do not commit to Git)
```

---

## 🚀 Quickstart: Local Setup

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your machine.
- A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone or Download the Project
```bash
git clone https://github.com/your-username/mediscan-ai.git
cd mediscan-ai
```

### 3. Create and Activate a Virtual Environment
```bash
# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your Gemini API Key
You can configure your API key in one of three ways:
1. **In-App Sidebar**: Enter your key directly into the password field when the app is running.
2. **Environment Variable**:
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"   # Linux/macOS
   set GEMINI_API_KEY="your_actual_api_key_here"      # Windows CMD
   $env:GEMINI_API_KEY="your_actual_api_key_here"     # Windows PowerShell
   ```
3. **Streamlit Secrets File**:
   Create a folder named `.streamlit` and add a file named `secrets.toml`:
   ```toml
   # .streamlit/secrets.toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🐙 How to Push the Code to GitHub

Follow these steps to publish your code to a new GitHub repository:

### Step 1: Initialize Git and Ignore Secrets
Create a `.gitignore` file so your secret keys and virtual environment are never pushed online:
```bash
# Create .gitignore
cat <<EOF > .gitignore
venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
EOF
```

### Step 2: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: MediScan AI Streamlit application"
```

### Step 3: Create a New GitHub Repository
1. Go to [GitHub](https://github.com/) and click **New Repository**.
2. Name your repository (e.g., `mediscan-ai`).
3. Set the repository visibility to **Public** (required for free Streamlit Community Cloud hosting) or **Private**.
4. Leave "Add a README file" unchecked (you already have one).
5. Click **Create repository**.

### Step 4: Link and Push
Copy the repository URL from GitHub and run:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mediscan-ai.git
git push -u origin main
```

---

## ☁️ How to Deploy on Streamlit Community Cloud

Streamlit Community Cloud offers free, seamless hosting for Streamlit applications directly linked to GitHub:

1. **Sign in to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and click **Continue with GitHub**.
2. **Create a New App**:
   - Click **Create app** (or **New app**).
   - Select **I already have an app**.
3. **Configure App Repository**:
   - **Repository**: Select `YOUR_USERNAME/mediscan-ai`.
   - **Branch**: `main`.
   - **Main file path**: `app.py`.
4. **Configure Secrets (Crucial for API Key)**:
   - Click **Advanced settings...** before deploying (or go to **Settings > Secrets** after creating).
   - In the **Secrets** text box, enter your Gemini API key:
     ```toml
     GEMINI_API_KEY = "AIzaSy..."
     ```
   - Click **Save**.
5. **Deploy**:
   - Click **Deploy!**.
   - Streamlit will automatically install dependencies from `requirements.txt` and launch your live web application with a shareable URL (e.g., `https://mediscan-ai.streamlit.app`).

---

## ⚠️ Important Medical & Legal Disclaimer

> **MediScan AI is strictly an informational and educational prototype.**  
> It is not a certified medical device and does not provide formal medical diagnosis, clinical prescriptions, or healthcare treatment recommendations. Pill appearance (size, shape, color, scoring) can be shared by multiple drugs or counterfeit formulations. Always verify medications with a licensed physician or pharmacist. In case of an emergency, contact your local emergency medical service immediately.
