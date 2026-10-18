import os
import random
import threading
from flask import Flask
import discord
from discord.ext import commands

# --- خادم وهمي لإرضاء منصة Render ---
app = Flask('')

@app.route('/')
def home():
    return "Sanad Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()
# -----------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {bot.user}')

# قائمة الألعاب والفعاليات
@bot.command(name='العاب')
async def games_menu(ctx):
    embed = discord.Embed(
        title="🎮 ألعاب وفعاليات سند",
        description="تحدّ البوت أو جرب الفعاليات مع أصحابك! اكتب الأمر الموضح للبدء:",
        color=discord.Color.gold()
    )

    games_list = (
        "• `-روليت` : لعبة الروليت 🎰\n"
        "• `-حجر` أو `-ورقة` أو `-مقص` : حجر ورقة مقص ✂️\n"
        "• `-خمن` : لعبة تخمين الرقم من 1 إلى 10 🎯\n"
        "• `-سؤال` : سؤال عشوائي ❓\n"
        "• `-نسبة @عضو` : نسبة التوافق/الحب 💘\n"
        "• `-عملة` : ملك أم كتابة 🪙\n"
        "• `-نرد` : رمي النرد 🎲"
    )

    embed.add_field(name="🎲 الألعاب المتاحة:", value=games_list, inline=False)
    embed.set_footer(text="سند - خويك في الفعاليات 🚀")
    await ctx.send(embed=embed)

# 1. لعبة الروليت
@bot.command(name='روليت')
async def roulette(ctx):
    outcomes = [
        "💥 **بوووم!** طاحت الرصاصة عليك وحدك الخسران! (اختر عقاب لنفسك 😈)",
        "🛡️ **نجوت!** المسدس كان فاضي، دور الشخص اللي بعدك.",
        "✨ **حظك قوي!** نجوت وشردت من العقاب.",
        "💀 **طلقتين مو واحدة!** اختر عقابين أو نفذ طلب للشباب في السيرفر."
    ]
    await ctx.send(f"🎰 **تلف الروليت...**\n{random.choice(outcomes)}")

# 2. لعبة حجر ورقة مقص
@bot.command(name='حجر')
async def rps_rock(ctx):
    await play_rps(ctx, 'حجر')

@bot.command(name='ورقة')
async def rps_paper(ctx):
    await play_rps(ctx, 'ورقة')

@bot.command(name='مقص')
async def rps_scissors(ctx):
    await play_rps(ctx, 'مقص')

async def play_rps(ctx, user_choice):
    options = ['حجر', 'ورقة', 'مقص']
    bot_choice = random.choice(options)
    
    if user_choice == bot_choice:
        result = f"🤝 **تعادل!** كلينا اخترنا `{bot_choice}`"
    elif (user_choice == 'حجر' and bot_choice == 'مقص') or \
         (user_choice == 'ورقة' and bot_choice == 'حجر') or \
         (user_choice == 'مقص' and bot_choice == 'ورقة'):
        result = f"🎉 **كفووو فزت علي!** أنت اخترت `{user_choice}` وأنا اخترت `{bot_choice}`"
    else:
        result = f"😈 **هاردلك أنا فزت عليك!** أنت اخترت `{user_choice}` وأنا اخترت `{bot_choice}`"

    await ctx.send(result)

# 3. تخمين الرقم
@bot.command(name='خمن')
async def guess_number(ctx):
    secret_num = random.randint(1, 10)
    await ctx.send("🎯 **تحدي التخمين!** فكرت في رقم من **1 إلى 10**.\nاكتب: `-رقم [رقمك]`")
    bot.secret_number = secret_num

@bot.command(name='رقم')
async def check_guess(ctx, number: int):
    if not hasattr(bot, 'secret_number'):
        await ctx.send("❌ اكتب `-خمن` أولاً لتبدأ اللعبة!")
        return

    if number == bot.secret_number:
        await ctx.send(f"🎯 **صح عليك بطل!** الرقم الصحيح كان `{bot.secret_number}`")
        del bot.secret_number
    elif number < bot.secret_number:
        await ctx.send("⬆️ الرقم أكبر من كذا!")
    else:
        await ctx.send("⬇️ الرقم أصغر من كذا!")

# 4. أسئلة فعاليات
@bot.command(name='سؤال')
async def ask_question(ctx):
    questions = [
        "لو يعطونك مليون دولار وترترك ألعاب الفيديو لمدة سنة، توافق؟",
        "وش أكثر لعبة ندّمت إنك اشتريتها؟",
        "لو تقدر تعيش داخل عالم لعبة واحدة، وش تختار؟",
        "مين أكثر شخص تحب تلعب معاه في السيرفر؟",
        "وش أول لعبة تختيم ختمتها في حياتك؟"
    ]
    await ctx.send(f"❓ **سؤال الفعالية:** {random.choice(questions)}")

# 5. نسبة التوافق
@bot.command(name='نسبة')
async def love_percentage(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("❌ يرجى منشن الشخص! مثال: `-نسبة @اسم_العضو`")
        return
    percentage = random.randint(0, 100)
    await ctx.send(f"💘 نسبة التوافق بين **{ctx.author.display_name}** و **{member.display_name}** هي: **{percentage}%**!")

# 6. عملة ونرد
@bot.command(name='عملة')
async def flip_coin(ctx):
    await ctx.send(f"🪙 النتيجة هي: **{random.choice(['ملك 👑', 'كتابة 📝'])}**")

@bot.command(name='نرد')
async def roll_dice(ctx):
    await ctx.send(f"🎲 طلع لك الرقم: **{random.randint(1, 6)}**")

# تشغيل الخادم والبوت
keep_alive()
bot.run(os.environ.get("TOKEN"))
