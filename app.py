"""
MediScan AI - Medicine & Tablet Identifier
Built with Streamlit & Google Gemini Flash.
Analyzes medicine images to identify purpose, benefits, harmful facts/side effects, and precautions.
"""

import io
import os
import sys
import time
from typing import Optional, Tuple
from PIL import Image
import streamlit as st

# Check for Google GenAI SDK availability (modern vs legacy)
HAS_GENAI = False
HAS_LEGACY_GENAI = False

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    import google.generativeai as legacy_genai
    HAS_LEGACY_GENAI = True
except ImportError:
    HAS_LEGACY_GENAI = False


# Set Page Configuration
st.set_page_config(
    page_title="MediScan AI - Medicine & Tablet Guide",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished medical theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #0e7490;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .disclaimer-card {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        color: #78350f;
    }
    .info-card {
        background-color: #f0fdf4;
        border-left: 5px solid #10b981;
        padding: 0.9rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #064e3b;
    }
    .warning-card {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 0.9rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #7f1d1d;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #0d9488 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-size: 1.05rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #0f766e 100%);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def get_api_key() -> str:
    """Retrieve Gemini API Key from secrets, env vars, or session state."""
    # 1. Check Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # 2. Check environment variable
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        return env_key
    
    # 3. Check session state (set from sidebar)
    return st.session_state.get("gemini_api_key", "")


def build_medical_prompt(target_language: str, user_notes: str = "") -> str:
    """Construct structured clinical prompt for Gemini Flash."""
    notes_section = f"\nUser Additional Notes / Inquiry:\n\"{user_notes}\"\n" if user_notes else ""
    
    prompt = f"""You are a licensed clinical pharmacist and pharmaceutical identification specialist.
A user has provided an image of a medicine, tablet, capsule, blister pack, syrup bottle, or prescription packaging.
Carefully inspect the image, identify any visible text, imprint codes, brand names, color, shape, strength, and packaging.

{notes_section}

Please formulate your response in **{target_language}** using clean, professional Markdown with clear section headings, bullet points, and high readability.

Organize your analysis into the following exact sections:

### 1. 🔍 Medicine Identification
- **Generic Name (Active Ingredient):** State the scientific/generic compound(s).
- **Brand / Trade Names:** List common commercial names (including the one visible in the image if identifiable).
- **Strength & Dosage Form:** (e.g., 500mg Film-Coated Tablet, 250mg/5ml Suspension, Capsule).
- **Drug Classification:** (e.g., NSAID, Broad-Spectrum Antibiotic, Antihypertensive, Antihistamine).
*(Note: If the image is blurry, ambiguous, or unidentifiable, explicitly inform the user and suggest closest possibilities based on visual cues, warning them not to rely on uncertain identification).*

### 2. 🎯 Purpose & Medical Uses (What is it used for?)
- Detail the primary health conditions, illnesses, or symptoms this medication is approved to treat.
- Explain under what conditions doctors typically prescribe it.

### 3. ✨ Benefits & Therapeutic Action (How it helps)
- Explain in simple, understandable terms how this medicine works inside the human body.
- Highlight the key expected therapeutic benefits and symptoms relief.

### 4. ⚠️ Harmful Facts, Risks & Side Effects
- **Common Mild Side Effects:** (e.g., nausea, mild headache, drowsiness, dry mouth).
- **Serious Adverse Reactions:** Warning signs that require stopping the drug and contacting a doctor immediately.
- **Contraindications & Who Should NOT Take It:** (e.g., pregnancy, nursing, kidney/liver impairment, asthma, peptic ulcers).
- **Harmful Interactions:** Negative interactions with alcohol, specific food items, or other medications.
- **Overdose & Misuse Risks:** Clear warning regarding the danger of exceeding recommended limits.

### 5. 🛡️ Safe Usage Guidelines & Storage
- General administration guidelines (e.g., take with plenty of water, take after meals, do not crush extended-release tablets).
- Proper storage conditions (temperature, moisture, direct sunlight, keep out of reach of children).

### 6. 🚨 Important Clinical Disclaimer
- Emphasize clearly that this AI analysis is for informational and educational awareness only.
- Remind the user that AI visual identification can make errors and must NEVER replace a professional doctor's prescription or licensed pharmacist's verification.
"""
    return prompt


def analyze_with_google_genai(
    image_bytes: bytes,
    mime_type: str,
    api_key: str,
    model_name: str,
    prompt: str
) -> str:
    """Analyze image using modern google-genai SDK."""
    client = genai.Client(api_key=api_key)
    
    # Modern SDK content payload
    contents = [
        types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        ),
        prompt
    ]
    
    response = client.models.generate_content(
        model=model_name,
        contents=contents
    )
    return response.text


