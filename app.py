import streamlit as st
import os
from travel_planner import TravelPlanner
from map_generator import MapGenerator
import time

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'itinerary_generated' not in st.session_state:
    st.session_state.itinerary_generated = False
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None
if 'map_data' not in st.session_state:
    st.session_state.map_data = None

def main():
    st.title("🌍 AI-Powered Travel Planner")
    st.markdown("Plan your perfect trip with AI-generated personalized itineraries!")
    
    # Initialize travel planner
    travel_planner = TravelPlanner()
    map_generator = MapGenerator()
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Trip Details")
        
        # Destination input
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Paris, France",
            help="Enter the city or country you want to visit"
        )
        
        # Budget input
        budget = st.selectbox(
            "Budget Range",
            ["Budget ($0-$50/day)", "Mid-range ($50-$150/day)", "Luxury ($150+/day)"],
            help="Select your daily budget range per person"
        )
        
        # Number of people
        num_people = st.number_input(
            "Number of People",
            min_value=1,
            max_value=20,
            value=2,
            help="How many people will be traveling?"
        )
        
        # Trip duration
        num_days = st.number_input(
            "Trip Duration (days)",
            min_value=1,
            max_value=30,
            value=3,
            help="How many days will you be traveling?"
        )
        
        # Interests selection
        st.subheader("Interests")
        interests = []
        
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("Food & Dining"):
                interests.append("food")
            if st.checkbox("Beaches"):
                interests.append("beaches")
            if st.checkbox("Museums"):
                interests.append("museums")
            if st.checkbox("Nightlife"):
                interests.append("nightlife")
            if st.checkbox("Adventure"):
                interests.append("adventure")
        
        with col2:
            if st.checkbox("Shopping"):
                interests.append("shopping")
            if st.checkbox("Nature & Parks"):
                interests.append("nature")
            if st.checkbox("History & Culture"):
                interests.append("culture")
            if st.checkbox("Architecture"):
                interests.append("architecture")
            if st.checkbox("Photography"):
                interests.append("photography")
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Itinerary",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if generate_button:
        if not destination:
            st.error("Please enter a destination to generate your itinerary.")
            return
        
        if not interests:
            st.warning("Please select at least one interest to personalize your itinerary.")
            return
        
        # Show loading state
        with st.spinner("🤖 AI is crafting your perfect itinerary..."):
            try:
                # Generate itinerary
                itinerary_data = travel_planner.generate_itinerary(
                    destination=destination,
                    budget=budget,
                    num_people=num_people,
                    num_days=num_days,
                    interests=interests
                )
                
                if itinerary_data:
                    # Generate map data
                    map_data = map_generator.generate_map(destination, itinerary_data)
                    
                    # Store in session state
                    st.session_state.itinerary_data = itinerary_data
                    st.session_state.map_data = map_data
                    st.session_state.itinerary_generated = True
                    
                    st.success("✅ Your personalized itinerary is ready!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to generate itinerary. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Display results if available
    if st.session_state.itinerary_generated and st.session_state.itinerary_data:
        display_itinerary(st.session_state.itinerary_data, st.session_state.map_data)

def display_itinerary(itinerary_data, map_data):
    """Display the generated itinerary and map"""
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Day-by-Day Itinerary", "🗺️ Interactive Map", "🏛️ Famous Places", "📋 Trip Summary"])
    
    with tab1:
        st.header("Your Personalized Itinerary")
        
        # Display daily itinerary with enhanced details
        if 'daily_plan' in itinerary_data:
            for day, activities in itinerary_data['daily_plan'].items():
                with st.expander(f"🗓️ {day}", expanded=True):
                    for activity in activities:
                        # Main activity header
                        st.markdown(f"**📍 {activity['name']}**")
                        st.markdown(f"⏰ **Time:** {activity.get('time', 'Flexible timing')}")
                        
                        # Detailed description
                        st.markdown(f"📝 **Description:** {activity.get('description', 'No description available')}")
                        
                        # Specific places to visit
                        if activity.get('specific_places'):
                            st.markdown("🏛️ **Places to Visit:**")
                            for place in activity['specific_places']:
                                st.markdown(f"   • {place}")
                        
                        # Food items to try
                        if activity.get('food_items'):
                            st.markdown("🍽️ **Famous Food to Try:**")
                            for food in activity['food_items']:
                                st.markdown(f"   • {food}")
                        
                        # Nearby restaurants
                        if activity.get('nearby_restaurants'):
                            st.markdown("🏪 **Recommended Restaurants:**")
                            for restaurant in activity['nearby_restaurants']:
                                st.markdown(f"   • {restaurant}")
                        
                        # Cost information
                        if activity.get('estimated_cost'):
                            st.markdown(f"💰 **Estimated cost:** {activity['estimated_cost']}")
                        
                        st.markdown("---")
    
    with tab2:
        st.header("Interactive Map")
        if map_data:
            st.components.v1.html(map_data, height=600)
        else:
            st.info("Map data is being processed. Please refresh to see the interactive map.")
    
    with tab3:
        st.header("Famous Places & Their Specialties")
        
        # Import landmarks data to display famous places
        from landmarks_data import get_landmarks_for_destination
        
        destination = itinerary_data.get('destination', '')
        landmarks_data = get_landmarks_for_destination(destination)
        
        if landmarks_data and landmarks_data.get('landmarks'):
            st.write(f"Here are the most famous places to visit in {destination} and their signature foods:")
            
            for landmark in landmarks_data['landmarks']:
                with st.container():
                    # Create columns for image placeholder and content
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Placeholder for landmark image (you could add actual images later)
                        st.markdown(f"### 🏛️ {landmark['name']}")
                        st.markdown(f"**Type:** {landmark['type']}")
                    
                    with col2:
                        st.markdown(f"**Description:** {landmark['description']}")
                        
                        # Famous foods at this landmark
                        st.markdown("**🍽️ Famous Foods to Try:**")
                        for food in landmark['famous_foods']:
                            st.markdown(f"   • {food}")
                        
                        # Nearby food spots
                        st.markdown("**🏪 Where to Find Them:**")
                        for spot in landmark['nearby_food_spots']:
                            st.markdown(f"   • {spot}")
                    
                    st.markdown("---")
        else:
            st.info(f"Explore the local attractions and discover the authentic flavors of {destination}!")
    
    with tab4:
        st.header("Trip Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Destination", itinerary_data.get('destination', 'N/A'))
            st.metric("Duration", f"{itinerary_data.get('num_days', 'N/A')} days")
        
        with col2:
            st.metric("Travelers", f"{itinerary_data.get('num_people', 'N/A')} people")
            st.metric("Budget Range", itinerary_data.get('budget', 'N/A'))
        
        with col3:
            if 'total_estimated_cost' in itinerary_data:
                st.metric("Estimated Total Cost", itinerary_data['total_estimated_cost'])
            
            interests_text = ", ".join(itinerary_data.get('interests', []))
            st.markdown(f"**Interests:** {interests_text}")
        
        # Additional trip tips
        if 'travel_tips' in itinerary_data:
            st.subheader("💡 Travel Tips")
            for tip in itinerary_data['travel_tips']:
                st.markdown(f"• {tip}")
        
        # Reset button
        if st.button("🔄 Plan Another Trip", use_container_width=True):
            st.session_state.itinerary_generated = False
            st.session_state.itinerary_data = None
            st.session_state.map_data = None
            st.rerun()

if __name__ == "__main__":
    main()
