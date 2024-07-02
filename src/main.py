import time
from playwright.sync_api import sync_playwright

# Einstellungen für grundlegende Funktionen
do_screenshots = True
do_timestamps = True

# Einstellungen, welche Daten berücksichtigt werden sollen
use_url = True
use_username = True
use_nickname = True
use_video_caption = True
use_video_sound = True
use_number_likes = True
use_number_comments = True
use_number_bookmarks = True
use_upload_date = True


# Grundlegende Funktion zum suchen von bestimmten Tags
def get_content(tag, search):
    data = page.query_selector('%s[data-e2e="%s"]' % (tag, search))
    if data:
        return data.text_content()
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    print("")
    print(data)
    print("")
    return ""


# Funktion gibt URL von dem aktuellen Video aus
def get_video_url():
    return get_content("p", "browse-video-link").split("?")[0]


# Funktion gibt den Username des Authors von dem aktuellen Video aus
def get_username():
    return get_content("span", "browse-username")


# Funktion gibt den Nickname des Authors von dem aktuellen Video aus
def get_nickname():
    return get_content("span", "browser-nickname").split("·")[0]


# Funktion gibt die Beschreibung von dem aktuellen Video aus
def get_video_caption():
    return get_content("div", "browse-video-desc")


# Funktion gibt den namen des Sounds von dem aktuellen Video aus
def get_video_sound():
    return get_content("h4", "browse-music")


# Funktion gibt Anzahl der Likes von dem aktuellen Video aus
def get_number_likes():
    return get_content("strong", "browse-like-count")


# Funktion gibt Anzahl der Kommentare von dem aktuellen Video aus
def get_number_comments():
    return get_content("strong", "browse-comment-count")


# Funktion gibt Anzahl der Lesezeichen von dem aktuellen Video aus
def get_number_bookmarks():
    return get_content("strong", "undefined-count")


def get_upload_date():
    return get_content("span", "browser-nickname").split(" · ")[1]


def on_button_next_click():
    print("BUTTON CLICKED!!!")


def listener_button_next_click(page):
    page.expose_function("onButtonClick", on_button_next_click)
    page.evaluate("""() => {
                        const button = document.querySelector('button[data-e2e="arrow-right"]');
                        if (button) {
                            button.addEventListener('click', () => window.onButtonClick());
                        }
                    }""")


with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://tiktok.com")

    input("Drücke auf Enter sobald du bereit bist.")

    timestamp = time.time()
    video_url = get_video_url()
    username = get_username()
    nickname = get_nickname()
    video_caption = get_video_caption()
    video_sound = get_video_sound()
    number_likes = get_number_likes()
    number_comments = get_number_comments()
    number_bookmarks = get_number_bookmarks()
    upload_date = get_upload_date()

    print("Timestamp: %s" % timestamp)
    print("URL: %s" % video_url)
    print("Username: %s" % username)
    print("Nickname: %s" % nickname)
    print("Video Caption: %s" % video_caption)
    print("Video Sound: %s" % video_sound)
    print("Number Likes: %s" % number_likes)
    print("Number Comments: %s" % number_comments)
    print("Number Bookmarks: %s" % number_bookmarks)
    print("Upload Date: %s" % upload_date)

    input("Press Enter to Stop")
    browser.close()