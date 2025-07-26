# ✈️ AI-Powered Travel Planner

A **Streamlit** web app that uses **AI from Hugging Face** to generate personalized travel itineraries, display interactive maps, and recommend famous landmarks and foods based on your destination.

---

## 🌟 Features

- 🤖 **AI-Generated Itineraries**  
  Get custom day-by-day travel plans tailored to your **destination, budget, group size, duration**, and **interests** using the `flan-t5-large` model from Hugging Face.

- 🗺️ **Interactive Map Visualization**  
  Your itinerary is displayed on an interactive **Folium** map with markers for places and foods.

- 📍 **Famous Places & Foods**  
  Discover popular landmarks and signature dishes for any **city or country**. Special data is available for well-known destinations, with smart fallbacks for others.

- 💡 **Travel Tips & Cost Estimates**  
  Receive practical travel advice and average budget ranges for your trip.

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-travel-planner.git
cd ai-travel-planner
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your Hugging Face API Key  
Get your API key from: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

Then run:
```bash
export HUGGING_FACE_API_KEY=your_huggingface_api_key_here
```

### 4. Launch the App
```bash
streamlit run app.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deployment Options

### ✅ Streamlit Community Cloud (Free & Easy)

1. Push your project to GitHub.
2. Visit [Streamlit Sharing](https://share.streamlit.io/) and link your GitHub repo.
3. In **App Settings**, add your Hugging Face API key under `secrets.toml`.

```toml
# .streamlit/secrets.toml
HUGGING_FACE_API_KEY = "your_huggingface_api_key_here"
```

### 🧩 Other Options
- [ ] Heroku  
- [ ] AWS / GCP / Azure  
- [ ] DigitalOcean  
- [ ] Self-hosted

*See the `deployment.md` (coming soon) for detailed instructions.*

---

## 📁 Project Structure

```
.
├── app.py                # Main Streamlit app
├── travel_planner.py     # Core AI itinerary logic
├── map_generator.py      # Map creation & geocoding
├── landmarks_data.py     # Famous places and foods
├── utils.py              # Helper functions
├── requirements.txt      # Dependencies
└── README.md             # You're reading it!
```

---

## 📦 Requirements

- Python 3.7+
- streamlit
- folium
- geopy
- requests

Install with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Customization Tips

- ✏️ **More Destinations:** Add cities and food recommendations in `landmarks_data.py`.
- 🧠 **Change AI Prompts:** Tweak prompts in `travel_planner.py` for different travel styles or tone (fun, formal, budget-friendly, etc.).
- 🌍 **Multi-language Support:** You can enhance the app to work in multiple languages using Hugging Face translation models.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 💬 Feedback & Contributions

Feel free to open issues or submit pull requests for new features or improvements.  
We welcome contributors to make this project better for travelers everywhere!

---

**Enjoy planning your next adventure with AI! 🌏✨**
