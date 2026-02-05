import feedparser
import smtplib
import os
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
    "intern",
    "internship",
    "trainee",
    "training",
    "summer intern",
    "summer internship",
    "graduate intern",
    "student intern",
    "placement",
    "co-op",
    "coop",
    "apprentice",
    "entry level intern",
    "intern position",
    "intern role",
    "internship program",
    "internship opportunity",
    "training program",
    "program intern",
    "تدريب",
    "متدرب",
    "تدريب صيفي",
    "برنامج تدريب",
    "فرصة تدريب",
    "تدريب طلبة",
]

FIELD_KEYWORDS = [
    # Core AI
    "ai",
    "a.i",
    "artificial intelligence",
    "machine learning",
    "ml",
    "deep learning",
    "dl",
    "neural network",
    "neural networks",
    "nlp",
    "natural language processing",
    "computer vision",
    "cv",
    "speech recognition",
    "llm",
    "large language model",
    "generative ai",
    "gen ai",
    "ai model",
    "ai engineer",
    "ai developer",
    "ai research",
    "ai research engineer",

    # Data & analytics (AI-adjacent internships)
    "data science",
    "data scientist",
    "data analyst",
    "data analytics",
    "data engineering",
    "data engineer",
    "big data",
    "data mining",
    "predictive modeling",
    "statistics",
    "pandas",
    "numpy",
    "scikit",
    "tensorflow",
    "pytorch",

    # Automation / modern AI stack
    "ai automation",
    "mlops",
    "model deployment",
    "model training",
    "rag",
    "retrieval augmented",
    "vector database",
    "prompt engineering",
    "ai agent",
    "agents",
    "langchain",
    "openai",
    "huggingface",

    # Robotics & embedded AI
    "robotics",
    "autonomous",
    "self driving",
    "drone ai",

    # Arabic AI terms
    "ذكاء اصطناعي",
    "الذكاء الاصطناعي",
    "تعلم الآلة",
    "تعلم الالة",
    "رؤية حاسوبية",
    "معالجة اللغة الطبيعية",
    "تحليل البيانات",
    "علم البيانات",
]
# ============================


# ========= EMAIL CONFIG =========
EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASS"]
TO_EMAIL = os.environ["TO_EMAIL"]
# =================================


def matches(text: str) -> bool:
    """Check if text contains internship + field keywords."""
    text = text.lower()
    return any(i in text for i in INTERN_KEYWORDS) and any(
        f in text for f in FIELD_KEYWORDS
    )


def send_email(subject: str, body: str):
    """Send email using Gmail SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


def main():
    found_any = False

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        # Only check latest 3 posts → prevents timeout on GitHub Actions
        for entry in feed.entries[:3]:
            text = f"{entry.title} {entry.get('summary', '')}"

            if matches(text):
                found_any = True
                send_email(
                    "New AI Internship Found 🚀",
                    f"{entry.title}\n{entry.link}",
                )

    if not found_any:
        print("No matching internships found this run.")


if __name__ == "__main__":
    main()
