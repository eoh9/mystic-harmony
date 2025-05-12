import datetime
import math
import random
from dateutil import tz
import ephem
import lunardate
from dateutil import parser
import os
from typing import Dict, List, Any
from gpt_enhancer import GPTEnhancer

class FortuneEngine:
    """
    Core engine for calculating and generating combined Eastern and Western astrology readings.
    This is a simplified version that focuses on algorithmic storytelling without external APIs.
    """
    
    def __init__(self):
        # Western zodiac signs and their date ranges
        self.zodiac_signs = [
            {"name": "Aries", "start_month": 3, "start_day": 21, "end_month": 4, "end_day": 19, "element": "Fire", "symbol": "♈"},
            {"name": "Taurus", "start_month": 4, "start_day": 20, "end_month": 5, "end_day": 20, "element": "Earth", "symbol": "♉"},
            {"name": "Gemini", "start_month": 5, "start_day": 21, "end_month": 6, "end_day": 20, "element": "Air", "symbol": "♊"},
            {"name": "Cancer", "start_month": 6, "start_day": 21, "end_month": 7, "end_day": 22, "element": "Water", "symbol": "♋"},
            {"name": "Leo", "start_month": 7, "start_day": 23, "end_month": 8, "end_day": 22, "element": "Fire", "symbol": "♌"},
            {"name": "Virgo", "start_month": 8, "start_day": 23, "end_month": 9, "end_day": 22, "element": "Earth", "symbol": "♍"},
            {"name": "Libra", "start_month": 9, "start_day": 23, "end_month": 10, "end_day": 22, "element": "Air", "symbol": "♎"},
            {"name": "Scorpio", "start_month": 10, "start_day": 23, "end_month": 11, "end_day": 21, "element": "Water", "symbol": "♏"},
            {"name": "Sagittarius", "start_month": 11, "start_day": 22, "end_month": 12, "end_day": 21, "element": "Fire", "symbol": "♐"},
            {"name": "Capricorn", "start_month": 12, "start_day": 22, "end_month": 1, "end_day": 19, "element": "Earth", "symbol": "♑"},
            {"name": "Aquarius", "start_month": 1, "start_day": 20, "end_month": 2, "end_day": 18, "element": "Air", "symbol": "♒"},
            {"name": "Pisces", "start_month": 2, "start_day": 19, "end_month": 3, "end_day": 20, "element": "Water", "symbol": "♓"}
        ]
        
        # Chinese zodiac animals
        self.chinese_zodiac = [
            {"name": "Rat", "years": [1924, 1936, 1948, 1960, 1972, 1984, 1996, 2008, 2020], "element": "Water", "symbol": "🐀"},
            {"name": "Ox", "years": [1925, 1937, 1949, 1961, 1973, 1985, 1997, 2009, 2021], "element": "Earth", "symbol": "🐂"},
            {"name": "Tiger", "years": [1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022], "element": "Wood", "symbol": "🐅"},
            {"name": "Rabbit", "years": [1927, 1939, 1951, 1963, 1975, 1987, 1999, 2011, 2023], "element": "Wood", "symbol": "🐇"},
            {"name": "Dragon", "years": [1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024], "element": "Earth", "symbol": "🐉"},
            {"name": "Snake", "years": [1929, 1941, 1953, 1965, 1977, 1989, 2001, 2013, 2025], "element": "Fire", "symbol": "🐍"},
            {"name": "Horse", "years": [1930, 1942, 1954, 1966, 1978, 1990, 2002, 2014, 2026], "element": "Fire", "symbol": "🐎"},
            {"name": "Goat", "years": [1931, 1943, 1955, 1967, 1979, 1991, 2003, 2015, 2027], "element": "Earth", "symbol": "🐐"},
            {"name": "Monkey", "years": [1932, 1944, 1956, 1968, 1980, 1992, 2004, 2016, 2028], "element": "Metal", "symbol": "🐒"},
            {"name": "Rooster", "years": [1933, 1945, 1957, 1969, 1981, 1993, 2005, 2017, 2029], "element": "Metal", "symbol": "🐓"},
            {"name": "Dog", "years": [1934, 1946, 1958, 1970, 1982, 1994, 2006, 2018, 2030], "element": "Earth", "symbol": "🐕"},
            {"name": "Pig", "years": [1935, 1947, 1959, 1971, 1983, 1995, 2007, 2019, 2031], "element": "Water", "symbol": "🐖"}
        ]
        
        # Heavenly Stems and Earthly Branches (Ten Celestial Stems)
        self.heavenly_stems = [
            {"name": "Jia", "element": "Wood", "yin_yang": "Yang"},
            {"name": "Yi", "element": "Wood", "yin_yang": "Yin"},
            {"name": "Bing", "element": "Fire", "yin_yang": "Yang"},
            {"name": "Ding", "element": "Fire", "yin_yang": "Yin"},
            {"name": "Wu", "element": "Earth", "yin_yang": "Yang"},
            {"name": "Ji", "element": "Earth", "yin_yang": "Yin"},
            {"name": "Geng", "element": "Metal", "yin_yang": "Yang"},
            {"name": "Xin", "element": "Metal", "yin_yang": "Yin"},
            {"name": "Ren", "element": "Water", "yin_yang": "Yang"},
            {"name": "Gui", "element": "Water", "yin_yang": "Yin"}
        ]
        
        # Time branches for hour pillar
        self.time_branches = {
            "dawn": {"branch": "Yin", "element": "Wood"},
            "morning": {"branch": "Mao", "element": "Wood"},
            "noon": {"branch": "Wu", "element": "Fire"},
            "afternoon": {"branch": "You", "element": "Metal"},
            "evening": {"branch": "Xu", "element": "Earth"}
        }
        
        # Element relationships
        self.element_relationships = {
            "Wood": {"generates": "Fire", "weakens": "Earth", "strengthened_by": "Water", "weakened_by": "Metal"},
            "Fire": {"generates": "Earth", "weakens": "Metal", "strengthened_by": "Wood", "weakened_by": "Water"},
            "Earth": {"generates": "Metal", "weakens": "Water", "strengthened_by": "Fire", "weakened_by": "Wood"},
            "Metal": {"generates": "Water", "weakens": "Wood", "strengthened_by": "Earth", "weakened_by": "Fire"},
            "Water": {"generates": "Wood", "weakens": "Fire", "strengthened_by": "Metal", "weakened_by": "Earth"}
        }
        
        # Personality traits for each element
        self.element_traits = {
            "Wood": ["creative", "idealistic", "generous", "cooperative", "flexible", "compassionate", "expansive"],
            "Fire": ["passionate", "dynamic", "expressive", "enthusiastic", "adventurous", "persuasive", "confident"],
            "Earth": ["practical", "reliable", "stable", "hardworking", "prudent", "nurturing", "honest"],
            "Metal": ["precise", "organized", "self-reliant", "decisive", "principled", "methodical", "structured"],
            "Water": ["intuitive", "reflective", "introspective", "empathetic", "mysterious", "perceptive", "adaptable"]
        }
        
        # Personality traits for zodiac signs
        self.zodiac_traits = {
            "Aries": ["pioneering", "courageous", "energetic", "direct", "impulsive", "leadership-oriented"],
            "Taurus": ["dependable", "persistent", "practical", "devoted", "patient", "harmony-seeking"],
            "Gemini": ["adaptable", "versatile", "communicative", "witty", "intellectual", "curious"],
            "Cancer": ["nurturing", "emotional", "protective", "intuitive", "home-loving", "sympathetic"],
            "Leo": ["generous", "creative", "enthusiastic", "dignified", "dramatic", "self-confident"],
            "Virgo": ["analytical", "attentive", "practical", "diligent", "discriminating", "detail-oriented"],
            "Libra": ["diplomatic", "balanced", "fair", "partnership-oriented", "social", "harmonious"],
            "Scorpio": ["intense", "passionate", "resilient", "resourceful", "mysterious", "investigative"],
            "Sagittarius": ["optimistic", "freedom-loving", "philosophical", "straightforward", "adventurous"],
            "Capricorn": ["ambitious", "disciplined", "patient", "responsible", "structured", "goal-oriented"],
            "Aquarius": ["independent", "original", "humanitarian", "inventive", "progressive", "idealistic"],
            "Pisces": ["compassionate", "adaptable", "accepting", "imaginative", "intuitive", "emotional"]
        }
        
        # Career paths aligned with elements
        self.element_careers = {
            "Wood": ["teacher", "counselor", "social worker", "environmentalist", "artist", "designer", "writer"],
            "Fire": ["entrepreneur", "marketer", "performer", "motivational speaker", "fitness trainer", "chef"],
            "Earth": ["accountant", "real estate agent", "manager", "farmer", "insurance agent", "nurse", "caretaker"],
            "Metal": ["engineer", "lawyer", "banker", "technician", "surgeon", "researcher", "architect"],
            "Water": ["philosopher", "psychologist", "spiritual guide", "healer", "poet", "musician", "diplomat"]
        }
        
        # Initialize the GPT enhancer (for enhanced text generation)
        try:
            # 원래 코드: self.gpt_enhancer = GPTEnhancer()
            # proxies 인자를 전달하지 않도록 명시적으로 초기화
            from gpt_enhancer import GPTEnhancer
            self.gpt_enhancer = GPTEnhancer()
            self.use_gpt = True
        except Exception as e:
            print(f"Error initializing GPT enhancer: {e}")
            self.use_gpt = False
    
    def analyze_fortune(self, birth_date, birth_time):
        """
        Analyze a person's fortune based on birth date and time
        
        Args:
            birth_date: datetime.date object
            birth_time: string (dawn, morning, noon, afternoon, evening)
            
        Returns:
            Dictionary with complete fortune analysis
        """
        # Calculate Western zodiac sign
        western_zodiac = self._calculate_western_zodiac(birth_date)
        
        # Calculate Chinese zodiac animal
        chinese_zodiac = self._calculate_chinese_zodiac(birth_date.year)
        
        # Calculate Four Pillars (simplified)
        four_pillars = self._calculate_four_pillars(birth_date, birth_time)
        
        # Calculate element balance
        element_balance = self._calculate_element_balance(western_zodiac, chinese_zodiac, four_pillars)
        
        # Generate personalized story
        story = self._generate_story(western_zodiac, chinese_zodiac, four_pillars, element_balance)
        
        # Construct the complete result
        result = {
            "western_zodiac": western_zodiac,
            "chinese_zodiac": chinese_zodiac,
            "four_pillars": four_pillars,
            "element_balance": element_balance,
            "story": story
        }
        
        return result
    
    def _calculate_western_zodiac(self, birth_date):
        """Calculate Western zodiac sign from birth date"""
        month = birth_date.month
        day = birth_date.day
        
        for sign in self.zodiac_signs:
            # Handle zodiac signs that span across years (e.g., Capricorn)
            if sign["start_month"] > sign["end_month"]:
                if (month == sign["start_month"] and day >= sign["start_day"]) or \
                   (month == sign["end_month"] and day <= sign["end_day"]):
                    return {
                        "sign": sign["name"],
                        "element": sign["element"],
                        "symbol": sign["symbol"],
                        "traits": self.zodiac_traits[sign["name"]]
                    }
            else:
                if (month == sign["start_month"] and day >= sign["start_day"]) or \
                   (month == sign["end_month"] and day <= sign["end_day"]) or \
                   (month > sign["start_month"] and month < sign["end_month"]):
                    return {
                        "sign": sign["name"],
                        "element": sign["element"],
                        "symbol": sign["symbol"],
                        "traits": self.zodiac_traits[sign["name"]]
                    }
        
        # Default fallback
        return {
            "sign": "Aries",
            "element": "Fire",
            "symbol": "♈",
            "traits": self.zodiac_traits["Aries"]
        }
    
    def _calculate_chinese_zodiac(self, year):
        """Calculate Chinese zodiac animal from birth year"""
        # Calculate lunar year (simplified)
        lunar_year = year
        
        # Find the zodiac animal
        for animal in self.chinese_zodiac:
            if year % 12 == animal["years"][0] % 12:
                # Calculate the elemental aspect (Heavenly Stem)
                stem_index = (year - 4) % 10
                heavenly_stem = self.heavenly_stems[stem_index]
                
                return {
                    "animal": animal["name"],
                    "element": animal["element"],
                    "heavenly_stem": heavenly_stem["name"],
                    "stem_element": heavenly_stem["element"],
                    "yin_yang": heavenly_stem["yin_yang"],
                    "symbol": animal["symbol"]
                }
        
        # Default fallback
        return {
            "animal": "Dragon",
            "element": "Earth",
            "heavenly_stem": "Wu",
            "stem_element": "Earth",
            "yin_yang": "Yang",
            "symbol": "🐉"
        }
    
    def _calculate_four_pillars(self, birth_date, birth_time):
        """Calculate Four Pillars (simplified version)"""
        # Year Pillar
        year_stem_index = (birth_date.year - 4) % 10
        year_stem = self.heavenly_stems[year_stem_index]
        
        # Month Pillar (simplified)
        month_stem_index = ((year_stem_index * 2) + birth_date.month + 1) % 10
        month_stem = self.heavenly_stems[month_stem_index]
        
        # Day Pillar (simplified)
        day_of_year = birth_date.timetuple().tm_yday
        day_stem_index = (year_stem_index * 2 + day_of_year) % 10
        day_stem = self.heavenly_stems[day_stem_index]
        
        # Hour Pillar
        hour_branch = self.time_branches[birth_time]
        
        # Determine day master (the day stem's element)
        day_master = day_stem["element"]
        
        # Count elements to find dominant element
        elements = [
            year_stem["element"],
            month_stem["element"],
            day_stem["element"],
            hour_branch["element"]
        ]
        
        element_count = {
            "Wood": elements.count("Wood"),
            "Fire": elements.count("Fire"),
            "Earth": elements.count("Earth"),
            "Metal": elements.count("Metal"),
            "Water": elements.count("Water")
        }
        
        dominant_element = max(element_count, key=element_count.get)
        
        # Check if the chart is balanced or imbalanced
        max_count = max(element_count.values())
        min_count = min(element_count.values())
        
        if max_count - min_count >= 3:
            balance = "Highly Imbalanced"
        elif max_count - min_count >= 2:
            balance = "Moderately Imbalanced"
        else:
            balance = "Relatively Balanced"
        
        # Determine lucky and unlucky elements
        lucky_element = self.element_relationships[day_master]["strengthened_by"]
        unlucky_element = self.element_relationships[day_master]["weakened_by"]
        
        return {
            "year_stem": year_stem["name"],
            "year_element": year_stem["element"],
            "month_stem": month_stem["name"],
            "month_element": month_stem["element"],
            "day_stem": day_stem["name"],
            "day_element": day_stem["element"],
            "hour_branch": hour_branch["branch"],
            "hour_element": hour_branch["element"],
            "day_master": day_master,
            "dominant_element": dominant_element,
            "balance": balance,
            "lucky_element": lucky_element,
            "unlucky_element": unlucky_element,
            "element_count": element_count
        }
    
    def _calculate_element_balance(self, western_zodiac, chinese_zodiac, four_pillars):
        """Calculate the balance of five elements"""
        # Base element strengths
        element_strength = {
            "Wood": 0,
            "Fire": 0,
            "Earth": 0,
            "Metal": 0,
            "Water": 0
        }
        
        # Add Western zodiac element (strongest influence)
        element_strength[western_zodiac["element"]] += 30
        
        # Add Chinese zodiac elements
        element_strength[chinese_zodiac["element"]] += 15
        element_strength[chinese_zodiac["stem_element"]] += 15
        
        # Add Four Pillars elements
        element_count = four_pillars["element_count"]
        for element, count in element_count.items():
            element_strength[element] += count * 10
        
        # Boost day master
        element_strength[four_pillars["day_master"]] += 10
        
        # Normalize to ensure total is 100
        total = sum(element_strength.values())
        for element in element_strength:
            element_strength[element] = round((element_strength[element] / total) * 100)
        
        # Make sure we sum to 100
        adjustment = 100 - sum(element_strength.values())
        element_strength[max(element_strength, key=element_strength.get)] += adjustment
        
        return element_strength
    
    def _generate_story(self, western_zodiac, chinese_zodiac, four_pillars, element_balance):
        """Generate a personalized fortune story"""
        # Get main traits and elements
        dominant_element = four_pillars["dominant_element"]
        western_sign = western_zodiac["sign"]
        chinese_animal = chinese_zodiac["animal"]
        day_master = four_pillars["day_master"]
        lucky_element = four_pillars["lucky_element"]
        unlucky_element = four_pillars["unlucky_element"]
        
        # Select random traits from both zodiacs
        western_traits = random.sample(western_zodiac["traits"], min(3, len(western_zodiac["traits"])))
        element_traits = random.sample(self.element_traits[dominant_element], min(3, len(self.element_traits[dominant_element])))
        
        # Generate personality description
        personality = f"Your unique character blends {western_sign}'s {western_traits[0]} and {western_traits[1]} qualities with the {chinese_animal}'s inherent {element_traits[0]} nature. With {day_master} as your day master, you possess natural {self.element_traits[day_master][0]} and {self.element_traits[day_master][1]} tendencies. This makes you especially gifted at seeing connections others miss and finding creative solutions to complex problems. Your {dominant_element} dominant element infuses you with {element_traits[2]} energy, giving you a distinct approach to life's challenges that combines both Eastern and Western influences in your character."
        
        # Generate life path
        balance_description = ""
        if four_pillars["balance"] == "Highly Imbalanced":
            balance_description = "Your chart shows significant elemental imbalance, suggesting a life of dramatic contrasts and powerful transformations."
        elif four_pillars["balance"] == "Moderately Imbalanced":
            balance_description = "Your elemental balance shows moderate asymmetry, indicating a life with clear phases of transformation and growth."
        else:
            balance_description = "Your elements are relatively balanced, suggesting a life of harmonious progression and steady development."
        
        strongest_element = max(element_balance, key=element_balance.get)
        weakest_element = min(element_balance, key=element_balance.get)
        
        life_path = f"{balance_description} Your {strongest_element} energy ({element_balance[strongest_element]}%) guides your life direction, giving you natural talents in {self.element_traits[strongest_element][0]} and {self.element_traits[strongest_element][1]} pursuits. Your chart reveals that {lucky_element} activities and environments will generally bring you good fortune, while excessive {unlucky_element} influences may create challenges you'll need to overcome. The combination of your {western_sign} sun sign and {chinese_animal} Chinese zodiac suggests a life purpose that involves balancing {western_traits[2]} action with {element_traits[1]} reflection, particularly in matters related to {random.choice(['personal growth', 'relationships', 'career advancement', 'creative expression', 'spiritual development'])}."
        
        # Generate career guidance
        suitable_careers = random.sample(self.element_careers[dominant_element], min(3, len(self.element_careers[dominant_element])))
        supporting_careers = random.sample(self.element_careers[lucky_element], min(2, len(self.element_careers[lucky_element])))
        
        career = f"Your professional strengths are rooted in your {dominant_element} dominant element, making you well-suited for careers as a {suitable_careers[0]}, {suitable_careers[1]}, or {suitable_careers[2]}. Your {day_master} day master gives you excellent {self.element_traits[day_master][2]} abilities that would also support roles involving {supporting_careers[0]} or {supporting_careers[1]} work. The {western_sign} influence in your chart suggests you thrive in environments that value {western_traits[0]} approaches, while your {chinese_animal} nature brings valuable {element_traits[0]} energy to your work. For optimal career satisfaction, seek positions that allow you to express your {strongest_element} qualities while developing your underrepresented {weakest_element} aspects."
        
        # Generate relationship insights
        relationships = f"In relationships, your {western_sign} sun sign blends with your {chinese_animal} Chinese zodiac to create a unique approach to connections. You naturally bring {western_traits[1]} and {element_traits[1]} qualities to your partnerships, making you a {random.choice(['supportive', 'inspiring', 'grounding', 'exciting', 'loyal'])} presence in others' lives. Your {day_master} day master suggests you relate most harmoniously with people who appreciate your {self.element_traits[day_master][0]} nature and who can complement your {weakest_element} aspects. Relationship challenges may arise when you encounter excessive {unlucky_element} energy in partners, which might manifest as {random.choice(['communication difficulties', 'emotional distance', 'competing priorities', 'differing values', 'misaligned goals'])}. For most fulfilling connections, seek relationships that honor both your Eastern and Western aspects, allowing for both {western_traits[2]} expression and {element_traits[2]} depth."
        
        # Generate current year forecast
        current_year = datetime.datetime.now().year
        year_animal = self._calculate_chinese_zodiac(current_year)
        
        # Determine if current year's energy supports or challenges the person's chart
        year_element = year_animal["stem_element"]
        is_supportive = (year_element == lucky_element or 
                         year_element == self.element_relationships[dominant_element]["generates"] or
                         year_element == self.element_relationships[dominant_element]["strengthened_by"])
        
        if is_supportive:
            current_year_fortune = f"The {year_animal['stem_element']} {year_animal['animal']} year of {current_year} generally supports your personal energy, particularly enhancing your {self.element_relationships[day_master]['strengthened_by']} qualities. This is an excellent time for {random.choice(['starting new projects', 'deepening relationships', 'learning new skills', 'expanding your horizons', 'personal transformation'])}. Pay special attention to opportunities involving {lucky_element} activities or environments, as these align particularly well with this year's energy and your personal chart."
        else:
            current_year_fortune = f"The {year_animal['stem_element']} {year_animal['animal']} year of {current_year} presents some energetic challenges to your chart, as it emphasizes {year_element} qualities that may require adjustment from your dominant {dominant_element} nature. Focus on developing flexibility and consider this a year for {random.choice(['reflection and planning', 'strengthening foundations', 'completing unfinished business', 'internal growth', 'careful preparation'])}. By consciously balancing your natural tendencies with this year's energy, you can transform potential challenges into valuable growth opportunities."
        
        return {
            "personality": personality,
            "life_path": life_path,
            "career": career,
            "relationships": relationships,
            "current_year": current_year_fortune
        } 