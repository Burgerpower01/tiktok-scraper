import asyncio
import time
import csv
import json
import os
from playwright.async_api import async_playwright, Page
from pathlib import Path

# Einstellungen für grundlegende Funktionen
do_screenshots = True
do_debbuging = False
load_time = 1 # How long to wait in seconds for video to load

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
use_video_length = True

time_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
if not os.path.exists("./out/"): os.mkdir("./out/")
csv_filename = "./out/%s_data.csv" % (time_str)
cookie_filename = "./cookies.json"

if do_screenshots:
    if not os.path.exists("./out/screenshots/"): os.mkdir("./out/screenshots/")
    if not os.path.exists("./out/screenshots/%s" % time_str): os.mkdir("./out/screenshots/%s" % time_str)


# Grundlegende Funktion zum suchen von bestimmten Tags
async def get_content(tag, search, page: Page):
    data = await page.query_selector('%s[data-e2e="%s"]' % (tag, search))
    if data:
        data_text = await data.text_content()
        if data_text.strip() != "":
            return data_text
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


async def get_content_v2(tag, search, page: Page):
    time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector('%s[class="%s"]' % (tag, search))
    if data:
        data_text = await data.text_content()
        if data_text.strip() != "":
            return data_text
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


# Funktion gibt URL von dem aktuellen Video aus
async def get_video_url(page: Page):
    result = await get_content("p", "browse-video-link", page)
    if result == "":
        return "" 
    return result.split("?")[0].replace(",", "")


# Funktion gibt den Username des Authors von dem aktuellen Video aus
async def get_username(page: Page):
    result = await get_content("span", "browse-username", page)
    return result.replace(",", "")


# Funktion gibt den Nickname des Authors von dem aktuellen Video aus
async def get_nickname(page: Page):
    result = await get_content("span", "browser-nickname", page)
    if result == "":
        return "" 
    return result.split("·")[0].replace(",", "")


# Funktion gibt die Beschreibung von dem aktuellen Video aus
async def get_video_caption(page: Page):
    result = await get_content("div", "browse-video-desc", page)
    return result.replace(",", "")


# Funktion gibt den namen des Sounds von dem aktuellen Video aus
async def get_video_sound(page: Page):
    result = await get_content("h4", "browse-music", page)
    return result.replace(",", "")


# Funktion gibt Anzahl der Likes von dem aktuellen Video aus
async def get_number_likes(page: Page):
    result = await get_content("strong", "browse-like-count", page)
    return result.replace(",", "")


# Funktion gibt Anzahl der Kommentare von dem aktuellen Video aus
async def get_number_comments(page: Page):
    result = await get_content("strong", "browse-comment-count", page)
    return result.replace(",", "")


# Funktion gibt Anzahl der Lesezeichen von dem aktuellen Video aus
async def get_number_bookmarks(page: Page):
    result = await get_content("strong", "undefined-count", page)
    return result.replace(",", "")


async def get_upload_date(page: Page):
    result = await get_content("span", "browser-nickname", page)
    if result == "":
        return "" 
    return result.split(" · ")[1].replace(",", "")

async def get_video_length(page: Page):
    result = await get_content_v2("div", "css-o2z5xv-DivSeekBarTimeContainer e1rpry1m1", page)
    if result == "":
        return ""
    return result.strip().split("/")[1]


async def listener_button_next_click(page: Page):

    async def on_button_next_click():
        write_csv(await fetch_data(page))

    await page.expose_function("onButtonClick", on_button_next_click)
    await page.evaluate("""() => {
                        const button = document.querySelector('button[data-e2e="arrow-right"]');
                        if (button) {
                            button.addEventListener('click', () => window.onButtonClick());
                        }
                    }""")
    

async def fetch_data(page: Page):
    
    # timestamp = time.time()
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    data_dict = { 'timestamp': timestamp } 

    for fieldname in get_csv_fieldnames():
        if fieldname == "video_url": 
            data_dict["video_url"] = await get_video_url(page)

        if fieldname == "username": 
            data_dict["username"] = await get_username(page)

        if fieldname == "nickname": 
            data_dict["nickname"] = await get_nickname(page)

        if fieldname == "video_caption": 
            data_dict["video_caption"] = await get_video_caption(page)

        if fieldname == "video_sound": 
            data_dict["video_sound"] = await get_video_sound(page)

        if fieldname == "number_likes": 
            data_dict["number_likes"] = await get_number_likes(page)

        if fieldname == "number_comments": 
            data_dict["number_comments"] = await get_number_comments(page)

        if fieldname == "number_bookmarks": 
            data_dict["number_bookmarks"] = await get_number_bookmarks(page)

        if fieldname == "upload_date": 
            data_dict["upload_date"] = await get_upload_date(page)

        if fieldname == "video_length":
            data_dict["video_length"] = await get_video_length(page)

    if do_debbuging:
        print(data_dict)
        print("")

    if do_screenshots:
        await page.screenshot(path="./out/screenshots/%s/%s_screenshot.png" % (time_str, timestamp))

    return data_dict
    

def get_csv_fieldnames():
    fieldnames = ['timestamp']

    if use_url: fieldnames.append('video_url')
    if use_username: fieldnames.append('username')
    if use_nickname: fieldnames.append('nickname')
    if use_video_caption: fieldnames.append('video_caption')
    if use_video_sound: fieldnames.append('video_sound')
    if use_number_likes: fieldnames.append('number_likes')
    if use_number_comments: fieldnames.append('number_comments')
    if use_number_bookmarks: fieldnames.append('number_bookmarks')
    if use_upload_date: fieldnames.append('upload_date')
    if use_video_length: fieldnames.append('video_length')

    return fieldnames


def write_csv(data_dict):
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=get_csv_fieldnames())
        writer.writerow(data_dict)


async def save_cookies(page: Page):
    cookies = await page.context.cookies()
    Path(cookie_filename).write_text(json.dumps(cookies))
    

async def restore_cookies(page: Page):
    await page.context.add_cookies(json.loads(Path(cookie_filename).read_text()))


async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=False)
        page = await browser.new_page()

        # Restore Cookies with login etc.
        if os.path.exists(cookie_filename):
            await restore_cookies(page)
            print("Login Data has been restored.")

        await page.goto("https://tiktok.com")

        # Schreibe CSV Header
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=get_csv_fieldnames())
            writer.writeheader()

        # Warte, bis der nutzer Enter drückt
        input("Drücke auf Enter sobald du bereit bist.")

        # Save cookies if not already saved
        if not os.path.exists(cookie_filename):
            await save_cookies(page)
            print("Login Data has been saved.")

        write_csv(await fetch_data(page))
        await listener_button_next_click(page)

        try:
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print("Exiting...")
        finally:
            await page.close()
            await browser.close()


asyncio.run(main())