def parse_budget_range(budget_selection):
    """Parse budget selection into a readable format"""
    
    budget_mapping = {
        "Budget ($0-$50/day)": "$0-50 per day",
        "Mid-range ($50-$150/day)": "$50-150 per day", 
        "Luxury ($150+/day)": "$150+ per day"
    }
    
    return budget_mapping.get(budget_selection, budget_selection)

def format_interests(interests_list):
    """Format interests list into readable text"""
    
    if not interests_list:
        return "general sightseeing"
    
    # Convert interest codes to readable names
    interest_names = {
        'food': 'Food & Dining',
        'beaches': 'Beaches',
        'museums': 'Museums',
        'nightlife': 'Nightlife',
        'adventure': 'Adventure Activities',
        'shopping': 'Shopping',
        'nature': 'Nature & Parks',
        'culture': 'History & Culture',
        'architecture': 'Architecture',
        'photography': 'Photography'
    }
    
    formatted_interests = [interest_names.get(interest, interest.title()) for interest in interests_list]
    
    if len(formatted_interests) == 1:
        return formatted_interests[0]
    elif len(formatted_interests) == 2:
        return " and ".join(formatted_interests)
    else:
        return ", ".join(formatted_interests[:-1]) + ", and " + formatted_interests[-1]

def estimate_total_cost(daily_activities, budget_range, num_people, num_days):
    """Estimate total trip cost based on activities and budget"""
    
    budget_values = {
        "Budget ($0-$50/day)": 35,
        "Mid-range ($50-$150/day)": 100,
        "Luxury ($150+/day)": 200
    }
    
    daily_budget = budget_values.get(budget_range, 100)
    total_cost = daily_budget * num_people * num_days
    
    return f"${total_cost:,} - ${int(total_cost * 1.3):,}"

def validate_user_inputs(destination, interests, num_days, num_people):
    """Validate user inputs and return error messages if any"""
    
    errors = []
    
    if not destination or len(destination.strip()) < 2:
        errors.append("Please enter a valid destination")
    
    if not interests:
        errors.append("Please select at least one interest")
    
    if num_days < 1 or num_days > 30:
        errors.append("Trip duration must be between 1 and 30 days")
    
    if num_people < 1 or num_people > 20:
        errors.append("Number of people must be between 1 and 20")
    
    return errors

def format_day_label(day_number):
    """Format day number into readable label"""
    
    day_names = {
        1: "Day 1", 2: "Day 2", 3: "Day 3", 4: "Day 4", 5: "Day 5",
        6: "Day 6", 7: "Day 7", 8: "Day 8", 9: "Day 9", 10: "Day 10"
    }
    
    return day_names.get(day_number, f"Day {day_number}")

def extract_location_keywords(text):
    """Extract potential location names from text"""
    
    import re
    
    # Common location indicators
    location_patterns = [
        r'visit\s+([A-Z][a-zA-Z\s]+)',
        r'go\s+to\s+([A-Z][a-zA-Z\s]+)',
        r'explore\s+([A-Z][a-zA-Z\s]+)',
        r'at\s+([A-Z][a-zA-Z\s]+)',
    ]
    
    locations = []
    for pattern in location_patterns:
        matches = re.findall(pattern, text)
        locations.extend(matches)
    
    # Clean and filter locations
    cleaned_locations = []
    for location in locations:
        location = location.strip()
        if len(location) > 2 and len(location) < 50:
            cleaned_locations.append(location)
    
    return list(set(cleaned_locations))  # Remove duplicates

def create_fallback_itinerary(destination, num_days, interests):
    """Create a basic fallback itinerary if AI generation fails"""
    
    daily_plan = {}
    
    for day in range(1, num_days + 1):
        day_key = f"Day {day}"
        
        if day == 1:
            activities = [
                {
                    'name': f'Arrival and {destination} city center exploration',
                    'time': 'Morning to afternoon',
                    'description': 'Get oriented with the city and visit main attractions',
                    'estimated_cost': 'Low to moderate'
                }
            ]
        elif day == num_days:
            activities = [
                {
                    'name': 'Final shopping and departure preparation',
                    'time': 'Morning',
                    'description': 'Last-minute souvenirs and travel preparations',
                    'estimated_cost': 'Varies'
                }
            ]
        else:
            # Create activities based on interests
            if 'museums' in interests:
                activities = [
                    {
                        'name': f'{destination} Museum District',
                        'time': 'Morning',
                        'description': 'Explore local museums and cultural sites',
                        'estimated_cost': 'Moderate'
                    }
                ]
            elif 'nature' in interests:
                activities = [
                    {
                        'name': f'{destination} Parks and Gardens',
                        'time': 'Full day',
                        'description': 'Enjoy outdoor spaces and natural attractions',
                        'estimated_cost': 'Low'
                    }
                ]
            else:
                activities = [
                    {
                        'name': f'{destination} Highlights Tour',
                        'time': 'Full day',
                        'description': 'Visit top-rated attractions and landmarks',
                        'estimated_cost': 'Moderate'
                    }
                ]
        
        daily_plan[day_key] = activities
    
    return {
        'destination': destination,
        'num_days': num_days,
        'interests': interests,
        'daily_plan': daily_plan,
        'food_recommendations': [
            {
                'name': f'Traditional {destination} cuisine',
                'description': 'Local specialties and traditional dishes',
                'price_range': 'Moderate',
                'restaurant': 'Local restaurants'
            }
        ],
        'travel_tips': [
            'Research local customs and etiquette',
            'Check weather conditions for your travel dates',
            'Learn basic local phrases',
            'Keep important documents secure'
        ]
    }
