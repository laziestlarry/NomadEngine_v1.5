import yt_dlp
from db.engine import init_engine
from db.session import create_session
from db.models import IncomeRecord
from events.event_bus import EventBus
from common.timestamps import now_utc

def get_transcript(url):
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    info = ydl.extract_info(url, download=False)
    return info.get("description", "")

def summarize(text):
    # Pseudo call to your existing AutonomaX/Commander LLM pipe
    # Replace with real API if desired
    return text[:250] + "..."

def run(url):
    transcript = get_transcript(url)
    summary = summarize(transcript)

    session = create_session(init_engine())

    record = IncomeRecord(
        platform="youtube-automation",
        amount=1.0,
        currency="USD",
        received_at=now_utc(),
        notes=f"Test income for video: {url}",
    )
    session.add(record)
    session.commit()

    EventBus().publish(
        "income_detected",
        {"platform": "youtube-automation", "amount": 1.0},
        category="income"
    )

    print("Income logged and event emitted.")

if __name__ == "__main__":
    run("https://www.youtube.com/watch?v=dQw4w9WgXcQ")