import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# 📌 ID ผู้ใช้ที่ได้รับอนุญาตให้ใช้คำสั่งได้คนเดียว
# ----------------------------------------------------
ALLOWED_USER_ID = 123456789012345678  # เปลี่ยนเป็น Discord User ID ของคุณ

NEW_SERVER_NAME = "🍓 Strawberry Cake Shop 🎂"

# ----------------------------------------------------
# 1. ยศและการกำหนดสิทธิ์ระดับยศ (Roles Data)
# ----------------------------------------------------
perm_owner = discord.Permissions.all()

perm_manager = discord.Permissions(
    manage_roles=True,
    manage_channels=True,
    kick_members=True,
    ban_members=True,
    manage_messages=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    view_channel=True,
    send_messages=True,
    connect=True,
    speak=True
)

perm_staff = discord.Permissions(
    manage_messages=True,
    mute_members=True,
    view_channel=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    read_message_history=True,
    connect=True,
    speak=True
)

perm_member = discord.Permissions(
    view_channel=True,
    send_messages=True,
    read_message_history=True,
    add_reactions=True,
    attach_files=True,
    connect=True,
    speak=True
)

# เรียงจากยศสูงไปยศต่ำ
ROLES_DATA = [
    {"name": "👑 Owner", "color": discord.Color.from_rgb(255, 105, 180), "permissions": perm_owner},      # ชมพูเข้ม
    {"name": "🍰 Manager", "color": discord.Color.from_rgb(255, 182, 193), "permissions": perm_manager},  # ชมพูอ่อน
    {"name": "🎀 Staff", "color": discord.Color.from_rgb(240, 128, 128), "permissions": perm_staff},     # คอรัล
    {"name": "🧁 Designer", "color": discord.Color.from_rgb(221, 160, 221), "permissions": perm_staff},  # พลัมอ่อน
    {"name": "🌸 Customer", "color": discord.Color.from_rgb(255, 192, 203), "permissions": perm_member},  # ชมพู
    {"name": "🍓 Whipping Cream", "color": discord.Color.from_rgb(255, 240, 245), "permissions": perm_member}, # ขาวชมพู
]

# ----------------------------------------------------
# 2. หมวดหมู่และช่องทั้งหมด (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🌸 Ⅰ・WELCOME": {
        "text": ["🌷・welcome", "📜・rules", "🎀・roles"],
        "voice": [],
        "access": "public",
        "read_only_public": True
    },
    "🛍️ Ⅱ・STRAWBERRY SHOP": {
        "text": ["🛒・shop", "💰・price-list", "🖼️・portfolio", "🎁・promotion", "⭐・reviews"],
        "voice": [],
        "access": "public",
        "read_only_public": True  # ให้สมาชิกอ่านได้ แต่ส่งข้อความไม่ได้ (Staff พิมพ์ได้)
    },
    "🎫 Ⅲ・ORDER": {
        "text": ["🎟️・open-ticket", "📋・how-to-order", "💳・payment", "📦・order-status"],
        "voice": [],
        "access": "public",
        "read_only_public": True
    },
    "💬 Ⅳ・COMMUNITY": {
        "text": ["💬・chat", "🍓・strawberry-talk", "📸・gallery", "🎀・customer-showcase"],
        "voice": [],
        "access": "public",
        "read_only_public": False # พิมพ์พูดคุยได้ทุกคน
    },
    "🏠 Ⅴ・BACKSTAGE": {
        "text": [
            "💬・staff-chat", "📋・order-management", "📦・order-log", 
            "💰・payment-log", "🛠️・work-progress", "⚠️・issue-report", 
            "💡・staff-ideas", "📢・staff-announcement"
        ],
        "voice": [],
        "access": "staff_only"
    },
    "👑 Ⅵ・ADMIN": {
        "text": ["👑・admin-chat", "⚙️・server-settings", "📊・sales-log", "🔐・admin-log", "🚨・staff-report"],
        "voice": [],
        "access": "admin_only"
    },
    "🎧 Ⅶ・VOICE": {
        "text": [],
        "voice": [
            {"name": "🍓・Strawberry Café", "staff_only": False},
            {"name": "🧁・Whipping Cream", "staff_only": False},
            {"name": "🍰・Cake Room", "staff_only": False},
            {"name": "🌸・Sweet Room", "staff_only": False},
            {"name": "🔒・Staff Room", "staff_only": True}
        ],
        "access": "public",
        "read_only_public": False
    }
}

