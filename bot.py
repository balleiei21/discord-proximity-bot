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

NEW_SERVER_NAME = "NEXORA SHOP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Ordered by Hierarchy)
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

perm_muted = discord.Permissions(
    view_channel=True, send_messages=False, add_reactions=False, connect=False, speak=False
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
    {"name": "🤖・Bot", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "บอทในเซิร์ฟเวอร์"},
    {"name": "🔇・Muted", "color": discord.Color.from_rgb(105, 105, 105), "permissions": perm_muted, "desc": "สมาชิกที่ถูกจำกัดสิทธิ์"}
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่องทั้งหมด (NEXORA SHOP Structure)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "📌 INFORMATION": {
        "text": [
            "꒰📢꒱・ยินดีต้อนรับ",
            "꒰📜꒱・กฎของร้าน",
            "꒰📋꒱・รายละเอียดบริการ",
            "꒰💳꒱・ช่องทางชำระเงิน",
            "꒰⭐꒱・รีวิวจากลูกค้า"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "🛒 SHOP": {
        "text": [
            "꒰🛍️꒱・ร้านค้า",
            "꒰🎮꒱・เติมเกม",
            "꒰💎꒱・ไอเทมเกม",
            "꒰🎁꒱・โปรโมชั่น"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "🎨 SERVICES": {
        "text": [
            "꒰👕꒱・รับทำสกิน",
            "꒰🧱꒱・รับทำแมพมายคราฟ",
            "꒰⚙️꒱・รับทำแอดออน",
            "꒰💻꒱・รับทำดิส",
            "꒰🎨꒱・รับทำคอมช",
            "꒰💳꒱・รับเติมเกม",
            "꒰🤖꒱・รับฟาร์ม-roblox",
            "꒰🔥꒱・รับดันแรงค์-freefire",
            "꒰⚔️꒱・รับดันแรงค์-aov"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "📂 PORTFOLIO": {
        "text": [
            "꒰🎨꒱・ผลงานสกิน",
            "꒰🧱꒱・ผลงานแมพมายคราฟ",
            "꒰⚙️꒱・ผลงานแอดออน",
            "꒰💻꒱・ผลงานตกแต่งดิส",
            "꒰🖌️꒱・ผลงานคอมมิชชัน"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "🧾 CUSTOMER": {
        "text": [
            "꒰🎫꒱・เปิด-ticket",
            "꒰📦꒱・สถานะงาน",
            "꒰💬꒱・สอบถามบริการ",
            "꒰📜꒱・เครดิตลูกค้า"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "💬 COMMUNITY": {
        "text": [
            "꒰💬꒱・พูดคุย",
            "꒰🎮꒱・คุยเรื่องเกม",
            "꒰📸꒱・แชร์ผลงาน",
            "꒰🤝꒱・หาเพื่อนเล่นเกม"
        ],
        "voice": [
            "🔊・ห้องคุยเล่น 1",
            "🔊・ห้องคุยเล่น 2"
        ],
        "access": "public",
        "read_only": False
    },
    "🏆 CREDIT": {
        "text": [
            "꒰🏆꒱・เครดิตร้าน",
            "꒰💖꒱・ขอบคุณลูกค้า",
            "꒰📸꒱・ผลงานลูกค้า"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "🔒 STAFF": {
        "text": [
            "꒰🔧꒱・ห้องทีมงาน",
            "꒰📋꒱・จัดการออเดอร์",
            "꒰💰꒱・รายรับ",
            "꒰📝꒱・บันทึกงาน"
        ],
        "voice": [],
        "access": "staff_only",
        "read_only": False
    },
    "🔐 MANAGEMENT": {
        "text": [],
        "voice": [],
        "access": "management_special",
        "read_only": False
    }
}

# ----------------------------------------------------
# ฟังก์ชันสร้าง Text Channel แบบป้องกัน Rate Limit
# ----------------------------------------------------
async def safe_create_text_channel(category, name, overwrites=None):
    while True:
        try:
            ch = await category.create_text_channel(name, overwrites=overwrites)
            await asyncio.sleep(0.5)
            return ch
        except discord.HTTPException as e:
            if e.status == 429:  # Too Many Requests / Rate Limit
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                print(f"ติด Rate Limit กำลังรอ {retry_after} วินาที...")
                await asyncio.sleep(retry_after)
            else:
                print(f"สร้างช่อง {name} ไม่สำเร็จ: {e}")
                return None

# ----------------------------------------------------
# ฟังก์ชันสร้าง Voice Channel แบบป้องกัน Rate Limit
# ----------------------------------------------------
async def safe_create_voice_channel(category, name, overwrites=None):
    while True:
        try:
            vc = await category.create_voice_channel(name, overwrites=overwrites)
            await asyncio.sleep(0.5)
            return vc
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                print(f"ติด Rate Limit กำลังรอ {retry_after} วินาที...")
                await asyncio.sleep(retry_after)
            else:
                print(f"สร้างช่องเสียง {name} ไม่สำเร็จ: {e}")
                return None

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
        await message.channel.send(f"รับทราบครับ **กำลังเนรมิตร้าน {NEW_SERVER_NAME}... (ระบบปรับความเร็วเพื่อป้องกันสร้างช่องไม่ครบ) 🛍️✨**")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # 2. ลบช่องเดิมทั้งหมด
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # 3. ลบยศเดิมทั้งหมด
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"ลบยศ {role.name} ไม่ได้: {e}")

        # 4. สร้างยศใหม่ตามลำดับยศ
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
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        # ดึงออบเจ็กต์ยศไว้ตั้งสิทธิ์
        r_owner = created_roles.get("👑・Owner")
        r_co_owner = created_roles.get("💎・Co-Owner")
        r_executive = created_roles.get("🏆・Executive")
        r_manager = created_roles.get("⚜️・Manager")
        r_admin = created_roles.get("🔧・Admin")
        r_mod = created_roles.get("🛡️・Moderator")
        r_support = created_roles.get("🎧・Support")
        r_ticket_staff = created_roles.get("🎫・Ticket Staff")
        r_customer = created_roles.get("⭐・Customer")
        r_muted = created_roles.get("🔇・Muted")
        everyone_role = guild.default_role

        # กลุ่มสิทธิ์ทีมงานทั่วไป (Staff Up)
        all_staff_roles = [r for r in [r_owner, r_co_owner, r_executive, r_manager, r_admin, r_mod, r_support, r_ticket_staff] if r]
        # กลุ่มระดับ Manager ขึ้นไป
        manager_up_roles = [r for r in [r_owner, r_co_owner, r_executive, r_manager] if r]

        report_channel = None

        # 5. สร้างหมวดหมู่ ช่องข้อความ ช่องเสียง และตั้งค่า Permissions
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            if r_muted:
                overwrites[r_muted] = discord.PermissionOverwrite(send_messages=False, connect=False, speak=False)

            if access_type == "public":
                if data.get("read_only"):
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True)
                    for st_role in all_staff_roles:
                        overwrites[st_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                else:
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "staff_only":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                for st_role in all_staff_roles:
                    overwrites[st_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            try:
                category = await guild.create_category(cat_name, overwrites=overwrites)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"สร้างหมวดหมู่ {cat_name} ไม่สำเร็จ: {e}")
                continue

            # --- กรณีพิเศษ หมวดหมู่ MANAGEMENT ---
            if cat_name == "🔐 MANAGEMENT":
                mgmt_channels = [
                    {"name": "꒰👑꒱・ห้อง-owner", "roles": [r_owner, r_co_owner]},
                    {"name": "꒰💼꒱・ห้องบริหาร", "roles": [r_owner, r_co_owner, r_executive, r_manager]},
                    {"name": "꒰📊꒱・รายงานร้าน", "roles": [r_owner, r_co_owner, r_executive]},
                    {"name": "꒰⚙️꒱・ตั้งค่าระบบ", "roles": [r_owner, r_co_owner, r_admin]}
                ]
                for m_ch in mgmt_channels:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    for allowed_r in m_ch["roles"]:
                        if allowed_r:
                            ch_overwrites[allowed_r] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    
                    await safe_create_text_channel(category, m_ch["name"], overwrites=ch_overwrites)
                continue

            # --- สร้าง Text Channels ปกติ ---
            for txt_name in data["text"]:
                ch_overwrites = {}
                
                # กรณีพิเศษ: ช่องสถานะงาน ให้ Customer + Staff เห็นเท่านั้น
                if "สถานะงาน" in txt_name:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    if r_customer: ch_overwrites[r_customer] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
                    for st_role in all_staff_roles:
                        ch_overwrites[st_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                # กรณีพิเศษ: ช่องรายรับ ให้ Manager ขึ้นไปเห็นเท่านั้น
                elif "รายรับ" in txt_name:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    for m_role in manager_up_roles:
                        ch_overwrites[m_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                ch = await safe_create_text_channel(
                    category,
                    txt_name,
                    overwrites=ch_overwrites if ch_overwrites else None
                )

                if ch and "บันทึกงาน" in txt_name:
                    report_channel = ch

            # --- สร้าง Voice Channels ---
            for vc_name in data["voice"]:
                await safe_create_voice_channel(category, vc_name)

        # 6. ส่ง Embed รายงานไปยังช่อง ꒰📝꒱・บันทึกงาน
        if report_channel:
            try:
                embed_roles = discord.Embed(
                    title="👑 รายงานบทบาทประจำร้าน NEXORA SHOP",
                    description="สรุปบทบาทและยศทั้งหมดตามลำดับโครงสร้างร้าน:",
                    color=discord.Color.gold()
                )
                for r in ROLES_DATA:
                    embed_roles.add_field(name=r["name"], value=f"• **หน้าที่:** {r['desc']}", inline=False)

                embed_summary = discord.Embed(
                    title="⚔️ รายงานการจัดตั้งเซิร์ฟเวอร์ร้านค้าสำเร็จ ⚔️",
                    description=f"🏰 **{NEW_SERVER_NAME}** ได้รับการตั้งค่าโครงสร้างร้านค้าและระบบสิทธิ์เรียบร้อยแล้ว!",
                    color=discord.Color.purple()
                )

                for cat_name, data in CATEGORIES_DATA.items():
                    channels_list = []
                    if data["text"]:
                        channels_list.extend([f"`{t}`" for t in data["text"]])
                    if data["voice"]:
                        channels_list.extend([f"🔊 `{v}`" for v in data["voice"]])
                    if cat_name == "🔐 MANAGEMENT":
                        channels_list = ["`꒰👑꒱・ห้อง-owner`", "`꒰💼꒱・ห้องบริหาร`", "`꒰📊꒱・รายงานร้าน`", "`꒰⚙️꒱・ตั้งค่าระบบ`"]

                    value_str = " | ".join(channels_list) if channels_list else "ไม่มีช่อง"
                    embed_summary.add_field(name=cat_name, value=value_str, inline=False)

                await report_channel.send(embed=embed_roles)
                await report_channel.send(embed=embed_summary)
                await report_channel.send("เนรมิตร้าน NEXORA SHOP ครบถ้วน 100% แล้วครับ! บันทึกรายงานเข้าห้องทีมงานเรียบร้อยแล้ว 🛍️✨")
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
