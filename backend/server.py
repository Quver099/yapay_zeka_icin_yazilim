# Kurulum: pip install fastapi uvicorn anthropic
# Çalıştırma: export ANTHROPIC_API_KEY=sk-ant-...   (Windows: set ANTHROPIC_API_KEY=...)
#             uvicorn server:app --reload --port 8000
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

client = Anthropic()  # anahtar ortam değişkeninden okunur
MODEL = "claude-sonnet-5-5"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

YONETMELIK = """
1. Hiçbir kayıt silinmez; silme yalnızca görünürlüğü kapatır.
2. Oy hakkını kaldıran, defteri silen veya kimlik ifşa eden öneriler kabul edilmez.
3. Her değişiklik oylamayla yapılır.
4. Temel haklara dokunan öneriler 2/3 çoğunluk ister.
5. Azınlığı susturmayı veya yasaklamayı hedefleyen öneriler kabul edilmez.
"""


def ask_json(system: str, user: str) -> dict:
    r = client.messages.create(
        model=MODEL, max_tokens=500, system=system,
        messages=[{"role": "user", "content": user}])
    text = r.content[0].text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)


class VoteReq(BaseModel):
    topic_title: str
    topic_text: str
    domain: str
    proposal_type: str  # edit | delete | close
    payload: str
    constitutional: bool


class RegReq(BaseModel):
    title: str
    text: str


@app.post("/ai/vote")
def ai_vote(q: VoteReq):
    system = ("Sen bir karar forumunda oy veren yapay zekâ delegesisin. "
              "Yalnızca JSON döndür: {\"vote\": true|false, \"reason\": \"en fazla 2 cümle Türkçe gerekçe\"}. "
              "Yönetmelik:\n" + YONETMELIK)
    user = (f"Konu: {q.topic_title}\nAlan: {q.domain}\nMevcut karar metni: {q.topic_text}\n"
            f"Öneri türü: {q.proposal_type}\nÖnerilen metin/gerekçe: {q.payload}\n"
            f"Anayasal mı: {q.constitutional}")
    try:
        return ask_json(system, user)
    except Exception as e:
        return {"vote": False, "reason": f"AI hatası, çekimser sayıldı: {e}", "error": True}


@app.post("/ai/regulation")
def regulation(q: RegReq):
    system = ("Forum yönetmeliği denetçisisin. Yalnızca JSON döndür: "
              "{\"ok\": true|false, \"rule\": \"ihlal edilen madde no veya null\", \"reason\": \"kısa Türkçe açıklama\"}. "
              "Yönetmelik:\n" + YONETMELIK)
    try:
        return ask_json(system, f"Başlık: {q.title}\nMetin: {q.text}")
    except Exception:
        return {"ok": True, "rule": None, "reason": "AI denetimi yapılamadı", "error": True}
