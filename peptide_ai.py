"""
AI-Powered Peptide Recommendation System
Uses OpenAI to analyze metabolic data and recommend personalized peptide protocols
"""
import os
from openai import OpenAI

class PeptideRecommendationAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_and_recommend(self, metabolic_data, user_goals=None):
        """
        Analyze metabolic data and recommend peptide protocols

        Args:
            metabolic_data (dict): User's metabolic test data
            user_goals (list): User's health/fitness goals

        Returns:
            dict: Comprehensive peptide recommendations
        """

        # Build the prompt with metabolic context
        prompt = self._build_analysis_prompt(metabolic_data, user_goals)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            recommendation_text = response.choices[0].message.content

            # Parse the AI response into structured recommendations
            recommendations = self._parse_recommendations(recommendation_text)

            return recommendations

        except Exception as e:
            print(f"Error generating peptide recommendations: {e}")
            return self._get_fallback_recommendations()

    def _get_system_prompt(self):
        """System prompt defining the AI's role and expertise"""
        return """You are an expert peptide therapy advisor and metabolic health specialist.
You analyze metabolic test data (VO2 Max, RMR, substrate utilization, etc.) and provide
evidence-based peptide protocol recommendations.

Your recommendations should:
1. Be personalized based on the user's metabolic profile
2. Consider their fitness/health goals
3. Include specific peptides with dosing protocols
4. Explain the scientific rationale
5. Mention expected benefits and timeline
6. Include safety considerations and contraindications
7. Be practical and actionable

Focus on these peptide categories:
- Recovery & Healing: BPC-157, TB-500, GHK-Cu
- Fat Loss & Metabolism: Semaglutide, Tirzepatide, AOD-9604, CJC-1295/Ipamorelin
- Muscle Growth: CJC-1295, Ipamorelin, Tesamorelin, MK-677
- Anti-Aging & Longevity: Epithalon, MOTS-c, Thymosin Alpha-1
- Performance: BPC-157, TB-500, Hexarelin
- Sleep & Recovery: DSIP, Selank

Always provide disclaimers about consulting with healthcare providers."""

    def _build_analysis_prompt(self, metabolic_data, user_goals):
        """Build the analysis prompt with user data"""

        prompt = f"""Analyze this metabolic profile and recommend personalized peptide protocols:

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
- Biological Age: {metabolic_data.get('biological_age', 'N/A')}

## User Goals:
{', '.join(user_goals) if user_goals else 'General health and performance optimization'}

Please provide:
1. **Primary Peptide Recommendations** (2-3 peptides most suited to this profile)
2. **Dosing Protocol** for each recommended peptide
3. **Scientific Rationale** - why these peptides match this metabolic profile
4. **Expected Benefits** and timeline
5. **Stacking Recommendations** - which peptides work well together
6. **Safety Considerations** - contraindications and side effects
7. **Lifestyle Optimization** - diet/exercise recommendations to enhance peptide efficacy

Format your response clearly with headers and bullet points."""

        return prompt

    def _parse_recommendations(self, ai_response):
        """Parse AI response into structured format"""
        return {
            'raw_analysis': ai_response,
            'primary_peptides': self._extract_primary_peptides(ai_response),
            'timestamp': self._get_timestamp()
        }

    def _extract_primary_peptides(self, text):
        """Extract primary peptide names from the response"""
        # Common peptide names to look for
        peptides = [
            'BPC-157', 'TB-500', 'CJC-1295', 'Ipamorelin', 'Semaglutide',
            'Tirzepatide', 'AOD-9604', 'Tesamorelin', 'MK-677', 'GHK-Cu',
            'Epithalon', 'MOTS-c', 'Thymosin Alpha-1', 'Hexarelin', 'DSIP', 'Selank'
        ]

        found_peptides = []
        text_upper = text.upper()

        for peptide in peptides:
            if peptide.upper() in text_upper:
                found_peptides.append(peptide)

        return found_peptides[:5]  # Return top 5

    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _get_fallback_recommendations(self):
        """Fallback recommendations if AI fails"""
        return {
            'raw_analysis': """## General Peptide Recommendations

Based on metabolic optimization principles:

### For Fat Loss & Metabolic Health:
- **CJC-1295/Ipamorelin**: 100-300mcg each, before bed
- **AOD-9604**: 300mcg daily, split into 2 doses

### For Recovery & Performance:
- **BPC-157**: 250-500mcg daily
- **TB-500**: 2-2.5mg twice weekly

### For Overall Health:
- **Thymosin Alpha-1**: 750mcg-1.5mg, 2-3x weekly

**Important**: Consult with a qualified healthcare provider before starting any peptide protocol.""",
            'primary_peptides': ['CJC-1295', 'Ipamorelin', 'BPC-157'],
            'timestamp': self._get_timestamp(),
            'error': True
        }
