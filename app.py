import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import openai
from openai import OpenAI
from PIL import Image
import os
import json
from dateutil import tz
from dotenv import load_dotenv
from fortune_engine import FortuneEngine
from partner_matcher import PartnerMatcher
from face_generator import FaceGenerator

# Load environment variables
load_dotenv()

# Configure OpenAI API - basic approach to avoid compatibility issues
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Set global API key for older-style usage
    openai.api_key = api_key
    # Create client with minimal parameters - avoid incompatible 'proxies'
    try:
        client = OpenAI(api_key=api_key)
    except TypeError as e:
        print(f"Warning: Could not initialize OpenAI client: {e}")
        client = None

# Check if using Azure OpenAI
if os.getenv("AZURE_OPENAI_API_KEY"):
    # Azure OpenAI 설정
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Set the page config
st.set_page_config(
    page_title="Mystic Harmony - East Meets West Fortune",
    page_icon="🔮",
    layout="wide"
)

# App styling
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #7047A3;
        font-family: 'Arial', sans-serif;
    }
    .stButton button {
        background-color: #7047A3;
        color: white;
        border-radius: 10px;
    }
    .reading-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .fortune-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .element-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Eastern Astrology Functions
def get_chinese_zodiac(year):
    zodiac_animals = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 
                       'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
    return zodiac_animals[(year - 4) % 12]

def get_celestial_stem(year):
    stems = ['Yang Wood', 'Yin Wood', 'Yang Fire', 'Yin Fire', 'Yang Earth', 
             'Yin Earth', 'Yang Metal', 'Yin Metal', 'Yang Water', 'Yin Water']
    return stems[(year - 4) % 10]

def get_five_elements(birth_date, time_of_day):
    # This is a simplified version - a real implementation would be more complex
    month = birth_date.month
    day = birth_date.day
    
    elements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
    
    # Primary element based on month
    primary_element = elements[(month - 1) % 5]
    
    # Secondary element based on day
    secondary_element = elements[(day - 1) % 5]
    
    # Tertiary element based on time
    time_mapping = {
        'dawn': 'Wood',
        'morning': 'Fire',
        'noon': 'Earth',
        'afternoon': 'Metal',
        'evening': 'Water'
    }
    tertiary_element = time_mapping.get(time_of_day, 'Earth')
    
    return primary_element, secondary_element, tertiary_element

# Western Astrology Functions
def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

def get_astrological_house(birth_hour):
    # This is a simplified version - real house determination requires more data
    houses = {
        1: "Identity and Self-Image",
        2: "Values and Possessions",
        3: "Communication and Immediate Environment",
        4: "Home and Family",
        5: "Creativity and Pleasure",
        6: "Health and Service",
        7: "Partnerships and Relationships",
        8: "Transformation and Shared Resources",
        9: "Higher Learning and Beliefs",
        10: "Career and Public Image",
        11: "Friendships and Goals",
        12: "Spirituality and Subconscious"
    }
    
    # Simplified house calculation based only on hour
    house_number = (birth_hour % 12) + 1
    return house_number, houses[house_number]

def get_moon_phase(birth_date):
    # This is a simplified algorithm - a real implementation would use astronomical calculations
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    
    # Simplified lunar calculation (not astronomically accurate but works for prototyping)
    if month < 3:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = int(a / 4)
    c = 2 - a + b
    e = int(365.25 * (year + 4716))
    f = int(30.6001 * (month + 1))
    jd = c + day + e + f - 1524.5
    
    days_since_new_moon = (jd % 29.53) # Lunar cycle is approximately 29.53 days
    
    if days_since_new_moon < 3.69:
        return "New Moon"
    elif days_since_new_moon < 7.38:
        return "Waxing Crescent"
    elif days_since_new_moon < 11.07:
        return "First Quarter"
    elif days_since_new_moon < 14.76:
        return "Waxing Gibbous"
    elif days_since_new_moon < 18.45:
        return "Full Moon"
    elif days_since_new_moon < 22.14:
        return "Waning Gibbous"
    elif days_since_new_moon < 25.83:
        return "Last Quarter"
    else:
        return "Waning Crescent"

