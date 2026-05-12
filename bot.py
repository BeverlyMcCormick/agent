"""
Standup Bot Agent — Telegram Bot
SJ Project Planner | Code Without Barriers Hackathon

Team members submit daily standups in a Telegram group; agent parses each
update into structured fields, flags blockers, and generates team digest.
"""
import os
import json
import logging
from datetime import datetime, date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Auto-load .env file from this folder

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

# AI Client
client = OpenAI(
    base_url=os.getenv("AI_ENDPOINT", "https://integrate.api.nvidia.com/v1"),
    api_key=os.getenv("AI_API_KEY", "YOUR_API_KEY_HERE")
)
MODEL = os.getenv("AI_MODEL", "meta/llama-3.1-70b-instruct")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_STANDUP", "YOUR_TELEGRAM_BOT_TOKEN")

# Storage (production: Cosmos DB)
STANDUPS = []


def parse_standup(text: str, user: str) -> dict:
    prompt = f"""Parse this daily standup into JSON.

User: {user}
Update: "{text}"

Return ONLY:
{{
  "yesterday": ["..."],
  "today": ["..."],
  "blockers": ["..."],
  "sentiment": "positive" | "neutral" | "concerning",
  "needs_help": true/false,
  "tags": ["frontend","backend","infra","design","qa","devops","mobile"]
}}"""
    try:
        r = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.2, max_tokens=400
        )
        c = r.choices[0].message.content
        return json.loads(c[c.find("{"):c.rfind("}")+1])
    except Exception as e:
        log.error(f"Parse error: {e}")
        return {"yesterday": [text], "today": [], "blockers": [], "sentiment": "neutral", "needs_help": False, "tags": []}


def generate_team_digest() -> str:
    today_standups = [s for s in STANDUPS if s["date"] == str(date.today())]
    if not today_standups:
        return "No standups submitted today."

    prompt = f"""You are SJ Group's Standup Bot Agent. Synthesize today's team standup into a digest.

Standups: {json.dumps(today_standups, default=str, indent=2)}

Produce concise markdown digest with sections:
*🌅 Today's Team Standup — {date.today().strftime('%B %d, %Y')}*

*✅ Wins from Yesterday*
*🎯 Today's Focus*
*🚨 Blockers Requiring Attention* (with user names)
*🔗 Cross-Team Dependencies*
*📊 Team Pulse* (one-line)

Use bold (asterisks) sparingly. Reference user names. Keep it under 800 chars total."""
    try:
        r = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=1000
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Could not generate digest: {e}"


# -------- Bot Handlers --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *SJ Project Planner — Standup Bot*\n\n"
        "Drop your daily standup in this chat or group. I'll parse it, "
        "flag blockers, and synthesize a team digest.\n\n"
        "Commands:\n"
        "  /standup — Submit standup\n"
        "  /digest — Generate today's team digest\n"
        "  /today — Show all of today's standups\n\n"
        "_Or just type your update — I'll auto-parse it._\n\n"
        "_Powered by Microsoft Agent Framework_",
        parse_mode="Markdown"
    )


async def standup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Type your standup update.*\n\n"
        "Example:\n"
        "_Yesterday I finished the foundation work on Sector A. "
        "Today starting Sector B excavation. Blocked on equipment shipment._",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Treat any non-command text as a standup."""
    text = update.message.text
    user = update.effective_user.full_name or update.effective_user.username or "Anonymous"

    if len(text) < 20:
        return  # ignore tiny messages

    await update.message.reply_text("🤖 _Parsing your standup..._", parse_mode="Markdown")

    parsed = parse_standup(text, user)
    record = {
        "id": str(len(STANDUPS) + 1),
        "user": user,
        "user_id": update.effective_user.id,
        "text": text,
        "parsed": parsed,
        "date": str(date.today()),
        "timestamp": datetime.now().isoformat()
    }
    STANDUPS.append(record)

    # Format response
    msg_parts = [f"✅ *Standup received from {user}*\n"]

    if parsed.get("yesterday"):
        msg_parts.append("*Yesterday:*")
        msg_parts.extend(f"• {y}" for y in parsed["yesterday"])

    if parsed.get("today"):
        msg_parts.append("\n*Today:*")
        msg_parts.extend(f"• {t}" for t in parsed["today"])

    if parsed.get("blockers"):
        msg_parts.append("\n🚨 *Blockers:*")
        msg_parts.extend(f"• {b}" for b in parsed["blockers"])

    if parsed.get("tags"):
        msg_parts.append(f"\n🏷️ {' '.join('#' + t for t in parsed['tags'])}")

    if parsed.get("needs_help"):
        msg_parts.append("\n⚠️ _Marked as needing help — will flag in team digest._")

    await update.message.reply_text("\n".join(msg_parts), parse_mode="Markdown")


async def digest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 _Synthesizing team digest..._", parse_mode="Markdown")
    digest = generate_team_digest()
    await update.message.reply_text(digest, parse_mode="Markdown")


async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today_standups = [s for s in STANDUPS if s["date"] == str(date.today())]
    if not today_standups:
        await update.message.reply_text("📭 No standups submitted today yet.")
        return
    msg = f"📋 *Today's Standups ({len(today_standups)})*\n\n"
    for s in today_standups:
        blocker_flag = " 🚨" if s["parsed"].get("blockers") else ""
        msg += f"• *{s['user']}*{blocker_flag}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")


def main():
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("⚠️  Set TELEGRAM_TOKEN_STANDUP environment variable.")
        print("   Get a token from @BotFather on Telegram (takes 2 minutes).")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("standup", standup_cmd))
    app.add_handler(CommandHandler("digest", digest_cmd))
    app.add_handler(CommandHandler("today", today_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Standup Bot (Telegram) is running...")
    print("   Add the bot to your team's group, send /start")
    app.run_polling()


if __name__ == "__main__":
    main()
