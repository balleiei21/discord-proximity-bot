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

CATEGORIES_DATA = {
    "📌 INFORMATION": {
        "text": ["꒰📢꒱・ยินดีต้อนรับ", "꒰📜꒱・กฎของร้าน", "꒰📋꒱・รายละเอียดบริการ", "꒰💳꒱・ช่องทางชำระเงิน", "꒰⭐꒱・รีวิวจากลูกค้า"],
        "voice": [], "access": "public", "read_only": True
    },
    "🛒 SHOP": {
        "text": ["꒰🛍️꒱・ร้านค้า", "꒰🎮꒱・เติมเกม", "꒰💎꒱・ไอเทมเกม", "꒰🎁꒱・โปรโมชั่น"],
        "voice": [], "access": "public", "read_only": True
    },
    "🎨 SERVICES": {
        "text": ["꒰👕꒱・รับทำสกิน", "꒰🧱꒱・รับทำแมพมายคราฟ", "꒰⚙️꒱・รับทำแอดออน", "꒰💻꒱・รับทำดิส", "꒰🎨꒱・รับทำคอมช", "꒰💳꒱・รับเติมเกม", "꒰🤖꒱・รับฟาร์ม Roblox", "꒰🔥꒱・รับดันแรงค์ Free Fire", "꒰⚔️꒱・รับดันแรงค์ AOV"],
        "voice": [], "access": "public", "read_only": True
    },
    "📂 PORTFOLIO": {
        "text": ["꒰🖼️꒱・ผลงานสกิน", "꒰🗺️꒱・ผลงานแมพ", "꒰⚙️꒱・ผลงานแอดออน", "꒰💬꒱・ผลงานดิส", "꒰🎨꒱・ผลงานคอมช"],
        "voice": [], "access": "public", "read_only": True
    },
    "🧾 CUSTOMER": {
        "text": ["꒰🎫꒱・เปิด Ticket", "꒰📦꒱・สถานะงาน", "꒰💬꒱・สอบถามบริการ", "꒰📜꒱・เครดิตลูกค้า"],
        "voice": [], "access": "public", "read_only": False
    },
    "💬 COMMUNITY": {
        "text": ["꒰💬꒱・พูดคุย", "꒰🎮꒱・คุยเรื่องเกม", "꒰📸꒱・แชร์ผลงาน", "꒰🤝꒱・หาเพื่อนเล่นเกม"],
        "voice": ["🔊・ห้องคุยเล่น 1", "🔊・ห้องคุยเล่น 2"],
        "access": "public", "read_only": False
    },
    "🏆 CREDIT": {
        "text": ["꒰🏆꒱・เครดิตร้าน", "꒰💖꒱・ขอบคุณลูกค้า", "꒰📸꒱・ผลงานลูกค้า"],
        "voice": [], "access": "public", "read_only": False
    },
    "🔒 STAFF": {
        "text": ["꒰🔧꒱・ห้องทีมงาน", "꒰📋꒱・จัดการออเดอร์", "꒰💰꒱・รายรับ", "꒰📝꒱・บันทึกงาน"],
        "voice": [], "access": "staff_only", "read_only": False
    },
    "🔐 MANAGEMENT": {
        "text": [], "voice": [], "access": "management_special", "read_only": False
    }
}

