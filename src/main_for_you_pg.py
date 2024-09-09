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
load_time = 3 # How long to wait in seconds for video to load

# Einstellungen, welche Daten berücksichtigt werden sollen
use_url = False
use_username = True
use_nickname = False
use_video_caption = True
use_video_sound = False
use_number_likes = True
use_number_comments = True
use_number_bookmarks = True
use_upload_date = False
use_video_length = False

time_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
if not os.path.exists("./out/"): os.mkdir("./out/")
csv_filename = "./out/%s_data.csv" % (time_str)
cookie_filename = "./cookies.json"

data_list_length = 0

if do_screenshots:
    if not os.path.exists("./out/screenshots/"): os.mkdir("./out/screenshots/")
    if not os.path.exists("./out/screenshots/%s" % time_str): os.mkdir("./out/screenshots/%s" % time_str)


# Grundlegende Funktion zum suchen von bestimmten Tags anhand von 'data-e2e='
async def get_content_by_data_e2e(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector('%s[data-e2e="%s"]' % (tag, search))
    if data:
        data_text = await data.text_content()
        if data_text.strip() != "":
            return data_text
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


# Grundlegende Funktion zum suchen von bestimmten Tags anhand von 'data-e2e='
async def get_all_content_by_data_e2e(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector_all('%s[data-e2e="%s"]' % (tag, search))
    data_text_list = []
    if data:
        for item in data:
            decoded_item = await item.text_content()
            if decoded_item.strip() == "":
                print("[Warning] Missing %s in <%s>" % (search, tag))

            data_text_list.append(decoded_item)

        return data_text_list

    print("[Error] No %s in <%s> does exist. Consider turning it off in the script" % (search, tag))
    return []

# Grundlegende Funktion zum suchen von bestimmten Tags anhand von 'class='
async def get_content_by_class(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector('%s[class="%s"]' % (tag, search))
    if data:
        data_text = await data.text_content()
        if data_text.strip() != "":
            return data_text
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


# 
async def get_all_content_by_class(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector_all('%s[class="%s"]' % (tag, search))
    data_text_list = []
    if data:
        for item in data:
            decoded_item = await item.text_content()
            if decoded_item.strip() == "":
                print("[Warning] Missing %s in <%s>" % (search, tag))

            data_text_list.append(decoded_item)

        return data_text_list

    print("[Error] No %s in <%s> does exist. Consider turning it off in the script" % (search, tag))
    return []


# Grundlegende Funktion zum suchen von bestimmten Tags anhand von 'id='
async def get_content_by_class(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector('%s[id="%s"]' % (tag, search))
    if data:
        data_text = await data.text_content()
        if data_text.strip() != "":
            return data_text
    print("Content für '%s' konnte in einem %s-Tag nicht gefunden werden." % (search, tag))
    return ""


# 
async def get_all_content_by_class(tag, search, page: Page):
    # time.sleep(load_time) # Wait 1s for video to load
    data = await page.query_selector_all('%s[id="%s"]' % (tag, search))
    data_text_list = []
    if data:
        for item in data:
            decoded_item = await item.text_content()
            if decoded_item.strip() == "":
                print("[Warning] Missing %s in <%s>" % (search, tag))

            data_text_list.append(decoded_item)

        return data_text_list

    print("[Error] No %s in <%s> does exist. Consider turning it off in the script" % (search, tag))
    return []

### ------------------------------------------------------------------------

# # Funktion gibt URL von dem aktuellen Video aus NEU
# async def get_video_url(page: Page):
#     result = await get_content_by_data_e2e("span", "share-icon", page)
#     if result == "":
#         return "" 
#     return result.split("?")[0].replace(",", "")


# # Funktion gibt den Username des Authors von dem aktuellen Video aus NEU
# async def get_username(page: Page):
#     result = await get_content_by_data_e2e("h3", "video-author-uniqueid", page)
#     return result.replace(",", "")


# # Funktion gibt den Nickname des Authors von dem aktuellen Video aus NEU
# async def get_nickname(page: Page):
#     result = await get_content_by_data_e2e("a", "user-card-username", page)
#     if result == "":
#         return "" 
#     return result.split("·")[0].replace(",", "")


# # Funktion gibt die Beschreibung von dem aktuellen Video aus NEU
# async def get_video_caption(page: Page):
#     result = await get_content_by_data_e2e("div", "video-desc", page)
#     return result.replace(",", "")


# # Funktion gibt den namen des Sounds von dem aktuellen Video aus NEU
# async def get_video_sound(page: Page):
#     result = await get_content_by_data_e2e("div", "css-pvx3oa-DivMusicText epjbyn3", page)
#     return result.replace(",", "")


# # Funktion gibt Anzahl der Likes von dem aktuellen Video aus NEU
# async def get_number_likes(page: Page):
#     result = await get_content_by_data_e2e("strong", "like-count", page)
#     return result.replace(",", "")


# # Funktion gibt Anzahl der Kommentare von dem aktuellen Video aus NEU
# async def get_number_comments(page: Page):
#     result = await get_content_by_data_e2e("strong", "comment-count", page)
#     return result.replace(",", "")


# # Funktion gibt Anzahl der Lesezeichen von dem aktuellen Video aus NEU
# async def get_number_bookmarks(page: Page):
#     result = await get_content_by_data_e2e("strong", "undefined-count", page)
#     return result.replace(",", "")

# # upload-date auch nicht zu finden --> egal
# async def get_upload_date(page: Page):
#     result = await get_content_by_data_e2e("span", "user-card-username", page)
#     if result == "":
#         return "" 
#     return result.split(" · ")[1].replace(",", "")

# # Length --> schwierig; nur relative/verbleibende Zeit --> egal
# async def get_video_length(page: Page):
#     result = await get_content_by_class("div", "css-o2z5xv-DivSeekBarTimeContainer e1rpry1m1", page)
#     if result == "":
#         return ""
#     return result.strip().split("/")[1]


### ------------------------------------------------------------------------

async def get_video_url_all(page: Page):
    result = await get_all_content_by_data_e2e("span", "share-icon", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.split("?")[0].replace(",", ""))
    return filtered_result


async def get_username_all(page: Page):
    print("Getting username...")
    result = await get_all_content_by_data_e2e("h3", "video-author-uniqueid", page)
    filtered_result = []
    for item in result:
        if item == "":
            print("DEBUG\n")
            print(item)
            filtered_result.append(item)
            continue
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_nickname_all(page: Page):
    result = await get_all_content_by_data_e2e("a", "user-card-username", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.split("·")[0].replace(",", ""))
    return filtered_result


async def get_video_caption_all(page: Page):
    print("Getting video_caption...")
    result = await get_all_content_by_data_e2e("div", "video-desc", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_video_sound_all(page: Page):
    result = await get_all_content_by_data_e2e("div", "css-pvx3oa-DivMusicText epjbyn3", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_number_likes_all(page: Page):
    print("Getting Likes...")
    result = await get_all_content_by_data_e2e("strong", "like-count", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_number_comments_all(page: Page):
    print("Getting Number Comments...")
    result = await get_all_content_by_data_e2e("strong", "comment-count", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_number_bookmarks_all(page: Page):
    print("Getting Bookmarks...")
    result = await get_all_content_by_data_e2e("strong", "undefined-count", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        print("Appending %s" % item)
        filtered_result.append(item.replace(",", ""))
    return filtered_result


async def get_upload_date_all(page: Page):
    result = await get_all_content_by_data_e2e("span", "user-card-username", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.split(" · ")[1].replace(",", ""))
    return filtered_result


async def get_video_length_all(page: Page):
    result = await get_all_content_by_class("div", "css-o2z5xv-DivSeekBarTimeContainer e1rpry1m1", page)
    filtered_result = []
    for item in result:
        if item == "":
            filtered_result.append(item)
            continue
        filtered_result.append(item.strip().split("/")[1])
    return filtered_result


# Funktion, die ausgeführt wird wenn man die Pfeiltaste nach unten auf der Tastatur drückt 
async def listener_arrow_down_pressed(page: Page):

    async def on_arrow_down_pressed():
        write_csv_block(await fetch_data_block(page))

    await page.expose_function("onArrowPressed", on_arrow_down_pressed)
    await page.evaluate("""() => {
                            window.addEventListener("keydown", () => { onArrowPressed(); })
                        }""")
    

# Funktion, die alle Informationen in einem "Packet" speichert
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


async def fetch_data_block(page: Page):
    timestamp = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

    time.sleep(load_time)

    temp_list_length = 0
    valid_list_length = True
    list_video_url = []
    list_username = []
    list_nickname = []
    list_video_caption = []
    list_video_sound = []
    list_number_likes = []
    list_number_comments = []
    list_bookmarks = []
    list_upload_date = []
    list_video_length = []

    data_dict_block = []

    for fieldname in get_csv_fieldnames():
        if fieldname == "video_url": 
            list_video_url = await get_video_url_all(page)
            list_len = len(list_video_url)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Video URL List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "username": 
            list_username = await get_username_all(page)
            list_len = len(list_username)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Username List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "nickname": 
            list_nickname = await get_nickname_all(page)
            list_len = len(list_nickname)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Nickname List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "video_caption": 
            list_video_caption = await get_video_caption_all(page)
            list_len = len(list_video_caption)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Video Caption List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "video_sound": 
            list_video_sound = await get_video_sound_all(page)
            list_len = len(list_video_sound)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Video Sound List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "number_likes": 
            list_number_likes = await get_number_likes_all(page)
            list_len = len(list_number_likes)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Number Like List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "number_comments": 
            list_number_comments = await get_number_comments_all(page)
            list_len = len(list_number_comments)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Number Comments List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "number_bookmarks": 
            list_bookmarks = await get_number_bookmarks_all(page)
            list_len = len(list_bookmarks)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Bookmarks List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "upload_date": 
            list_upload_date = await get_upload_date_all(page)
            list_len = len(list_upload_date)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Upload Date List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

        if fieldname == "video_length":
            list_video_length = await get_video_length_all(page)
            list_len = len(list_video_length)
            if temp_list_length == 0 and list_len != 0:
                temp_list_length = list_len
            elif temp_list_length != list_len:
                print("[Error] Video Length List has an unexpected length=%d/%d! This could result in false data" % (list_len, temp_list_length))
                valid_list_length = False

    if not valid_list_length:
        exit(1)
        return {}

    for i in range(temp_list_length):
        data_dict = { 'timestamp': timestamp } 

        if list_video_url != []:
            data_dict["video_url"] = list_video_url[i]

        if list_username != []:
            data_dict["username"] = list_username[i]

        if list_nickname != []:
            data_dict["nickname"] = list_nickname[i]

        if list_video_caption != []:
            data_dict["video_caption"] = list_video_caption[i]

        if list_video_sound != []:
            data_dict["video_sound"] = list_video_sound[i]

        if list_number_likes != []:
            data_dict["number_likes"] = list_number_likes[i]

        if list_number_comments != []:
            data_dict["number_comments"] = list_number_comments[i]

        if list_bookmarks != []:
            data_dict["number_bookmarks"] = list_bookmarks[i]

        if list_upload_date != []:
            data_dict["upload_date"] = list_upload_date[i]

        if list_video_length != []:
            data_dict["video_length"] = list_video_length[i]

        data_dict_block.append(data_dict)

    return data_dict_block


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


def write_csv_block(data_dict_block):
    block_length = len(data_dict_block)

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=get_csv_fieldnames())
        writer.writeheader()

        for data_dict in data_dict_block:
            writer.writerow(data_dict)

    print("BLOCK WRITTEN - %d Entries saved" % block_length)


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


        # Warte, bis der nutzer Enter drückt
        input("Drücke auf Enter sobald du bereit bist.")

        # Save cookies if not already saved
        if not os.path.exists(cookie_filename):
            await save_cookies(page)
            print("Login Data has been saved.")

        # Schreibe erste Zeile von der CSV mit den Feldnamen
        # write_csv(await fetch_data(page))

        # Regestriere dich auf den "Weiter" Knopf, damit das Programm weiß, wann er gedrückt wird
        await listener_arrow_down_pressed(page)

        # Ab da dreht sich das Programm und reagriert immer auf den "Weiter" Button
        try:
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print("Exiting...")
        finally:
            await page.close()
            await browser.close()


asyncio.run(main())
