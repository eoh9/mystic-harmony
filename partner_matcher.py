import random
import datetime
from typing import Dict, List, Any
from gpt_enhancer import GPTEnhancer

class PartnerMatcher:
    """Class for matching compatible partners based on astrological profiles."""
    
    def __init__(self):
        # Element relationships (promoting, controlling)
        self.element_relationships = {
            "Wood": {"promotes": "Fire", "controls": "Earth", "is_controlled_by": "Metal"},
            "Fire": {"promotes": "Earth", "controls": "Metal", "is_controlled_by": "Water"},
            "Earth": {"promotes": "Metal", "controls": "Water", "is_controlled_by": "Wood"},
            "Metal": {"promotes": "Water", "controls": "Wood", "is_controlled_by": "Fire"},
            "Water": {"promotes": "Wood", "controls": "Fire", "is_controlled_by": "Earth"}
        }
        
        # Zodiac compatibility 
        self.zodiac_compatibility = {
            "Aries": ["Leo", "Sagittarius", "Gemini", "Aquarius"],
            "Taurus": ["Virgo", "Capricorn", "Cancer", "Pisces"],
            "Gemini": ["Libra", "Aquarius", "Aries", "Leo"],
            "Cancer": ["Scorpio", "Pisces", "Taurus", "Virgo"],
            "Leo": ["Aries", "Sagittarius", "Gemini", "Libra"],
            "Virgo": ["Taurus", "Capricorn", "Cancer", "Scorpio"],
            "Libra": ["Gemini", "Aquarius", "Leo", "Sagittarius"],
            "Scorpio": ["Cancer", "Pisces", "Virgo", "Capricorn"],
            "Sagittarius": ["Aries", "Leo", "Libra", "Aquarius"],
            "Capricorn": ["Taurus", "Virgo", "Scorpio", "Pisces"],
            "Aquarius": ["Gemini", "Libra", "Aries", "Sagittarius"],
            "Pisces": ["Cancer", "Scorpio", "Taurus", "Capricorn"]
        }
        
        # Chinese zodiac compatibility
        self.chinese_compatibility = {
            "Rat": ["Dragon", "Monkey", "Ox"],
            "Ox": ["Snake", "Rooster", "Rat"],
            "Tiger": ["Horse", "Dog", "Pig"],
            "Rabbit": ["Sheep", "Pig", "Dog"],
            "Dragon": ["Monkey", "Rat", "Rooster"],
            "Snake": ["Rooster", "Ox", "Monkey"],
            "Horse": ["Sheep", "Tiger", "Dog"],
            "Sheep": ["Rabbit", "Horse", "Pig"],
            "Monkey": ["Rat", "Dragon", "Snake"],
            "Rooster": ["Ox", "Snake", "Dragon"],
            "Dog": ["Tiger", "Rabbit", "Horse"],
            "Pig": ["Rabbit", "Sheep", "Tiger"]
        }
        
        # Personality traits by element
        self.element_traits = {
            "Wood": ["Creative", "Flexible", "Idealistic", "Compassionate", "Visionary", "Growth-oriented"],
            "Fire": ["Passionate", "Dynamic", "Expressive", "Enthusiastic", "Confident", "Adventurous"],
            "Earth": ["Stable", "Practical", "Nurturing", "Patient", "Reliable", "Grounded"],
            "Metal": ["Precise", "Organized", "Disciplined", "Independent", "Determined", "Detail-oriented"],
            "Water": ["Intuitive", "Empathetic", "Deep", "Reflective", "Adaptable", "Philosophical"]
        }
        
        # Meeting locations by element affinity
        self.meeting_locations = {
            "Wood": ["Park", "Botanical garden", "Yoga studio", "Art gallery", "Book store", "Farmers market"],
            "Fire": ["Fitness class", "Concert", "Dance club", "Sports event", "Food festival", "Beach party"],
            "Earth": ["Coffee shop", "Cooking class", "Home improvement store", "Community garden", "Pottery studio", "Local restaurant"],
            "Metal": ["Tech conference", "Museum", "Library", "Professional networking event", "Luxury store", "Design exhibition"],
            "Water": ["Aquarium", "Meditation retreat", "Poetry reading", "Film festival", "Spa", "Ocean-side cafe"]
        }
        
        # Meeting times by element
        self.meeting_times = {
            "Wood": ["Morning", "Spring season", "During outdoor activities"],
            "Fire": ["Midday", "Summer season", "At social gatherings"],
            "Earth": ["Late afternoon", "End of each season", "During practical activities"],
            "Metal": ["Evening", "Autumn season", "During organized events"],
            "Water": ["Night", "Winter season", "During quiet contemplative moments"]
        }
        
        # Initialize the GPT enhancer for richer descriptions
        try:
            # 원래 코드: self.gpt_enhancer = GPTEnhancer()
            # proxies 인자를 전달하지 않도록 명시적으로 초기화
            from gpt_enhancer import GPTEnhancer
            self.gpt_enhancer = GPTEnhancer()
            self.use_gpt = True
        except Exception as e:
            print(f"Error initializing GPT enhancer: {e}")
            self.use_gpt = False

    def find_ideal_partner(self, fortune_data):
        """Generate an ideal partner profile based on the user's fortune data."""
        
        # Get the user's elements and signs
        user_western_sign = fortune_data.get('western_zodiac', {}).get('sign', 'Gemini')
        user_chinese_sign = fortune_data.get('chinese_zodiac', {}).get('animal', 'Dragon')
        user_four_pillars = fortune_data.get('four_pillars', {})
        user_dominant_element = user_four_pillars.get('dominant_element', 'Fire')
        
        # Calculate ideal partner elements
        partner_elements = self._calculate_ideal_partner_elements(user_dominant_element)
        
        # Calculate compatibility scores
        element_compatibility = random.randint(65, 95)
        zodiac_compatibility = self._calculate_zodiac_compatibility(user_western_sign, user_chinese_sign)
        overall_score = int((element_compatibility + zodiac_compatibility) / 2)
        
        # Generate personality traits
        personality_traits = self._generate_personality_traits(partner_elements)
        
        # Generate relationship dynamics
        dynamics = self._analyze_relationship_dynamics(
            user_dominant_element, 
            partner_elements[0], 
            user_western_sign,
            user_chinese_sign
        )
        
        # Generate meeting scenarios
        scenarios = self._generate_meeting_scenarios(partner_elements)
        
        # Enhance with GPT if available
        if self.use_gpt:
            try:
                # Create a profile dictionary for the existing data
                profile = {
                    "compatible_elements": partner_elements,
                    "compatibility_score": overall_score,
                    "element_compatibility": element_compatibility,
                    "zodiac_compatibility": zodiac_compatibility,
                    "personality_traits": personality_traits,
                    "relationship_dynamics": dynamics,
                    "meeting_scenarios": scenarios
                }
                
                # Enhance the relationship dynamics with GPT
                enhanced_dynamics = self.gpt_enhancer.enhance_partner_description(
                    fortune_data, profile
                )
                
                if enhanced_dynamics:
                    dynamics = enhanced_dynamics
                
                # Enhance meeting scenarios
                enhanced_scenarios = self.gpt_enhancer.enhance_meeting_scenarios(scenarios)
                
                if enhanced_scenarios:
                    scenarios = enhanced_scenarios
            except Exception as e:
                print(f"Error enhancing partner profile with GPT: {e}")
                # Fall back to basic descriptions if GPT fails
        
        return {
            "compatible_elements": partner_elements,
            "compatibility_score": overall_score,
            "element_compatibility": element_compatibility,
            "zodiac_compatibility": zodiac_compatibility,
            "personality_traits": personality_traits,
            "relationship_dynamics": dynamics,
            "meeting_scenarios": scenarios
        }

    def _calculate_ideal_partner_elements(self, user_element):
        """Determine the most compatible elements for the user."""
        ideal_elements = []
        
        # First choice: element that is promoted by the user's element
        for element, relationships in self.element_relationships.items():
            if relationships["is_controlled_by"] == user_element:
                ideal_elements.append(element)
                break
        
        # Second choice: element that promotes the user's element
        for element, relationships in self.element_relationships.items():
            if relationships["promotes"] == user_element:
                if element not in ideal_elements:
                    ideal_elements.append(element)
                break
        
        # Third choice: occasionally, the same element can create harmony
        if random.random() < 0.3:  # 30% chance
            if user_element not in ideal_elements:
                ideal_elements.append(user_element)
        else:
            # Otherwise, add a random different element
            remaining_elements = [e for e in ["Wood", "Fire", "Earth", "Metal", "Water"] 
                                 if e not in ideal_elements and e != user_element]
            if remaining_elements:
                ideal_elements.append(random.choice(remaining_elements))
        
        return ideal_elements[:3]  # Return top 3 elements

    def _calculate_zodiac_compatibility(self, western_sign, chinese_sign):
        """Calculate compatibility score based on zodiac signs."""
        score = 70  # Base score
        
        # Western zodiac compatibility adds up to 15 points
        if western_sign in self.zodiac_compatibility:
            compatible_signs = self.zodiac_compatibility[western_sign]
            # Higher score for more compatible signs
            western_bonus = int(15 * (0.5 + 0.5 * random.random()))
            score += western_bonus
        
        # Chinese zodiac compatibility adds up to 15 points
        if chinese_sign in self.chinese_compatibility:
            compatible_signs = self.chinese_compatibility[chinese_sign]
            # Higher score for more compatible signs
            chinese_bonus = int(15 * (0.5 + 0.5 * random.random()))
            score += chinese_bonus
        
        return min(score, 100)  # Cap at 100

    def _generate_personality_traits(self, elements):
        """Generate personality traits based on the compatible elements."""
        traits = []
        
        # Get 2-3 traits from each compatible element
        for element in elements:
            if element in self.element_traits:
                element_traits = self.element_traits[element]
                num_traits = min(random.randint(2, 3), len(element_traits))
                selected_traits = random.sample(element_traits, num_traits)
                traits.extend(selected_traits)
        
        # Ensure we don't have duplicates
        return list(set(traits))[:7]  # Return at most 7 traits

    def _analyze_relationship_dynamics(self, user_element, partner_element, western_sign, chinese_sign):
        """Create a description of the relationship dynamics."""
        
        dynamics_templates = [
            "Your {user_element} energy creates a {relationship_type} with their {partner_element} nature, leading to a relationship where {dynamic_detail}.",
            "As a {western_sign}, you'll find their {partner_element} qualities to be {compatibility_adjective}, creating a bond where {bond_description}.",
            "The {chinese_sign} in you responds well to their {partner_element} influence, resulting in a connection where {connection_detail}.",
            "Your {user_element} essence {interaction_verb} their {partner_element} character, forming a relationship that {relationship_outcome}.",
            "Together, your {western_sign} traits and their {partner_element} energy create a {balance_type} balance, where {balance_detail}."
        ]
        
        relationship_types = {
            "complementary": ["you both enhance each other's strengths", "mutual growth is constant", "inspiration flows naturally"],
            "harmonious": ["communication feels effortless", "understanding comes naturally", "you feel at peace together"],
            "dynamic": ["exciting energy is always present", "you challenge each other positively", "growth comes through creative tension"],
            "nurturing": ["support is freely given and received", "emotional safety is prioritized", "you help each other heal and grow"],
            "balanced": ["give and take feels natural", "you compensate for each other's weaknesses", "stability and excitement coexist"]
        }
        
        compatibility_adjectives = ["refreshing", "grounding", "inspiring", "calming", "energizing", "stabilizing", "transformative"]
        
        bond_descriptions = [
            "you both value personal growth while maintaining togetherness",
            "communication feels both stimulating and comfortable",
            "there's a natural rhythm to how you interact and resolve differences",
            "you inspire each other to become better versions of yourselves",
            "you create a safe space for vulnerability and authenticity"
        ]
        
        connection_details = [
            "intuitive understanding transcends words",
            "mutual respect forms the foundation of your interaction",
            "playfulness and depth coexist beautifully",
            "your shared values create a sense of purpose",
            "daily life together feels both comfortable and exciting"
        ]
        
        interaction_verbs = ["complements", "balances", "enhances", "harmonizes with", "transforms"]
        
        relationship_outcomes = [
            "brings out the best in both of you",
            "creates space for both independence and intimacy",
            "evolves naturally through different life stages",
            "feels both familiar and fresh as time passes",
            "provides both security and adventure"
        ]
        
        balance_types = ["yin-yang", "complementary", "dynamic", "harmonious", "synergistic"]
        
        balance_details = [
            "strength and vulnerability are equally valued",
            "practical matters and emotional needs both receive attention",
            "you support each other's ambitions while maintaining connection",
            "independence and togetherness find a natural rhythm",
            "communication flows even during challenging times"
        ]
        
        # Select and fill templates
        paragraphs = []
        for _ in range(3):  # Generate 3 paragraphs
            template = random.choice(dynamics_templates)
            
            filled_template = template.format(
                user_element=user_element,
                partner_element=partner_element,
                western_sign=western_sign,
                chinese_sign=chinese_sign,
                relationship_type=random.choice(list(relationship_types.keys())),
                dynamic_detail=random.choice(relationship_types[random.choice(list(relationship_types.keys()))]),
                compatibility_adjective=random.choice(compatibility_adjectives),
                bond_description=random.choice(bond_descriptions),
                connection_detail=random.choice(connection_details),
                interaction_verb=random.choice(interaction_verbs),
                relationship_outcome=random.choice(relationship_outcomes),
                balance_type=random.choice(balance_types),
                balance_detail=random.choice(balance_details)
            )
            
            paragraphs.append(filled_template)
        
        return " ".join(paragraphs)

    def _generate_meeting_scenarios(self, partner_elements):
        """Generate potential meeting scenarios based on compatible elements."""
        scenarios = []
        
        # Create 2-3 meeting scenarios
        num_scenarios = random.randint(2, 3)
        used_locations = set()
        
        for _ in range(num_scenarios):
            # Select an element to base this scenario on
            element = random.choice(partner_elements)
            
            # Select location
            potential_locations = [loc for loc in self.meeting_locations[element] if loc not in used_locations]
            if not potential_locations:  # If we've used all locations for this element
                potential_locations = self.meeting_locations[element]
            
            location = random.choice(potential_locations)
            used_locations.add(location)
            
            # Select time
            time = random.choice(self.meeting_times[element])
            
            # Generate scenario description
            situation_templates = [
                "You both reach for the same {item} and your eyes meet.",
                "They ask you for {advice} and the conversation flows naturally.",
                "You notice them {activity} and feel drawn to their energy.",
                "You're introduced by a mutual {connection} who thinks you'd click.",
                "You both comment on the same {observation} and discover a shared perspective.",
                "You accidentally {mishap} and they help you with a warm smile.",
                "You overhear them talking about {topic} which happens to be your passion too."
            ]
            
            items = ["book", "coffee", "artwork", "menu item", "product", "seat", "handout"]
            advice = ["recommendation", "direction", "opinion", "help with a decision", "perspective"]
            activities = ["reading your favorite author", "enjoying the music", "practicing a skill", "deeply focused on their work", "laughing at something"]
            connections = ["friend", "colleague", "family member", "acquaintance", "neighbor"]
            observations = ["unusual event", "beautiful detail", "interesting person", "quality of the atmosphere", "unexpected occurrence"]
            mishaps = ["drop something", "bump into them", "lose your way", "misunderstand an instruction", "struggle with something simple"]
            topics = ["a book you love", "a place you've visited", "a hobby you enjoy", "a philosophical idea", "a shared interest"]
            
            template = random.choice(situation_templates)
            
            if "{item}" in template:
                situation = template.format(item=random.choice(items))
            elif "{advice}" in template:
                situation = template.format(advice=random.choice(advice))
            elif "{activity}" in template:
                situation = template.format(activity=random.choice(activities))
            elif "{connection}" in template:
                situation = template.format(connection=random.choice(connections))
            elif "{observation}" in template:
                situation = template.format(observation=random.choice(observations))
            elif "{mishap}" in template:
                situation = template.format(mishap=random.choice(mishaps))
            elif "{topic}" in template:
                situation = template.format(topic=random.choice(topics))
            else:
                situation = template
            
            scenarios.append({
                "location": location,
                "time": time,
                "situation": situation
            })
        
        return scenarios 