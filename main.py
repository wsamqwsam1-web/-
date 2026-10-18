import discord
from discord.ext import commands
from discord.ui import Button, View
import random

# ================= ================= =================
# ⚙️ الإعدادات الأساسية (قم بتعديل هذه القيم)
# ================= ================= =================
WELCOME_CHANNEL_ID = 1560593133908262912  # 🔴 ضع هنا ID روم الترحيب
TICKET_CATEGORY_ID = 1560871031961427998  # 🔴 ضع هنا ID الكاتيجوري التي تفتح فيها التذاكر

# ================= ================= =================
# 🚀 تهيئة البوت
# ================= ================= =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قاعدة بيانات بسيطة للمستويات (تُحفظ أثناء تشغيل البوت)
user_levels = {}

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول بنجاح باسم: {bot.user.name}")
    print("🚀 جميع الأنظمة (الترحيب، اللفل، الألعاب، التذاكر، الردود) شغالين بنجاح!")


# ================= ================= =================
# 1️⃣ نظام الترحيب التلقائي (Welcome System)
# ================= ================= =================
@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🎉 أهلاً وسهلاً بك في السيرفر!",
            description=f"أنرت السيرفر يا {member.mention} 💙\nنتمنى لك وقتاً ممتعاً معنا!",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="👥 عدد الأعضاء الآن:", value=f"{member.guild.member_count} عضو", inline=False)
        embed.set_footer(text="نتمنى لك تجربة رائعة!")

        await channel.send(embed=embed)


# ================= ================= =================
# 2️⃣ نظام اللفل والرد التلقائي (Leveling & Auto-Response)
# ================= ================= =================
@bot.event
async def on_message(message):
    # تجنب رد البوت على نفسه
    if message.author.bot:
        return

    user_id = message.author.id

    # --- زيادة نقاط الـ XP والمستوى ---
    if user_id not in user_levels:
        user_levels[user_id] = {"xp": 0, "level": 1}

    user_levels[user_id]["xp"] += 10
    xp_needed = user_levels[user_id]["level"] * 100

    # الترقية لمستوى جديد
    if user_levels[user_id]["xp"] >= xp_needed:
        user_levels[user_id]["level"] += 1
        user_levels[user_id]["xp"] = 0
        new_lvl = user_levels[user_id]["level"]
        await message.channel.send(f"🎉 مبروك يا {message.author.mention}! ارتقيت إلى **المستوى {new_lvl}** 🏆")

    # --- نظام الرد التلقائي (Auto-Response) ---
    msg_content = message.content.lower()

    if msg_content in ["السلام عليكم", "السلام عليكم ورحمة الله", "سلام عليكم"]:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا {message.author.mention} 🌹")
    elif msg_content == "الاسعار":
        await message.channel.send("💰 **الباقات المتوفرة:**\n• الباقة العادية: 50 SAR\n• الباقة المتوسطة: 120 SAR\n• الباقة الاحترافية: 300 SAR")
    elif msg_content == "مساعدة":
        await message.channel.send("🛠️ للحصول على مساعدة افتح تذكرة عبر كود التذاكر `!setup_ticket`!")

    # معالجة بقية الأوامر البرمجية
    await bot.process_commands(message)


# امر لعرض لفل المستخدم
@bot.command()
async def level(ctx, member: discord.Member = None):
    target = member or ctx.author
    user_data = user_levels.get(target.id, {"xp": 0, "level": 1})

    embed = discord.Embed(title=f"📊 مستوى {target.display_name}", color=discord.Color.gold())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="المستوى الحالي (Level):", value=f"⭐ {user_data['level']}", inline=True)
    embed.add_field(name="النقاط الحالية (XP):", value=f"✨ {user_data['xp']} / {user_data['level'] * 100}", inline=True)

    await ctx.send(embed=embed)


# ================= ================= =================
# 3️⃣ نظام الألعاب (Mini-Games)
# ================= ================= =================

import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {bot.user}')

# قائمة الألعاب الشاملة (المنيو)
@bot.command(name='العاب')
async def games_menu(ctx):
    embed = discord.Embed(
        title="🎮 ألعاب وفعاليات سند",
        description="تحدّ البوت أو جرب الفعاليات مع أصحابك! اكتب الأمر الموضح للبدء:",
        color=discord.Color.gold()
    )

    games_list = (
        "• `-روليت` : لعبة الروليت (العقاب أو التحدي) 🎰\n"
        "• `-حجر` أو `-ورقة` أو `-مقص` : حجر ورقة مقص ✂️\n"
        "• `-خمن` : لعبة تخمين الرقم من 1 إلى 10 🎯\n"
        "• `-سؤال` : سؤال عشوائي للفعاليات ❓\n"
        "• `-نسبة @عضو` : نسبة التوافق/الحب بينك وبين أي شخص 💘\n"
        "• `-عملة` : رمي العملة (ملك أم كتابة) 🪙\n"
        "• `-نرد` : رمي النرد 🎲"
    )

    embed.add_field(name="🎲 الألعاب والفعاليات المتاحة:", value=games_list, inline=False)
    embed.set_footer(text="سند - خويك في الفعاليات 🚀")

    await ctx.send(embed=embed)

