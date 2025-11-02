"""
Universal AI-Powered Recommendation System
Works with ANY subject: Peptides, Supplements, Training, Nutrition, Recovery, etc.
"""
import os
from openai import OpenAI
from datetime import datetime

class UniversalRecommendationAI:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            # Configure OpenAI client with timeout and retry settings
            self.client = OpenAI(
                api_key=api_key,
                timeout=60.0,  # Increase timeout to 60 seconds
                max_retries=3   # Retry up to 3 times on connection errors
            )

        # Knowledge base for different subjects
        self.subject_templates = {
            'peptides': {
                'expert_role': 'expert peptide therapy advisor and metabolic health specialist',
                'categories': [
                    'Recovery & Healing: BPC-157, TB-500, GHK-Cu',
                    'Fat Loss & Metabolism: Semaglutide, Tirzepatide, AOD-9604, CJC-1295/Ipamorelin',
                    'Muscle Growth: CJC-1295, Ipamorelin, Tesamorelin, MK-677',
                    'Anti-Aging & Longevity: Epithalon, MOTS-c, Thymosin Alpha-1',
                    'Performance: BPC-157, TB-500, Hexarelin',
                    'Sleep & Recovery: DSIP, Selank'
                ],
                'output_sections': [
                    'Primary Peptide Recommendations (2-3 most suited)',
                    'Dosing Protocol for each',
                    'Scientific Rationale',
                    'Expected Benefits and Timeline',
                    'Stacking Recommendations',
                    'Safety Considerations',
                    'Lifestyle Optimization tips'
                ]
            },
            'supplements': {
                'expert_role': 'expert nutritionist and supplementation specialist',
                'categories': [
                    'Performance: Creatine, Beta-Alanine, Citrulline, Caffeine',
                    'Recovery: Magnesium, Zinc, Vitamin D, Omega-3',
                    'Metabolic Health: Berberine, Alpha Lipoic Acid, CoQ10',
                    'Cognitive: Lion\'s Mane, Bacopa, Rhodiola, L-Theanine',
                    'Longevity: NAD+, NMN, Resveratrol, Spermidine',
                    'Gut Health: Probiotics, Digestive Enzymes, L-Glutamine'
                ],
                'output_sections': [
                    'Primary Supplement Stack (4-6 supplements)',
                    'Dosing & Timing Protocol',
                    'Scientific Rationale',
                    'Expected Benefits',
                    'Synergistic Combinations',
                    'Quality & Sourcing Recommendations',
                    'Dietary Optimization tips'
                ]
            },
            'training': {
                'expert_role': 'elite strength and conditioning coach with expertise in metabolic optimization',
                'categories': [
                    'Zone 2 Training: Low-intensity aerobic work',
                    'HIIT: High-intensity interval training',
                    'Strength Training: Progressive overload protocols',
                    'Power Development: Explosive movements',
                    'Mobility & Recovery: Active recovery protocols',
                    'Sport-Specific: Periodization strategies'
                ],
                'output_sections': [
                    'Weekly Training Schedule',
                    'Specific Workout Protocols',
                    'Intensity Zones (based on metabolic data)',
                    'Progressive Overload Strategy',
                    'Recovery Protocols',
                    'Periodization Plan',
                    'Performance Metrics to Track'
                ]
            },
            'nutrition': {
                'expert_role': 'registered dietitian specialized in metabolic health and performance nutrition',
                'categories': [
                    'Macronutrient Distribution',
                    'Meal Timing & Frequency',
                    'Pre/Post Workout Nutrition',
                    'Metabolic Flexibility Strategies',
                    'Fat Adaptation Protocols',
                    'Carb Cycling Approaches'
                ],
                'output_sections': [
                    'Personalized Macro Targets',
                    'Daily Meal Plan Structure',
                    'Nutrient Timing Strategy',
                    'Food Quality Recommendations',
                    'Hydration Protocol',
                    'Metabolic Flexibility Tips',
                    'Supplementation to Complement Diet'
                ]
            },
            'recovery': {
                'expert_role': 'recovery and regeneration specialist',
                'categories': [
                    'Sleep Optimization',
                    'Active Recovery Protocols',
                    'Stress Management',
                    'Cold/Heat Therapy',
                    'Bodywork & Manual Therapy',
                    'Technology-Assisted Recovery'
                ],
                'output_sections': [
                    'Sleep Protocol',
                    'Daily Recovery Routine',
                    'Weekly Recovery Schedule',
                    'Stress Reduction Strategies',
                    'Recovery Modalities',
                    'Tracking & Monitoring',
                    'Red Flags to Watch For'
                ]
            },
            'longevity': {
                'expert_role': 'longevity medicine specialist focused on healthspan optimization',
                'categories': [
                    'Metabolic Health Optimization',
                    'Cellular Health & Autophagy',
                    'Inflammation Management',
                    'Hormetic Stressors',
                    'Biomarker Tracking',
                    'Preventive Interventions'
                ],
                'output_sections': [
                    'Longevity Protocol Overview',
                    'Dietary Interventions',
                    'Exercise & Movement',
                    'Supplement Stack',
                    'Lifestyle Practices',
                    'Biomarkers to Monitor',
                    'Long-term Health Strategy'
                ]
            }
        }

    def get_recommendations(self, subject, metabolic_data, user_goals=None, custom_context=None):
        """
        Get AI-powered recommendations for ANY subject

        Args:
            subject (str): The subject area (peptides, supplements, training, nutrition, etc.)
            metabolic_data (dict): User's metabolic test data
            user_goals (list): User's health/fitness goals
            custom_context (str): Additional custom context

        Returns:
            dict: Comprehensive recommendations
        """

        # Normalize subject
        subject = subject.lower()

        # Get template or use custom if subject not in templates
        if subject in self.subject_templates:
            template = self.subject_templates[subject]
        else:
            # Create generic template for custom subjects
            template = self._create_custom_template(subject)

        # Build the prompt
        prompt = self._build_prompt(subject, template, metabolic_data, user_goals, custom_context)

        # Check if API client is available
        if not self.client:
            return {
                'subject': subject,
                'recommendations': '''AI recommendations are currently unavailable because the OpenAI API key is not configured.

To enable AI recommendations:
1. Add the OPENAI_API_KEY environment variable to your Render service
2. Get an API key from https://platform.openai.com/api-keys
3. Restart your service after adding the key

Once configured, you'll be able to generate unlimited personalized recommendations for peptides, supplements, training, nutrition, and more!''',
                'timestamp': datetime.now().isoformat(),
                'metabolic_summary': self._summarize_metabolic_data(metabolic_data),
                'error': True
            }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(template)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )

            recommendation_text = response.choices[0].message.content

            return {
                'subject': subject,
                'recommendations': recommendation_text,
                'timestamp': datetime.now().isoformat(),
                'metabolic_summary': self._summarize_metabolic_data(metabolic_data)
            }

        except Exception as e:
            error_msg = str(e)
            print(f"Error generating {subject} recommendations: {error_msg}")
            return {
                'subject': subject,
                'recommendations': f"""## Error Generating {subject.title()} Recommendations

**Error Details:** {error_msg}

This error occurred while trying to generate AI recommendations. Common causes:
- OpenAI API quota exceeded or billing issue
- Invalid API key
- Rate limiting
- Network connectivity issue

Please check your OpenAI account at https://platform.openai.com/account/usage to verify:
1. Your API key is valid
2. You have available credits
3. Your usage limits haven't been exceeded""",
                'timestamp': datetime.now().isoformat(),
                'metabolic_summary': self._summarize_metabolic_data(metabolic_data),
                'error': True,
                'error_message': error_msg
            }

    def _create_custom_template(self, subject):
        """Create a template for custom subjects"""
        return {
            'expert_role': f'expert {subject} specialist with deep knowledge of metabolic health',
            'categories': [f'{subject.title()} strategies and protocols'],
            'output_sections': [
                f'Top {subject.title()} Recommendations',
                'Personalized Protocol',
                'Scientific Rationale',
                'Expected Outcomes',
                'Implementation Guide',
                'Safety & Considerations'
            ]
        }

    def _get_system_prompt(self, template):
        """Build system prompt based on template"""
        categories_text = '\n'.join([f'- {cat}' for cat in template['categories']])

        return f"""You are an {template['expert_role']}.

You analyze metabolic test data (VO2 Max, RMR, substrate utilization, heart rate zones, etc.)
and provide evidence-based, personalized recommendations.

Key Areas of Focus:
{categories_text}

Your recommendations should:
1. Be deeply personalized based on the metabolic profile
2. Consider the user's specific goals
3. Be evidence-based and scientifically sound
4. Include specific, actionable protocols
5. Explain the scientific rationale
6. Mention expected benefits and timelines
7. Include safety considerations
8. Be practical and realistic

Always provide appropriate disclaimers about consulting healthcare providers."""

    def _build_prompt(self, subject, template, metabolic_data, user_goals, custom_context):
        """Build the user prompt with all context"""

        sections_text = '\n'.join([f'{i+1}. **{section}**' for i, section in enumerate(template['output_sections'])])

        goals_text = ', '.join(user_goals) if user_goals else 'General health and performance optimization'

        custom_text = f"\n\n## Additional Context:\n{custom_context}" if custom_context else ""

        prompt = f"""Analyze this metabolic profile and provide personalized {subject} recommendations:

## Metabolic Data:
- VO2 Max: {metabolic_data.get('vo2_max', 'N/A')} ml/kg/min
- Resting Metabolic Rate: {metabolic_data.get('rmr', 'N/A')} kcal/day
- Max Heart Rate: {metabolic_data.get('max_hr', 'N/A')} bpm
- Resting Heart Rate: {metabolic_data.get('resting_hr', 'N/A')} bpm
- Fat Oxidation Rate: {metabolic_data.get('fat_oxidation', 'N/A')} g/min
- Carb Oxidation Rate: {metabolic_data.get('carb_oxidation', 'N/A')} g/min
- Respiratory Exchange Ratio (RER): {metabolic_data.get('rer', 'N/A')}
- Age: {metabolic_data.get('age', 'N/A')}
- Gender: {metabolic_data.get('gender', 'N/A')}
- Weight: {metabolic_data.get('weight', 'N/A')} kg
- Height: {metabolic_data.get('height', 'N/A')} cm
- Biological Age: {metabolic_data.get('biological_age', 'N/A')}
- Metabolic Efficiency: {metabolic_data.get('metabolic_score', 'N/A')}/100

## User Goals:
{goals_text}{custom_text}

Please provide a comprehensive {subject} protocol covering:
{sections_text}

Format your response with clear headers, bullet points, and actionable recommendations."""

        return prompt

    def _summarize_metabolic_data(self, data):
        """Create a summary of key metabolic metrics"""
        return {
            'vo2_max': data.get('vo2_max'),
            'rmr': data.get('rmr'),
            'metabolic_age': data.get('biological_age'),
            'aerobic_fitness': self._classify_vo2_max(data.get('vo2_max'), data.get('age'), data.get('gender'))
        }

    def _classify_vo2_max(self, vo2_max, age, gender):
        """Classify VO2 max fitness level"""
        if not vo2_max or not age or not gender:
            return 'Unknown'

        try:
            vo2 = float(vo2_max)
            age = int(age)

            # Simple classification (male, age 20-40)
            if gender.lower() == 'male':
                if vo2 >= 50:
                    return 'Excellent'
                elif vo2 >= 43:
                    return 'Good'
                elif vo2 >= 35:
                    return 'Average'
                else:
                    return 'Below Average'
            else:
                if vo2 >= 42:
                    return 'Excellent'
                elif vo2 >= 35:
                    return 'Good'
                elif vo2 >= 27:
                    return 'Average'
                else:
                    return 'Below Average'
        except:
            return 'Unknown'

    def _get_fallback(self, subject, metabolic_data):
        """Fallback response if AI fails"""
        return {
            'subject': subject,
            'recommendations': f"""## {subject.title()} Recommendations

I apologize, but I'm having trouble generating personalized {subject} recommendations at this moment.

### General Guidance:
Based on your metabolic profile, consider consulting with a qualified professional who specializes in {subject} to develop a personalized protocol.

**Important**: Always work with licensed healthcare providers when implementing new {subject} protocols.
""",
            'timestamp': datetime.now().isoformat(),
            'metabolic_summary': self._summarize_metabolic_data(metabolic_data),
            'error': True
        }

    def get_available_subjects(self):
        """Return list of pre-configured subjects"""
        return list(self.subject_templates.keys())
