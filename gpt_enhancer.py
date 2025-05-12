import os
import openai
from openai import OpenAI
from typing import Dict, List, Any

class GPTEnhancer:
    """
    Class to enhance astrological readings using OpenAI's GPT models
    """
    
    def __init__(self, proxies=None, **kwargs):
        """
        Initialize the OpenAI client with API key from environment variables
        
        Args:
            proxies: Proxy settings (ignored)
            **kwargs: Additional arguments (ignored)
        """
        # 기본 전역 API 키 설정 (옛 방식)
        api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key
        
        # 호환성 문제를 방지하기 위해 최소한의 매개변수로 클라이언트 생성
        try:
            self.client = OpenAI(api_key=api_key)
        except TypeError as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            self.client = None
            
        self.model = "gpt-4.1-mini"  # Using GPT-4.1-mini for enhanced descriptions
    
    def enhance_fortune_reading(self, fortune_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Enhance the fortune reading with more detailed and poetic descriptions
        using the GPT model
        
        Args:
            fortune_data: Dictionary containing the user's fortune data
            
        Returns:
            Dictionary with enhanced descriptions for different aspects of the reading
        """
        western_zodiac = fortune_data.get('western_zodiac', {}).get('sign', 'Gemini')
        chinese_zodiac = fortune_data.get('chinese_zodiac', {}).get('animal', 'Dragon')
        elements = fortune_data.get('element_balance', {})
        four_pillars = fortune_data.get('four_pillars', {})
        
        # Prepare prompt for personality description
        personality_prompt = f"""
        Create a rich, insightful personality description for someone born under the Western zodiac sign {western_zodiac} 
        and the Chinese zodiac sign {chinese_zodiac}. Their dominant element is {four_pillars.get('dominant_element', 'Fire')}.
        Use metaphorical language and reference both Eastern and Western astrological traditions.
        Keep the response under 200 words and make it personal and positive.
        """
        
        # Get personality description
        personality = self._generate_text(personality_prompt)
        
        # Prepare prompt for life path
        life_path_prompt = f"""
        Describe the life journey and path for someone with these astrological influences:
        - Western zodiac: {western_zodiac}
        - Chinese zodiac: {chinese_zodiac}
        - Elements balance: {', '.join([f"{k}: {v}%" for k, v in elements.items()][:3])}
        
        Focus on their unique strengths, challenges they might face, and how their astrological blueprint 
        shapes their life trajectory. Include wisdom from both Eastern and Western traditions.
        Keep the response under 200 words and make it inspiring.
        """
        
        # Get life path description
        life_path = self._generate_text(life_path_prompt)
        
        # Prepare prompt for career guidance
        career_prompt = f"""
        Provide career guidance for someone with these astrological influences:
        - Western zodiac: {western_zodiac}
        - Chinese zodiac: {chinese_zodiac}
        - Dominant element: {four_pillars.get('dominant_element', 'Fire')}
        
        Suggest career paths, work environments, and professional strengths.
        Blend Eastern and Western astrological insights into practical advice.
        Keep the response under 180 words and make it specific and actionable.
        """
        
        # Get career guidance
        career = self._generate_text(career_prompt)
        
        # Prepare prompt for relationships
        relationships_prompt = f"""
        Describe relationship patterns and romantic tendencies for someone with:
        - Western zodiac: {western_zodiac}
        - Chinese zodiac: {chinese_zodiac}
        - Elements balance: {', '.join([f"{k}: {v}%" for k, v in elements.items()][:3])}
        
        Include insights about their approach to love, communication style, and what they need in a partner.
        Blend both Eastern and Western astrological traditions.
        Keep the response under 180 words and make it thoughtful and balanced.
        """
        
        # Get relationships description
        relationships = self._generate_text(relationships_prompt)
        
        # Prepare prompt for current year
        current_year_prompt = f"""
        Provide a forecast for the current year for someone with:
        - Western zodiac: {western_zodiac}
        - Chinese zodiac: {chinese_zodiac}
        - Dominant element: {four_pillars.get('dominant_element', 'Fire')}
        
        Include insights about opportunities, challenges, and important themes for the year.
        Blend Eastern and Western astrological traditions.
        Keep the response under 150 words and make it hopeful but realistic.
        """
        
        # Get current year forecast
        current_year = self._generate_text(current_year_prompt)
        
        return {
            "personality": personality,
            "life_path": life_path,
            "career": career,
            "relationships": relationships,
            "current_year": current_year
        }
    
    def enhance_partner_description(self, user_fortune: Dict[str, Any], 
                                   partner_profile: Dict[str, Any]) -> str:
        """
        Create an enhanced, poetic description of the ideal partner
        
        Args:
            user_fortune: The user's fortune data
            partner_profile: The generated partner profile
            
        Returns:
            Enhanced description of the ideal partner
        """
        # Extract relevant information
        user_western = user_fortune.get('western_zodiac', {}).get('sign', 'Gemini')
        user_chinese = user_fortune.get('chinese_zodiac', {}).get('animal', 'Dragon')
        user_element = user_fortune.get('four_pillars', {}).get('dominant_element', 'Fire')
        
        partner_elements = partner_profile.get('compatible_elements', ['Wood', 'Water'])
        partner_traits = partner_profile.get('personality_traits', 
                                          ['Creative', 'Intuitive', 'Compassionate'])
        
        # Prepare prompt
        prompt = f"""
        Create a poetic and vivid description of an ideal romantic partner for someone with:
        - Western zodiac: {user_western}
        - Chinese zodiac: {user_chinese}
        - Dominant element: {user_element}
        
        Their ideal partner exhibits these elements: {', '.join(partner_elements[:2])}
        And these personality traits: {', '.join(partner_traits[:5])}
        
        Describe their presence, essence, and the feeling of being with them. Include physical and
        energetic qualities without being overly specific about exact appearance.
        Make the description atmospheric, inspiring, and emotionally resonant.
        Blend Eastern and Western astrological traditions in your poetic description.
        Keep the response under 250 words.
        """
        
        return self._generate_text(prompt)
    
    def enhance_meeting_scenarios(self, scenarios: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Enhance the meeting scenarios with more vivid and detailed descriptions
        
        Args:
            scenarios: List of meeting scenario dictionaries
            
        Returns:
            Enhanced scenarios with more detailed descriptions
        """
        enhanced_scenarios = []
        
        for scenario in scenarios:
            location = scenario.get('location', 'a cafe')
            time = scenario.get('time', 'afternoon')
            situation = scenario.get('situation', 'a chance encounter')
            
            # Prepare prompt
            prompt = f"""
            Create a vivid, romantic first meeting scenario that happens at {location} during {time}.
            The basic situation is: {situation}
            
            Expand this into a detailed, atmospheric mini-story about a first encounter with destiny.
            Include sensory details, emotions, and the feeling of cosmic recognition.
            Keep it under 150 words and make it both realistic and magical.
            """
            
            # Get enhanced description
            enhanced_description = self._generate_text(prompt)
            
            # Create enhanced scenario
            enhanced_scenarios.append({
                'location': location,
                'time': time,
                'situation': enhanced_description
            })
            
            # Limit to 2 enhanced scenarios to manage API usage
            if len(enhanced_scenarios) >= 2:
                break
        
        return enhanced_scenarios
    
    def _generate_text(self, prompt: str) -> str:
        """
        Generate text using the OpenAI GPT model
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated text
        """
        try:
            # 클라이언트 객체가 없는 경우 대체 응답 반환
            if self.client is None:
                return "The celestial energies are currently in transition. Trust your intuition at this time."
                
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a poetic astrologer who blends Eastern and Western traditions. Your responses are insightful, nuanced, and spiritually resonant without being overly technical."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Return the generated text
            return response.choices[0].message.content.strip()
        except Exception as e:
            # In case of any errors with the API, return a fallback response
            print(f"Error generating text with OpenAI: {e}")
            return "The celestial energies are currently clouded. Trust your intuition for guidance at this time." 