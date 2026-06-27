from setuptools import setup

APP = ['main.py']

OPTIONS = {
    'argv_emulation': True,
    'packages': ['flask', 'requests', 'webview'],
    'includes': ['WebKit', 'Foundation'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'vk ph to url',
        'CFBundleDisplayName': 'vk ph to url',
        'CFBundleIdentifier': 'com.vkalbum.photourls',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '12.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)