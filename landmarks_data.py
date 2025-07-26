# Dummy data for famous landmarks and foods for demonstration

def get_landmarks_for_destination(destination):
    """Return famous landmarks and their specialties for a given destination"""
    # Example data for Paris, France
    if destination.lower() in ["paris", "paris, france"]:
        return {
            "landmarks": [
                {
                    "name": "Eiffel Tower",
                    "type": "Monument",
                    "description": "Iconic symbol of Paris with panoramic city views.",
                    "famous_foods": ["Crêpes", "Baguette Sandwiches"],
                    "nearby_food_spots": ["Le Champ de Mars Café", "Bistro Parisien"]
                },
                {
                    "name": "Louvre Museum",
                    "type": "Museum",
                    "description": "World's largest art museum and a historic monument.",
                    "famous_foods": ["French Pastries", "Croissants"],
                    "nearby_food_spots": ["Café Marly", "Le Fumoir"]
                },
                {
                    "name": "Montmartre",
                    "type": "Neighborhood",
                    "description": "Historic district known for its bohemian atmosphere and artists.",
                    "famous_foods": ["Escargots", "Ratatouille"],
                    "nearby_food_spots": ["Le Consulat", "La Maison Rose"]
                }
            ]
        }
    # Example data for New York
    elif destination.lower() in ["new york", "new york city", "nyc"]:
        return {
            "landmarks": [
                {
                    "name": "Statue of Liberty",
                    "type": "Monument",
                    "description": "Famous symbol of freedom and democracy.",
                    "famous_foods": ["New York Hot Dog", "Soft Pretzel"],
                    "nearby_food_spots": ["Liberty Island Café", "Battery Gardens"]
                },
                {
                    "name": "Central Park",
                    "type": "Park",
                    "description": "Urban park in Manhattan with scenic walking paths and lakes.",
                    "famous_foods": ["Bagels", "NY Cheesecake"],
                    "nearby_food_spots": ["The Loeb Boathouse", "Tavern on the Green"]
                },
                {
                    "name": "Times Square",
                    "type": "Entertainment District",
                    "description": "Bustling commercial and entertainment hub with bright lights.",
                    "famous_foods": ["Pizza Slice", "Deli Sandwich"],
                    "nearby_food_spots": ["Junior's Restaurant", "Carmine's"]
                }
            ]
        }
    # Example data for Hyderabad
    elif destination.lower() in ["hyderabad", "hyderabad, india", "hyd"]:
        return {
            "landmarks": [
                {
                    "name": "Charminar",
                    "type": "Monument",
                    "description": "Iconic 16th-century mosque with four grand arches, symbol of Hyderabad.",
                    "famous_foods": ["Hyderabadi Biryani", "Irani Chai"],
                    "nearby_food_spots": ["Shadab Hotel", "Nimrah Cafe"]
                },
                {
                    "name": "Golconda Fort",
                    "type": "Fort",
                    "description": "Historic fortress known for its acoustics, palaces, and scenic views.",
                    "famous_foods": ["Haleem", "Double Ka Meetha"],
                    "nearby_food_spots": ["Pista House", "Cafe Bahar"]
                },
                {
                    "name": "Hussain Sagar Lake",
                    "type": "Lake",
                    "description": "Heart-shaped lake with a large Buddha statue and boating activities.",
                    "famous_foods": ["Mirchi Bajji", "Corn on the Cob"],
                    "nearby_food_spots": ["Eat Street", "Waterfront Restaurant"]
                }
            ]
        }
    # Example data for Delhi
    elif destination.lower() in ["delhi", "new delhi", "delhi, india", "del"]:
        return {
            "landmarks": [
                {
                    "name": "Red Fort",
                    "type": "Fort",
                    "description": "Historic 17th-century fort and UNESCO World Heritage Site.",
                    "famous_foods": ["Chole Bhature", "Paratha"],
                    "nearby_food_spots": ["Paranthe Wali Gali", "Karim's"]
                },
                {
                    "name": "Qutub Minar",
                    "type": "Minaret",
                    "description": "Tallest brick minaret in the world, built in 1193.",
                    "famous_foods": ["Dahi Bhalla", "Aloo Tikki"],
                    "nearby_food_spots": ["Haldiram's", "Bengali Sweet House"]
                },
                {
                    "name": "India Gate",
                    "type": "Monument",
                    "description": "War memorial and iconic landmark in central Delhi.",
                    "famous_foods": ["Kulfi Falooda", "Bhel Puri"],
                    "nearby_food_spots": ["India Gate Street Vendors", "Kwality Restaurant"]
                }
            ]
        }
    # Example data for Mumbai
    elif destination.lower() in ["mumbai", "bombay", "mumbai, india", "bom"]:
        return {
            "landmarks": [
                {
                    "name": "Gateway of India",
                    "type": "Monument",
                    "description": "Grand arch monument overlooking the Arabian Sea.",
                    "famous_foods": ["Vada Pav", "Bhel Puri"],
                    "nearby_food_spots": ["Bademiya", "Leopold Cafe"]
                },
                {
                    "name": "Chhatrapati Shivaji Maharaj Terminus",
                    "type": "Railway Station",
                    "description": "UNESCO World Heritage Site and historic railway station.",
                    "famous_foods": ["Bombay Sandwich", "Frankie"],
                    "nearby_food_spots": ["Cannon Pav Bhaji", "Ayub's"]
                },
                {
                    "name": "Marine Drive",
                    "type": "Promenade",
                    "description": "Scenic boulevard along the coast, known as the Queen's Necklace.",
                    "famous_foods": ["Pav Bhaji", "Kulfi"],
                    "nearby_food_spots": ["Sukh Sagar", "Tiwari Bros Mithaiwala"]
                }
            ]
        }
    # Example data for Chennai
    elif destination.lower() in ["chennai", "madras", "chennai, india", "maa"]:
        return {
            "landmarks": [
                {
                    "name": "Marina Beach",
                    "type": "Beach",
                    "description": "Longest urban beach in India, popular for walks and street food.",
                    "famous_foods": ["Sundal", "Murukku"],
                    "nearby_food_spots": ["Marina Beach Stalls", "Ratna Cafe"]
                },
                {
                    "name": "Kapaleeshwarar Temple",
                    "type": "Temple",
                    "description": "Ancient Dravidian-style temple dedicated to Lord Shiva.",
                    "famous_foods": ["Filter Coffee", "Idli Sambar"],
                    "nearby_food_spots": ["Mylai Karpagambal Mess", "Rayar's Cafe"]
                },
                {
                    "name": "Fort St. George",
                    "type": "Fort",
                    "description": "Historic British fort and museum complex.",
                    "famous_foods": ["Dosa", "Vada"],
                    "nearby_food_spots": ["Murugan Idli Shop", "Saravana Bhavan"]
                }
            ]
        }
    # Example data for Goa
    elif destination.lower() in ["goa", "goa, india", "goi"]:
        return {
            "landmarks": [
                {
                    "name": "Baga Beach",
                    "type": "Beach",
                    "description": "Popular beach known for nightlife, water sports, and shacks.",
                    "famous_foods": ["Goan Fish Curry", "Prawn Balchao"],
                    "nearby_food_spots": ["Britto's", "St. Anthony's Shack"]
                },
                {
                    "name": "Basilica of Bom Jesus",
                    "type": "Church",
                    "description": "UNESCO World Heritage Site famous for baroque architecture.",
                    "famous_foods": ["Bebinca", "Sannas"],
                    "nearby_food_spots": ["Fisherman's Wharf", "Mum's Kitchen"]
                },
                {
                    "name": "Fort Aguada",
                    "type": "Fort",
                    "description": "17th-century Portuguese fort with panoramic sea views.",
                    "famous_foods": ["Chicken Cafreal", "Feni"],
                    "nearby_food_spots": ["Souza Lobo", "Fat Fish"]
                }
            ]
        }
    # Generic fallback for any other destination
    else:
        # Try to provide more realistic and descriptive places and foods
        destination_lower = destination.lower()
        if "france" in destination_lower:
            return {
                "landmarks": [
                    {
                        "name": "Eiffel Tower",
                        "type": "Monument",
                        "description": "Iconic Parisian landmark with panoramic city views.",
                        "famous_foods": ["Crêpes", "Baguette", "Croissant"],
                        "nearby_food_spots": ["Le Champ de Mars Café", "Bistro Parisien"]
                    },
                    {
                        "name": "Louvre Museum",
                        "type": "Museum",
                        "description": "World's largest art museum and a historic monument in Paris.",
                        "famous_foods": ["French Pastries", "Macarons"],
                        "nearby_food_spots": ["Café Marly", "Le Fumoir"]
                    },
                    {
                        "name": "Mont Saint-Michel",
                        "type": "Island Abbey",
                        "description": "Medieval abbey on a tidal island, a UNESCO World Heritage Site.",
                        "famous_foods": ["Omelette de la Mère Poulard", "Seafood Platter"],
                        "nearby_food_spots": ["La Mère Poulard", "Le Relais du Roy"]
                    }
                ]
            }
        elif "italy" in destination_lower:
            return {
                "landmarks": [
                    {
                        "name": "Colosseum",
                        "type": "Amphitheatre",
                        "description": "Ancient Roman amphitheatre in the heart of Rome.",
                        "famous_foods": ["Pizza Margherita", "Gelato"],
                        "nearby_food_spots": ["Trattoria Luzzi", "Gelateria La Dolce Vita"]
                    },
                    {
                        "name": "Leaning Tower of Pisa",
                        "type": "Tower",
                        "description": "Famous leaning bell tower in Pisa.",
                        "famous_foods": ["Pasta Carbonara", "Tiramisu"],
                        "nearby_food_spots": ["Ristorante Piazza dei Miracoli", "Osteria in Domo"]
                    },
                    {
                        "name": "Venice Grand Canal",
                        "type": "Canal",
                        "description": "Picturesque waterway lined with Renaissance and Gothic palaces.",
                        "famous_foods": ["Risotto", "Cicchetti"],
                        "nearby_food_spots": ["Osteria alle Testiere", "Cantina Do Spade"]
                    }
                ]
            }
        elif "japan" in destination_lower:
            return {
                "landmarks": [
                    {
                        "name": "Mount Fuji",
                        "type": "Mountain",
                        "description": "Japan's tallest peak and iconic symbol.",
                        "famous_foods": ["Sushi", "Ramen"],
                        "nearby_food_spots": ["Fujiyama Restaurant", "Sushi Zanmai"]
                    },
                    {
                        "name": "Fushimi Inari Shrine",
                        "type": "Shrine",
                        "description": "Famous for its thousands of vermilion torii gates in Kyoto.",
                        "famous_foods": ["Yakitori", "Matcha Sweets"],
                        "nearby_food_spots": ["Inari Sushi Koji", "Kyoto Saryo"]
                    },
                    {
                        "name": "Tokyo Skytree",
                        "type": "Tower",
                        "description": "Tallest structure in Japan with observation decks and city views.",
                        "famous_foods": ["Tempura", "Takoyaki"],
                        "nearby_food_spots": ["Skytree Cafe", "Asakusa Menchi"]
                    }
                ]
            }
        else:
            # Default fallback for any other destination
            return {
                "landmarks": [
                    {
                        "name": f"Central {destination.title()} Landmark",
                        "type": "Landmark",
                        "description": f"A must-see attraction in {destination.title()} with local history and culture.",
                        "famous_foods": [f"Signature {destination.title()} Dish", f"Popular {destination.title()} Snack"],
                        "nearby_food_spots": [f"Famous {destination.title()} Eatery", f"Popular {destination.title()} Cafe"]
                    },
                    {
                        "name": f"Historic {destination.title()} Site",
                        "type": "Historic Site",
                        "description": f"A place of historical importance in {destination.title()} with unique architecture.",
                        "famous_foods": [f"Traditional {destination.title()} Food", f"Local {destination.title()} Dessert"],
                        "nearby_food_spots": [f"Best {destination.title()} Restaurant", f"Traditional {destination.title()} Sweet Shop"]
                    },
                    {
                        "name": f"{destination.title()} Park or Beach",
                        "type": "Park/Beach",
                        "description": f"A scenic spot for relaxation and recreation in {destination.title()}.",
                        "famous_foods": [f"Local {destination.title()} Treat", f"Refreshing {destination.title()} Drink"],
                        "nearby_food_spots": [f"Best {destination.title()} Food Stall", f"Popular {destination.title()} Bar"]
                    }
                ]
            }
