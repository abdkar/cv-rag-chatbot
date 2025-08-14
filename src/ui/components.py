"""
UI Components module for CV RAG Chatbot.
Contains all UI-related functions and styling.
"""

import base64
import os
import sys
from typing import Optional

# Add the parent directory to sys.path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from configs.app_config import config


def load_profile_image() -> str:
    """
    Load profile image and convert to base64.
    
    Returns:
        Base64 encoded image string
    """
    import os
    
    # Get the project root directory (assuming we're in src/ui/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    profile_paths = config.ui.profile_photo_paths or []
    for profile_path in profile_paths:
        absolute_path = profile_path  # Initialize with original path
        try:
            # Convert relative path to absolute path
            if not os.path.isabs(profile_path):
                absolute_path = os.path.join(project_root, profile_path)
            else:
                absolute_path = profile_path
                
            with open(absolute_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            print(f"Failed to load image from {absolute_path}: {e}")
            continue
    return ""


def inject_custom_css():
    """Inject custom CSS styling for the application."""
    
    banner_b64 = load_profile_image()
    
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Global animations and variables */
:root {{
    --primary-color: #003147;
    --secondary-color: #5b9bd5;
    --accent-color: #194bfb;
    --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --glass-bg: rgba(255, 255, 255, 0.95);
    --shadow-light: 0 8px 32px rgba(31, 38, 135, 0.15);
    --shadow-medium: 0 12px 40px rgba(31, 38, 135, 0.25);
    --shadow-heavy: 0 16px 48px rgba(31, 38, 135, 0.35);
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes slideInRight {{
    from {{
        opacity: 0;
        transform: translateX(30px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes pulse {{
    0%, 100% {{
        transform: scale(1);
        opacity: 1;
    }}
    50% {{
        transform: scale(1.05);
        opacity: 0.8;
    }}
}}

@keyframes float {{
    0%, 100% {{
        transform: translateY(0px);
    }}
    50% {{
        transform: translateY(-10px);
    }}
}}

@keyframes shimmer {{
    0% {{
        background-position: -200% 0;
    }}
    100% {{
        background-position: 200% 0;
    }}
}}

@keyframes gradient-shift {{
    0%, 100% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
}}

/* Global styling */
html, body, [class*="css"] {{ 
    font-family: 'Poppins', 'Inter', sans-serif; 
    scroll-behavior: smooth;
}}

.block-container {{ 
    max-width: 1400px !important; 
    padding-top: 1rem !important; 
    padding-bottom: 2rem !important;
    animation: fadeInUp 0.8s ease-out;
}}

/* Enhanced background */
body {{ 
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
    background-size: 400% 400%;
    animation: gradient-shift 15s ease infinite;
    min-height: 100vh;
}}

/* Glass morphism main container */
.main .block-container {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 2rem;
    margin-top: 0.5rem;
    box-shadow: var(--shadow-heavy);
    border: 1px solid rgba(255, 255, 255, 0.3);
    position: relative;
    overflow: hidden;
}}

.main .block-container::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 300% 100%;
    animation: shimmer 3s linear infinite;
}}

/* Hide footer */
footer {{ visibility: hidden !important; }}

/* Enhanced profile container */
.profile-container {{
    background: linear-gradient(135deg, #003147 0%, #004968 50%, #005580 100%);
    padding: 2.5rem;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-heavy);
    animation: fadeInUp 0.8s ease-out 0.2s both;
}}

.profile-container::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
    background-size: 200% 200%;
    animation: shimmer 4s ease-in-out infinite;
    pointer-events: none;
}}

/* Floating profile photo */
.profile-photo {{
    width: 160px;
    height: 160px;
    border-radius: 50%;
    margin: 0 auto 1.5rem auto;
    background: url(data:image/jpeg;base64,{banner_b64}) center top 1px/cover no-repeat;
    border: 5px solid rgba(255,255,255,0.9);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3), 0 5px 15px rgba(0,0,0,0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: float 6s ease-in-out infinite;
    position: relative;
    z-index: 2;
}}

.profile-photo:hover {{
    transform: scale(1.08) rotate(5deg);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 8px 20px rgba(0,0,0,0.25);
}}

/* Animated skill tags */
.skill-tag {{
    background: linear-gradient(135deg, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0.15) 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 4px;
    display: inline-block;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}}

.skill-tag:hover {{
    transform: translateY(-3px) scale(1.05);
    background: linear-gradient(135deg, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.25) 100%);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}}

.skill-tag::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}}

