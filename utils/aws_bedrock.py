"""
AWS Bedrock Integration for HIPAA-Compliant AI
Uses Claude via AWS Bedrock instead of direct Anthropic API

AWS Bedrock is covered under the AWS BAA, making it HIPAA-compliant
for processing PHI in AI recommendations.
"""

import boto3
import json
import os
from typing import Optional, Dict, Any

class BedrockClaudeClient:
    """
    HIPAA-compliant Claude client using AWS Bedrock

    This replaces direct OpenAI/Anthropic API calls with Bedrock,
    which is covered under your AWS Business Associate Agreement.
    """

    def __init__(self, region: str = None, model_id: str = None):
        """
        Initialize Bedrock client

        Args:
            region: AWS region (defaults to AWS_REGION env var or us-east-1)
            model_id: Bedrock model ID (defaults to Claude 3 Sonnet)
        """
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.model_id = model_id or "anthropic.claude-3-sonnet-20240229-v1:0"

        # Initialize Bedrock runtime client
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=self.region
        )

    def generate_recommendations(
        self,
        patient_data: Dict[str, Any],
        focus_areas: list = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI recommendations for metabolic data

        Args:
            patient_data: Dictionary containing patient metabolic metrics
            focus_areas: List of focus areas (e.g., ['supplements', 'training', 'nutrition'])
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)

        Returns:
            AI-generated recommendations as string
        """
        focus_areas = focus_areas or ['general wellness', 'metabolic optimization']

        # Build the prompt
        prompt = self._build_recommendation_prompt(patient_data, focus_areas)

        # Prepare request body for Claude via Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            # Invoke the model
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body)
            )

            # Parse response
            response_body = json.loads(response['body'].read())

            # Extract the text content
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']

            return "Unable to generate recommendations at this time."

        except Exception as e:
            print(f"[BEDROCK ERROR] {str(e)}")
            raise Exception(f"AI recommendation generation failed: {str(e)}")

    def _build_recommendation_prompt(
        self,
        patient_data: Dict[str, Any],
        focus_areas: list
    ) -> str:
        """Build the recommendation prompt from patient data"""

        prompt = f"""You are a metabolic health expert. Based on the following metabolic test data,
provide personalized recommendations for optimizing health and performance.

METABOLIC TEST DATA:
-------------------
"""
        # Add metabolic metrics
        metrics = [
            ('VO2max', patient_data.get('vo2max'), 'ml/kg/min'),
            ('Resting Metabolic Rate', patient_data.get('rmr'), 'kcal/day'),
            ('Respiratory Exchange Ratio', patient_data.get('rer'), ''),
            ('Fat Oxidation Rate', patient_data.get('fat_max'), 'g/min'),
            ('Carb Oxidation Rate', patient_data.get('carb_max'), 'g/min'),
            ('Anaerobic Threshold', patient_data.get('anaerobic_threshold'), 'bpm'),
            ('Biological Age', patient_data.get('biological_age'), 'years'),
            ('Chronological Age', patient_data.get('age'), 'years'),
        ]

        for name, value, unit in metrics:
            if value is not None:
                prompt += f"- {name}: {value} {unit}\n"

        # Add patient info if available
        if patient_data.get('name'):
            prompt += f"\nPatient: {patient_data.get('name')}\n"
        if patient_data.get('gender'):
            prompt += f"Gender: {patient_data.get('gender')}\n"

        prompt += f"""
FOCUS AREAS: {', '.join(focus_areas)}

Please provide detailed, actionable recommendations in the following areas:
1. Training Zone Optimization
2. Nutrition Strategy
3. Supplement Recommendations (if appropriate)
4. Recovery Protocols
5. Lifestyle Modifications

Important guidelines:
- Be specific and actionable
- Base recommendations on the metabolic data provided
- Include relevant heart rate zones for training
- Consider the biological vs chronological age difference
- Provide evidence-based suggestions

Format your response with clear headers and bullet points for easy reading.
"""

        return prompt

    def generate_peptide_recommendations(
        self,
        patient_data: Dict[str, Any],
        health_goals: list = None,
        max_tokens: int = 4096
    ) -> str:
        """
        Generate peptide therapy recommendations

        Args:
            patient_data: Patient metabolic data
            health_goals: Specific health goals
            max_tokens: Maximum response length

        Returns:
            Peptide recommendations as string
        """
        health_goals = health_goals or ['metabolic optimization', 'longevity']

        prompt = f"""You are an expert in peptide therapy and metabolic optimization.
Based on the following metabolic test data and health goals, provide peptide therapy recommendations.

METABOLIC DATA:
- VO2max: {patient_data.get('vo2max', 'N/A')} ml/kg/min
- RMR: {patient_data.get('rmr', 'N/A')} kcal/day
- Biological Age: {patient_data.get('biological_age', 'N/A')} years
- Chronological Age: {patient_data.get('age', 'N/A')} years

HEALTH GOALS: {', '.join(health_goals)}

Provide peptide recommendations including:
1. Recommended peptides and their benefits
2. Suggested dosing protocols
3. Timing and administration
4. Potential synergies between peptides
5. Safety considerations and contraindications

IMPORTANT DISCLAIMER: These recommendations are for educational purposes only.
Peptide therapy should only be administered under the supervision of a licensed healthcare provider.
"""

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": 0.5,  # Lower temperature for medical content
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body)
            )

            response_body = json.loads(response['body'].read())

            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']

            return "Unable to generate peptide recommendations at this time."

        except Exception as e:
            print(f"[BEDROCK ERROR] {str(e)}")
            raise Exception(f"Peptide recommendation generation failed: {str(e)}")


# Convenience function to replace existing OpenAI/Anthropic calls
def get_ai_recommendations(patient_data: Dict[str, Any], focus_areas: list = None) -> str:
    """
    Drop-in replacement for existing AI recommendation function

    Args:
        patient_data: Patient metabolic data dictionary
        focus_areas: List of focus areas for recommendations

    Returns:
        AI-generated recommendations string
    """
    client = BedrockClaudeClient()
    return client.generate_recommendations(patient_data, focus_areas)


def get_peptide_recommendations(patient_data: Dict[str, Any], health_goals: list = None) -> str:
    """
    Generate peptide therapy recommendations

    Args:
        patient_data: Patient metabolic data
        health_goals: List of health goals

    Returns:
        Peptide recommendations string
    """
    client = BedrockClaudeClient()
    return client.generate_peptide_recommendations(patient_data, health_goals)
