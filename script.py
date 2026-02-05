import feedparser
import smtplib
import os
import json
import re
from email.mime.text import MIMEText

# ================= RSS FEEDS =================
RSS_FEEDS = [
    "https://rsshub.pseudoyu.com/linkedin/company/advansys-esc/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/alahlymomknfore-payments/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/algoriza/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/aman-holding-for-financials/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/aramex/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/atos/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/wearablabs/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/barqsystems/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/bbiai/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/beinex-consulting/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/bostaapp/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/breadfast/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/careem/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/cartona-egypt/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/cyshield/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/dsquares/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/dxctechnology/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/e-finance/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/gameball/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/geidea/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/giza-systems/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/halan/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/incorta/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/instabug/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/integrant-inc/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/itworx/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/jumia-group/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/khazna/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/link-development/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/liquidc2mena/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/lyriseai/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/maxab/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/moneyfellows/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/mylerz-co/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/naqla/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/nawyestate/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/nooncom/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/paymobcompany/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/rabbitmart/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/sumerge/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/taagercom/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/talabat-com/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/thndrapp/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/trellaapp/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/truflatech/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/twentytooai/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/vezeeta/posts",
    "https://rsshub.pseudoyu.com/linkedin/company/wuzzuf-com/posts",
]
# =============================================


# ========= KEYWORDS =========
INTERN_KEYWORDS = [
    "intern", "internship", "trainee", "training",
    "summer intern", "summer internship", "co-op", "coop",
    "apprentice", "تدريب", "متدرب", "تدريب صيفي",
]

FIELD_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning",
    "deep learning", "nlp", "computer vision", "llm",
    "generative ai", "data science", "ذكاء اصطناعي",
]
# ============================

EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASS"]
TO_EMAIL = os.environ["TO_EMAIL"]

SEEN_FILE = "seen_posts.json"


# ---------- Deduplication ----------
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


# ---------- Smart summary (FREE, no AI) ----------
def extract_summary(text: str):
    text = text.lower()

    # role guess
    role = "AI Internship"
    role_patterns = [
        "ai intern", "machine learning intern", "data science intern",
        "ml intern", "ai trainee"
    ]
    for p in role_patterns:
        if p in text:
            role = p.title()
            break

    # skills guess
    skills = []
    skill_keywords = [
        "python", "pytorch", "tensorflow", "nlp",
        "computer vision", "sql", "pandas", "numpy"
    ]
    for s in skill_keywords:
        if s in text:
            skills.append(s)

    return role, ", ".join(skills) if skills else "Not specified"


# ---------- Internship filter ----------
def is_real_internship(text: str) -> bool:
    text = text.lower()

    has_intern = any(k in text for k in INTERN_KEYWORDS)
    has_field = any(k in text for k in FIELD_KEYWORDS)

    bad_words = [
        "event", "webinar", "conference",
        "partnership", "announcement",
        "celebrating", "highlights",
    ]
    looks_marketing = any(b in text for b in bad_words)

    return has_intern and has_field and not looks_marketing


# ---------- Email ----------
def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


# ---------- Main ----------
def main():
    seen = load_seen()
    new_seen = set(seen)

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:3]:
            post_id = entry.get("id") or entry.get("link")

            if post_id in seen:
                continue

            text = f"{entry.title} {entry.get('summary', '')}"

            if is_real_internship(text):
                role, skills = extract_summary(text)

                email_body = f"""
Company Post: {entry.title}

Detected Role: {role}
Skills Mentioned: {skills}

Link:
{entry.link}
"""

                send_email("New AI Internship Found 🚀", email_body)

                new_seen.add(post_id)

    save_seen(new_seen)


if __name__ == "__main__":
    main()