.skill-tag:hover::before {{
    left: 100%;
}}

/* Enhanced chat message styling */
div[data-testid="stChatMessage"] {{ 
    border-radius: 20px; 
    padding: 1.5rem 2rem; 
    margin-bottom: 1.5rem; 
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    animation: slideInRight 0.6s ease-out;
    position: relative;
    overflow: hidden;
}}

div[data-testid="stChatMessage"]:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}}

div[data-testid="stChatMessage"] p {{ 
    margin-bottom: 0.5rem; 
    line-height: 1.7;
    font-weight: 400;
}}

/* Assistant messages with gradient */
div[data-testid="stChatMessage"][data-testid*="assistant"], 
div[data-testid="stChatMessage"].assistant-msg {{
    background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(248,250,255,0.95) 50%, rgba(240,245,255,0.95) 100%); 
    border-left: 5px solid var(--secondary-color);
    box-shadow: var(--shadow-light);
}}

div[data-testid="stChatMessage"][data-testid*="assistant"]::before,
div[data-testid="stChatMessage"].assistant-msg::before {{
    content: '🤖';
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 1.2rem;
    opacity: 0.7;
    animation: pulse 2s ease-in-out infinite;
}}

/* User messages with gradient */
div[data-testid="stChatMessage"][data-testid*="user"], 
div[data-testid="stChatMessage"].user-msg {{ 
    background: linear-gradient(145deg, rgba(25,75,251,0.08) 0%, rgba(91,155,213,0.12) 50%, rgba(64,123,255,0.08) 100%); 
    border-left: 5px solid var(--accent-color);
    box-shadow: var(--shadow-light);
}}

div[data-testid="stChatMessage"][data-testid*="user"]::before,
div[data-testid="stChatMessage"].user-msg::before {{
    content: '👤';
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 1.2rem;
    opacity: 0.7;
}}

/* Enhanced buttons with 3D effect */
.stButton > button {{
    background: linear-gradient(145deg, var(--primary-color) 0%, #004968 50%, #005580 100%);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    box-shadow: 0 6px 20px rgba(0, 49, 71, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.stButton > button::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}}

.stButton > button:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 30px rgba(0, 49, 71, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
    background: linear-gradient(145deg, #004968 0%, #005580 50%, #0066a0 100%);
}}

.stButton > button:hover::before {{
    left: 100%;
}}

.stButton > button:active {{
    transform: translateY(-1px) scale(0.98);
    box-shadow: 0 5px 15px rgba(0, 49, 71, 0.3);
}}

/* Enhanced quick start buttons */
.stButton > button[kind="secondary"] {{
    background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(248,250,255,0.9) 100%);
    color: var(--primary-color);
    border: 2px solid rgba(91,155,213,0.3);
    font-weight: 500;
}}

.stButton > button[kind="secondary"]:hover {{
    background: linear-gradient(145deg, rgba(91,155,213,0.1) 0%, rgba(64,123,255,0.15) 100%);
    border-color: var(--secondary-color);
    color: var(--accent-color);
}}

/* Beautiful scrollbar */
::-webkit-scrollbar {{ width: 12px; }}
::-webkit-scrollbar-track {{ 
    background: rgba(255, 255, 255, 0.1); 
    border-radius: 10px;
}}
::-webkit-scrollbar-thumb {{ 
    background: linear-gradient(145deg, var(--secondary-color), var(--accent-color)); 
    border-radius: 10px; 
    border: 2px solid rgba(255,255,255,0.2);
}}
::-webkit-scrollbar-thumb:hover {{ 
    background: linear-gradient(145deg, #82a8d6, var(--secondary-color)); 
}}

/* Enhanced info boxes */
.stInfo {{
    background: linear-gradient(145deg, rgba(25, 75, 251, 0.08) 0%, rgba(255, 255, 255, 0.9) 50%, rgba(91, 155, 213, 0.08) 100%);
    border-left: 4px solid var(--secondary-color);
    border-radius: 15px;
    backdrop-filter: blur(15px);
    padding: 1rem 1.5rem;
    box-shadow: var(--shadow-light);
    animation: fadeInUp 0.6s ease-out;
}}

.stSuccess {{
    background: linear-gradient(145deg, rgba(40, 167, 69, 0.08) 0%, rgba(255, 255, 255, 0.9) 50%, rgba(40, 167, 69, 0.08) 100%);
    border-left: 4px solid #28a745;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow: var(--shadow-light);
}}

.stWarning {{
    background: linear-gradient(145deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 255, 255, 0.9) 50%, rgba(255, 193, 7, 0.08) 100%);
    border-left: 4px solid #ffc107;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow: var(--shadow-light);
}}

.stError {{
    background: linear-gradient(145deg, rgba(220, 53, 69, 0.08) 0%, rgba(255, 255, 255, 0.9) 50%, rgba(220, 53, 69, 0.08) 100%);
    border-left: 4px solid #dc3545;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    box-shadow: var(--shadow-light);
}}

/* Sidebar enhancements */
.css-1d391kg {{
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,255,0.95) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(91,155,213,0.2);
    box-shadow: 4px 0 20px rgba(31, 38, 135, 0.1);
}}

.css-1d391kg .stSelectbox > div > div {{
    background: rgba(255,255,255,0.8);
    border: 2px solid rgba(91,155,213,0.2);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}}

.css-1d391kg .stFileUploader {{
    border: 2px dashed rgba(91,155,213,0.3);
    border-radius: 15px;
    padding: 1rem;
    background: rgba(255,255,255,0.5);
    transition: all 0.3s ease;
}}

.css-1d391kg .stFileUploader:hover {{
    border-color: var(--secondary-color);
    background: rgba(91,155,213,0.1);
}}

/* Text input enhancements */
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.9);
    border: 2px solid rgba(91,155,213,0.2);
    border-radius: 15px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}}