# Combined Astrology Reading Functions
def generate_combined_profile(chinese_zodiac, celestial_stem, five_elements, 
                              zodiac_sign, moon_phase, house_info):
    """Generate a basic profile without using external APIs"""
    
    primary_element, secondary_element, tertiary_element = five_elements
    house_number, house_meaning = house_info
    
    # Basic personality traits
    chinese_traits = {
        'Rat': 'quick-witted, resourceful, and adaptable',
        'Ox': 'diligent, dependable, and determined',
        'Tiger': 'brave, confident, and competitive',
        'Rabbit': 'quiet, elegant, and kind',
        'Dragon': 'strong, proud, and enigmatic',
        'Snake': 'wise, intuitive, and introspective',
        'Horse': 'energetic, independent, and passionate',
        'Goat': 'gentle, compassionate, and creative',
        'Monkey': 'intelligent, witty, and versatile',
        'Rooster': 'observant, hardworking, and confident',
        'Dog': 'loyal, honest, and reliable',
        'Pig': 'compassionate, generous, and diligent'
    }
    
    zodiac_traits = {
        'Aries': 'pioneering, courageous, and enthusiastic',
        'Taurus': 'reliable, patient, and determined',
        'Gemini': 'adaptable, outgoing, and curious',
        'Cancer': 'emotional, intuitive, and protective',
        'Leo': 'creative, passionate, and generous',
        'Virgo': 'analytical, practical, and meticulous',
        'Libra': 'diplomatic, fair-minded, and cooperative',
        'Scorpio': 'passionate, resourceful, and brave',
        'Sagittarius': 'optimistic, freedom-loving, and philosophical',
        'Capricorn': 'responsible, disciplined, and self-controlled',
        'Aquarius': 'progressive, original, and independent',
        'Pisces': 'compassionate, artistic, and intuitive'
    }
    
    element_traits = {
        'Wood': 'growth, creativity, and flexibility',
        'Fire': 'passion, energy, and transformation',
        'Earth': 'stability, practicality, and nurturing',
        'Metal': 'precision, efficiency, and structure',
        'Water': 'intuition, emotion, and adaptability'
    }
    
    moon_influences = {
        'New Moon': 'new beginnings and setting intentions',
        'Waxing Crescent': 'gathering strength and focus',
        'First Quarter': 'taking action and overcoming challenges',
        'Waxing Gibbous': 'refining and perfecting your path',
        'Full Moon': 'illumination and heightened intuition',
        'Waning Gibbous': 'gratitude and sharing with others',
        'Last Quarter': 'release and letting go',
        'Waning Crescent': 'surrender and reflection'
    }
    
    # Combine all elements into a comprehensive reading
    profile = f"""## Your Celestial Harmony Reading

### Eastern Astrology Insights
You were born in the year of the **{chinese_zodiac}**, under the influence of **{celestial_stem}**. This makes you {chinese_traits.get(chinese_zodiac, 'unique and multifaceted')}. 

Your elemental makeup is primarily **{primary_element}** ({element_traits.get(primary_element, '')}), with secondary influences of **{secondary_element}** and **{tertiary_element}**. This combination gives you a natural affinity for balancing {element_traits.get(primary_element, '')} with {element_traits.get(secondary_element, '')}.

### Western Astrology Insights
Your sun sign is **{zodiac_sign}**, making you {zodiac_traits.get(zodiac_sign, 'unique and multifaceted')}. 

You were born during a **{moon_phase}** phase, which influences your life with {moon_influences.get(moon_phase, 'unique emotional patterns')}. 

Your birth hour places emphasis on the **{house_number}th House** of {house_meaning}, suggesting that matters of {house_meaning.lower()} play a significant role in your life journey.

### Combined Reading
The harmonious blend of **{chinese_zodiac}** and **{zodiac_sign}** energies creates a unique soul signature that is both {chinese_traits.get(chinese_zodiac, '').split(', ')[0]} and {zodiac_traits.get(zodiac_sign, '').split(', ')[0]}. Your **{primary_element}** element strengthens your {zodiac_traits.get(zodiac_sign, '').split(', ')[1]} nature.

Throughout your life, you'll find that your greatest strengths emerge when you embrace both your {chinese_traits.get(chinese_zodiac, '').split(', ')[1]} Eastern nature and your {zodiac_traits.get(zodiac_sign, '').split(', ')[2]} Western qualities. The **{moon_phase}** moon phase of your birth suggests that you're particularly gifted in {moon_influences.get(moon_phase, '').split(' and ')[0]}.

Your life path weaves together Eastern wisdom and Western insight, creating a tapestry that is uniquely yours. By honoring both traditions, you unlock a deeper understanding of your true potential.
"""
    return profile