def analyze_with_legacy_genai(
    image: Image.Image,
    api_key: str,
    model_name: str,
    prompt: str
) -> str:
    """Analyze image using google-generativeai SDK fallback."""
    legacy_genai.configure(api_key=api_key)
    model = legacy_genai.GenerativeModel(model_name=model_name)
    response = model.generate_content([prompt, image])
    return response.text


def generate_medicine_analysis(
    image: Image.Image,
    image_bytes: bytes,
    mime_type: str,
    api_key: str,
    model_name: str,
    target_language: str,
    user_notes: str
) -> str:
    """Unified entry point for Gemini image analysis with fallback handling."""
    if not api_key:
        raise ValueError("API Key is missing. Please enter your Gemini API key in the sidebar.")
    
    prompt = build_medical_prompt(target_language=target_language, user_notes=user_notes)
    
    # Try modern google-genai SDK first
    if HAS_GENAI:
        try:
            return analyze_with_google_genai(
                image_bytes=image_bytes,
                mime_type=mime_type,
                api_key=api_key,
                model_name=model_name,
                prompt=prompt
            )
        except Exception as e:
            # If modern SDK fails, try legacy if available
            if HAS_LEGACY_GENAI:
                return analyze_with_legacy_genai(
                    image=image,
                    api_key=api_key,
                    model_name=model_name,
                    prompt=prompt
                )
            raise e
            
    # If only legacy SDK is installed
    elif HAS_LEGACY_GENAI:
        return analyze_with_legacy_genai(
            image=image,
            api_key=api_key,
            model_name=model_name,
            prompt=prompt
        )
    else:
        raise ImportError(
            "Neither `google-genai` nor `google-generativeai` is installed. "
            "Please run: pip install google-genai pillow"
        )