# ----------------------------------------------------
# 3. ระบบทำงานเมื่อพิมพ์ "เบลอ้วน"
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "เบลอ้วน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild
        await message.channel.send("🍓 **กำลังเริ่มเนรมิตร้าน Strawberry Cake Shop... 🎂**")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # 2. ลบช่องเดิมทั้งหมด
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # 3. ลบยศเดิมทั้งหมด
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.15)
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
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        role_owner = created_roles.get("👑 Owner")
        role_manager = created_roles.get("🍰 Manager")
        role_staff = created_roles.get("🎀 Staff")
        role_designer = created_roles.get("🧁 Designer")
        everyone_role = guild.default_role

        log_channel = None

        # 5. สร้างหมวดหมู่ ช่อง และตั้งค่า Permissions
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            # กำหนดสิทธิ์พื้นฐานของหมวดหมู่
            if access_type == "public":
                if data.get("read_only_public"):
                    # อ่านได้อย่างเดียว สมาชิกพิมพ์ไม่ได้ (Staff ขึ้นไปพิมพ์ได้)
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True)
                    if role_staff: overwrites[role_staff] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_designer: overwrites[role_designer] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                else:
                    # สาธารณะ พิมพ์/พูดคุยได้ทุกคน
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "staff_only":
                # ปิดคนนอก เปิดเฉพาะ Staff / Designer / Manager / Owner
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_staff: overwrites[role_staff] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_designer: overwrites[role_designer] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "admin_only":
                # เปิดเฉพาะ Manager / Owner
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            category = await guild.create_category(cat_name, overwrites=overwrites)
            await asyncio.sleep(0.3)

            # สร้าง Text Channels
            for txt_name in data["text"]:
                ch = await guild.create_text_channel(txt_name, category=category)
                if txt_name == "📦・order-log":
                    log_channel = ch
                await asyncio.sleep(0.2)

            # สร้าง Voice Channels
            for vc in data["voice"]:
                vc_overwrites = {}
                if vc.get("staff_only"):
                    vc_overwrites[everyone_role] = discord.PermissionOverwrite(connect=False)
                    if role_staff: vc_overwrites[role_staff] = discord.PermissionOverwrite(connect=True)
                    if role_manager: vc_overwrites[role_manager] = discord.PermissionOverwrite(connect=True)
                    if role_owner: vc_overwrites[role_owner] = discord.PermissionOverwrite(connect=True)

                await guild.create_voice_channel(vc["name"], category=category, overwrites=vc_overwrites if vc_overwrites else None)
                await asyncio.sleep(0.2)

        # 6. รายงานสรุปผลระบบไปยังห้อง 📦・order-log ใน Backstage
        if log_channel:
            embed = discord.Embed(
                title="🍓 สรุปการตั้งค่าระบบร้าน Strawberry Cake Shop 🎂",
                description="ระบบได้ทำการสร้างยศ จัดหมวดหมู่ช่อง และกำหนดสิทธิ์การมองเห็นแยกหน้าร้าน/หลังบ้านเรียบร้อยแล้ว!",
                color=discord.Color.from_rgb(255, 105, 180)
            )

            embed.add_field(
                name="🌸 Ⅰ・WELCOME & 🛍️ Ⅱ・STRAWBERRY SHOP (หน้าร้าน)",
                value="• `🌷・welcome` | `📜・rules` | `🎀・roles`\n• `🛒・shop` | `💰・price-list` | `🖼️・portfolio` | `🎁・promotion` | `⭐・reviews`\n*(ทุกคนมองเห็นได้ อ่านได้อย่างเดียว เพื่อความเป็นระเบียบ)*",
                inline=False
            )

            embed.add_field(
                name="🎫 Ⅲ・ORDER & 💬 Ⅳ・COMMUNITY (สั่งงาน/พูดคุย)",
                value="• `🎟️・open-ticket` | `📋・how-to-order` | `💳・payment` | `📦・order-status`\n• `💬・chat` | `🍓・strawberry-talk` | `📸・gallery` | `🎀・customer-showcase`\n*(เป็นพื้นที่สำหรับเปิดตั๋วสั่งงาน และช่องพูดคุยทั่วไปของสมาชิก)*",
                inline=False
            )

            embed.add_field(
                name="🏠 Ⅴ・BACKSTAGE (หลังบ้านทีมงาน)",
                value="• `💬・staff-chat` | `📋・order-management` | `📦・order-log` | `💰・payment-log` | `🛠️・work-progress` | `⚠️・issue-report` | `💡・staff-ideas` | `📢・staff-announcement`\n*(เฉพาะ Staff, Designer, Manager, Owner ที่มองเห็น)*",
                inline=False
            )

            embed.add_field(
                name="👑 Ⅵ・ADMIN (ผู้บริหาร)",
                value="• `👑・admin-chat` | `⚙️・server-settings` | `📊・sales-log` | `🔐・admin-log` | `🚨・staff-report`\n*(เฉพาะ Manager และ Owner เท่านั้น)*",
                inline=False
            )

            embed.add_field(
                name="🎧 Ⅶ・VOICE (ห้องเสียง)",
                value="• ห้องพูดคุยทั่วไป 4 ห้อง และห้อง `🔒・Staff Room` สำหรับทีมงานคุยงาน",
                inline=False
            )

            embed.set_footer(text="Strawberry Cake Shop • System Ready 🍓", icon_url=guild.icon.url if guild.icon else None)

            await log_channel.send(embed=embed)

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