.stTextInput > div > div > input:focus {{
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 3px rgba(91,155,213,0.1);
    background: rgba(255,255,255,1);
}}

/* Social links styling with hover effects */
.social-links-container {{
    animation: fadeInUp 0.8s ease-out 0.4s both;
}}

.social-links-container a > div {{
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border-radius: 12px;
}}

.social-links-container a > div:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}}

.social-links-container a > div:hover svg {{
    transform: scale(1.1);
    transition: transform 0.3s ease;
}}

.social-links-container a > div:active {{
    transform: translateY(-1px) scale(0.98);
}}

/* Quick start section */
.quick-start-section {{
    animation: fadeInUp 0.8s ease-out 0.6s both;
}}

/* Knowledge base status */
.kb-status-container {{
    animation: slideInRight 0.8s ease-out 0.8s both;
}}

/* Loading animation */
.stSpinner > div {{
    border-top-color: var(--secondary-color) !important;
}}

/* Custom loading dots */
.loading-dots {{
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
}}

.loading-dots div {{
    position: absolute;
    top: 33px;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: var(--secondary-color);
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
}}

.loading-dots div:nth-child(1) {{
    left: 8px;
    animation: loading-dots1 0.6s infinite;
}}

.loading-dots div:nth-child(2) {{
    left: 8px;
    animation: loading-dots2 0.6s infinite;
}}

.loading-dots div:nth-child(3) {{
    left: 32px;
    animation: loading-dots2 0.6s infinite;
}}

.loading-dots div:nth-child(4) {{
    left: 56px;
    animation: loading-dots3 0.6s infinite;
}}

@keyframes loading-dots1 {{
    0% {{ transform: scale(0); }}
    100% {{ transform: scale(1); }}
}}

@keyframes loading-dots3 {{
    0% {{ transform: scale(1); }}
    100% {{ transform: scale(0); }}
}}

@keyframes loading-dots2 {{
    0% {{ transform: translate(0, 0); }}
    100% {{ transform: translate(24px, 0); }}
}}

