
import asyncio
import time
from functools import partial, wraps

import aiohttp
from num2words import num2words
from pyrogram import filters, emoji
from pyrogram.types import CallbackQuery, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..main import Assistant

command = partial(filters.command, prefixes=list("#!"))

async def reply_and_delete(message: Message, text: str):
    await asyncio.gather(
        message.delete(),
        message.reply(
            text,
            quote=False,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
            disable_web_page_preview=True
        )
    )


def admins_only(func):
    @wraps(func)
    async def decorator(bot: Assistant, message: Message):
        if bot.is_admin(message):
            await func(bot, message)

        await message.delete()

    decorator.admin = True

    return decorator


################################

PING_TTL = 5


@Assistant.on_message(command("ping"))
async def ping(_, message: Message):
    """Ping the assistant"""
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!** `{delta_ping * 1000:.3f} ms`")


################################


LOG = """
**حالت لاگ را فعال کنید: کد زیر را در بالای کد خود پیست کنید و دوباره کد را اجرا کنید.**

```import logging
logging.basicConfig(level=logging.INFO)```
برای گرفتن لاگ دقیق تر؛ از
`level=logging.DEBUG`
استفاده کنید.
"""

@Assistant.on_message(command("log"))
async def log(_, message: Message):
    """Enable debug logging"""
    await reply_and_delete(message, LOG)


################################


EX = """
Please, provide us a **minimal** and **reproducible** example in order to easily understand and reproduce the problem.
[How do I create a minimal, reproducible example?](https://stackoverflow.com/help/minimal-reproducible-example)
"""


@Assistant.on_message(command("ex"))
async def ex(_, message: Message):
    """Ask for minimal example"""
    await reply_and_delete(message, EX)


################################


OT = """
**گفت و گوی شما خارج از موضوع گروه میباشد.‌**

برای تست ربات ها از گروه @PyrogramTesting استفاده کنید
"""


@Assistant.on_message(command("ot"))
async def ot(_, message: Message):
    """offtopic conversation"""
    answer = OT
    await reply_and_delete(message, answer)


################################


ASK = """
**متاسفانه سوال شما قابل فهم نیست. لطفا با سناریو و مثال دیگری مشکل خود را توضیح دهید.**
[چطور سوال بهتری بپرسم؟](https://www.chetor.com/154278-%D8%AA%DA%A9%D9%86%DB%8C%DA%A9-%D8%B3%D9%88%D8%A7%D9%84-%D9%BE%D8%B1%D8%B3%DB%8C%D8%AF%D9%86/)
"""


@Assistant.on_message(command("ask"))
async def ask(_, message: Message):
    """How to ask questions"""
    await reply_and_delete(message, ASK)


################################


LEARN = "**مشکل شما به پایروگرام مربوط نمیشود. لطفا اول بر زبان پایتون مسلط شوید و سپس اقدام به مطرح کردن مشکلات خود کنید.**"


@Assistant.on_message(command("learn"))
async def learn(_, message: Message):
    """Tell to learn Python"""
    await reply_and_delete(message, LEARN)


################################