def generate_compatibility_profile(user_profile, chinese_zodiac, celestial_stem, 
                                  zodiac_sign, elements):
    """Generate compatibility insights without using external APIs"""
    
    # Complementary zodiac signs in Chinese astrology
    chinese_compatibility = {
        'Rat': ['Dragon', 'Monkey'],
        'Ox': ['Snake', 'Rooster'],
        'Tiger': ['Horse', 'Dog'],
        'Rabbit': ['Sheep', 'Pig'],
        'Dragon': ['Rat', 'Monkey'],
        'Snake': ['Ox', 'Rooster'],
        'Horse': ['Tiger', 'Dog'],
        'Goat': ['Rabbit', 'Pig'],
        'Monkey': ['Rat', 'Dragon'],
        'Rooster': ['Ox', 'Snake'],
        'Dog': ['Tiger', 'Horse'],
        'Pig': ['Rabbit', 'Sheep']
    }
    
    # Complementary zodiac signs in Western astrology
    western_compatibility = {
        'Aries': ['Leo', 'Sagittarius', 'Gemini', 'Aquarius'],
        'Taurus': ['Virgo', 'Capricorn', 'Cancer', 'Pisces'],
        'Gemini': ['Libra', 'Aquarius', 'Aries', 'Leo'],
        'Cancer': ['Scorpio', 'Pisces', 'Taurus', 'Virgo'],
        'Leo': ['Aries', 'Sagittarius', 'Gemini', 'Libra'],
        'Virgo': ['Taurus', 'Capricorn', 'Cancer', 'Scorpio'],
        'Libra': ['Gemini', 'Aquarius', 'Leo', 'Sagittarius'],
        'Scorpio': ['Cancer', 'Pisces', 'Virgo', 'Capricorn'],
        'Sagittarius': ['Aries', 'Leo', 'Libra', 'Aquarius'],
        'Capricorn': ['Taurus', 'Virgo', 'Scorpio', 'Pisces'],
        'Aquarius': ['Gemini', 'Libra', 'Sagittarius', 'Aries'],
        'Pisces': ['Cancer', 'Scorpio', 'Capricorn', 'Taurus']
    }
    
    # Complementary elements in Eastern philosophy
    element_compatibility = {
        'Wood': ['Water', 'Earth'],
        'Fire': ['Wood', 'Earth'],
        'Earth': ['Fire', 'Metal'],
        'Metal': ['Earth', 'Water'],
        'Water': ['Metal', 'Wood']
    }
    
    # Get compatible signs
    compatible_chinese = chinese_compatibility.get(chinese_zodiac, ['various signs'])
    compatible_western = western_compatibility.get(zodiac_sign, ['various signs'])
    primary_element, _, _ = elements
    compatible_elements = element_compatibility.get(primary_element, ['various elements'])
    
    # Generate compatibility profile
    compatibility = f"""## Your Ideal Partner Profile

### Eastern Astrology Compatibility
Based on your **{chinese_zodiac}** sign, you have natural harmony with those born in the years of the **{compatible_chinese[0]}** and **{compatible_chinese[1]}**. These connections bring balance to your {chinese_zodiac} nature.

Your **{primary_element}** element is nourished by partners with **{compatible_elements[0]}** or **{compatible_elements[1]}** elemental influences, creating a relationship of mutual growth and support.

### Western Astrology Compatibility
Your **{zodiac_sign}** sun sign forms strong connections with **{compatible_western[0]}**, **{compatible_western[1]}**, and potentially **{compatible_western[2]}** signs. These relationships offer both harmony and the right amount of contrast to help you grow.

### Your Ideal Partner
The stars suggest that your most harmonious relationship would be with someone who embodies both Eastern and Western complementary energies to your own. This person would likely have:

- A nurturing yet independent spirit
- A balance of practical wisdom and emotional intelligence
- The ability to understand your unique blend of {zodiac_sign} and {chinese_zodiac} energies
- Natural affinities with either {compatible_elements[0]} or {compatible_western[0]} qualities

This person would appreciate your authentic self and create space for both closeness and personal growth. They would understand when to support you and when to challenge you, creating a relationship that evolves over time.

Your connection would be characterized by mutual respect, shared values, and a deep understanding that transcends cultural boundaries, bringing together the best of both Eastern and Western perspectives on love and partnership.
"""
    return compatibility