/* Responsive design */
@media (max-width: 768px) {{
    .profile-container {{
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    .profile-photo {{
        width: 120px;
        height: 120px;
    }}
    
    .skill-tag {{
        padding: 6px 12px;
        font-size: 0.8rem;
    }}
    
    div[data-testid="stChatMessage"] {{
        padding: 1rem 1.5rem;
    }}
    
    .stButton > button {{
        padding: 0.6rem 1.2rem;
        font-size: 0.9rem;
    }}
}}

@media (max-width: 480px) {{
    .profile-container {{
        padding: 1rem;
    }}
    
    .profile-photo {{
        width: 100px;
        height: 100px;
    }}
    
    .main .block-container {{
        padding: 1rem;
        border-radius: 20px;
    }}
}}

/* Dark mode support */
@media (prefers-color-scheme: dark) {{
    .main .block-container {{
        background: rgba(20, 20, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    div[data-testid="stChatMessage"][data-testid*="assistant"],
    div[data-testid="stChatMessage"].assistant-msg {{
        background: linear-gradient(145deg, rgba(40,40,50,0.9) 0%, rgba(50,50,60,0.9) 100%);
        color: #e0e0e0;
    }}
}}

/* Performance optimizations */
* {{
    will-change: auto;
}}

.profile-photo,
.stButton > button,
.skill-tag {{
    will-change: transform;
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


def render_profile_section():
    """Render the enhanced profile section with photo and animated information."""
    st.markdown(f"""
    <div class='profile-container'>
        <div class='profile-photo'></div>
        <h1 style='font-size: 2rem; margin-bottom: 0.5rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            Abdolamir Karbalaie
        </h1>
        <div style='margin-bottom: 1.5rem;'>
            <span class='skill-tag'> AI Engineer</span>
            <span class='skill-tag'> RAG & GenAI</span>
            <span class='skill-tag'> MLOps</span>
            <span class='skill-tag'> LLM Safety</span>
        </div>
        <p style='font-size: 1rem; line-height: 1.6; opacity: 0.95; max-width: 600px; margin: 0 auto; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>
            Senior AI Engineer and Data Scientist specializing in <strong>Retrieval Augmented Generation</strong>, 
            <strong>MLOps</strong>, and <strong>reliable AI systems development</strong>. 
            Passionate about creating intelligent solutions that bridge the gap between cutting-edge research and real-world applications.
        </p>
        <div style='margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;'>
            💬 Ask about experience, architecture decisions, measurable impact, leadership, or AI system reliability
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_social_links():
    """Render professional social media links with real platform icons."""
    st.markdown("""
    <div class='social-links-container'>
        <h3 style='color: #003147; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center;'>
            🔗 Professional Links
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    social_links = config.ui.social_links
    if social_links:
        cols = st.columns(len(social_links))
        for i, (platform, url) in enumerate(social_links.items()):
            with cols[i]:
                if platform == "LinkedIn":
                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="background: linear-gradient(135deg, #0077B5 0%, #005885 100%); 
                                   color: white; padding: 12px; border-radius: 12px; text-align: center; 
                                   transition: all 0.3s ease; margin-bottom: 8px;
                                   box-shadow: 0 4px 15px rgba(0,119,181,0.3);
                                   cursor: pointer; position: relative; overflow: hidden;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-bottom: 4px;">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                            <br><strong>LinkedIn</strong>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                elif platform == "GitHub":
                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="background: linear-gradient(135deg, #333 0%, #24292e 100%); 
                                   color: white; padding: 12px; border-radius: 12px; text-align: center; 
                                   transition: all 0.3s ease; margin-bottom: 8px;
                                   box-shadow: 0 4px 15px rgba(36,41,46,0.3);
                                   cursor: pointer; position: relative; overflow: hidden;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-bottom: 4px;">
                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                            </svg>
                            <br><strong>GitHub</strong>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                elif platform == "Google Scholar":
                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="background: linear-gradient(135deg, #4285F4 0%, #1976D2 100%); 
                                   color: white; padding: 12px; border-radius: 12px; text-align: center; 
                                   transition: all 0.3s ease; margin-bottom: 8px;
                                   box-shadow: 0 4px 15px rgba(66,133,244,0.3);
                                   cursor: pointer; position: relative; overflow: hidden;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-bottom: 4px;">
                                <path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/>
                            </svg>
                            <br><strong>Scholar</strong>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                elif platform == "Web of Science":
                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); 
                                   color: white; padding: 12px; border-radius: 12px; text-align: center; 
                                   transition: all 0.3s ease; margin-bottom: 8px;
                                   box-shadow: 0 4px 15px rgba(30,136,229,0.3);
                                   cursor: pointer; position: relative; overflow: hidden;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-bottom: 4px;">
                                <path d="M3 12c0-4.97 4.03-9 9-9s9 4.03 9 9c0 3.83-2.39 7.1-5.77 8.41L12 15l-3.23 5.41C5.39 19.1 3 15.83 3 12z" fill="#8B5CF6"/>
                                <path d="M12 3C7.03 3 3 7.03 3 12c0 1.45.32 2.83.9 4.06L12 8l8.1 8.06c.58-1.23.9-2.61.9-4.06 0-4.97-4.03-9-9-9z" fill="#10B981"/>
                                <circle cx="12" cy="12" r="3" fill="white"/>
                            </svg>
                            <br><strong>Web of Science</strong>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)


def render_quick_start_buttons() -> Optional[str]:
    """
    Render enhanced quick start question buttons with animations.
    
    Returns:
        Selected question text or None
    """
    st.markdown("""
    <div class='quick-start-section'>
        <h3 style='color: #003147; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center;'>
            ⚡ Quick Start Questions
        </h3>
        <p style='color: #666; margin-bottom: 1.5rem; font-size: 0.9rem;'>
            Click any button below to start exploring my professional experience and capabilities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    suggested_query = None
    
    with col1:
        if st.button("End-to-End ML", use_container_width=True, key="ml_exp"):
            suggested_query = "Tell me about your end-to-end machine learning experience and the complete ML lifecycle projects you've delivered"
    
    with col2:
        if st.button("Technical Skills", use_container_width=True, key="tech_skills"):
            suggested_query = "What are your core technical skills and expertise areas? Tell me about your proficiency with different technologies and frameworks"
    
    with col3:
        if st.button("AI Reliability", use_container_width=True, key="reliability"):
            suggested_query = "How do you ensure reliability, safety, and robustness in AI systems? What practices do you follow for responsible AI development?"
    
    with col4:
        if st.button("RAG Systems", use_container_width=True, key="rag_exp"):
            suggested_query = "Tell me about your experience with RAG (Retrieval Augmented Generation) development, deployment, and optimization"
    
    return suggested_query


def render_sidebar_controls():
    """
    Render sidebar controls for file upload and settings.
    
    Returns:
        Tuple of (use_uploaded, uploaded_file)
    """
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Vector source selection
        st.subheader("📊 Vector Source")
        use_uploaded = st.radio(
            "Choose content source:",
            options=[False, True],
            format_func=lambda x: "📄 Knowledge Base" if not x else "📤 Uploaded File",
            help="Switch between your base knowledge and uploaded file vectors"
        )
        
        # File upload section
        st.subheader("📁 Upload CV/Resume")
        uploaded_file = st.file_uploader(
            "Choose your CV/Resume file",
            type=["txt", "pdf"],
            help="Upload a TXT or PDF file to add to the knowledge base"
        )
        
        return use_uploaded, uploaded_file


def render_knowledge_base_status():
    """Render current knowledge base status information with enhanced styling."""
    from src.utils.file_processing import get_content_stats
    
    st.markdown("""
    <div class='kb-status-container'>
        <h4 style='color: #003147; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center;'>
            📊 Knowledge Base Status
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Check both old and new paths for knowledge base
        kb_paths = [config.paths.knowledge_base_file, "knowledge_base.txt"]
        kb_content = None
        
        for kb_path in kb_paths:
            if os.path.exists(kb_path):
                with open(kb_path, "r", encoding="utf-8") as f:
                    kb_content = f.read()
                break
        
        if kb_content:
            stats = get_content_stats(kb_content)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(40,167,69,0.1) 0%, rgba(255,255,255,0.9) 100%); 
                       padding: 1rem; border-radius: 12px; margin-bottom: 1rem; 
                       border-left: 4px solid #28a745; backdrop-filter: blur(10px);'>
                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.2rem; margin-right: 0.5rem;'>📄</span>
                    <strong style='color: #28a745;'>Base Knowledge</strong>
                </div>
                <div style='font-size: 0.9rem; color: #666;'>
                    📝 {stats['characters']:,} characters • 📖 {stats['words']:,} words
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Check uploaded content
        upload_paths = [config.paths.uploaded_content_file, "uploaded_content.txt"]
        for upload_path in upload_paths:
            if os.path.exists(upload_path):
                with open(upload_path, "r", encoding="utf-8") as f:
                    uploaded_content = f.read()
                stats = get_content_stats(uploaded_content)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(25,75,251,0.1) 0%, rgba(255,255,255,0.9) 100%); 
                           padding: 1rem; border-radius: 12px; margin-bottom: 1rem; 
                           border-left: 4px solid #194bfb; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <span style='font-size: 1.2rem; margin-right: 0.5rem;'>📤</span>
                        <strong style='color: #194bfb;'>Uploaded Content</strong>
                    </div>
                    <div style='font-size: 0.9rem; color: #666;'>
                        📝 {stats['characters']:,} characters • 📖 {stats['words']:,} words
                    </div>
                </div>
                """, unsafe_allow_html=True)
                break
            
    except FileNotFoundError:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255,193,7,0.1) 0%, rgba(255,255,255,0.9) 100%); 
                   padding: 1rem; border-radius: 12px; margin-bottom: 1rem; 
                   border-left: 4px solid #ffc107; backdrop-filter: blur(10px);'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.2rem; margin-right: 0.5rem;'>⚠️</span>
                <span style='color: #856404;'>Knowledge base file not found</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_success_message(message: str):
    """Show an enhanced success message with animation."""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(40,167,69,0.1) 0%, rgba(255,255,255,0.95) 100%); 
               border-left: 5px solid #28a745; border-radius: 15px; padding: 1rem 1.5rem; 
               margin: 1rem 0; backdrop-filter: blur(15px); 
               box-shadow: 0 4px 20px rgba(40,167,69,0.15);
               animation: fadeInUp 0.5s ease-out;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 1.3rem; margin-right: 0.75rem; animation: pulse 1.5s ease-in-out infinite;'>✅</span>
            <span style='color: #155724; font-weight: 500; font-size: 1rem;'>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_error_message(message: str):
    """Show an enhanced error message with animation."""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(220,53,69,0.1) 0%, rgba(255,255,255,0.95) 100%); 
               border-left: 5px solid #dc3545; border-radius: 15px; padding: 1rem 1.5rem; 
               margin: 1rem 0; backdrop-filter: blur(15px); 
               box-shadow: 0 4px 20px rgba(220,53,69,0.15);
               animation: fadeInUp 0.5s ease-out;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 1.3rem; margin-right: 0.75rem; animation: pulse 1.5s ease-in-out infinite;'>❌</span>
            <span style='color: #721c24; font-weight: 500; font-size: 1rem;'>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_warning_message(message: str):
    """Show an enhanced warning message with animation."""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(255,193,7,0.1) 0%, rgba(255,255,255,0.95) 100%); 
               border-left: 5px solid #ffc107; border-radius: 15px; padding: 1rem 1.5rem; 
               margin: 1rem 0; backdrop-filter: blur(15px); 
               box-shadow: 0 4px 20px rgba(255,193,7,0.15);
               animation: fadeInUp 0.5s ease-out;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 1.3rem; margin-right: 0.75rem; animation: pulse 1.5s ease-in-out infinite;'>⚠️</span>
            <span style='color: #856404; font-weight: 500; font-size: 1rem;'>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_info_message(message: str):
    """Show an enhanced info message with animation."""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(25,75,251,0.1) 0%, rgba(255,255,255,0.95) 100%); 
               border-left: 5px solid #194bfb; border-radius: 15px; padding: 1rem 1.5rem; 
               margin: 1rem 0; backdrop-filter: blur(15px); 
               box-shadow: 0 4px 20px rgba(25,75,251,0.15);
               animation: fadeInUp 0.5s ease-out;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 1.3rem; margin-right: 0.75rem; animation: pulse 1.5s ease-in-out infinite;'>ℹ️</span>
            <span style='color: #004085; font-weight: 500; font-size: 1rem;'>{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_loading_animation(message: str = "Processing your request..."):
    """Show a beautiful loading animation."""
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.9); 
               border-radius: 20px; margin: 1rem 0; backdrop-filter: blur(15px);'>
        <div class='loading-dots' style='margin: 0 auto 1rem auto;'>
            <div></div><div></div><div></div><div></div>
        </div>
        <p style='color: #003147; font-weight: 500; margin: 0; font-size: 1.1rem;'>{message}</p>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Please wait while I analyze and respond...</p>
    </div>
    """, unsafe_allow_html=True)


def render_chat_header():
    """Render the main chat interface header."""
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0; animation: fadeInUp 0.8s ease-out;'>
        <h2 style='color: #003147; font-weight: 700; font-size: 2.2rem; margin-bottom: 0.5rem;'>
            💬 Chat with my AI Professional Persona
        </h2>
        <p style='color: #666; font-size: 1.1rem; line-height: 1.6; max-width: 800px; margin: 0 auto;'>
            Ask about experience, architecture decisions, measurable impact, leadership, or how I deliver reliable AI systems. 
            <br><span style='font-weight: 500; color: #003147;'>Answers are strictly grounded in my curated professional knowledge base (RAG retrieval).</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
