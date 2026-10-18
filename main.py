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

# 🎮 لعبة حجرة ورقة مقص
@bot.command()
async def rps(ctx, choice: str = None):
    options = ["حجرة", "ورقة", "مقص"]
    if not choice or choice not in options:
        await ctx.send("❌ يرجى اختيار إحدى الخيارات التالية: `!rps حجرة` أو `!rps ورقة` أو `!rps مقص`")
        return

    bot_choice = random.choice(options)

    if choice == bot_choice:
        result = "🤝 تعادل!"
    elif (choice == "حجرة" and bot_choice == "مقص") or \
         (choice == "ورقة" and bot_choice == "حجرة") or \
         (choice == "مقص" and bot_choice == "ورقة"):
        result = "🎉 مبروك! أنت فزت علي!"
    else:
        result = "😈 أنا فزت عليك!"

    embed = discord.Embed(title="🎮 لعبة حجرة ورقة مقص", color=discord.Color.purple())
    embed.add_field(name="اختيارك:", value=choice, inline=True)
    embed.add_field(name="اختيار البوت:", value=bot_choice, inline=True)
    embed.add_field(name="النتيجة:", value=f"**{result}**", inline=False)

    await ctx.send(embed=embed)


# 🎲 لعبة تخمين الرقم
@bot.command()
async def guess(ctx):
    secret_number = random.randint(1, 10)
    await ctx.send("🎲 اخترت رقماً بين 1 و 10! حاول تخمينه بحساب كتابة الرقم خلال 15 ثانية:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg = await bot.wait_for('message', check=check, timeout=15.0)
        guess_num = int(msg.content)
        if guess_num == secret_number:
            await ctx.send(f"🎯 كفووو! تخمينك صحيح الرقم كان **{secret_number}**!")
        else:
            await ctx.send(f"❌ للأسف تخمين خاطئ، الرقم الصحيح كان **{secret_number}**.")
    except Exception:
        await ctx.send(f"⏱️ انتهى الوقت! الرقم الصحيح كان **{secret_number}**.")


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
TOKEN = "MTU2MDg1Njc5MzMzOTUzNTQwMw.GaHur1.gPtMqZO5GO_cF0NB86pUoYGNJP-4ttxpRxYerM"
bot.run(TOKEN)