def generate_partner_description(chinese_zodiac, zodiac_sign, elements):
    """Generate a description of the ideal partner without using external APIs"""
    
    primary_element, secondary_element, _ = elements
    
    # Physical traits based on Western zodiac
    physical_traits = {
        'Aries': 'athletic build, confident stance, and expressive eyes that radiate determination',
        'Taurus': 'strong, grounded appearance with warm eyes and a welcoming smile',
        'Gemini': 'expressive face, bright eyes, and an animated, youthful appearance',
        'Cancer': 'soft features, caring eyes, and a warm, nurturing presence',
        'Leo': 'confident posture, radiant smile, and striking, memorable features',
        'Virgo': 'neat appearance, thoughtful eyes, and precise, elegant movements',
        'Libra': 'symmetrical features, graceful movements, and a balanced, harmonious presence',
        'Scorpio': 'intense gaze, magnetic presence, and mysterious, compelling features',
        'Sagittarius': 'open, friendly expression, athletic build, and an adventurous aura',
        'Capricorn': 'distinguished features, composed demeanor, and an aura of quiet authority',
        'Aquarius': 'unique style, expressive eyes, and an distinctive, unforgettable presence',
        'Pisces': 'dreamy eyes, gentle movements, and an otherworldly, artistic appearance'
    }
    
    # Personality traits based on Chinese zodiac
    personality_traits = {
        'Rat': 'clever mind, adaptable nature, and resourceful approach to life',
        'Ox': 'reliable character, patient disposition, and steadfast loyalty',
        'Tiger': 'passionate spirit, brave heart, and natural leadership abilities',
        'Rabbit': 'gentle soul, refined tastes, and diplomatic communication style',
        'Dragon': 'charismatic presence, confident outlook, and visionary thinking',
        'Snake': 'wise perspective, intuitive understanding, and elegant sophistication',
        'Horse': 'free-spirited energy, sociable nature, and straightforward honesty',
        'Goat': 'creative imagination, compassionate heart, and artistic sensibilities',
        'Monkey': 'quick wit, problem-solving genius, and playful enthusiasm',
        'Rooster': 'practical mind, attention to detail, and confident self-expression',
        'Dog': 'loyal heart, protective instincts, and principled character',
        'Pig': 'generous spirit, honest communication, and appreciative enjoyment of life'
    }
    
    # Elemental influences on character
    element_influences = {
        'Wood': 'growth-oriented mindset, flexible thinking, and natural creativity',
        'Fire': 'passionate energy, transformative presence, and warm enthusiasm',
        'Earth': 'grounded perspective, nurturing reliability, and practical wisdom',
        'Metal': 'refined precision, clear boundaries, and elegant structure',
        'Water': 'emotional depth, adaptable flow, and intuitive wisdom'
    }
    
    # Generate partner description
    description = f"""## Your Destined Partner

The celestial harmonies reveal that your most compatible partner would embody the perfect balance of qualities that complement your unique energy signature.

### Physical Essence
This person would likely have a {physical_traits.get(zodiac_sign, 'distinctive and appealing appearance')}. Their presence in a room would be noticeable not just for their physical appearance, but for the energy they bring—a unique blend of confidence and warmth that draws you in naturally.

### Character and Spirit
Their inner nature would combine a {personality_traits.get(chinese_zodiac, 'multifaceted personality')} with a deep capacity for understanding your complex needs. They would possess a {element_influences.get(primary_element, 'unique spiritual quality')} that resonates with your inner world.

This person would understand when to support your dreams and when to provide constructive perspective. Their communication style would feel both refreshing and familiar, creating a sense of coming home even in your first conversations.

### Life Together
Together, you would create a relationship that honors both tradition and innovation, blending Eastern and Western philosophies of love into something uniquely your own. Your connection would be characterized by mutual growth, shared adventures, and a deep soul recognition that transcends ordinary relationships.

This partnership would support your authentic self-expression while challenging you to grow in ways you never imagined possible. The stars have aligned to bring this person into your life when you're both ready for the profound connection that awaits.
"""
    return description

