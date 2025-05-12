# Mystic Harmony - Eastern & Western Astrology Combined

A Streamlit application that combines Eastern and Western astrology traditions to provide personalized fortune readings and partner compatibility analysis, enhanced with GPT-4.1-mini.

## Features

- **Combined Fortune Reading**: Integrates Eastern Four Pillars (사주팔자), Chinese Zodiac (십이지간), Five Elements (오행), and Western Zodiac to create comprehensive readings
- **Personality Analysis**: Detailed breakdown of character traits, element balance, and life path
- **Partner Compatibility**: 간ind your ideal partner profile based on astrological compatibility
- **Visual Partner Generation**: Artistic representation of your ideal partner based on astrological calculations
- **Interactive User Interface**: Easy-to-use Streamlit interface with intuitive navigation
- **GPT-4.1-mini Integration**: Enhanced descriptions and storytelling powered by OpenAI's GPT models

## Setup

1. Clone this repository:
```
git clone <repository-url>
cd mystic-harmony
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key in the `.env` file
   - The app uses GPT-4.1-mini model for enhanced descriptions

4. Run the application:
```
streamlit run app.py
```

## File Structure

- `app.py`: Main Streamlit application
- `fortune_engine.py`: Core calculations for Eastern and Western astrology
- `partner_matcher.py`: Algorithms for partner compatibility
- `face_generator.py`: Visualization of ideal partner profile
- `gpt_enhancer.py`: OpenAI integration for enhanced descriptions
- `requirements.txt`: Dependencies
- `.env`: Configuration (API keys, etc.)

## Technologies

- **Streamlit**: Front-end framework
- **Python**: Backend logic
- **Pillow**: Image processing for face generation
- **Plotly**: Visualization of element balance
- **OpenAI GPT-4.1-mini**: Enhanced storytelling and descriptions

## Usage

1. Enter your birth date and approximate time
2. View your combined Eastern and Western astrological profile with rich descriptions
3. Explore compatibility with potential partners through detailed narratives
4. Generate a visual representation of your ideal partner
5. Experience poetic meeting scenarios powered by GPT

## Future Enhancements

- Enhanced GPT integration for more detailed storytelling
- Historical fortune analysis
- Real-time astrological events and their impact
- Fortune predictions for specific future time periods
- Mobile app version 