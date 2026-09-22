import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# 📌 ใส่ Discord User ID ของคุณตรงนี้
# ----------------------------------------------------
ALLOWED_USER_ID = 933529869487321161  

NEW_SERVER_NAME = "ChillCraft"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data)
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
    {"name": "👑 OWNER", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "เจ้าของ"},
    {"name": "🛡️ ADMIN", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_admin, "desc": "ผู้ดูแลหลัก"},
    {"name": "🔨 MOD", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_staff, "desc": "ทีมดูแล"},
    {"name": "🛠️ DEVELOPER", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_staff, "desc": "ทีมพัฒนา"},
    {"name": "💎 VIP", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "สมาชิกพิเศษ"},
    {"name": "👤 MEMBER", "color": discord.Color.from_rgb(189, 195, 199), "permissions": perm_member, "desc": "สมาชิกทั่วไป"},
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่องทั้งหมด (ChillCraft Structure)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "📌 INFORMATION": {
        "text": [
            "📢・ประกาศ",
            "📜・กฎของเซิร์ฟ",
            "📖・คู่มือ",
            "❓・คำถามที่พบบ่อย",
            "📋・อัปเดตโปรเจกต์"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "💬 COMMUNITY": {
        "text": [
            "💬・พูดคุยทั่วไป",
            "🎮・พูดคุยเกม",
            "📸・แชร์รูป",
            "🤖・บอท",
            "💡・เสนอความคิดเห็น"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "🛒 SERVICE / SHOP": {
        "text": [
            "🛍️・สินค้าและบริการ",
            "🎫・เปิด-ticket",
            "💳・ช่องทางชำระเงิน",
            "📦・สถานะออเดอร์",
            "⭐・รีวิว"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "🛠️ PROJECT": {
        "text": [
            "📌・รายละเอียดโปรเจกต์",
            "📊・สถานะโปรเจกต์",
            "📝・งานที่กำลังทำ",
            "🐛・แจ้งปัญหา",
            "💡・เสนอฟีเจอร์"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "🔒 STAFF": {
        "text": [
            "🔐・staff-chat",
            "📋・staff-log",
            "🚨・รายงาน",
            "📝・งานทีม",
            "📊・สถิติ"
        ],
        "voice": [],
        "access": "staff_only",
        "read_only": False
    },
    "🔊 VOICE": {
        "text": [],
        "voice": [
            "🔊・พูดคุย",
            "🎮・Gaming 01",
            "🎮・Gaming 02",
            "🎵・Music",
            "💤・AFK"
        ],
        "access": "public",
        "read_only": False
    }
}

# ----------------------------------------------------
# 3. ระบบทำงานเมื่อพิมพ์ "เริ่มงาน"
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "เริ่มงาน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"รับทราบครับ **กำลังเนรมิตเซิร์ฟเวอร์ {NEW_SERVER_NAME}... 🛠️**")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # 2. ลบช่องเดิมทั้งหมด
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # 3. ลบยศเดิมทั้งหมด
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"ลบยศ {role.name} ไม่ได้: {e}")

        # 4. สร้างยศใหม่
        created_roles = {}
        for role_info in ROLES_DATA:
            try:
                role_obj = await guild.create_role(
                    name=role_info["name"],
                    color=role_info["color"],
                    permissions=role_info["permissions"],
                    hoist=True
                )
                created_roles[role_info["name"]] = role_obj
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        role_owner = created_roles.get("👑 OWNER")
        role_admin = created_roles.get("🛡️ ADMIN")
        role_mod = created_roles.get("🔨 MOD")
        role_dev = created_roles.get("🛠️ DEVELOPER")
        everyone_role = guild.default_role

        report_channel = None

        # 5. สร้างหมวดหมู่ ช่องข้อความ ช่องเสียง และตั้งค่า Permissions
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            if access_type == "public":
                if data.get("read_only"):
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True)
                    if role_mod: overwrites[role_mod] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_dev: overwrites[role_dev] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                else:
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "staff_only":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_mod: overwrites[role_mod] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_dev: overwrites[role_dev] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            try:
                category = await guild.create_category(cat_name, overwrites=overwrites)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"สร้างหมวดหมู่ {cat_name} ไม่สำเร็จ: {e}")
                continue

            # --- สร้าง Text Channels ---
            for txt_name in data["text"]:
                try:
                    ch = await category.create_text_channel(txt_name)
                    if "ประกาศ" in txt_name:
                        report_channel = ch
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(f"สร้างช่อง {txt_name} ไม่สำเร็จ: {e}")

            # --- สร้าง Voice Channels ---
            for vc_name in data["voice"]:
                try:
                    vc_overwrites = None
                    if "AFK" in vc_name:
                        vc_overwrites = {
                            everyone_role: discord.PermissionOverwrite(connect=True, speak=False)
                        }

                    await category.create_voice_channel(
                        name=vc_name,
                        overwrites=vc_overwrites
                    )
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"สร้างช่องเสียง {vc_name} ไม่สำเร็จ: {e}")

        # 6. ส่ง Embed รายงานไปยังช่อง 📢・ประกาศ
        if report_channel:
            try:
                embed_roles = discord.Embed(
                    title="👑 รายงานบทบาทประจำเซิร์ฟเวอร์ (Roles List)",
                    description="สรุปบทบาทและหน้าที่ของแต่ละยศใน ChillCraft:",
                    color=discord.Color.gold()
                )
                for r in ROLES_DATA:
                    embed_roles.add_field(name=r["name"], value=f"• **หน้าที่:** {r['desc']}", inline=False)

                embed_summary = discord.Embed(
                    title="⚔️ รายงานการจัดตั้งเซิร์ฟเวอร์สำเร็จ ⚔️",
                    description=f"🏰 **{NEW_SERVER_NAME}** ได้รับการตั้งค่าโครงสร้างเรียบร้อยแล้ว!",
                    color=discord.Color.blue()
                )

                for cat_name, data in CATEGORIES_DATA.items():
                    channels_list = []
                    if data["text"]:
                        channels_list.extend([f"`{t}`" for t in data["text"]])
                    if data["voice"]:
                        channels_list.extend([f"🔊 `{v}`" for v in data["voice"]])
                    
                    value_str = " | ".join(channels_list) if channels_list else "ไม่มีช่อง"
                    embed_summary.add_field(name=cat_name, value=value_str, inline=False)

                await report_channel.send(embed=embed_roles)
                await report_channel.send(embed=embed_summary)
                await report_channel.send("ตั้งค่าเซิร์ฟเวอร์เรียบร้อยแล้วครับ! 🌲✨")
            except Exception as e:
                print(f"ส่งรายงาน Embed ล้มเหลว: {e}")

@bot.event
async def on_ready():
    print(f"บอทพร้อมทำงานแล้วในชื่อ {bot.user}")

TOKEN = os.getenv("TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("ไม่พบ TOKEN ใน Variables กรุณาตั้งค่า TOKEN บน Railway")
