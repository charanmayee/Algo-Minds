import os
import requests
import streamlit as st
from utils import parse_budget_range, format_interests
from landmarks_data import get_landmarks_for_destination

class TravelPlanner:
    def __init__(self):
        self.hf_api_key = os.getenv("HUGGING_FACE_API_KEY", "")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}

    def generate_itinerary(self, destination, budget, num_people, num_days, interests):
        """Generate a personalized travel itinerary using Hugging Face API with fallback"""
        try:
            if self.hf_api_key:
                ai_result = self._try_huggingface_api(destination, budget, num_people, num_days, interests)
                if ai_result:
                    return ai_result
            st.info("Using template-based itinerary generation...")
            return self._generate_template_itinerary(destination, budget, num_people, num_days, interests)
        except Exception as e:
            st.warning(f"Error during generation: {str(e)}. Using template-based approach.")
            return self._generate_template_itinerary(destination, budget, num_people, num_days, interests)

    def _try_huggingface_api(self, destination, budget, num_people, num_days, interests):
        try:
            prompt = self._create_prompt(destination, budget, num_people, num_days, interests)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 1000,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    if generated_text and len(generated_text.strip()) > 50:
                        return self._parse_itinerary_response(generated_text, destination, budget, num_people, num_days, interests)
            elif response.status_code == 401:
                st.error("Invalid Hugging Face API key. Please check your configuration.")
            elif response.status_code == 503:
                st.warning("AI model is loading. Using template generation for now.")
            else:
                st.warning(f"API returned status {response.status_code}. Using template generation.")
        except requests.RequestException as e:
            st.warning(f"Network error: {str(e)}. Using template generation.")
        except Exception as e:
            st.warning(f"API error: {str(e)}. Using template generation.")
        return None

    def _create_prompt(self, destination, budget, num_people, num_days, interests):
        budget_range = parse_budget_range(budget)
        interests_text = format_interests(interests)
        prompt = f"""Create a detailed {num_days}-day travel itinerary for {destination} for {num_people} people with a {budget} budget.\n\nTraveler interests: {interests_text}\n\nPlease provide:\n1. Day-by-day itinerary with specific places to visit\n2. Recommended local food and restaurants\n3. Estimated costs for activities\n4. Travel tips specific to {destination}\n5. Best times to visit each location\n\nFormat the response as a structured plan with clear daily schedules, including:\n- Morning, afternoon, and evening activities\n- Specific restaurant recommendations with cuisine types\n- Estimated costs per person\n- Transportation suggestions between locations\n- Cultural etiquette tips\n\nBudget range: {budget_range} per person per day\nDuration: {num_days} days\nGroup size: {num_people} people\nDestination: {destination}\n"""
        return prompt

    def _parse_itinerary_response(self, generated_text, destination, budget, num_people, num_days, interests):
        try:
            itinerary_data = {
                'destination': destination,
                'budget': budget,
                'num_people': num_people,
                'num_days': num_days,
                'interests': interests,
                'raw_response': generated_text,
                'daily_plan': {},
                'food_recommendations': [],
                'travel_tips': []
            }
            lines = generated_text.split('\n')
            current_day = None
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if any(day_word in line.lower() for day_word in ['day 1', 'day 2', 'day 3', 'day one', 'day two', 'day three']):
                    current_day = line
                    itinerary_data['daily_plan'][current_day] = []
                    current_section = 'daily'
                elif any(food_word in line.lower() for food_word in ['food', 'restaurant', 'cuisine', 'dining']):
                    current_section = 'food'
                elif any(tip_word in line.lower() for tip_word in ['tip', 'advice', 'recommendation', 'note']):
                    current_section = 'tips'
                elif current_section == 'daily' and current_day:
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        activity = self._parse_activity(line)
                        itinerary_data['daily_plan'][current_day].append(activity)
                elif current_section == 'food':
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        food_item = self._parse_food_item(line)
                        itinerary_data['food_recommendations'].append(food_item)
                elif current_section == 'tips':
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        tip = line.lstrip('-•* ').strip()
                        itinerary_data['travel_tips'].append(tip)
            if not itinerary_data['daily_plan']:
                itinerary_data['daily_plan'] = self._create_basic_daily_plan(generated_text, num_days)
            if not itinerary_data['food_recommendations']:
                itinerary_data['food_recommendations'] = self._extract_food_recommendations(generated_text, destination)
            if not itinerary_data['travel_tips']:
                itinerary_data['travel_tips'] = self._extract_travel_tips(generated_text)
            return itinerary_data
        except Exception as e:
            st.error(f"Error parsing itinerary response: {str(e)}")
            return {
                'destination': destination,
                'budget': budget,
                'num_people': num_people,
                'num_days': num_days,
                'interests': interests,
                'raw_response': generated_text,
                'daily_plan': self._create_basic_daily_plan(generated_text, num_days),
                'food_recommendations': self._extract_food_recommendations(generated_text, destination),
                'travel_tips': self._extract_travel_tips(generated_text)
            }

    def _parse_activity(self, line):
        activity = {
            'name': line.lstrip('-•* ').strip(),
            'time': 'Flexible timing',
            'description': 'Activity details from AI recommendation',
            'estimated_cost': 'Varies'
        }
        if ':' in line and any(time_word in line.lower() for time_word in ['morning', 'afternoon', 'evening', 'am', 'pm']):
            parts = line.split(':')
            if len(parts) >= 2:
                activity['time'] = parts[0].lstrip('-•* ').strip()
                activity['name'] = parts[1].strip()
        return activity

    def _parse_food_item(self, line):
        food_item = {
            'name': line.lstrip('-•* ').strip(),
            'description': 'Local specialty dish',
            'price_range': 'Moderate',
            'restaurant': None
        }
        if '@' in line or 'at ' in line.lower():
            parts = line.split('@') if '@' in line else line.split(' at ')
            if len(parts) >= 2:
                food_item['name'] = parts[0].lstrip('-•* ').strip()
                food_item['restaurant'] = parts[1].strip()
        return food_item

    def _create_basic_daily_plan(self, text, num_days):
        daily_plan = {}
        for day in range(1, num_days + 1):
            day_key = f"Day {day}"
            daily_plan[day_key] = [
                {
                    'name': f'Explore {day_key} highlights',
                    'time': 'Full day',
                    'description': 'Based on AI recommendations and your interests',
                    'estimated_cost': 'Varies by activity'
                }
            ]
        return daily_plan

    def _extract_food_recommendations(self, text, destination):
        food_keywords = ['food', 'restaurant', 'dish', 'cuisine', 'eat', 'dining', 'meal']
        food_recommendations = []
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in food_keywords):
                if line.strip() and not line.strip().startswith('#'):
                    food_recommendations.append({
                        'name': line.strip()[:50] + ('...' if len(line.strip()) > 50 else ''),
                        'description': f'Local {destination} specialty',
                        'price_range': 'Moderate',
                        'restaurant': 'Various locations'
                    })
        if not food_recommendations:
            food_recommendations = [
                {
                    'name': f'Traditional {destination} cuisine',
                    'description': 'Authentic local dishes',
                    'price_range': 'Moderate',
                    'restaurant': 'Local restaurants'
                }
            ]
        return food_recommendations[:5]

    def _extract_travel_tips(self, text):
        tip_keywords = ['tip', 'advice', 'remember', 'important', 'note', 'recommend']
        tips = []
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in tip_keywords):
                if line.strip() and not line.strip().startswith('#'):
                    tips.append(line.strip())
        if not tips:
            tips = [
                'Check local weather conditions before your trip',
                'Learn basic local phrases for better communication',
                'Keep copies of important documents',
                'Research local customs and etiquette'
            ]
        return tips[:5]

    def _generate_template_itinerary(self, destination, budget, num_people, num_days, interests):
        from utils import create_fallback_itinerary
        base_itinerary = create_fallback_itinerary(destination, num_days, interests)
        landmarks_data = get_landmarks_for_destination(destination)
        enhanced_daily_plan = {}
        for day_num in range(1, num_days + 1):
            day_key = f"Day {day_num}"
            activities = []
            if day_num == 1:
                if landmarks_data and landmarks_data.get('landmarks'):
                    first_landmark = landmarks_data['landmarks'][0]
                    activities = [
                        {
                            'name': f'Arrival in {destination}',
                            'time': 'Morning',
                            'description': 'Check into accommodation and get oriented with the city center',
                            'estimated_cost': '$20-50'
                        },
                        {
                            'name': f'Visit {first_landmark["name"]}',
                            'time': 'Afternoon',
                            'description': f'{first_landmark["description"]} - {first_landmark["type"]}',
                            'specific_places': [first_landmark["name"]],
                            'food_items': first_landmark["famous_foods"],
                            'nearby_restaurants': first_landmark["nearby_food_spots"],
                            'estimated_cost': '$15-40'
                        }
                    ]
                else:
                    activities = [
                        {
                            'name': f'Arrival in {destination}',
                            'time': 'Morning',
                            'description': 'Check into accommodation and get oriented with the city center',
                            'estimated_cost': '$20-50'
                        },
                        {
                            'name': f'{destination} City Walking Tour',
                            'time': 'Afternoon',
                            'description': 'Explore main streets, landmarks, and get your bearings',
                            'estimated_cost': '$0-30'
                        }
                    ]
            elif day_num == num_days and num_days > 1:
                activities = [
                    {
                        'name': 'Last-minute Shopping & Souvenirs',
                        'time': 'Morning',
                        'description': 'Visit local markets or shops for gifts and mementos',
                        'estimated_cost': '$30-100'
                    },
                    {
                        'name': 'Departure Preparations',
                        'time': 'Afternoon',
                        'description': 'Check out, travel to airport/station',
                        'estimated_cost': '$20-50'
                    }
                ]
            else:
                if landmarks_data and landmarks_data.get('landmarks') and len(landmarks_data['landmarks']) > day_num - 1:
                    landmark = landmarks_data['landmarks'][day_num - 1]
                    landmark_activity = {
                        'name': f'Explore {landmark["name"]}',
                        'time': 'Morning',
                        'description': f'{landmark["description"]} - Experience this {landmark["type"].lower()} and discover its cultural significance.',
                        'specific_places': [landmark["name"]],
                        'food_items': landmark["famous_foods"],
                        'nearby_restaurants': landmark["nearby_food_spots"],
                        'estimated_cost': '$20-60'
                    }
                    afternoon_activity = self._get_interest_activity(destination, interests, 'afternoon')
                    evening_activity = self._get_interest_activity(destination, interests, 'evening')
                    activities = [landmark_activity, afternoon_activity, evening_activity]
                else:
                    morning_activity = self._get_interest_activity(destination, interests, 'morning')
                    afternoon_activity = self._get_interest_activity(destination, interests, 'afternoon')
                    evening_activity = self._get_interest_activity(destination, interests, 'evening')
                    activities = [morning_activity, afternoon_activity, evening_activity]
            enhanced_daily_plan[day_key] = activities
        food_recommendations = self._get_destination_food_recommendations(destination, interests)
        travel_tips = self._get_destination_travel_tips(destination, num_people, budget)
        return {
            'destination': destination,
            'budget': budget,
            'num_people': num_people,
            'num_days': num_days,
            'interests': interests,
            'daily_plan': enhanced_daily_plan,
            'food_recommendations': food_recommendations,
            'travel_tips': travel_tips,
            'total_estimated_cost': self._estimate_trip_cost(budget, num_people, num_days)
        }

    def _get_interest_activity(self, destination, interests, time_of_day):
        # Simplified for brevity; you can expand this as needed
        default_activities = {
            'morning': {
                'name': f'{destination} Historic Landmarks Tour',
                'description': f'Visit the most iconic landmarks and monuments in {destination}.',
                'specific_places': ['Historic City Center'],
                'food_items': ['Traditional breakfast items']
            },
            'afternoon': {
                'name': f'{destination} Cultural Districts & Neighborhoods',
                'description': f'Explore diverse neighborhoods that showcase the cultural heart of {destination}.',
                'specific_places': ['Artist Quarters'],
                'food_items': ['Neighborhood specialties']
            },
            'evening': {
                'name': f'{destination} Entertainment & Nightlife',
                'description': f'Experience the vibrant evening scene of {destination}.',
                'specific_places': ['Entertainment Districts'],
                'food_items': ['Evening dining specialties']
            }
        }
        template = default_activities[time_of_day]
        return {
            'name': template['name'],
            'time': time_of_day.title(),
            'description': template['description'],
            'specific_places': template.get('specific_places', []),
            'food_items': template.get('food_items', []),
            'estimated_cost': '$25-70'
        }

    def _get_destination_food_recommendations(self, destination, interests):
        return [
            {
                'name': f'Traditional {destination} Breakfast Experience',
                'description': f'Start your day with an authentic {destination} breakfast.',
                'price_range': '$8-18',
                'restaurant': 'Traditional breakfast cafes',
            },
            {
                'name': f'{destination} Street Food Adventure',
                'description': f'Dive into the vibrant street food scene of {destination}.',
                'price_range': '$3-12',
                'restaurant': 'Street vendors',
            }
        ]

    def _get_destination_travel_tips(self, destination, num_people, budget):
        tips = [
            f'Research {destination}\'s local customs and etiquette before your trip',
            f'Check the weather forecast for {destination} and pack accordingly',
            'Download offline maps and translation apps for easier navigation',
            'Keep digital and physical copies of important documents',
            'Inform your bank about travel plans to avoid card blocks'
        ]
        if num_people > 2:
            tips.append('Book group activities and restaurant reservations in advance')
            tips.append('Designate a group leader for each day to help coordinate activities')
        if 'Budget' in budget:
            tips.extend([
                'Look for free walking tours and public spaces',
                'Shop at local markets for affordable meals and snacks',
                'Use public transportation instead of taxis when possible'
            ])
        elif 'Luxury' in budget:
            tips.extend([
                'Book premium experiences and skip-the-line tickets',
                'Consider hiring private guides for personalized experiences',
                'Make reservations at high-end restaurants well in advance'
            ])
        return tips[:8]

    def _estimate_trip_cost(self, budget, num_people, num_days):
        daily_estimates = {
            'Budget ($0-$50/day)': 35,
            'Mid-range ($50-$150/day)': 100,
            'Luxury ($150+/day)': 200
        }
        daily_cost = daily_estimates.get(budget, 100)
        total = daily_cost * num_people * num_days
        return f"${total:,} - ${int(total * 1.2):,}"
