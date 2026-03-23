# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and Streamlit. Select any movie and instantly get 5 similar recommendations along with their posters — fetched live from [The Movie Database (TMDb)](https://www.themoviedb.org/).

---

## 📌 Features

- Content-based filtering using cosine similarity
- Interactive web UI powered by Streamlit
- Movie poster fetching via the TMDb API
- Pre-trained similarity model for fast recommendations
- Clean and simple user experience

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Web Framework | Streamlit |
| ML / Data | Pandas, Scikit-learn, NLTK |
| Model Storage | Pickle (`.pkl`) |
| Poster API | TMDb API |
| Notebook | Jupyter Notebook |

---

## 📁 Project Structure

```
movie-recommendation-system/
│
├── data preprocess and model build/   # Jupyter notebook for EDA, preprocessing & model training
│
├── main.py                            # Streamlit app (frontend + recommendation logic)
├── movie_dict.pkl                     # Serialized movie metadata dictionary
├── movies.pkl                         # Serialized movies DataFrame
├── similarity.pkl                     # Precomputed cosine similarity matrix
│
├── .gitignore
├── .gitattributes
└── README.md
```

---

## ⚙️ How It Works

1. **Data Preprocessing** — Movie metadata (genres, cast, crew, keywords, overview) is cleaned and combined into a single "tags" feature per movie.
2. **Vectorization** — Tags are converted into numerical vectors using CountVectorizer.
3. **Similarity Computation** — Cosine similarity is computed between all movie vectors and saved as `similarity.pkl`.
4. **Recommendation** — When a user selects a movie, the top 5 most similar movies are fetched from the precomputed matrix.
5. **Poster Fetching** — Movie posters are retrieved in real time from the TMDb API using each movie's ID.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A free [TMDb API key](https://www.themoviedb.org/settings/api)

### Installation

```bash
# Clone the repository
git clone https://github.com/NavdeepR24/movie-recommendation-system.git
cd movie-recommendation-system

# Install dependencies
pip install streamlit pandas scikit-learn requests
```

### Configuration

Open `main.py` and replace the placeholder with your TMDb API key:

```python
API_KEY = "your_tmdb_api_key_here"
```

### Run the App

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🔁 Rebuilding the Model

If you want to retrain the model on fresh data, open the Jupyter notebook inside the `data preprocess and model build/` folder and run all cells. This will regenerate `movie_dict.pkl`, `movies.pkl`, and `similarity.pkl`.

---

## 📷 Poster Attribution

Movie poster images are sourced from [TMDb](https://www.themoviedb.org/) in accordance with their usage guidelines. This product uses the TMDb API but is not endorsed or certified by TMDb.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Navdeep** — [@NavdeepR24](https://github.com/NavdeepR24)