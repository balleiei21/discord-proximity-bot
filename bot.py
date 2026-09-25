import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_USER_ID = 933529869487321161  
NEW_SERVER_NAME = "NEXORA SHOP"

# ----------------------------------------------------
# 1. ข้อมูลยศ
# ----------------------------------------------------
perm_owner = discord.Permissions.all()
perm_admin = discord.Permissions(administrator=True)

perm_staff = discord.Permissions(
    manage_messages=True, mute_members=True, deafen_members=True, move_members=True,
    view_channel=True, send_messages=True, embed_links=True, attach_files=True,
    read_message_history=True, connect=True, speak=True
)

perm_member = discord.Permissions(
    view_channel=True, send_messages=True, read_message_history=True, add_reactions=True,
    attach_files=True, connect=True, speak=True, use_voice_activation=True
)

ROLES_DATA = [
    # 👑 MANAGEMENT
    {"name": "👑・Owner", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "เจ้าของร้าน"},
    {"name": "💎・Co-Owner", "color": discord.Color.from_rgb(0, 191, 255), "permissions": perm_owner, "desc": "หุ้นส่วนร้าน"},
    {"name": "🏆・Executive", "color": discord.Color.from_rgb(148, 0, 211), "permissions": perm_admin, "desc": "ผู้บริหาร"},
    {"name": "⚜️・Manager", "color": discord.Color.from_rgb(255, 140, 0), "permissions": perm_admin, "desc": "ผู้จัดการร้าน"},

    # 🛡️ STAFF
    {"name": "🔧・Admin", "color": discord.Color.from_rgb(220, 20, 60), "permissions": perm_admin, "desc": "ผู้ดูแลระบบ"},
    {"name": "🛡️・Moderator", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_staff, "desc": "ผู้ดูแลความเรียบร้อย"},
    {"name": "🎧・Support", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ฝ่ายบริการลูกค้า"},
    {"name": "🎫・Ticket Staff", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_staff, "desc": "ทีมงานดูแล Ticket"},

    # 🎨 CREATOR TEAM
    {"name": "👕・Skin Designer", "color": discord.Color.from_rgb(255, 105, 180), "permissions": perm_staff, "desc": "ช่างทำสกิน"},
    {"name": "🧱・Map Builder", "color": discord.Color.from_rgb(139, 69, 19), "permissions": perm_staff, "desc": "ช่างทำแมพ Minecraft"},
    {"name": "⚙️・Addon Developer", "color": discord.Color.from_rgb(100, 149, 237), "permissions": perm_staff, "desc": "นักพัฒนาแอดออน"},
    {"name": "💻・Discord Developer", "color": discord.Color.from_rgb(114, 137, 218), "permissions": perm_staff, "desc": "นักพัฒนาดิสคอร์ด"},
    {"name": "🎨・Commission Artist", "color": discord.Color.from_rgb(238, 130, 238), "permissions": perm_staff, "desc": "นักวาดคอมมิชชัน"},

    # 🎮 GAME SERVICE
    {"name": "💳・Topup Staff", "color": discord.Color.from_rgb(50, 205, 50), "permissions": perm_staff, "desc": "ทีมงานเติมเกม"},
    {"name": "🤖・Roblox Service", "color": discord.Color.from_rgb(255, 69, 0), "permissions": perm_staff, "desc": "ทีมงานฟาร์ม Roblox"},
    {"name": "🔥・Free Fire Service", "color": discord.Color.from_rgb(255, 0, 0), "permissions": perm_staff, "desc": "ทีมงานดันแรงค์ Free Fire"},
    {"name": "⚔️・AOV Service", "color": discord.Color.from_rgb(30, 144, 255), "permissions": perm_staff, "desc": "ทีมงานดันแรงค์ AOV"},

    # 💎 CUSTOMER
    {"name": "👑・VIP", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_member, "desc": "ลูกค้า VIP"},
    {"name": "💎・Premium", "color": discord.Color.from_rgb(186, 85, 211), "permissions": perm_member, "desc": "ลูกค้า Premium"},
    {"name": "⭐・Customer", "color": discord.Color.from_rgb(255, 255, 0), "permissions": perm_member, "desc": "ลูกค้าประจำ"},
    {"name": "🛍️・Buyer", "color": discord.Color.from_rgb(173, 216, 230), "permissions": perm_member, "desc": "ผู้ซื้อสินค้า"},
    {"name": "👤・Member", "color": discord.Color.from_rgb(211, 211, 211), "permissions": perm_member, "desc": "สมาชิกทั่วไป"},

    # 🤖 SYSTEM
    {"name": "🤖・Bot", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "บอทในเซิร์ฟเวอร์"}
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่อง
# ----------------------------------------------------
CATEGORIES_DATA = {
    "📌 INFORMATION": {
        "text": ["꒰📢꒱・ยินดีต้อนรับ", "꒰📜꒱・กฎของร้าน", "꒰📋꒱・รายละเอียดบริการ", "꒰💳꒱・ช่องทางชำระเงิน", "꒰⭐꒱・รีวิวจากลูกค้า"],
        "voice": []
    },
    "🛒 SHOP": {
        "text": ["꒰🛍️꒱・ร้านค้า", "꒰🎮꒱・เติมเกม", "꒰💎꒱・ไอเทมเกม", "꒰🎁꒱・โปรโมชั่น"],
        "voice": []
    },
    "🎨 SERVICES": {
        "text": ["꒰👕꒱・รับทำสกิน", "꒰🧱꒱・รับทำแมพมายคราฟ", "꒰⚙️꒱・รับทำแอดออน", "꒰💻꒱・รับทำดิส", "꒰🎨꒱・รับทำคอมช", "꒰💳꒱・รับเติมเกม", "꒰🤖꒱・รับฟาร์ม Roblox", "꒰🔥꒱・รับดันแรงค์ Free Fire", "꒰⚔️꒱・รับดันแรงค์ AOV"],
        "voice": []
    },
    "📂 PORTFOLIO": {
        "text": ["꒰🖼️꒱・ผลงานสกิน", "꒰🗺️꒱・ผลงานแมพ", "꒰⚙️꒱・ผลงานแอดออน", "꒰💬꒱・ผลงานดิส", "꒰🎨꒱・ผลงานคอมช"],
        "voice": []
    },
    "🧾 CUSTOMER": {
        "text": ["꒰🎫꒱・เปิด Ticket", "꒰📦꒱・สถานะงาน", "꒰💬꒱・สอบถามบริการ", "꒰📜꒱・เครดิตลูกค้า"],
        "voice": []
    },
    "💬 COMMUNITY": {
        "text": ["꒰💬꒱・พูดคุย", "꒰🎮꒱・คุยเรื่องเกม", "꒰📸꒱・แชร์ผลงาน", "꒰🤝꒱・หาเพื่อนเล่นเกม"],
        "voice": ["🔊・ห้องคุยเล่น 1", "🔊・ห้องคุยเล่น 2"]
    },
    "🏆 CREDIT": {
        "text": ["꒰🏆꒱・เครดิตร้าน", "꒰💖꒱・ขอบคุณลูกค้า", "꒰📸꒱・ผลงานลูกค้า"],
        "voice": []
    },
    "🔒 STAFF": {
        "text": ["꒰🔧꒱・ห้องทีมงาน", "꒰📋꒱・จัดการออเดอร์", "꒰💰꒱・รายรับ", "꒰📝꒱・บันทึกงาน"],
        "voice": []
    },
    "🔐 MANAGEMENT": {
        "text": ["꒰👑꒱・ห้อง owner", "꒰💼꒱・ห้องบริหาร", "꒰📊꒱・รายงานร้าน", "꒰⚙️꒱・ตั้งค่าระบบ"],
        "voice": []
    }
}

async def safe_run(func, *args, **kwargs):
    while True:
        try:
            res = await func(*args, **kwargs)
            await asyncio.sleep(1.2) # เว้นระยะเพื่อกัน Rate Limit 429
            return res
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ติดบล็อก รอระบบปลดล็อก {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
            else:
                print(f"[API Error] {e}")
                return None
        except Exception as e:
            print(f"[Error] {e}")
            return None

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    cmd = message.content.strip()
    if cmd in ["เริ่มงาน", "เริ่มต้น"]:
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"🚀 **รับทราบคำสั่ง! กำลังเริ่มจัดสร้างเซิร์ฟเวอร์ {NEW_SERVER_NAME}...**\n*(ใช้เวลาประมาณ 2-3 นาที ระบบกำลังสร้างให้อย่างเสถียร ห้ามปิดบอท)*")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        await safe_run(guild.edit, name=NEW_SERVER_NAME)

        # 2. ลบช่องเดิมทั้งหมด
        print("--- เริ่มลบช่องเดิม ---")
        for channel in list(guild.channels):
            await safe_run(channel.delete)

        # 3. ลบยศเดิมทั้งหมด
        print("--- เริ่มลบยศเดิม ---")
        for role in list(guild.roles):
            if not role.is_default() and not role.managed:
                await safe_run(role.delete)

        # 4. สร้างยศใหม่ทั้งหมด
        print("--- เริ่มสร้างยศใหม่ ---")
        created_roles = {}
        for role_info in ROLES_DATA:
            role_obj = await safe_run(
                guild.create_role,
                name=role_info["name"],
                color=role_info["color"],
                permissions=role_info["permissions"],
                hoist=True
            )
            if role_obj:
                created_roles[role_info["name"]] = role_obj

        # ยัดยศ Owner ให้ผู้สั่ง
        r_owner = created_roles.get("👑・Owner")
        if r_owner and message.author in guild.members:
            try:
                await message.author.add_roles(r_owner)
            except:
                pass

        report_channel = None

        # 5. สร้างหมวดหมู่และช่องทั้งหมด
        print("--- เริ่มสร้างหมวดหมู่และช่อง ---")
        for cat_name, data in CATEGORIES_DATA.items():
            category = await safe_run(guild.create_category, cat_name)
            if not category:
                continue

            # สร้าง Text Channels
            for txt_name in data["text"]:
                ch = await safe_run(category.create_text_channel, txt_name)
                if ch and "บันทึกงาน" in txt_name:
                    report_channel = ch

            # สร้าง Voice Channels
            for vc_name in data["voice"]:
                await safe_run(category.create_voice_channel, vc_name)

        # 6. รายงานสรุป
        if report_channel:
            try:
                embed_finish = discord.Embed(
                    title="🎉 การตั้งค่าเซิร์ฟเวอร์เสร็จสิ้นสมบูรณ์!",
                    description=f"สร้างช่องและยศครบทุกหมวดหมู่สำหรับ **{NEW_SERVER_NAME}** เรียบร้อยแล้วครับ!",
                    color=discord.Color.green()
                )
                await safe_run(report_channel.send, embed=embed_finish)

                embed_roles = discord.Embed(
                    title="👑 รายงานยศประจำร้าน NEXORA SHOP",
                    description="รายชื่อยศทั้งหมดที่ถูกสร้างขึ้นในเซิร์ฟเวอร์:",
                    color=discord.Color.gold()
                )
                for r in ROLES_DATA:
                    embed_roles.add_field(name=r["name"], value=f"• {r['desc']}", inline=False)

                await safe_run(report_channel.send, embed=embed_roles)
            except Exception as e:
                print(f"ส่งรายงานไม่สำเร็จ: {e}")

        print("=== สร้างเซิร์ฟเวอร์เสร็จสิ้นสมบูรณ์ ===")

@bot.event
async def on_ready():
    print(f"บอท {bot.user} ออนไลน์พร้อมใช้งานแล้ว!")

async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ไม่พบ TOKEN ในระบบ")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
