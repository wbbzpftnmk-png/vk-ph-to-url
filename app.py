import re
import json
import time
import requests
from pathlib import Path
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

VK_API_VERSION = "5.131"

APP_DATA_DIR = Path.home() / "Library" / "Application Support" / "VK Album Photo URLs"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
TOKENS_FILE = APP_DATA_DIR / "vk_tokens.json"
HISTORY_FILE = APP_DATA_DIR / "album_history.json"

HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VK Album Photo URLs</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
      max-width: 1100px;
      margin: 18px auto 24px;
      padding: 0 16px 40px;
      line-height: 1.5;
    }
    .topbar {
      font-size: 12px;
      color: #666;
      margin-bottom: 14px;
    }
    .topbar a { color: #0b57d0; }
    h1, h2, h3 { margin-bottom: 12px; }
    input, button, select, textarea {
      width: 100%;
      box-sizing: border-box;
      padding: 10px;
      font-size: 16px;
      margin: 8px 0 14px;
    }
    button { cursor: pointer; }
    textarea {
      min-height: 360px;
      resize: vertical;
      white-space: pre;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    .box {
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 14px;
      margin-bottom: 18px;
      background: #fafafa;
    }
    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 10px 0 16px;
    }
    .actions button {
      width: auto;
      margin: 0;
      flex: 1 1 180px;
    }
    .error { color: #b00020; }
    .status { margin-top: 8px; font-size: 14px; color: #0a7a2f; }
    .muted { color: #666; font-size: 14px; }
    .small { font-size: 13px; color: #666; }
    .helpbox {
      border-left: 4px solid #0b57d0;
      padding: 12px 14px;
      background: #f4f8ff;
      border-radius: 8px;
      margin-top: 10px;
    }
    a { color: #0b57d0; }
    .token-item, .history-item {
      padding: 8px 0;
      border-bottom: 1px solid #eee;
    }
    .token-head, .history-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .token-label, .history-label {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 78%;
    }
    .token-actions {
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }
    .token-actions form, .token-actions button {
      width: auto;
      margin: 0;
    }
    .token-actions button {
      padding: 8px 10px;
    }
    .hidden { display: none; }
    .dropdown-panel {
      border: 1px solid #d9d9d9;
      border-radius: 10px;
      background: #fff;
      padding: 12px;
      margin-top: 10px;
    }
    .dropdown-trigger {
      display: inline-block;
      width: auto;
      margin-top: 0;
    }
  </style>
</head>
<body>

  <div class="topbar">
    Захаров Максим · <a href="http://t.me/ph_zakharov_m" target="_blank" rel="noopener noreferrer">t.me/ph_zakharov_m</a>
  </div>

  <h1>VK Album Photo URLs</h1>

  <div class="box">
    <h2>1. VK API</h2>

    <label for="selected_token">Сохранённые API</label>
    <form method="post" action="/use_token">
      <select id="selected_token" name="selected_token">
        <option value="">-- выберите сохранённый API --</option>
        {% for t in tokens %}
          <option value="{{ t.id }}" {% if t.id == selected_token_id %}selected{% endif %}>
            {{ t.name }} — {{ t.preview }}
          </option>
        {% endfor %}
      </select>
      <button type="submit">Использовать выбранный API</button>
    </form>

    <button type="button" class="dropdown-trigger" onclick="toggleAddPanel()">Добавить новый API</button>

    <div id="addPanel" class="dropdown-panel hidden">
      <form method="post" action="/save_token">
        <label for="token_name">Название токена</label>
        <input id="token_name" name="token_name" type="text" placeholder="Например: домашняя сеть">

        <label for="token_value">Вставить API / access token</label>
        <input id="token_value" name="token_value" type="text" placeholder="vk1.a....">

        <button type="submit">Сохранить API локально</button>
      </form>

      <button type="button" onclick="toggleHelp()">Получить API</button>

      <div id="helpbox" class="helpbox hidden">
        <h3>Как получить VK API</h3>
        <ol>
          <li>Создайте приложение VK ID и получите access token через OAuth.</li>
          <li>Выбирайте токен только для той сети, где он будет использоваться.</li>
          <li>Если сеть или IP меняются, VK может выдать ошибку привязки токена к IP.</li>
          <li>После авторизации скопируйте access token из адресной строки.</li>
        </ol>
        <p>
          Официальные ссылки:
          <a href="https://id.vk.com/" target="_blank" rel="noopener noreferrer">VK ID</a>,
          <a href="https://dev.vk.com/ru/method/photos.get" target="_blank" rel="noopener noreferrer">photos.get</a>,
          <a href="https://oauth.vk.com/authorize" target="_blank" rel="noopener noreferrer">OAuth authorize</a>.
        </p>
        <p class="small">
          Пример OAuth-ссылки:<br>
          <code>https://oauth.vk.com/authorize?client_id=ВАШ_CLIENT_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos&response_type=token&v=5.131</code>
        </p>
        <p class="small">
          Важно: каждый API может быть привязан к своей сети и IP, поэтому не переносите один и тот же токен между разными Wi‑Fi, VPN или мобильным интернетом.
        </p>
      </div>
    </div>

    {% if tokens %}
      <div class="muted" style="margin-top:12px;">Сохранённые токены:</div>
      {% for t in tokens %}
        <div class="token-item">
          <div class="token-head">
            <div class="token-label">
              <strong>{{ t.name }}</strong>
              <div class="small">{{ t.preview }}</div>
            </div>
            <div class="token-actions">
              <form method="post" action="/use_token">
                <input type="hidden" name="selected_token" value="{{ t.id }}">
                <button type="submit">Выбрать</button>
              </form>
              <form method="post" action="/delete_token" onsubmit="return confirm('Удалить этот API из локального списка?');">
                <input type="hidden" name="token_id" value="{{ t.id }}">
                <button type="submit">Удалить</button>
              </form>
            </div>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p class="muted">Пока нет сохранённых API.</p>
    {% endif %}

    <p class="status">Активный API: <strong>{{ active_token_name or 'не выбран' }}</strong></p>
    {% if api_error %}
      <p class="error"><strong>Ошибка API:</strong> {{ api_error }}</p>
    {% endif %}
  </div>

  <div class="box">
    <h2>2. Альбом VK</h2>
    <form method="post" action="/fetch">
      <label for="albumUrl">Ссылка на альбом VK</label>
      <input id="albumUrl" name="albumUrl" type="text"
             placeholder="https://vk.com/album-123456_789012"
             value="{{ album_url or '' }}">
      <button type="submit">Проверить альбом</button>
      <div class="muted">После проверки покажется количество фото, ссылки и история.</div>
    </form>
  </div>

  {% if urls %}
    <div class="box">
      <h2>3. Ссылки на фото</h2>
      <div class="muted">Количество фото в альбоме: <strong>{{ photo_count }}</strong></div>
      <div class="actions">
        <button type="button" onclick="selectAllText()">Выделить все</button>
        <button type="button" onclick="copyAll()">Копировать все</button>
      </div>

      <label for="urlsArea">Ссылки</label>
      <textarea id="urlsArea" readonly>{{ urls|join('\\n') }}</textarea>
      <div id="status" class="status"></div>
    </div>
  {% endif %}

  <div class="box">
    <h2>4. История альбомов</h2>
    {% if history %}
      {% for item in history %}
        <div class="history-item">
          <div class="history-head">
            <div class="history-label">
              <strong>{{ item.title or 'Без названия' }}</strong>
              <div class="history-meta">
                <a href="{{ item.album_url }}" target="_blank" rel="noopener noreferrer">{{ item.album_url }}</a>
              </div>
              <div class="history-meta">
                Фото: {{ item.photo_count }} · Проверен: {{ item.checked_at }}
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p class="muted">История пока пустая.</p>
    {% endif %}
  </div>

  {% if error %}
    <p class="error"><strong>Ошибка:</strong> {{ error }}</p>
  {% endif %}

  <script>
    const urls = {{ urls|tojson if urls else '[]' }};

    function toggleHelp() {
      document.getElementById('helpbox').classList.toggle('hidden');
    }

    function toggleAddPanel() {
      document.getElementById('addPanel').classList.toggle('hidden');
    }

    function getTextarea() {
      return document.getElementById('urlsArea');
    }

    function setStatus(text, isError=false) {
      const el = document.getElementById('status');
      if (!el) return;
      el.textContent = text;
      el.style.color = isError ? '#b00020' : '#0a7a2f';
    }

    function selectAllText() {
      const ta = getTextarea();
      if (!ta) return;
      ta.focus();
      ta.select();
      if (ta.setSelectionRange) ta.setSelectionRange(0, ta.value.length);
      setStatus('Все ссылки выделены');
    }

    function fallbackCopy(text) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      ta.style.top = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      let ok = false;
      try {
        ok = document.execCommand('copy');
      } catch (e) {
        ok = false;
      }
      document.body.removeChild(ta);
      return ok;
    }

    async function copyText(text) {
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          return true;
        } catch (e) {}
      }
      return fallbackCopy(text);
    }

    async function copyAll() {
      const text = urls.join('\\n');
      const ok = await copyText(text);
      setStatus(ok ? 'Все ссылки скопированы в буфер обмена' : 'Не удалось скопировать ссылки', !ok);
    }

    const ta = getTextarea();
    if (ta) ta.addEventListener('click', () => ta.focus());
  </script>
</body>
</html>
"""

def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_tokens():
    return load_json(TOKENS_FILE, [])

def save_tokens(tokens):
    save_json(TOKENS_FILE, tokens)

def load_history():
    return load_json(HISTORY_FILE, [])

def save_history(history):
    save_json(HISTORY_FILE, history)

def add_history(album_url, title, photo_count):
    history = load_history()
    entry = {
        "album_url": album_url,
        "title": title or "",
        "photo_count": photo_count,
        "checked_at": time.strftime("%Y-%m-%d %H:%M")
    }
    history = [h for h in history if h.get("album_url") != album_url]
    history.insert(0, entry)
    history = history[:20]
    save_history(history)

def mask_token(token):
    token = token or ""
    if len(token) <= 12:
        return token
    return f"{token[:8]}...{token[-4:]}"

def get_selected_token():
    tokens = load_tokens()
    if not tokens:
        return None
    token_id = request.cookies.get("selected_token_id")
    if token_id:
        for t in tokens:
            if t["id"] == token_id:
                return t
    return tokens[0]

def verify_token(token):
    params = {"access_token": token, "v": VK_API_VERSION}
    r = requests.get("https://api.vk.com/method/users.get", params=params, timeout=20)
    data = r.json()
    if "error" in data:
        msg = data["error"].get("error_msg", "VK API error")
        if "another ip address" in msg.lower():
            raise ValueError("Этот API привязан к другой сети или IP-адресу. Используйте токен, полученный в текущей сети.")
        raise ValueError(msg)
    return True

def parse_album_link(url):
    if not url:
        return None
    url = url.strip().rstrip("/")
    last_part = url.split("/")[-1]
    m = re.match(r"^album(-?\d+)_([0-9]+)$", last_part)
    if not m:
        return None
    return m.group(1), m.group(2)

def choose_best_url(photo):
    for key in ["photo_2560", "photo_1280", "photo_807", "photo_604", "photo_130", "photo_75"]:
        if key in photo and photo[key]:
            return photo[key]
    sizes = photo.get("sizes", [])
    if sizes:
        best = max(sizes, key=lambda s: s.get("width", 0))
        return best.get("url", "")
    return ""

def get_all_photos(owner_id, album_id, token):
    all_items = []
    offset = 0
    count = 200

    while True:
        params = {
            "owner_id": owner_id,
            "album_id": album_id,
            "count": count,
            "offset": offset,
            "access_token": token,
            "v": VK_API_VERSION,
        }
        r = requests.get("https://api.vk.com/method/photos.get", params=params, timeout=30)
        data = r.json()

        if "error" in data:
            raise Exception(data["error"].get("error_msg", "VK API error"))

        response = data.get("response", {})
        items = response.get("items", [])
        total = response.get("count", 0)

        all_items.extend(items)
        offset += len(items)

        if offset >= total or not items:
            break

    return all_items, total

def get_album_title(owner_id, album_id, token):
    params = {
        "owner_id": owner_id,
        "album_id": album_id,
        "access_token": token,
        "v": VK_API_VERSION,
    }
    r = requests.get("https://api.vk.com/method/photos.getAlbums", params=params, timeout=20)
    data = r.json()
    if "error" in data:
        return ""
    response = data.get("response", [])
    if response:
        return response[0].get("title", "") or ""
    return ""

def build_album_data(album_url, token):
    if not token:
        raise ValueError("Сначала выберите или сохраните VK API")
    verify_token(token)

    parsed = parse_album_link(album_url)
    if not parsed:
        raise ValueError("Не удалось распознать ссылку. Пример: https://vk.com/album-123456_789012")

    owner_id, album_id = parsed
    album_title = get_album_title(owner_id, album_id, token)
    photos, total = get_all_photos(owner_id, album_id, token)
    urls = [choose_best_url(p) for p in photos]
    urls = [u for u in urls if u]
    return urls, total, album_title

def render_page(**kwargs):
    tokens = load_tokens()
    selected = get_selected_token()
    defaults = dict(
        tokens=[{"id": t["id"], "name": t["name"], "preview": mask_token(t["token"])} for t in tokens],
        selected_token_id=selected["id"] if selected else "",
        active_token_name=selected["name"] if selected else None,
        urls=[],
        photo_count=0,
        history=load_history(),
        error=None,
        api_error=None,
        album_url=""
    )
    defaults.update(kwargs)
    return render_template_string(HTML, **defaults)

@app.route("/", methods=["GET"])
def index():
    return render_page()

@app.route("/save_token", methods=["POST"])
def save_token():
    token_name = request.form.get("token_name", "").strip() or f"API {int(time.time())}"
    token_value = request.form.get("token_value", "").strip()

    if not token_value:
        return redirect(url_for("index"))

    try:
        verify_token(token_value)
    except Exception as e:
        return render_page(api_error=f"Токен не прошёл проверку: {e}")

    tokens = load_tokens()
    token_id = str(int(time.time() * 1000))
    tokens.append({"id": token_id, "name": token_name, "token": token_value})
    save_tokens(tokens)

    resp = redirect(url_for("index"))
    resp.set_cookie("selected_token_id", token_id, max_age=60 * 60 * 24 * 365)
    return resp

@app.route("/use_token", methods=["POST"])
def use_token():
    token_id = request.form.get("selected_token", "").strip()
    resp = redirect(url_for("index"))
    if token_id:
        resp.set_cookie("selected_token_id", token_id, max_age=60 * 60 * 24 * 365)
    return resp

@app.route("/delete_token", methods=["POST"])
def delete_token():
    token_id = request.form.get("token_id", "").strip()
    tokens = load_tokens()
    tokens = [t for t in tokens if t["id"] != token_id]
    save_tokens(tokens)

    resp = redirect(url_for("index"))
    if request.cookies.get("selected_token_id") == token_id:
        resp.delete_cookie("selected_token_id")
    return resp

@app.route("/fetch", methods=["POST"])
def fetch():
    album_url = request.form.get("albumUrl", "").strip()
    selected = get_selected_token()

    try:
        token = selected["token"] if selected else None
        urls, total, album_title = build_album_data(album_url, token)
        add_history(album_url, album_title, total)

        if not urls:
            return render_page(
                error="Фото не найдены или нет доступа к альбому.",
                album_url=album_url,
                photo_count=total
            )

        return render_page(
            urls=urls,
            album_url=album_url,
            photo_count=total
        )
    except Exception as e:
        return render_page(
            error=str(e),
            album_url=album_url
        )