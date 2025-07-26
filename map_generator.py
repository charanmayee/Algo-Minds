import folium
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import random

class MapGenerator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="travel_planner_app")
    
    def generate_map(self, destination, itinerary_data):
        """Generate an interactive map with recommended locations"""
        
        try:
            # Get coordinates for the destination
            destination_coords = self._get_coordinates(destination)
            
            if not destination_coords:
                st.warning(f"Could not find coordinates for {destination}. Using default map location.")
                destination_coords = (40.7128, -74.0060)  # Default to NYC coordinates
            
            # Create the base map
            map_center = destination_coords
            travel_map = folium.Map(
                location=map_center,
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Add destination marker
            folium.Marker(
                location=destination_coords,
                popup=f"<b>{destination}</b><br>Your destination",
                tooltip=destination,
                icon=folium.Icon(color='red', icon='star')
            ).add_to(travel_map)
            
            # Add markers for activities from itinerary
            self._add_activity_markers(travel_map, itinerary_data, destination_coords)
            
            # Add food recommendation markers
            self._add_food_markers(travel_map, itinerary_data, destination_coords)
            
            # Return the map as HTML
            return travel_map._repr_html_()
            
        except Exception as e:
            st.error(f"Error generating map: {str(e)}")
            return None
    
    def _get_coordinates(self, location_name):
        """Get latitude and longitude for a location"""
        
        try:
            # Add retry logic for geocoding
            for attempt in range(3):
                try:
                    location = self.geolocator.geocode(location_name, timeout=10)
                    if location:
                        return (location.latitude, location.longitude)
                    break
                except GeocoderTimedOut:
                    if attempt < 2:  # Don't sleep on the last attempt
                        time.sleep(1)
                    continue
                except GeocoderServiceError as e:
                    st.warning(f"Geocoding service error: {str(e)}")
                    break
            
            return None
            
        except Exception as e:
            st.warning(f"Could not geocode location {location_name}: {str(e)}")
            return None
    
    def _add_activity_markers(self, travel_map, itinerary_data, destination_coords):
        """Add markers for activities and attractions"""
        
        try:
            # Extract activity locations from daily plan
            activities = []
            for day, day_activities in itinerary_data.get('daily_plan', {}).items():
                for activity in day_activities:
                    activities.append({
                        'name': activity['name'],
                        'day': day,
                        'description': activity.get('description', ''),
                        'time': activity.get('time', ''),
                        'cost': activity.get('estimated_cost', '')
                    })
            
            # Generate coordinates for activities (around destination)
            lat, lon = destination_coords
            
            for i, activity in enumerate(activities[:10]):  # Limit to 10 activities
                # Generate random coordinates around the destination
                activity_lat = lat + random.uniform(-0.01, 0.01)
                activity_lon = lon + random.uniform(-0.01, 0.01)
                
                # Create popup content
                popup_content = f"""
                <div style="width: 200px;">
                    <b>{activity['name']}</b><br>
                    <i>{activity['day']}</i><br>
                    <small>{activity['description']}</small><br>
                    <small>Time: {activity['time']}</small><br>
                    <small>Cost: {activity['cost']}</small>
                </div>
                """
                
                # Choose icon color based on day
                day_number = 1
                if 'day' in activity['day'].lower():
                    try:
                        day_number = int(''.join(filter(str.isdigit, activity['day'])))
                    except:
                        day_number = i + 1
                
                colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']
                icon_color = colors[day_number % len(colors)]
                
                folium.Marker(
                    location=[activity_lat, activity_lon],
                    popup=folium.Popup(popup_content, max_width=250),
                    tooltip=activity['name'],
                    icon=folium.Icon(color=icon_color, icon='info-sign')
                ).add_to(travel_map)
                
        except Exception as e:
            st.warning(f"Could not add activity markers: {str(e)}")
    
    def _add_food_markers(self, travel_map, itinerary_data, destination_coords):
        """Add markers for food recommendations"""
        
        try:
            food_recommendations = itinerary_data.get('food_recommendations', [])
            lat, lon = destination_coords
            
            for i, food_item in enumerate(food_recommendations[:5]):  # Limit to 5 food recommendations
                # Generate random coordinates around the destination for restaurants
                food_lat = lat + random.uniform(-0.015, 0.015)
                food_lon = lon + random.uniform(-0.015, 0.015)
                
                # Create popup content
                popup_content = f"""
                <div style="width: 180px;">
                    <b>🍽️ {food_item['name']}</b><br>
                    <small>{food_item.get('description', 'Local specialty')}</small><br>
                    <small>Price: {food_item.get('price_range', 'Moderate')}</small><br>
                    <small>Location: {food_item.get('restaurant', 'Various')}</small>
                </div>
                """
                
                folium.Marker(
                    location=[food_lat, food_lon],
                    popup=folium.Popup(popup_content, max_width=200),
                    tooltip=food_item['name'],
                    icon=folium.Icon(color='orange', icon='cutlery')
                ).add_to(travel_map)
                
        except Exception as e:
            st.warning(f"Could not add food markers: {str(e)}")
    
    def _generate_area_coordinates(self, center_coords, radius=0.02):
        """Generate random coordinates within a radius of the center"""
        lat, lon = center_coords
        
        # Generate random offset within radius
        lat_offset = random.uniform(-radius, radius)
        lon_offset = random.uniform(-radius, radius)
        
        return (lat + lat_offset, lon + lon_offset)