def main():
    # Header Section
    st.markdown('<div class="main-header">💊 MediScan AI: Medicine & Tablet Guide</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Upload or take a photo of any tablet, capsule, or medicine box to discover its purpose, benefits, harmful effects, and safety guidelines.</div>',
        unsafe_allow_html=True
    )
    
    # Mandatory Safety Banner
    st.markdown("""
    <div class="disclaimer-card">
        <strong>⚠️ Crucial Medical & Safety Disclaimer:</strong><br>
        MediScan AI is an educational tool designed to assist with informational awareness. 
        It <strong>does not provide medical advice, diagnosis, or prescriptions</strong>. 
        Visual recognition may misidentify pills of similar shape or color. 
        Always consult a certified physician or licensed pharmacist before starting, changing, or discontinuing any medication.
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Configurations
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key handling
        stored_key = get_api_key()
        api_key_input = st.text_input(
            "Gemini API Key",
            value=stored_key,
            type="password",
            placeholder="AIzaSy...",
            help="Get your free key from Google AI Studio (https://aistudio.google.com/)"
        )
        if api_key_input:
            st.session_state["gemini_api_key"] = api_key_input
            active_key = api_key_input
        else:
            active_key = stored_key

        if active_key:
            st.success("✅ Gemini API Key detected", icon="🔑")
        else:
            st.warning("⚠️ Please provide a Gemini API Key to run analysis.")

        st.divider()

        # Model Selection
        model_name = st.selectbox(
            "Gemini Flash Model",
            options=["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
            index=0,
            help="Gemini 2.5 Flash is recommended for high-speed, multimodal vision analysis."
        )

        # Language Selection
        target_language = st.selectbox(
            "Output Language",
            options=["English", "Urdu (اردو)", "Spanish (Español)", "Hindi (हिंदी)", "Arabic (العربية)", "French (Français)"],
            index=0
        )

        st.divider()
        with st.expander("ℹ️ How to get a free API Key"):
            st.markdown("""
            1. Visit [Google AI Studio](https://aistudio.google.com/).
            2. Sign in with your Google Account.
            3. Click **Get API key** and create a new key.
            4. Paste the key above or save it in your project's `.streamlit/secrets.toml` as:
            ```toml
            GEMINI_API_KEY = "your_api_key_here"
            ```
            """)

        with st.expander("💡 Tips for Best Results"):
            st.markdown("""
            - Ensure good lighting and sharp focus.
            - Keep medicine name and dosage numbers readable.
            - Include the blister pack or outer packaging when possible.
            - Avoid blurry or shadowed angles.
            """)

    # Main Input Area
    col1, col2 = st.columns([1, 1], gap="large")

    image_source = None
    uploaded_image = None
    image_bytes = None
    mime_type = "image/jpeg"

    with col1:
        st.subheader("📸 Provide Medicine Picture")
        input_method = st.radio(
            "Choose Image Input Method:",
            options=["📁 Upload File", "📷 Live Camera Snap"],
            horizontal=True
        )

        if input_method == "📁 Upload File":
            image_source = st.file_uploader(
                "Upload tablet or packaging photo",
                type=["jpg", "jpeg", "png", "webp"],
                help="Supported formats: JPG, JPEG, PNG, WEBP"
            )
        else:
            image_source = st.camera_input("Take a photo of the tablet or packaging")

        user_notes = st.text_area(
            "Optional: Specific question or health context",
            placeholder="e.g., 'Is this safe for someone with diabetes?' or 'What is the dosage for fever?'",
            help="Add any specific questions you want the AI pharmacist to address."
        )

        analyze_button = st.button("🔍 Identify & Analyze Medicine", use_container_width=True)

    with col2:
        st.subheader("🖼️ Image Preview")
        if image_source is not None:
            try:
                # Read bytes and open with Pillow
                image_bytes = image_source.getvalue()
                uploaded_image = Image.open(io.BytesIO(image_bytes))
                
                # Determine mime type
                if hasattr(image_source, "type") and image_source.type:
                    mime_type = image_source.type
                else:
                    mime_type = "image/jpeg"

                st.image(
                    uploaded_image,
                    caption=f"Selected Picture ({uploaded_image.width}x{uploaded_image.height} px)",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error loading image: {e}")
        else:
            st.info("👆 Please upload a picture or capture a photo from the left panel to begin.")

    # Execution & Results Section
    if analyze_button:
        if not image_source or not image_bytes or not uploaded_image:
            st.error("❌ Please upload or capture an image of the medicine first.")
            return

        if not active_key:
            st.error("❌ Missing Gemini API Key. Please enter your API key in the sidebar.")
            return

        st.divider()
        st.subheader("📋 Comprehensive Medicine Details & Safety Report")

        with st.spinner("🤖 Gemini Flash is inspecting the tablet and consulting pharmaceutical data..."):
            start_time = time.time()
            try:
                report_markdown = generate_medicine_analysis(
                    image=uploaded_image,
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    api_key=active_key,
                    model_name=model_name,
                    target_language=target_language,
                    user_notes=user_notes
                )
                elapsed = time.time() - start_time

                # Metrics banner
                st.success(f"Analysis completed in {elapsed:.2f} seconds using {model_name}!", icon="✅")

                # Display Result
                st.markdown(report_markdown)

                # Downloadable Report
                st.divider()
                st.download_button(
                    label="📥 Download Medicine Safety Report (.md)",
                    data=report_markdown,
                    file_name="mediscan_report.md",
                    mime="text/markdown",
                    use_container_width=False
                )

            except Exception as ex:
                st.error(f"⚠️ Analysis Failed: {str(ex)}")
                st.info(
                    "Troubleshooting tip: Check your API key validity, ensure your model quota is active, "
                    "or verify that the image format is supported."
                )


if __name__ == "__main__":
    main()