# 1. لعبة الروليت (Roulette)
@bot.command(name='روليت')
async def roulette(ctx):
    outcomes = [
        "💥 **بوووم!** طاحت الرصاصة عليك وحدك الخسران! (اختر عقاب لنفسك 😈)",
        "🛡️ **نجوت!** المسدس كان فاضي، دور الشخص اللي بعدك.",
        "✨ **حظك قوي!** نجوت وشردت من العقاب.",
        "💀 **طلقتين مو واحدة!** اختر عقابين أو نفذ طلب للشباب في السيرفر."
    ]
    res = random.choice(outcomes)
    await ctx.send(f"🎰 **تلف الروليت...**\n{res}")

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

# 3. لعبة تخمين الرقم
@bot.command(name='خمن')
async def guess_number(ctx):
    secret_num = random.randint(1, 10)
    await ctx.send("🎯 **تحدي التخمين!** فكرت في رقم من **1 إلى 10**.\nجرب تخمن واكتب: `-رقم [رقمك]` (مثال: `-رقم 5`)")
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
        await ctx.send("⬆️ الرقم أكبر من كذا! حاول مرة ثانية.")
    else:
        await ctx.send("⬇️ الرقم أصغر من كذا! حاول مرة ثانية.")

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
    q = random.choice(questions)
    await ctx.send(f"❓ **سؤال الفعالية:** {q}")

# 5. نسبة التوافق / الحب
@bot.command(name='نسبة')
async def love_percentage(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("❌ يرجى منشن الشخص! مثال: `-نسبة @اسم_العضو`")
        return
    
    percentage = random.randint(0, 100)
    await ctx.send(f"💘 نسبة التوافق بين **{ctx.author.display_name}** و **{member.display_name}** هي: **{percentage}%**!")

# 6. رمي العملة والنرد
@bot.command(name='عملة')
async def flip_coin(ctx):
    res = random.choice(['ملك 👑', 'كتابة 📝'])
    await ctx.send(f"🪙 النتيجة هي: **{res}**")

@bot.command(name='نرد')
async def roll_dice(ctx):
    num = random.randint(1, 6)
    await ctx.send(f"🎲 طلع لك الرقم: **{num}**")

bot.run(os.environ.get("TOKEN"))

# ================= ================= =================
# 4️⃣ نظام التذاكر والتواضل (Ticket System)
# ================= ================= =================

# واجهة الزر لتشغيل التذكرة
# ================= ================= =================
# 4️⃣ نظام التذاكر والتواصل (Ticket System - محسّن)
# ================= ================= =================

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 فتح تذكرة دعم", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild

        # 1. الرد الفوري على التفاعل لكي لا يفشل الزر
        await interaction.response.defer(ephemeral=True)

        # 2. إعداد الصلاحيات (الرؤية فقط لصاحب التذكرة والبوت والأدمن)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        try:
            # 3. إنشاء قناة التذكرة مباشرة في السيرفر
            channel = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites=overwrites
            )

            # 4. إرسال رسالة التأكيد الخاصة للشخص
            await interaction.followup.send(f"✅ تم فتح تذكرتك بنجاح: {channel.mention}", ephemeral=True)

            # 5. إرسال محتوى التذكرة داخل الروم الجديد
            embed = discord.Embed(
                title="🎫 تذكرة جديدة",
                description=f"أهلاً بك {interaction.user.mention}، يرجى كتابة استفسارك وسيقوم فريق الدعم بالرد عليك قريباً.\n\nلإغلاق التذكرة اكتب: `!close`",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)

        except Exception as e:
            # في حال وجود خطأ في الصلاحيات يخبرك البوت بالسبب في الخاص
            await interaction.followup.send(
                f"❌ حدث خطأ أثناء إنشاء التذكرة. تأكد أن البوت يمتلك صلاحية (Manage Channels). التفاصيل: {e}",
                ephemeral=True)


# أمر نشر لوحة التذاكر (يستخدمه الأدمن)
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="🎫 مركز الدعم الفني والخدمات",
        description="اضغط على الزر أدناه لفتح تذكرة خاصة والتواصل مع الإدارة مباشرة.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())


# أمر إغلاق التذكرة
@bot.command()
async def close(ctx):
    if "ticket-" in ctx.channel.name:
        await ctx.send("🔒 سيتم إغلاق هذه التذكرة وحذف القناة خلال 3 ثوانٍ...")
        import asyncio
        await asyncio.sleep(3)
        await ctx.channel.delete()
    else:
        await ctx.send("❌ هذا الأمر يستخدم فقط داخل قنوات التذاكر!")
# ================= ================= =================
# 🔑 تشغيل البوت
# ================= ================= =================
import os

bot.run(os.environ.get("TOKEN"))
