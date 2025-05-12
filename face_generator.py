import numpy as np
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from typing import Dict, List, Any
import io
import base64
import math

class FaceGenerator:
    """
    Class to generate abstract visualizations of a potential partner's face
    based on their astrological profile.
    
    This is a simple implementation that creates abstract/artistic representations
    without using external ML APIs for actual face generation.
    """
    
    def __init__(self):
        # 얼굴 생성을 위한 기본 설정
        self.face_shapes = ['oval', 'round', 'square', 'heart', 'oblong']
        self.eye_shapes = ['almond', 'round', 'hooded', 'monolid', 'upturned']
        self.nose_types = ['straight', 'curved', 'button', 'aquiline']
        self.lip_shapes = ['full', 'thin', 'bow', 'heart', 'wide']
        
        # 원소별 특징
        self.element_features = {
            'Wood': {
                'face_shape': ['oval', 'oblong'],
                'features': 'soft and graceful',
                'complexion': 'fresh and clear',
                'expression': 'gentle and growing'
            },
            'Fire': {
                'face_shape': ['heart', 'diamond'],
                'features': 'sharp and defined',
                'complexion': 'warm and glowing',
                'expression': 'passionate and bright'
            },
            'Earth': {
                'face_shape': ['round', 'square'],
                'features': 'balanced and stable',
                'complexion': 'earthy and healthy',
                'expression': 'calm and grounded'
            },
            'Metal': {
                'face_shape': ['square', 'angular'],
                'features': 'precise and refined',
                'complexion': 'clear and luminous',
                'expression': 'focused and determined'
            },
            'Water': {
                'face_shape': ['round', 'fluid'],
                'features': 'soft and flowing',
                'complexion': 'smooth and hydrated',
                'expression': 'mysterious and deep'
            }
        }
        
        # Element color palettes
        self.element_colors = {
            'Wood': ['#4CAF50', '#81C784', '#A5D6A7'],  # Green
            'Fire': ['#F44336', '#EF5350', '#E57373'],  # Red
            'Earth': ['#FFC107', '#FFD54F', '#FFE082'],  # Yellow
            'Metal': ['#9E9E9E', '#BDBDBD', '#E0E0E0'],  # Gray
            'Water': ['#2196F3', '#42A5F5', '#64B5F6']   # Blue
        }
        
        # Shape characteristics for zodiac signs
        self.zodiac_shapes = {
            'Aries': {'shape': 'triangle', 'curves': 'sharp'},
            'Taurus': {'shape': 'round', 'curves': 'smooth'},
            'Gemini': {'shape': 'dual', 'curves': 'mixed'},
            'Cancer': {'shape': 'oval', 'curves': 'soft'},
            'Leo': {'shape': 'radiant', 'curves': 'bold'},
            'Virgo': {'shape': 'precise', 'curves': 'delicate'},
            'Libra': {'shape': 'balanced', 'curves': 'symmetric'},
            'Scorpio': {'shape': 'intense', 'curves': 'deep'},
            'Sagittarius': {'shape': 'arrows', 'curves': 'dynamic'},
            'Capricorn': {'shape': 'structured', 'curves': 'angular'},
            'Aquarius': {'shape': 'unusual', 'curves': 'wavy'},
            'Pisces': {'shape': 'flowing', 'curves': 'fluid'}
        }
        
        # Textures based on Chinese zodiac
        self.chinese_zodiac_textures = {
            'Rat': 'detailed',
            'Ox': 'solid',
            'Tiger': 'striped',
            'Rabbit': 'soft',
            'Dragon': 'scaled',
            'Snake': 'smooth',
            'Horse': 'strong',
            'Goat': 'textured',
            'Monkey': 'playful',
            'Rooster': 'detailed',
            'Dog': 'loyal',
            'Pig': 'rounded'
        }
        
    def generate_partner_face(self, user_fortune: Dict, partner_profile: Dict) -> Dict[str, Any]:
        """
        Generate a visual representation of the ideal partner's face
        
        Args:
            user_fortune: User's fortune data
            partner_profile: Partner compatibility data
            
        Returns:
            Dictionary containing the image and description
        """
        # Extract relevant attributes
        compatible_elements = partner_profile.get('compatible_elements', ['Wood', 'Water'])
        compatible_zodiacs = partner_profile.get('compatible_zodiacs', ['Libra'])
        compatible_chinese = partner_profile.get('compatible_chinese', ['Dragon'])
        aura_colors = partner_profile.get('aura_colors', [])
        
        # Default values if any are missing
        if not compatible_elements:
            compatible_elements = ['Wood', 'Water']
        if not compatible_zodiacs:
            compatible_zodiacs = ['Libra']
        if not compatible_chinese:
            compatible_chinese = ['Dragon']
        if not aura_colors:
            aura_colors = ['#4CAF50', '#2196F3', '#9C27B0']
        
        # Generate image
        image = self._create_abstract_face(
            compatible_elements,
            compatible_zodiacs[0] if compatible_zodiacs else 'Libra',
            compatible_chinese[0] if compatible_chinese else 'Dragon',
            aura_colors
        )
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Generate description
        aura_description = self._generate_aura_description(
            compatible_elements, 
            compatible_zodiacs[0] if compatible_zodiacs else 'Libra',
            compatible_chinese[0] if compatible_chinese else 'Dragon'
        )
        
        return {
            'image': img_str,
            'aura_description': aura_description,
            'color_palette': aura_colors
        }
        
    def _create_abstract_face(self, elements: List[str], zodiac: str, 
                             chinese: str, colors: List[str]) -> Image.Image:
        """Generate an abstract face image"""
        # Create a white background
        width, height = 500, 600
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Background aura
        self._draw_aura_background(image, colors)
        
        # Get shape characteristics
        shape_style = self.zodiac_shapes.get(zodiac, {'shape': 'oval', 'curves': 'smooth'})
        texture = self.chinese_zodiac_textures.get(chinese, 'detailed')
        
        # Face outline
        self._draw_face_outline(draw, width, height, shape_style, colors[0] if colors else '#9C27B0')
        
        # Eyes based on elements
        self._draw_eyes(draw, width, height, elements, colors)
        
        # Nose and mouth
        self._draw_nose_mouth(draw, width, height, zodiac, colors)
        
        # Apply texture and effects
        image = self._apply_texture(image, texture)
        image = self._add_element_effects(image, elements)
        
        return image
    
    def _draw_aura_background(self, image: Image.Image, colors: List[str]) -> None:
        """Draw aura-like background effect"""
        width, height = image.size
        
        # Create gradient overlay
        overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw radial gradient
        for i in range(10):
            radius = min(width, height) - i * 20
            color = colors[i % len(colors)]
            # Convert hex to RGB with alpha
            r, g, b = self._hex_to_rgb(color)
            alpha = 50 - i * 5  # Decreasing opacity
            rgba = (r, g, b, alpha)
            
            draw.ellipse(
                (width/2 - radius/2, height/2 - radius/2, 
                 width/2 + radius/2, height/2 + radius/2),
                fill=rgba,
                outline=None
            )
        
        # Blend overlay with original image
        image.paste(overlay, (0, 0), overlay)
        
        # Apply blur
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        
    def _draw_face_outline(self, draw: ImageDraw.Draw, width: int, height: int, 
                          shape_style: Dict, color: str) -> None:
        """Draw face outline based on zodiac shape"""
        shape = shape_style['shape']
        curves = shape_style['curves']
        
        # Convert hex to RGB
        rgb = self._hex_to_rgb(color)
        
        # Face center and dimensions
        center_x, center_y = width // 2, height // 2 - 50
        face_width = width * 0.7
        face_height = height * 0.6
        
        if shape == 'round' or shape == 'oval':
            # Oval face
            draw.ellipse(
                (center_x - face_width/2, center_y - face_height/2,
                 center_x + face_width/2, center_y + face_height/2),
                outline=rgb,
                width=3
            )
        elif shape == 'triangle' or shape == 'arrows':
            # More angular face
            points = [
                (center_x, center_y - face_height/2),  # Top
                (center_x - face_width/2, center_y + face_height/2),  # Bottom left
                (center_x + face_width/2, center_y + face_height/2)   # Bottom right
            ]
            draw.polygon(points, outline=rgb, fill=None)
        elif shape == 'balanced' or shape == 'structured':
            # More structured face
            draw.rectangle(
                (center_x - face_width/2, center_y - face_height/2,
                 center_x + face_width/2, center_y + face_height/2),
                outline=rgb,
                width=3
            )
        elif shape == 'dual':
            # Two overlapping shapes
            offset = 30
            draw.ellipse(
                (center_x - face_width/2 - offset, center_y - face_height/2,
                 center_x + face_width/2 - offset, center_y + face_height/2),
                outline=rgb,
                width=2
            )
            draw.ellipse(
                (center_x - face_width/2 + offset, center_y - face_height/2,
                 center_x + face_width/2 + offset, center_y + face_height/2),
                outline=rgb,
                width=2
            )
        else:
            # Default to oval with unique characteristics
            draw.ellipse(
                (center_x - face_width/2, center_y - face_height/2,
                 center_x + face_width/2, center_y + face_height/2),
                outline=rgb,
                width=3
            )
            
            # Add extra details based on curves
            if curves == 'wavy':
                # Add wavy lines
                for i in range(0, 360, 30):
                    angle = math.radians(i)
                    x1 = center_x + (face_width/2 - 10) * math.cos(angle)
                    y1 = center_y + (face_height/2 - 10) * math.sin(angle)
                    x2 = center_x + (face_width/2 + 20) * math.cos(angle)
                    y2 = center_y + (face_height/2 + 20) * math.sin(angle)
                    draw.line((x1, y1, x2, y2), fill=rgb, width=1)
            elif curves == 'sharp':
                # Add sharp angles
                points = []
                for i in range(0, 360, 40):
                    angle = math.radians(i)
                    r = face_width/2 if i % 80 == 0 else face_width/2 - 10
                    x = center_x + r * math.cos(angle)
                    y = center_y + r * math.sin(angle)
                    points.append((x, y))
                draw.polygon(points, outline=rgb, width=1, fill=None)
    
    def _draw_eyes(self, draw: ImageDraw.Draw, width: int, height: int, 
                  elements: List[str], colors: List[str]) -> None:
        """Draw eyes based on elements"""
        center_x, center_y = width // 2, height // 2 - 50
        eye_distance = width * 0.25
        eye_size = width * 0.12
        
        # Left eye
        left_eye_x = center_x - eye_distance / 2
        left_eye_y = center_y - height * 0.05
        
        # Right eye
        right_eye_x = center_x + eye_distance / 2
        right_eye_y = center_y - height * 0.05
        
        # Determine eye shape based on primary element
        primary_element = elements[0] if elements else 'Wood'
        
        if primary_element == 'Wood':
            # Almond-shaped eyes
            draw.ellipse(
                (left_eye_x - eye_size/2, left_eye_y - eye_size/3,
                 left_eye_x + eye_size/2, left_eye_y + eye_size/3),
                outline=self._hex_to_rgb(colors[0] if colors else '#4CAF50'),
                width=2
            )
            draw.ellipse(
                (right_eye_x - eye_size/2, right_eye_y - eye_size/3,
                 right_eye_x + eye_size/2, right_eye_y + eye_size/3),
                outline=self._hex_to_rgb(colors[0] if colors else '#4CAF50'),
                width=2
            )
        elif primary_element == 'Fire':
            # Sharp, angled eyes
            draw.polygon(
                [(left_eye_x - eye_size/2, left_eye_y),
                 (left_eye_x, left_eye_y - eye_size/3),
                 (left_eye_x + eye_size/2, left_eye_y),
                 (left_eye_x, left_eye_y + eye_size/3)],
                outline=self._hex_to_rgb(colors[0] if colors else '#F44336')
            )
            draw.polygon(
                [(right_eye_x - eye_size/2, right_eye_y),
                 (right_eye_x, right_eye_y - eye_size/3),
                 (right_eye_x + eye_size/2, right_eye_y),
                 (right_eye_x, right_eye_y + eye_size/3)],
                outline=self._hex_to_rgb(colors[0] if colors else '#F44336')
            )
        elif primary_element == 'Earth':
            # Round, stable eyes
            draw.ellipse(
                (left_eye_x - eye_size/2, left_eye_y - eye_size/2,
                 left_eye_x + eye_size/2, left_eye_y + eye_size/2),
                outline=self._hex_to_rgb(colors[0] if colors else '#FFC107'),
                width=2
            )
            draw.ellipse(
                (right_eye_x - eye_size/2, right_eye_y - eye_size/2,
                 right_eye_x + eye_size/2, right_eye_y + eye_size/2),
                outline=self._hex_to_rgb(colors[0] if colors else '#FFC107'),
                width=2
            )
        elif primary_element == 'Metal':
            # Sharp, precise eyes
            draw.rectangle(
                (left_eye_x - eye_size/2, left_eye_y - eye_size/4,
                 left_eye_x + eye_size/2, left_eye_y + eye_size/4),
                outline=self._hex_to_rgb(colors[0] if colors else '#9E9E9E'),
                width=2
            )
            draw.rectangle(
                (right_eye_x - eye_size/2, right_eye_y - eye_size/4,
                 right_eye_x + eye_size/2, right_eye_y + eye_size/4),
                outline=self._hex_to_rgb(colors[0] if colors else '#9E9E9E'),
                width=2
            )
        else:  # Water
            # Flowing, curved eyes
            for i in range(3):
                draw.arc(
                    (left_eye_x - eye_size/2 - i*2, left_eye_y - eye_size/3 - i*2,
                     left_eye_x + eye_size/2 + i*2, left_eye_y + eye_size/3 + i*2),
                    200, 340,
                    fill=self._hex_to_rgb(colors[0] if colors else '#2196F3'),
                    width=1
                )
                draw.arc(
                    (right_eye_x - eye_size/2 - i*2, right_eye_y - eye_size/3 - i*2,
                     right_eye_x + eye_size/2 + i*2, right_eye_y + eye_size/3 + i*2),
                    200, 340,
                    fill=self._hex_to_rgb(colors[0] if colors else '#2196F3'),
                    width=1
                )
    
    def _draw_nose_mouth(self, draw: ImageDraw.Draw, width: int, height: int, 
                        zodiac: str, colors: List[str]) -> None:
        """Draw nose and mouth based on zodiac sign"""
        center_x, center_y = width // 2, height // 2 - 50
        
        # Nose position
        nose_x, nose_y = center_x, center_y + height * 0.1
        nose_size = width * 0.05
        
        # Mouth position
        mouth_x, mouth_y = center_x, center_y + height * 0.25
        mouth_width = width * 0.3
        mouth_height = height * 0.05
        
        # Set color
        color = self._hex_to_rgb(colors[1] if len(colors) > 1 else colors[0] if colors else '#9C27B0')
        
        # Determine style based on zodiac
        if zodiac in ['Aries', 'Leo', 'Sagittarius']:  # Fire signs
            # Bold, expressive features
            draw.polygon(
                [(nose_x, nose_y - nose_size),
                 (nose_x - nose_size, nose_y + nose_size),
                 (nose_x + nose_size, nose_y + nose_size)],
                outline=color
            )
            
            # Smiling mouth
            draw.arc(
                (mouth_x - mouth_width/2, mouth_y - mouth_height,
                 mouth_x + mouth_width/2, mouth_y + mouth_height),
                0, 180,
                fill=color,
                width=2
            )
        elif zodiac in ['Taurus', 'Virgo', 'Capricorn']:  # Earth signs
            # Practical, grounded features
            draw.rectangle(
                (nose_x - nose_size/2, nose_y - nose_size,
                 nose_x + nose_size/2, nose_y + nose_size),
                outline=color
            )
            
            # Straight mouth
            draw.line(
                (mouth_x - mouth_width/2, mouth_y, 
                 mouth_x + mouth_width/2, mouth_y),
                fill=color,
                width=2
            )
        elif zodiac in ['Gemini', 'Libra', 'Aquarius']:  # Air signs
            # Light, intellectual features
            draw.line(
                (nose_x, nose_y - nose_size,
                 nose_x, nose_y + nose_size),
                fill=color,
                width=2
            )
            
            # Slight smile
            draw.arc(
                (mouth_x - mouth_width/2, mouth_y - mouth_height*2,
                 mouth_x + mouth_width/2, mouth_y + mouth_height*2),
                0, 180,
                fill=color,
                width=1
            )
        else:  # Water signs
            # Flowing, emotional features
            for i in range(3):
                draw.arc(
                    (nose_x - nose_size - i, nose_y - nose_size - i,
                     nose_x + nose_size + i, nose_y + nose_size + i),
                    220, 320,
                    fill=color,
                    width=1
                )
            
            # Wavy mouth
            for i in range(mouth_width):
                x = mouth_x - mouth_width/2 + i
                y = mouth_y + math.sin(i * 0.2) * mouth_height
                draw.point((x, y), fill=color)
    
    def _apply_texture(self, image: Image.Image, texture: str) -> Image.Image:
        """Apply texture effect based on Chinese zodiac"""
        if texture == 'detailed' or texture == 'striped':
            # Add some noise
            noise = Image.new('RGB', image.size, 'white')
            noise_draw = ImageDraw.Draw(noise)
            
            for x in range(0, image.width, 2):
                for y in range(0, image.height, 2):
                    if random.random() > 0.7:
                        noise_draw.point((x, y), fill='black')
            
            noise = noise.filter(ImageFilter.GaussianBlur(radius=1))
            image = Image.blend(image, noise, 0.1)
            
        elif texture == 'soft' or texture == 'smooth':
            # Soften the image
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(0.9)
            
        elif texture == 'scaled' or texture == 'textured':
            # Add a pattern
            pattern = Image.new('RGB', image.size, 'white')
            pattern_draw = ImageDraw.Draw(pattern)
            
            size = 10
            for x in range(0, image.width, size):
                for y in range(0, image.height, size):
                    if (x + y) % (size*2) == 0:
                        pattern_draw.rectangle(
                            (x, y, x + size, y + size),
                            fill=(211, 211, 211)
                        )
            
            pattern = pattern.filter(ImageFilter.GaussianBlur(radius=2))
            image = Image.blend(image, pattern, 0.1)
            
        elif texture == 'strong' or texture == 'loyal':
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
        
        return image
    
    def _add_element_effects(self, image: Image.Image, elements: List[str]) -> Image.Image:
        """Add special effects based on elements"""
        if not elements:
            return image
            
        # Create a copy to work with
        result = image.copy()
        width, height = image.size
        
        for element in elements:
            if element == 'Fire':
                # Add warm glow
                overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                
                center_x, center_y = width // 2, height // 2
                for i in range(5):
                    radius = 100 - i * 15
                    draw.ellipse(
                        (center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius),
                        fill=(255, 100, 0, 10),
                        outline=None
                    )
                
                # Convert to RGB for blending
                overlay_rgb = Image.new('RGB', image.size, 'white')
                overlay_rgb.paste(overlay, (0, 0), overlay)
                
                # Blend with result
                result = Image.blend(result, overlay_rgb, 0.2)
                
            elif element == 'Water':
                # Add blue shimmering effect
                result = result.filter(ImageFilter.GaussianBlur(radius=0.5))
                blue_overlay = Image.new('RGB', image.size, (230, 240, 255))
                result = Image.blend(result, blue_overlay, 0.1)
                
            elif element == 'Earth':
                # Add stability and warmth
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(1.2)
                
                brown_overlay = Image.new('RGB', image.size, (255, 250, 240))
                result = Image.blend(result, brown_overlay, 0.1)
                
            elif element == 'Metal':
                # Add sharpness and clarity
                enhancer = ImageEnhance.Sharpness(result)
                result = enhancer.enhance(1.5)
                
                gray_overlay = Image.new('RGB', image.size, (245, 245, 245))
                result = Image.blend(result, gray_overlay, 0.1)
                
            elif element == 'Wood':
                # Add vibrant green undertones
                green_overlay = Image.new('RGB', image.size, (240, 255, 240))
                result = Image.blend(result, green_overlay, 0.1)
                
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(1.1)
        
        return result
    
    def _generate_aura_description(self, elements: List[str], zodiac: str, chinese: str) -> str:
        """Generate a description of the partner's aura and energy"""
        element_qualities = {
            'Wood': 'growing, vital, and expansive',
            'Fire': 'warm, passionate, and dynamic',
            'Earth': 'grounding, nurturing, and stable',
            'Metal': 'clear, precise, and refined',
            'Water': 'flowing, intuitive, and adaptable'
        }
        
        zodiac_qualities = {
            'Aries': 'bold leadership and pioneering spirit',
            'Taurus': 'sensual presence and steadfast reliability',
            'Gemini': 'sparkling intelligence and quick wit',
            'Cancer': 'empathetic warmth and nurturing energy',
            'Leo': 'radiant charisma and generous heart',
            'Virgo': 'thoughtful precision and helpful nature',
            'Libra': 'harmonious balance and diplomatic grace',
            'Scorpio': 'magnetic intensity and transformative power',
            'Sagittarius': 'adventurous optimism and philosophical depth',
            'Capricorn': 'ambitious drive and practical wisdom',
            'Aquarius': 'innovative vision and humanitarian ideals',
            'Pisces': 'dreamy imagination and compassionate soul'
        }
        
        chinese_qualities = {
            'Rat': 'resourceful adaptability',
            'Ox': 'dependable diligence',
            'Tiger': 'courageous leadership',
            'Rabbit': 'gentle compassion',
            'Dragon': 'majestic creativity',
            'Snake': 'wise intuition',
            'Horse': 'spirited freedom',
            'Goat': 'artistic sensitivity',
            'Monkey': 'clever versatility',
            'Rooster': 'precise discernment',
            'Dog': 'loyal protection',
            'Pig': 'generous enjoyment'
        }
        
        # Element descriptions
        element_desc = []
        for element in elements:
            if element in element_qualities:
                element_desc.append(element_qualities[element])
        
        if not element_desc:
            element_desc = ["balanced and harmonious"]
        
        # Get zodiac and chinese qualities
        zodiac_quality = zodiac_qualities.get(zodiac, "balanced energy")
        chinese_quality = chinese_qualities.get(chinese, "harmonious presence")
        
        # Create description
        description = f"""
        This face emanates an aura that is {element_desc[0]}, with undertones of 
        {element_desc[1] if len(element_desc) > 1 else 'mystical depth'}. 
        
        The essence combines {zodiac_quality} with {chinese_quality}, creating a 
        unique visual energy signature that would complement your own celestial blueprint.
        
        The features reflect a soul whose elemental nature would create balance and 
        harmony with yours, enhancing both your strengths while providing support for 
        your challenges.
        """
        
        return description.strip()
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color code to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) 