# One place for all rules, the docs.
RULES = '''
1️⃣ − رعایت ادب از مهم ترین ارکان این گروه میباشد و در صورت مشاهده، بدون اخطار  مجبور به حذف خواهیم شد.

2️⃣ − درپاسخ به سوال سایرین ، هر چند ساده و ابتدایی، اگر قصد جواب دادن دارید با صبر و حوصله اقدام به این عمل نمایید و از کنایه و توهین بپرهیزید

3️⃣ − تبلیغات در این گروه فقط در زمینه برنامه نویسی و خرید و فروش سورس کد هایی  بر پایه پایروگرام مجاز خواهد بود. پس اگر قصد خرید یا فروش دارید محتوای خود را در قالب یک پیام ارسال و در انتها کاربر را به سمت چت خصوصی جهت شروع همکاری هدایت، کنید.

4️⃣ − وظیفه ما کمک به همدیگه هست؛ مسئولیت کدی که شما میزنین و پروژه ای که انجام میدین به عهده خودتون هست.

5️⃣ − شما میتونین هر نوع ربات و سورس کدی که توسط پایروگرام نوشته شده باشه رو داخل گروه در قالب یک پیام معرفی کنین. افراد گروه میتونن استفاده کنن و یا یک بخشی از توسعه دهنده های ربات شما بشن.

6️⃣ − گروه برای فارسی زبانان هست و ملزمه که فقط فارسی صحبت کنید؛ لطف کنید از انگلیسی صحبت کردن و تا حد امکان از فینگلیش صحبت کردن خودداری کنید. اگه هر فردی خارجی حتی به اشتباه وارد گروه شد شما ملزم هستید به زبان فارسی صحبت کنید و در صورتی که حرف های شما اهمیت خاصی برای طرف مقابل داشته باشه قطعا میتونه از برنامه های ترجمه استفاده کنه.

7️⃣ - صحبت در مورد ربات تبچی - اسپمر و از این دسته ربات های مخرب ممنوعه لطفا رعایت کنید.

8️⃣ − این گروه؛ گروه رسمی پایروگرام فارسی هست؛‌ لطف کنید سوالاتتون رو فقط در مورد کتابخونه پایروگرام بپرسید‌ (‌ در غیر این صورت؛ داخل گروه محدود میشین‌) ؛ برای بحث های خارج از موضوع میتونید از گروه بین المللی @PyrogramLounge استفاده کنید.

9⃣ برای سوال پرسیدن، پیام خود را در یک متن بفرستید و تیکه تیکه نفرستید تا حجم پیام ها زیاد نشه اگر خواستید کد طولانی بفرستید از nekobin.com استفاده کنید یا عکس واضح بفرستید 
'''

RULES_INDEX = [
    '1️⃣ − رعایت ادب از مهم ترین ارکان این گروه میباشد و در صورت مشاهده، بدون اخطار  مجبور به حذف خواهیم شد.',
    '2️⃣ − درپاسخ به سوال سایرین ، هر چند ساده و ابتدایی، اگر قصد جواب دادن دارید با صبر و حوصله اقدام به این عمل نمایید و از کنایه و توهین بپرهیزید',
    '3️⃣ − تبلیغات در این گروه فقط در زمینه برنامه نویسی و خرید و فروش سورس کد هایی  بر پایه پایروگرام مجاز خواهد بود. پس اگر قصد خرید یا فروش دارید محتوای خود را در قالب یک پیام ارسال و در انتها کاربر را به سمت چت خصوصی جهت شروع همکاری هدایت، کنید.',
    '4️⃣ − وظیفه ما کمک به همدیگه هست؛ مسئولیت کدی که شما میزنین و پروژه ای که انجام میدین به عهده خودتون هست.',
    '5️⃣ − شما میتونین هر نوع ربات و سورس کدی که توسط پایروگرام نوشته شده باشه رو داخل گروه در قالب یک پیام معرفی کنین. افراد گروه میتونن استفاده کنن و یا یک بخشی از توسعه دهنده های ربات شما بشن.',
    '6️⃣ − گروه برای فارسی زبانان هست و ملزمه که فقط فارسی صحبت کنید؛ لطف کنید از انگلیسی صحبت کردن و تا حد امکان از فینگلیش صحبت کردن خودداری کنید. اگه هر فردی خارجی حتی به اشتباه وارد گروه شد شما ملزم هستید به زبان فارسی صحبت کنید و در صورتی که حرف های شما اهمیت خاصی برای طرف مقابل داشته باشه قطعا میتونه از برنامه های ترجمه استفاده کنه.',
    '7️⃣ - صحبت در مورد ربات تبچی - اددر - اسپمر و از این دسته ربات های مخرب ممنوعه لطفا رعایت کنید.',
    '8️⃣ − این گروه؛ گروه رسمی پایروگرام فارسی هست؛‌ لطف کنید سوالاتتون رو فقط در مورد کتابخونه پایروگرام بپرسید‌ (‌ در غیر این صورت؛ داخل گروه محدود میشین‌) ؛ برای بحث های خارج از موضوع میتونید از گروه بین المللی @PyrogramLounge استفاده کنید.',
    '9⃣ برای سوال پرسیدن، پیام خود را در یک متن بفرستید و تیکه تیکه نفرستید تا حجم پیام ها زیاد نشه اگر خواستید کد طولانی بفرستید از nekobin.com استفاده کنید یا عکس واضح بفرستید ',
]