# ----------------------------------------------------
# ฟังก์ชันสร้างอย่างปลอดภัย (Safe API Handler)
# ----------------------------------------------------
async def safe_api_call(coro_fn, *args, **kwargs):
    while True:
        try:
            res = await coro_fn(*args, **kwargs)
            await asyncio.sleep(1.0) # ป้องกันส่งถี่เกินไป
            return res
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ชะลอการทำงาน รอ {retry_after:.2f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
            else:
                print(f"[API Error] {e}")
                return None
        except Exception as e:
            print(f"[Unexpected Error] {e}")
            return None

# ----------------------------------------------------
# คำสั่งระบบทำงาน
# ----------------------------------------------------
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
        await message.channel.send(f"🚀 **รับทราบคำสั่ง! กำลังจัดสร้างเซิร์ฟเวอร์ {NEW_SERVER_NAME}...**\n*(อาจใช้เวลา 1-3 นาทีเนื่องจากระบบต้องรักษาระยะห่าง API ไม่ให้โดน Discord บล็อก)*")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        await safe_api_call(guild.edit, name=NEW_SERVER_NAME)

        # 2. ลบช่องเดิมทั้งหมด
        for channel in list(guild.channels):
            await safe_api_call(channel.delete)

        # 3. ลบยศเดิมทั้งหมด
        for role in list(guild.roles):
            if not role.is_default() and not role.managed:
                await safe_api_call(role.delete)

        # 4. สร้างยศใหม่ทั้งหมด
        created_roles = {}
        for role_info in ROLES_DATA:
            role_obj = await safe_api_call(
                guild.create_role,
                name=role_info["name"],
                color=role_info["color"],
                permissions=role_info["permissions"],
                hoist=True
            )
            if role_obj:
                created_roles[role_info["name"]] = role_obj

        # ดึงออบเจ็กต์ยศ
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

        all_staff_roles = [r for r in [r_owner, r_co_owner, r_executive, r_manager, r_admin, r_mod, r_support, r_ticket_staff] if r]
        manager_up_roles = [r for r in [r_owner, r_co_owner, r_executive, r_manager] if r]

        report_channel = None

        # 5. สร้างหมวดหมู่และช่องตามลำดับ
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

            category = await safe_api_call(guild.create_category, cat_name, overwrites=overwrites)
            if not category:
                continue

            # --- กรณีพิเศษ: หมวดหมู่ MANAGEMENT ---
            if cat_name == "🔐 MANAGEMENT":
                mgmt_channels = [
                    {"name": "꒰👑꒱・ห้อง owner", "roles": [r_owner, r_co_owner]},
                    {"name": "꒰💼꒱・ห้องบริหาร", "roles": [r_owner, r_co_owner, r_executive, r_manager]},
                    {"name": "꒰📊꒱・รายงานร้าน", "roles": [r_owner, r_co_owner, r_executive]},
                    {"name": "꒰⚙️꒱・ตั้งค่าระบบ", "roles": [r_owner, r_co_owner, r_admin]}
                ]
                for m_ch in mgmt_channels:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    for allowed_r in m_ch["roles"]:
                        if allowed_r:
                            ch_overwrites[allowed_r] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    
                    await safe_api_call(category.create_text_channel, m_ch["name"], overwrites=ch_overwrites)
                continue

            # --- สร้าง Text Channels ---
            for txt_name in data["text"]:
                ch_overwrites = {}
                
                if "สถานะงาน" in txt_name:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    if r_customer: ch_overwrites[r_customer] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
                    for st_role in all_staff_roles:
                        ch_overwrites[st_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                elif "รายรับ" in txt_name:
                    ch_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
                    for m_role in manager_up_roles:
                        ch_overwrites[m_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                ch = await safe_api_call(
                    category.create_text_channel,
                    txt_name,
                    overwrites=ch_overwrites if ch_overwrites else None
                )

                if ch and "บันทึกงาน" in txt_name:
                    report_channel = ch

            # --- สร้าง Voice Channels ---
            for vc_name in data["voice"]:
                await safe_api_call(category.create_voice_channel, vc_name)

        # 6. ส่งรายงานสรุปเมื่อสร้างเสร็จสมบูรณ์
        if report_channel:
            try:
                embed_finish = discord.Embed(
                    title="🎉 การตั้งค่าเซิร์ฟเวอร์เสร็จสิ้นสมบูรณ์!",
                    description=f"ระบบได้สร้างโครงสร้างยศ หมวดหมู่ และช่องทั้งหมดสำหรับ **{NEW_SERVER_NAME}** เรียบร้อยแล้วครับ",
                    color=discord.Color.green()
                )
                await safe_api_call(report_channel.send, embed=embed_finish)

                embed_roles = discord.Embed(
                    title="👑 รายงานยศและสิทธิ์ประจำร้าน NEXORA SHOP",
                    description="สรุปรายชื่อยศที่ถูกสร้างขึ้นในเซิร์ฟเวอร์:",
                    color=discord.Color.gold()
                )
                for r in ROLES_DATA:
                    embed_roles.add_field(name=r["name"], value=f"• **หน้าที่:** {r['desc']}", inline=False)

                report_msg_1 = (
                    "📋 **[รายงานสรุปสิทธิ์และการเข้าถึงช่องต่าง ๆ]**\n\n"
                    "**📌 INFORMATION**\n• ทุกคนเข้าชมได้ (อ่านได้อย่างเดียว)\n\n"
                    "**🛒 SHOP & 🎨 SERVICES & 📂 PORTFOLIO**\n• ทุกคนเข้าชมได้ (ทีมงานโพสต์ข้อมูลได้)\n\n"
                    "**🧾 CUSTOMER**\n• `เปิด Ticket / สอบถามบริการ / เครดิตลูกค้า`: ทุกคนพิมพ์ได้\n"
                    "• `สถานะงาน`: เห็นเฉพาะ Customer + Staff\n\n"
                    "**💬 COMMUNITY & 🏆 CREDIT**\n• สมาชิกทุกคนเข้าใช้งานและพูดคุยได้ตามปกติ\n\n"
                    "**🔒 STAFF**\n• เห็นเฉพาะทีมงานขึ้นไป ( Staff + Managerขึ้นไป )\n"
                    "• `รายรับ`: เห็นเฉพาะ Manager / Executive / Co-Owner / Owner\n\n"
                    "**🔐 MANAGEMENT**\n"
                    "• `ห้อง Owner`: Owner, Co-Owner\n"
                    "• `ห้องบริหาร`: Owner, Co-Owner, Executive, Manager\n"
                    "• `รายงานร้าน`: Owner, Co-Owner, Executive\n"
                    "• `ตั้งค่าระบบ`: Owner, Co-Owner, Admin\n"
                )

                await safe_api_call(report_channel.send, embed=embed_roles)
                await safe_api_call(report_channel.send, report_msg_1)
            except Exception as e:
                print(f"ส่งรายงานไม่สำเร็จ: {e}")

@bot.event
async def on_ready():
    print(f"บอท {bot.user} ออนไลน์พร้อมใช้งานแล้ว!")

async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ไม่พบ TOKEN ในระบบ กรุณาตรวจสอบ Environment Variable")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
