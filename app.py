
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Dictionary mapping emotions to book quotes, titles, and links
emotion_quotes = {
    'hopeful': {
        'quote': "'But I know, somehow, that only when it is dark enough can you see the stars.'",
        'book': 'A Testament of Hope by Martin Luther King Jr.',
        'link': 'https://www.goodreads.com/quotes/1016-but-i-know-somehow-that-only-when-it-is-dark'
    },
    'lonely': {
        'quote': "'The worst part of holding the memories is not the pain. It's the loneliness of it. Memories need to be shared.'",
        'book': 'The Giver by Lois Lowry',
        'link': 'https://www.goodreads.com/quotes/14205-the-worst-part-of-holding-the-memories-is-not-the'
    },
    'joyful': {
        'quote': "'Happiness can be found even in the darkest of times, if one only remembers to turn on the light.'",
        'book': 'Harry Potter and the Prisoner of Azkaban by J.K. Rowling',
        'link': 'https://www.goodreads.com/quotes/4286-happiness-can-be-found-even-in-the-darkest-of-times'
    },
    'courage': {
        'quote': "'I am not afraid of storms, for I am learning how to sail my ship.'",
        'book': 'Little Women by Louisa May Alcott',
        'link': 'https://www.goodreads.com/quotes/1106-i-am-not-afraid-of-storms-for-i-am-learning'
    },
    'love': {
        'quote': "'Whatever our souls are made of, his and mine are the same.'",
        'book': 'Wuthering Heights by Emily Brontë',
        'link': 'https://www.goodreads.com/quotes/1886-whatever-our-souls-are-made-of-his-and-mine-are'
    },
    'anxious': {
        'quote': "'You can't stop the future. You can't rewind the past. The only way to learn the secret...is to press play.'",
        'book': 'Thirteen Reasons Why by Jay Asher',
        'link': 'https://www.goodreads.com/quotes/18613-you-can-t-stop-the-future-you-can-t-rewind-the'
    },
    'grateful': {
        'quote': "'Gratitude turns what we have into enough.'",
        'book': 'Aesop’s Fables',
        'link': 'https://www.goodreads.com/quotes/753-gratitude-turns-what-we-have-into-enough'
    },
    'brave': {
        'quote': "'Bran thought about it. 'Can a man still be brave if he's afraid?' 'That is the only time a man can be brave,' his father told him.'",
        'book': 'A Game of Thrones by George R.R. Martin',
        'link': 'https://www.goodreads.com/quotes/868-bran-thought-about-it-can-a-man-still-be-brave'
    },
    'curious': {
        'quote': "'The important thing is not to stop questioning. Curiosity has its own reason for existing.'",
        'book': 'Albert Einstein',
        'link': 'https://www.goodreads.com/quotes/944-the-important-thing-is-not-to-stop-questioning-curiosity-has'
    },
    'peaceful': {
        'quote': "'Peace begins with a smile.'",
        'book': 'Mother Teresa',
        'link': 'https://www.goodreads.com/quotes/1017-peace-begins-with-a-smile'
    },
    # Add more emotions and quotes as needed
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Quotes by Emotion</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&family=EB+Garamond:wght@500;700&family=Quicksand:wght@500&display=swap" rel="stylesheet">
    <style>
        body {
            background: url('https://www.transparenttextures.com/patterns/cream-paper.png'), linear-gradient(120deg, #f5e9da 0%, #e7d8c9 100%);
            font-family: 'EB Garamond', 'Quicksand', serif;
            min-height: 100vh;
            color: #5a4a3f;
        }
        .main-title {
            font-family: 'Montserrat', 'EB Garamond', serif;
            font-size: 2.5rem;
            color: #7c5e3c;
            letter-spacing: 1.5px;
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            text-shadow: 0 2px 8px #e7d8c9;
        }
        .mood-board {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            justify-content: center;
            margin-top: 2rem;
        }
        .quote-card {
            border-radius: 1.2rem 1.2rem 1.8rem 1.8rem;
            background: #fffbe9;
            border: 1.5px solid #e7d8c9;
            box-shadow: 0 6px 32px 0 rgba(120, 90, 60, 0.10), 0 1.5px 0 #e7d8c9;
            padding: 2.2rem 2rem 1.5rem 2rem;
            max-width: 540px;
            min-width: 320px;
            margin: 0 auto 2rem auto;
            position: relative;
            transition: box-shadow 0.2s, transform 0.2s;
        }
        .quote-card:before {
            content: '';
            position: absolute;
            top: -18px; left: 30px;
            width: 60px; height: 30px;
            background: url('https://www.transparenttextures.com/patterns/old-mathematics.png');
            opacity: 0.18;
            border-radius: 12px 12px 0 0;
        }
        .quote-card:hover {
            box-shadow: 0 12px 48px 0 rgba(120, 90, 60, 0.18);
            transform: translateY(-4px) scale(1.01);
        }
        .blockquote {
            font-size: 1.35rem;
            color: #5a4a3f;
            font-family: 'EB Garamond', serif;
            margin-bottom: 1.2rem;
        }
        .blockquote-footer {
            color: #b89b72;
            font-size: 1.05rem;
            font-family: 'Quicksand', sans-serif;
        }
        .emotion-input {
            border-radius: 2rem;
            border: 1.5px solid #b89b72;
            font-size: 1.1rem;
            background: #f9f6f2;
            color: #7c5e3c;
            font-family: 'Quicksand', sans-serif;
        }
        .btn-primary {
            background: linear-gradient(90deg, #b89b72 0%, #e7d8c9 100%);
            border: none;
            border-radius: 2rem;
            font-weight: 500;
            font-size: 1.1rem;
            padding: 0.5rem 2rem;
            color: #fffbe9;
            font-family: 'Quicksand', sans-serif;
            box-shadow: 0 2px 8px 0 rgba(120, 90, 60, 0.10);
        }
        .btn-primary:hover {
            background: linear-gradient(90deg, #a07c54 0%, #e7d8c9 100%);
            color: #fffbe9;
        }
        .btn-outline-secondary {
            border-radius: 2rem;
            border: 1.5px solid #b89b72;
            color: #b89b72;
            background: #fffbe9;
            font-family: 'Quicksand', sans-serif;
        }
        .btn-outline-secondary:hover {
            background: #e7d8c9;
            color: #7c5e3c;
        }
        .suggestion {
            font-size: 1.05rem;
            color: #b89b72;
            margin-top: 1.2rem;
            font-family: 'Quicksand', sans-serif;
        }
        .emotion-badges {
            margin-top: 0.5rem;
        }
        .emotion-badges .badge {
            margin: 0 0.2rem 0.2rem 0;
            font-size: 1.01rem;
            background: #e7d8c9;
            color: #7c5e3c;
            font-family: 'Quicksand', sans-serif;
            border-radius: 1.2rem;
            box-shadow: 0 1px 4px 0 rgba(120, 90, 60, 0.08);
        }
        .assistant-avatar {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: #e7d8c9;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 12px 0 rgba(120, 90, 60, 0.10);
            border: 2px solid #b89b72;
        }
        .fw-semibold.text-secondary {
            color: #b89b72 !important;
            font-family: 'Quicksand', sans-serif;
        }
    </style>
</head>
<body>
    <div class="container py-3">
        <div class="d-flex flex-column align-items-center mt-4 mb-2">
            <!-- Assistant Avatar SVG -->
            <div class="assistant-avatar mb-2">
                <svg width="90" height="90" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="45" cy="45" r="44" fill="#e7d8c9" stroke="#b89b72" stroke-width="2"/>
                  <ellipse cx="45" cy="50" rx="28" ry="24" fill="#fffbe9"/>
                  <ellipse cx="45" cy="40" rx="18" ry="16" fill="#f5e9da"/>
                  <ellipse cx="35" cy="44" rx="3.5" ry="4.5" fill="#b89b72"/>
                  <ellipse cx="55" cy="44" rx="3.5" ry="4.5" fill="#b89b72"/>
                  <path d="M38 58 Q45 64 52 58" stroke="#b89b72" stroke-width="2.5" stroke-linecap="round" fill="none"/>
                  <ellipse cx="45" cy="70" rx="10" ry="3" fill="#e7d8c9"/>
                </svg>
            </div>
            <div class="fw-semibold text-secondary" style="font-size:1.1rem;">Your Book Quote Assistant</div>
        </div>
        <h1 class="main-title text-center">Find a Book Quote for Your Emotion</h1>
        <form method="post" class="d-flex justify-content-center mb-2">
            <input type="text" name="emotion" class="form-control w-50 me-2 emotion-input" placeholder="Type any emotion (e.g., hopeful, grateful, brave)" required autofocus>
            <button type="submit" class="btn btn-primary">Find Quote</button>
        </form>
        <div class="suggestion text-center">Try emotions like:
            <span class="emotion-badges">
                {% for emo in emotions %}
                    <span class="badge">{{ emo }}</span>
                {% endfor %}
            </span>
        </div>
        <div class="mood-board">
            {% if result %}
            <div class="card quote-card shadow-sm">
                <div class="card-body">
                    <blockquote class="blockquote mb-3">
                        <p>{{ result['quote'] }}</p>
                    </blockquote>
                    <footer class="blockquote-footer mb-2">From <cite title="Book">{{ result['book'] }}</cite></footer>
                    <a href="{{ result['link'] }}" class="btn btn-outline-secondary" target="_blank">Learn more</a>
                </div>
            </div>
            {% elif searched %}
            <div class="card quote-card shadow-sm text-center">
                <div class="card-body">
                    <div class="alert alert-warning border-0 bg-transparent p-0" style="color:#b89b72; font-family:'Quicksand',sans-serif; font-size:1.1rem;">Sorry, we don't have a quote for that emotion yet.<br>Try another emotion from the suggestions above!</div>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    searched = False
    emotions = list(emotion_quotes.keys())
    if request.method == 'POST':
        emotion = request.form['emotion'].strip().lower()
        searched = True
        result = emotion_quotes.get(emotion)
    return render_template_string(HTML_TEMPLATE, result=result, searched=searched, emotions=emotions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
