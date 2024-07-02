import asyncio
import time
from playwright.async_api import async_playwright, Page

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
async def get_content(tag, search, page: Page):
    data = await page.query_selector('%s[data-e2e="%s"]' % (tag, search))
    if data:
        return await data.text_content()
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


# Funktion gibt URL von dem aktuellen Video aus
async def get_video_url(page: Page):
    result = await get_content("p", "browse-video-link", page)
    if result == "":
        return "" 
    return result.split("?")[0]


# Funktion gibt den Username des Authors von dem aktuellen Video aus
async def get_username(page: Page):
    return await get_content("span", "browse-username", page)


# Funktion gibt den Nickname des Authors von dem aktuellen Video aus
async def get_nickname(page: Page):
    result = await get_content("span", "browser-nickname", page)
    if result == "":
        return "" 
    return result.split("·")[0]


# Funktion gibt die Beschreibung von dem aktuellen Video aus
async def get_video_caption(page: Page):
    return await get_content("div", "browse-video-desc", page)


# Funktion gibt den namen des Sounds von dem aktuellen Video aus
async def get_video_sound(page: Page):
    return await get_content("h4", "browse-music", page)


# Funktion gibt Anzahl der Likes von dem aktuellen Video aus
async def get_number_likes(page: Page):
    return await get_content("strong", "browse-like-count", page)


# Funktion gibt Anzahl der Kommentare von dem aktuellen Video aus
async def get_number_comments(page: Page):
    return await get_content("strong", "browse-comment-count", page)


# Funktion gibt Anzahl der Lesezeichen von dem aktuellen Video aus
async def get_number_bookmarks(page: Page):
    return await get_content("strong", "undefined-count", page)


async def get_upload_date(page: Page):
    result = await get_content("span", "browser-nickname", page)
    if result == "":
        return "" 
    return result.split(" · ")[1]


async def listener_button_next_click(page: Page):

    async def on_button_next_click():
        await fetch_data(page)

    await page.expose_function("onButtonClick", on_button_next_click)
    await page.evaluate("""() => {
                        const button = document.querySelector('button[data-e2e="arrow-right"]');
                        if (button) {
                            button.addEventListener('click', () => window.onButtonClick());
                        }
                    }""")
    

async def fetch_data(page: Page):
    timestamp = time.time()
    video_url = await get_video_url(page)
    username = await get_username(page)
    nickname = await get_nickname(page)
    video_caption = await get_video_caption(page)
    video_sound = await get_video_sound(page)
    number_likes = await get_number_likes(page)
    number_comments = await get_number_comments(page)
    number_bookmarks = await get_number_bookmarks(page)
    upload_date = await get_upload_date(page)

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
    print("")


async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://tiktok.com")

        input("Drücke auf Enter sobald du bereit bist.")

        await fetch_data(page)
        await listener_button_next_click(page)

        try:
            while True:
                await asyncio.sleep(1)  # Asynchronously sleep to keep the event loop running
        except Exception as e:
            print("Exiting...")
        finally:
            await browser.close()


asyncio.run(main())