@Assistant.on_message(command("rules"))
async def rules(_, message: Message):
    """Show Pyrogram rules"""
    try:
        index = int(message.command[1])
        text = '⚠️ متن قوانین :\n'
        text += RULES_INDEX[index - 1]
    except Exception:
        text = RULES

    await reply_and_delete(message, text)

################################

FAQ = (
    "**سوال شما در حال حاضر در قسمت سوالات رایج پاسخ داده شده است.**\n"
    "لطفا در قسمت [سوالات رایج](https://docs.pyrogram.org/faq) جستجو کنید."
)


@Assistant.on_message(command("faq"))
async def faq(_, message: Message):
    """Answer is in the FAQ"""
    await reply_and_delete(message, FAQ)


################################


RTD = "لطفا؛ داکیومنت را مطالعه کنید : https://docs.pyrogram.org"


@Assistant.on_message(command("rtd"))
async def rtd(_, message: Message):
    """Tell to RTD (gentle)"""
    await reply_and_delete(message, RTD)


################################


FMT = (
    "لطفا کد خود را با استفاده از بک-تیک ارسال کنید تا خوانایی بیشتری داشته باشد..\n"
    "<code>```your code here```</code>"
)


@Assistant.on_message(command("fmt"))
@admins_only
async def fmt(_, message: Message):
    """Tell to format code"""
    await asyncio.gather(
        message.delete(),
        message.reply(
            FMT,
            quote=False,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
        )
    )

################################

EVIL = '''
✨ پایروگرام ابزاری متن باز - رایگان و تحت نظر انجمن است.
این به این معناست که شما میتوانید هرگونه استفاده ای از این ابزار را داشته باشید.
اما راهنمایی های افراد به شما یک مزیت برای شماست و کسی مکلف به کمک کردن به شما نیست؛
به خصوص اگر میخواهید رفتار درستی نشان ندهید و یا آسیبی به تلگرام و کاربر ها برسانید.
'''

@Assistant.on_message(command("evil"))
async def evil(_, message: Message):
    """No help for evil actions"""
    await reply_and_delete(message, EVIL)

################################

@Assistant.on_message(command("up"))
async def up(bot: Assistant, message: Message):
    """Show Assistant's uptime"""
    uptime = time.monotonic_ns() - bot.uptime_reference

    us, ns = divmod(uptime, 1000)
    ms, us = divmod(us, 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    try:
        arg = message.command[1]
    except IndexError:
        await reply_and_delete(message, f"**Uptime**: `{d}d {h}h {m}m {s}s`")
    else:
        if arg == "-v":
            await reply_and_delete(
                message,
                f"**Uptime**: `{d}d {h}h {m}m {s}s {ms}ms {us}μs {ns}ns`\n"
                f"**Since**: `{bot.start_datetime} UTC`"
            )
        elif arg == "-p":
            await reply_and_delete(
                message,
                f"**Uptime**: "
                f"`{num2words(d)} days, {num2words(h)} hours, {num2words(m)} minutes, "
                f"{num2words(s)} seconds, {num2words(ms)} milliseconds, "
                f"{num2words(us)} microseconds, {num2words(ns)} nanoseconds`\n"
                f""
                f"**Since**: `year {num2words(bot.start_datetime.year)}, "
                f"month {bot.start_datetime.strftime('%B').lower()}, day {num2words(bot.start_datetime.day)}, "
                f"hour {num2words(bot.start_datetime.hour)}, minute {num2words(bot.start_datetime.minute)}, "
                f"second {num2words(bot.start_datetime.second)}, "
                f"microsecond {num2words(bot.start_datetime.microsecond)}, Coordinated Universal Time`"
            )
        else:
            await message.delete()


################################

nl = "\n"

HELP = f"""
**دستورات قابل استفاده‌ :**
```
ping
log
ex
ask
learn
rules
faq
rtd
fmt
evil
up
```
"""

@Assistant.on_message(command("help") & filters.private)
async def help(bot: Assistant, message: Message):
    """Show this message"""
    await asyncio.gather(
        message.delete(),
        message.reply(
            HELP,
            quote=False,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
            )
    )