# Main App
def main():
    # Initialize session state variables if they don't exist
    if 'fortune_result' not in st.session_state:
        st.session_state.fortune_result = None
    if 'partner_profile' not in st.session_state:
        st.session_state.partner_profile = None
    if 'generated_face' not in st.session_state:
        st.session_state.generated_face = None
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
        
    st.title("Mystic Harmony 🌟")
    st.subheader("Eastern & Western Astrology Combined")
    
    # About section in sidebar
    st.sidebar.title("About Mystic Harmony")
    st.sidebar.info(
        """
        Mystic Harmony combines:
        - Eastern Four Pillars (사주팔자)
        - Chinese Zodiac (십이지)
        - Five Elements (오행)
        - Western Astrology
        To create a unique, personalized fortune reading experience.
        """
    )
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🔮 My Fortune", "💕 Ideal Partner", "🎨 Partner's Face"])

    with tab1:
        st.header("Discover Your Destiny")
        
        # 간단 모드와 고급 모드 선택
        mode = st.radio(
            "Choose Analysis Mode",
            ["Simple Analysis", "Advanced Analysis (FortuneEngine)"],
            key="mode_selection"
        )
        
        col1, col2 = st.columns(2)

        if mode == "Simple Analysis":
            # 간단한 모드 - 기존 함수 사용
            with col1:
                birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1), 
                                           max_value=date.today(), value=datetime(1995, 1, 1),
                                           key="birth_date_simple")
            
            with col2:
                birth_time_options = {
                    "Dawn (3-6 AM)": "dawn",
                    "Morning (6-11 AM)": "morning", 
                    "Noon (11 AM-1 PM)": "noon",
                    "Afternoon (1-6 PM)": "afternoon",
                    "Evening (6-11 PM)": "evening"
                }
                
                birth_time = st.selectbox(
                    "Birth Time",
                    options=list(birth_time_options.keys()),
                    key="birth_time_simple"
                )
                
                # Convert time selection to simplified format
                simple_time = birth_time_options[birth_time]
                
                # Get approximate hour for house calculation
                hour_mapping = {
                    "dawn": 5,
                    "morning": 9,
                    "noon": 12,
                    "afternoon": 16,
                    "evening": 20,
                    "night": 1
                }
                birth_hour = hour_mapping[simple_time]
            
            if st.button("✨ Read My Fortune", type="primary", key="read_fortune_simple"):
                with st.spinner("Consulting the cosmic wisdom..."):
                    # Calculate Eastern astrology components
                    chinese_zodiac = get_chinese_zodiac(birth_date.year)
                    celestial_stem = get_celestial_stem(birth_date.year)
                    five_elements = get_five_elements(birth_date, simple_time)
                    
                    # Calculate Western astrology components
                    zodiac_sign = get_zodiac_sign(birth_date.month, birth_date.day)
                    moon_phase = get_moon_phase(birth_date)
                    house_info = get_astrological_house(birth_hour)
                    
                    # Generate combined reading
                    profile = generate_combined_profile(
                        chinese_zodiac, 
                        celestial_stem, 
                        five_elements,
                        zodiac_sign,
                        moon_phase,
                        house_info
                    )
                    
                    # Display personal reading
                    st.markdown('<div class="reading-box">', unsafe_allow_html=True)
                    st.markdown(profile, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Save profile data for compatibility readings
                    st.session_state['profile_data'] = {
                        'chinese_zodiac': chinese_zodiac,
                        'celestial_stem': celestial_stem,
                        'five_elements': five_elements,
                        'zodiac_sign': zodiac_sign,
                        'moon_phase': moon_phase,
                        'house_info': house_info,
                        'profile_text': profile
                    }
                    
                    # Show options for partner readings
                    st.success("Your celestial reading is complete! Would you like to explore compatibility?")
                    
                    # Buttons for additional readings
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Reveal Compatible Partner Traits", key="compatibility"):
                            if 'profile_data' in st.session_state:
                                data = st.session_state['profile_data']
                                compatibility = generate_compatibility_profile(
                                    data['profile_text'],
                                    data['chinese_zodiac'],
                                    data['celestial_stem'],
                                    data['zodiac_sign'],
                                    data['five_elements']
                                )
                                
                                st.markdown('<div class="reading-box">', unsafe_allow_html=True)
                                st.markdown(compatibility, unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("Describe Your Destined Partner", key="partner_description"):
                            if 'profile_data' in st.session_state:
                                data = st.session_state['profile_data']
                                description = generate_partner_description(
                                    data['chinese_zodiac'],
                                    data['zodiac_sign'],
                                    data['five_elements']
                                )
                                
                                st.markdown('<div class="reading-box">', unsafe_allow_html=True)
                                st.markdown(description, unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # 고급 모드 - FortuneEngine 사용
            with col1:
                birth_date = st.date_input(
                    "Birth Date",
                    min_value=date(1900, 1, 1),
                    max_value=date.today(),
                    value=date(1995, 1, 1),
                    key="birth_date_advanced"
                )
                
            with col2:
                birth_time_options = {
                    "Dawn (3-6 AM)": "dawn",
                    "Morning (6-11 AM)": "morning", 
                    "Noon (11 AM-1 PM)": "noon",
                    "Afternoon (1-6 PM)": "afternoon",
                    "Evening (6-11 PM)": "evening"
                }
                
                birth_time = st.selectbox(
                    "Birth Time",
                    options=list(birth_time_options.keys()),
                    key="birth_time_advanced"
                )
    
            if st.button("✨ Read My Fortune", type="primary", key="read_fortune_advanced"):
                with st.spinner("Consulting the cosmic wisdom..."):
                    # FortuneEngine 초기화 및 분석
                    engine = FortuneEngine()
                    result = engine.analyze_fortune(
                        birth_date=birth_date,
                        birth_time=birth_time_options[birth_time]
                    )
                    st.session_state.fortune_result = result
    
            # 결과 표시
            if st.session_state.fortune_result:
                result = st.session_state.fortune_result
                
                # 기본 정보
                st.markdown("### 🌙 Your Cosmic Profile")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>Western Zodiac</h4>
                        <p>{result['western_zodiac']['sign']} {result['western_zodiac']['symbol']}</p>
                        <p style="font-size: 0.9rem; color: #666;">{result['western_zodiac']['element']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>Chinese Zodiac</h4>
                        <p>{result['chinese_zodiac']['animal']} {result['chinese_zodiac']['symbol']}</p>
                        <p style="font-size: 0.9rem; color: #666;">{result['chinese_zodiac']['element']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>Four Pillars</h4>
                        <p>Day Master: {result['four_pillars']['day_master']}</p>
                        <p style="font-size: 0.9rem; color: #666;">Element: {result['four_pillars']['dominant_element']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 오행 분석
                st.markdown("### 🔥 Five Elements Balance")
                
                import plotly.graph_objects as go
                
                elements = result['element_balance']
                fig = go.Figure(data=[go.Bar(
                    x=list(elements.keys()),
                    y=list(elements.values()),
                    marker_color=['#4CAF50', '#F44336', '#FFC107', '#9E9E9E', '#2196F3']
                )])
                
                fig.update_layout(
                    title="Your Element Distribution",
                    xaxis_title="Elements",
                    yaxis_title="Strength",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 스토리텔링
                st.markdown("### 📖 Your Life Story")
                
                tabs = st.tabs(["Personality", "Life Path", "Career", "Love", "This Year"])
                
                with tabs[0]:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>🌟 Personality Analysis</h4>
                        <p>{result['story']['personality']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[1]:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>🛤️ Life Path</h4>
                        <p>{result['story']['life_path']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[2]:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>💼 Career Guidance</h4>
                        <p>{result['story']['career']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[3]:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>💕 Love & Relationships</h4>
                        <p>{result['story']['relationships']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[4]:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>🎯 {date.today().year} Fortune</h4>
                        <p>{result['story']['current_year']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.header("Your Ideal Partner Profile")
        if st.session_state.fortune_result is None and st.session_state.profile_data is None:
            st.warning("Please read your fortune first to discover your ideal partner!")
        else:
            # 파트너 검색 버튼
            if st.button("💘 Find My Soulmate", type="primary", key="find_soulmate"):
                with st.spinner("Searching the cosmic connections..."):
                    if st.session_state.fortune_result is not None:
                        # FortuneEngine 결과가 있는 경우 사용
                        matcher = PartnerMatcher()
                        partner_profile = matcher.find_ideal_partner(st.session_state.fortune_result)
                        st.session_state.partner_profile = partner_profile
                    elif st.session_state.profile_data is not None:
                        # 간단 모드의 결과가 있는 경우 사용
                        data = st.session_state.profile_data
                        compatibility = generate_compatibility_profile(
                            data['profile_text'],
                            data['chinese_zodiac'],
                            data['celestial_stem'],
                            data['zodiac_sign'],
                            data['five_elements']
                        )
                        
                        st.markdown('<div class="reading-box">', unsafe_allow_html=True)
                        st.markdown(compatibility, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Partner description 추가
                        description = generate_partner_description(
                            data['chinese_zodiac'],
                            data['zodiac_sign'],
                            data['five_elements']
                        )
                        
                        st.markdown('<div class="reading-box">', unsafe_allow_html=True)
                        st.markdown(description, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # 고급 모드 결과 표시
            if st.session_state.partner_profile:
                profile = st.session_state.partner_profile
                
                # 호환성 점수
                st.markdown("### 💫 Compatibility Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Match", f"{profile['compatibility_score']}%")
                
                with col2:
                    st.metric("Element Harmony", f"{profile['element_compatibility']}%")
                
                with col3:
                    st.metric("Zodiac Sync", f"{profile['zodiac_compatibility']}%")
                
                # 파트너 특성
                st.markdown("### 👤 Partner Characteristics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>Personality Traits</h4>
                        <ul>
                        {"".join([f"<li>{trait}</li>" for trait in profile['personality_traits']])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h4>Compatible Elements</h4>
                        <div>
                        {"".join([f'<span class="element-badge" style="background-color: {color}; color: white;">{elem}</span>' 
                                 for elem, color in zip(profile['compatible_elements'], ['#4CAF50', '#F44336', '#FFC107'])])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 관계 역학
                st.markdown("### 💑 Relationship Dynamics")
                
                st.markdown(f"""
                <div class="fortune-card">
                    <p>{profile['relationship_dynamics']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 만남 시나리오
                st.markdown("### 🌈 Meeting Scenarios")
                
                for i, scenario in enumerate(profile['meeting_scenarios']):
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h5>Scenario {i+1}</h5>
                        <p><strong>Location:</strong> {scenario['location']}</p>
                        <p><strong>Time:</strong> {scenario['time']}</p>
                        <p><strong>Situation:</strong> {scenario['situation']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab3:
        st.header("Visualize Your Soulmate")
        if st.session_state.partner_profile is None:
            st.warning("Please generate your ideal partner profile first!")
        else:
            if st.button("🎨 Generate Partner's Face", type="primary", key="generate_face"):
                with st.spinner("Creating your soulmate's image..."):
                    generator = FaceGenerator()
                    face_result = generator.generate_partner_face(
                        st.session_state.fortune_result,
                        st.session_state.partner_profile
                    )
                    st.session_state.generated_face = face_result
            
            if st.session_state.generated_face:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.image(f"data:image/png;base64,{st.session_state.generated_face['image']}", caption="Your Ideal Partner")
                
                with col2:
                    st.markdown("### 🎨 Visual Characteristics")
                    
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h5>Aura & Energy</h5>
                        <p>{st.session_state.generated_face['aura_description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="fortune-card">
                        <h5>Color Palette</h5>
                        <div>
                        {"".join([f'<div style="background-color: {color}; width: 30px; height: 30px; display: inline-block; margin: 2px; border-radius: 50%;"></div>' 
                                 for color in st.session_state.generated_face['color_palette']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 