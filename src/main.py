import warnings
import time
from playwright.sync_api import sync_playwright

# Grundlegende Funktion zum suchen von bestimmten Tags
def get_content(tag, search):
    data = page.query_selector('%s[data-e2e="%s"]' % (tag, search))
    if data:
        return data.text_content()
    warnings.warn("Content connte nicht gefunden werden für %s als %s-Tag" % (search, tag))
    return ""


# Funktion gibt URL von dem aktuellen Video aus
def get_video_url():
    return get_content("p", "browse-video-link").split("?")[0]


# Funktion gibt den Username des Authors von dem aktuellen Video aus
def get_username():
    return get_content("span", "browse-username")


# Funktion gibt den Nickname des Authors von dem aktuellen Video aus
def get_nickname():
    return get_content("span", "browse-nickname")


# Funktion gibt die Beschreibung von dem aktuellen Video aus
def get_video_caption():
    return get_content("div", "browse-video-desc")


with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://tiktok.com")

    input("Drücke auf Enter sobald du bereit bist.")

    video_url = get_video_url()
    username = get_username()
    nickname = get_nickname()
    video_caption = get_video_caption()

    print("URL: %s \nUsername: %s \nNickname: %s \nCaption: %s" % (video_url, username, nickname, video_caption))
    page.screenshot(path="../out/screenshots/%s.png" % (video_url))
    browser.close() 