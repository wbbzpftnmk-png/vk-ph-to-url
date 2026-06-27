# 📸 vk ph to url

Приложение для получения списка URL-ссылок всех фотографий из альбома в социальной сети VK.

Приложение также хранит историю запросов локально на вашем компьютере.

---

## 🇷🇺 Русский

### ✨ Возможности

- Получение ссылок на все фотографии из альбома VK.
- Сохранение истории запросов.
- Локальное хранение VK API и истории запросов.
- Работа как macOS-приложение.

### 🧠 Как это работает

Приложение обращается к VK API, получает данные об альбоме и формирует список прямых URL-ссылок на фотографии.  
История запросов сохраняется локально на устройстве пользователя.

### 🔐 Privacy

- VK API и история запросов хранятся локально на вашем компьютере.
- Приложение не передаёт данные третьим лицам.
- Для работы требуется ваш VK access token.

### 🍏 Поддерживаемая система

- macOS 12 и выше

### 📦 Зависимости

- py2app
- Flask
- requests
- pywebview

### 🧪 Виртуальное окружение

Для работы проекта используется виртуальное окружение:

- `.venv`

#### Создание и активация

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Установка зависимостей

```bash
pip install -r requirements.txt
```

### 📁 Файлы проекта

- `requirements.txt` — список зависимостей.
- `main.py` — точка входа приложения.
- `setup.py` — сборка macOS-приложения.
- `app.py` — основная логика приложения.
- `icon.icns` — иконка приложения.

### 🔑 Как получить VK API

Для работы приложения нужен VK API access token.

#### Краткая инструкция

1. Откройте страницу VK для разработчиков.
2. Зарегистрируйте приложение или выберите уже созданное.
3. Получите access token / access key в настройках приложения.
4. Скопируйте токен и вставьте его в приложение.

VK API использует ключ доступа, который передаётся в запросах к API [web:54][web:58].

### 💻 Установка на Mac

1. Скачайте файл `.dmg` из раздела Releases.
2. Откройте скачанный файл.
3. Перетащите приложение в папку `Applications`.
4. Запустите приложение из Launchpad или из папки Applications.

### ▶️ Запуск из исходников

1. Создайте и активируйте `.venv`.
2. Установите зависимости.
3. Запустите `main.py`.

```bash
python3 main.py
```

### 📜 Лицензия

Проект распространяется под лицензией MIT.  
Полный текст лицензии находится в файле `LICENSE`.

### 👤 Автор

Захаров Максим

Telegram: [@ph_zakharov_m](http://t.me/ph_zakharov_m)

---

## 🇬🇧 English

### ✨ Features

- Get links to all photos from a VK album.
- Save request history.
- Store VK API data and request history locally.
- Works as a macOS application.

### 🧠 How it works

The app uses the VK API, retrieves album data, and builds a list of direct photo URLs.  
Request history is stored locally on the user’s device.

### 🔐 Privacy

- VK API data and request history are stored locally on your computer.
- The app does not send data to third parties.
- A valid VK access token is required.

### 🍏 Supported system

- macOS 12 and later

### 📦 Dependencies

- py2app
- Flask
- requests
- pywebview

### 🧪 Virtual environment

The project uses a virtual environment:

- `.venv`

#### Create and activate

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

### 📁 Project files

- `requirements.txt` — dependency list.
- `main.py` — application entry point.
- `setup.py` — macOS app build script.
- `app.py` — main application logic.
- `icon.icns` — application icon.

### 🔑 How to get VK API

The app requires a VK API access token.

#### Quick steps

1. Open the VK developer page.
2. Register a new app or select an existing one.
3. Get the access token / access key in the app settings.
4. Copy the token and paste it into the app.

VK API uses an access key that is passed with API requests [web:56][web:58].

### 💻 Install on Mac

1. Download the `.dmg` file from the Releases section.
2. Open the downloaded file.
3. Drag the app into the `Applications` folder.
4. Launch the app from Launchpad or Applications.

### ▶️ Run from source

1. Create and activate `.venv`.
2. Install dependencies.
3. Run `main.py`.

```bash
python3 main.py
```

### 📜 License

This project is licensed under the MIT License.  
See the `LICENSE` file for the full text.

### 👤 Author

Zaharov Maksim

Telegram: [@ph_zakharov_m](http://t.me/ph_zakharov_m)
