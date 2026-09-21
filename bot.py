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
ALLOWED_USER_ID = 933529869487321161  # ใส่ Discord User ID ของคุณตรงนี้

NEW_SERVER_NAME = "🍓 Strawberry Cake Community 🎂"

# ----------------------------------------------------
# 1. ยศและการกำหนดสิทธิ์ระดับยศ (Roles Data)
# ----------------------------------------------------
perm_owner = discord.Permissions.all()
perm_admin = discord.Permissions(administrator=True)

perm_manager = discord.Permissions(
    manage_roles=True, manage_channels=True, kick_members=True, ban_members=True,
    manage_messages=True, mute_members=True, deafen_members=True, move_members=True,
    view_channel=True, send_messages=True, connect=True, speak=True
)

perm_staff = discord.Permissions(
    manage_messages=True, mute_members=True, view_channel=True, send_messages=True,
    embed_links=True, attach_files=True, read_message_history=True, connect=True, speak=True
)

perm_member = discord.Permissions(
    view_channel=True, send_messages=True, read_message_history=True, add_reactions=True,
    attach_files=True, connect=True, speak=True, use_voice_activation=True
)

perm_muted = discord.Permissions(
    view_channel=True, send_messages=False, add_reactions=False, connect=False, speak=False
)

ROLES_DATA = [
    {"name": "👑・Strawberry Owner", "color": discord.Color.from_rgb(255, 105, 180), "permissions": perm_owner, "desc": "เจ้าของเซิร์ฟเวอร์ มีสิทธิ์สูงสุดในการดูแล"},
    {"name": "🌟・Strawberry Admin", "color": discord.Color.from_rgb(255, 165, 0), "permissions": perm_admin, "desc": "ผู้ดูแลระบบ จัดการบอท และสิทธิ์ภายในเซิร์ฟ"},
    {"name": "🍰・Cake Manager", "color": discord.Color.from_rgb(255, 182, 193), "permissions": perm_manager, "desc": "ผู้จัดการทีมงาน และดูแลความเรียบร้อยโดยรวม"},
    {"name": "🎀・Sweet Moderator", "color": discord.Color.from_rgb(240, 128, 128), "permissions": perm_staff, "desc": "ผู้ดูแลสมาชิก ควบคุมแชทให้เป็นไปตามกฎ"},
    {"name": "🧁・Event Team", "color": discord.Color.from_rgb(221, 160, 221), "permissions": perm_staff, "desc": "ทีมงานจัดกิจกรรม แจกของรางวัล และสร้างสีสัน"},
    {"name": "🍓・Whipping Cream", "color": discord.Color.from_rgb(255, 240, 245), "permissions": perm_member, "desc": "สมาชิกหลักของคอมมูนิตี้ (Member Role)"},
    {"name": "🌸・Fresh Strawberry", "color": discord.Color.from_rgb(255, 192, 203), "permissions": perm_member, "desc": "สมาชิกใหม่ที่เพิ่งเข้าร่วมเซิร์ฟเวอร์"},
    {"name": "🤍・Muted", "color": discord.Color.from_rgb(128, 128, 128), "permissions": perm_muted, "desc": "สมาชิกที่ถูกจำกัดสิทธิ์การพิมพ์และการพูด"},
]

# ----------------------------------------------------
# 2. หมวดหมู่และช่องทั้งหมด (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "꒰🌸꒱ Ⅰ・WELCOME": {
        "text": [
            "꒰🌷꒱・welcomeೀ",
            "꒰📜꒱・rulesೀ",
            "꒰🎀꒱・rolesೀ",
            "꒰📢꒱・announcementsೀ",
            "꒰🍓꒱・introductionsೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": True
    },
    "꒰🍰꒱ Ⅱ・STRAWBERRY GARDEN": {
        "text": [
            "꒰💬꒱・general-chatೀ",
            "꒰🍓꒱・strawberry-talkೀ",
            "꒰📷꒱・galleryೀ",
            "꒰🎮꒱・game-chatೀ",
            "꒰🎵꒱・music-roomೀ",
            "꒰🤍꒱・friend-zoneೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰🎀꒱ Ⅲ・SWEET EVENTS": {
        "text": [
            "꒰🎉꒱・eventsೀ",
            "꒰🎁꒱・giveawaysೀ",
            "꒰🏆꒱・event-resultsೀ",
            "꒰📅꒱・event-scheduleೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰💌꒱ Ⅳ・SUPPORT": {
        "text": [
            "꒰🎫꒱・open-ticketೀ",
            "꒰❓꒱・help-centerೀ",
            "꒰📩꒱・contact-staffೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰🧁꒱ Ⅴ・STAFF BACKSTAGE": {
        "text": [
            "꒰💬꒱・staff-chatೀ",
            "꒰📋꒱・staff-boardೀ",
            "꒰📢꒱・staff-newsೀ",
            "꒰⚠️꒱・member-reportsೀ",
            "꒰💡꒱・staff-ideasೀ",
            "꒰📊꒱・server-logೀ"
        ],
        "voice": [],
        "access": "staff_only",
        "read_only": False
    },
    "꒰👑꒱ Ⅵ・ADMIN ROOM": {
        "text": [
            "꒰👑꒱・admin-chatೀ",
            "꒰⚙️꒱・server-managementೀ",
            "꒰🔐꒱・admin-logೀ",
            "꒰📊꒱・server-statsೀ",
            "꒰🚨꒱・serious-reportsೀ"
        ],
        "voice": [],
        "access": "admin_only",
        "read_only": False
    },
    "꒰🎧꒱ Ⅶ・VOICE LOUNGE": {
        "text": [],
        "voice": [
            {"name": "꒰🍓꒱・Strawberry-Caféೀ", "staff_only": False},
            {"name": "꒰🧁꒱・Whipping-Creamೀ", "staff_only": False},
            {"name": "꒰🍰꒱・Cake-Roomೀ", "staff_only": False},
            {"name": "꒰🌸꒱・Sweet-Roomೀ", "staff_only": False},
            {"name": "꒰🎮꒱・Gaming-Roomೀ", "staff_only": False},
            {"name": "꒰🔒꒱・Staff-Loungeೀ", "staff_only": True}
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
        # ตรวจสอบ ID ผู้ใช้งาน
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("คุณไม่ใช่พ่อผม")
            return

        guild = message.guild
        await message.channel.send("รับทราบครับพ่อ 🍓 **กำลังเนรมิตคอมมูนิตี้ Strawberry Cake Community... 🎂**")

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

        role_owner = created_roles.get("👑・Strawberry Owner")
        role_admin = created_roles.get("🌟・Strawberry Admin")
        role_manager = created_roles.get("🍰・Cake Manager")
        role_mod = created_roles.get("🎀・Sweet Moderator")
        role_event = created_roles.get("🧁・Event Team")
        role_muted = created_roles.get("🤍・Muted")
        everyone_role = guild.default_role

        report_channel = None

        # 5. สร้างหมวดหมู่ ช่องข้อความ ช่องเสียง และตั้งค่า Permissions
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            # ล็อคยศ Muted ไม่ให้ส่งข้อความหรือพูด
            if role_muted:
                overwrites[role_muted] = discord.PermissionOverwrite(send_messages=False, connect=False, speak=False)

            if access_type == "public":
                if data.get("read_only"):
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True)
                    if role_mod: overwrites[role_mod] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_event: overwrites[role_event] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                    if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                else:
                    overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "staff_only":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_mod: overwrites[role_mod] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_event: overwrites[role_event] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            elif access_type == "admin_only":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_manager: overwrites[role_manager] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
                if role_owner: overwrites[role_owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

            category = await guild.create_category(cat_name, overwrites=overwrites)
            await asyncio.sleep(0.3)

            # --- สร้าง Text Channels ---
            for txt_name in data["text"]:
                ch = await guild.create_text_channel(txt_name, category=category)
                if "server-management" in txt_name:
                    report_channel = ch
                await asyncio.sleep(0.2)

            # --- สร้าง Voice Channels ---
            for vc in data["voice"]:
                vc_overwrites = {}
                if vc.get("staff_only"):
                    vc_overwrites[everyone_role] = discord.PermissionOverwrite(connect=False)
                    if role_mod: vc_overwrites[role_mod] = discord.PermissionOverwrite(connect=True)
                    if role_event: vc_overwrites[role_event] = discord.PermissionOverwrite(connect=True)
                    if role_manager: vc_overwrites[role_manager] = discord.PermissionOverwrite(connect=True)
                    if role_admin: vc_overwrites[role_admin] = discord.PermissionOverwrite(connect=True)
                    if role_owner: vc_overwrites[role_owner] = discord.PermissionOverwrite(connect=True)

                await guild.create_voice_channel(
                    name=vc["name"], 
                    category=category, 
                    overwrites=vc_overwrites if vc_overwrites else None
                )
                await asyncio.sleep(0.2)

        # 6. ส่งรายงานสรุปผล Embed ไปที่ห้อง server-managementೀ
        if report_channel:
            # --- Embed 1: รายงานยศประจำเซิร์ฟเวอร์ ---
            embed_roles = discord.Embed(
                title="🍓 รายงานโครงสร้างยศประจำเซิร์ฟเวอร์ (Roles List)",
                description="สรุปบทบาทและหน้าที่ของแต่ละยศในเซิร์ฟเวอร์:",
                color=discord.Color.from_rgb(255, 105, 180)
            )
            for r in ROLES_DATA:
                embed_roles.add_field(name=r["name"], value=f"• **หน้าที่:** {r['desc']}", inline=False)

            # --- Embed 2: รายงานช่องและหมวดหมู่ทั้งหมด ---
            embed_channels = discord.Embed(
                title="🎂 รายงานโครงสร้างหมวดหมู่และช่องใช้งาน (Channels Summary)",
                description="รายละเอียดหน้าที่ของแต่ละห้องในเซิร์ฟเวอร์:",
                color=discord.Color.from_rgb(255, 182, 193)
            )

            embed_channels.add_field(
                name="꒰🌸꒱ Ⅰ・WELCOME (อ่านได้อย่างเดียว)",
                value="• `welcomeೀ`: ต้อนรับสมาชิกใหม่\n• `rulesೀ`: กฎระเบียบเซิร์ฟเวอร์\n• `rolesೀ`: เลือกรับยศประจำตัว\n• `announcementsೀ`: ประกาศสำคัญ\n• `introductionsೀ`: ช่องแนะนำตัว",
                inline=False
            )

            embed_channels.add_field(
                name="꒰🍰꒱ Ⅱ・STRAWBERRY GARDEN (คอมมูนิตี้หลัก)",
                value="• `general-chatೀ`: พูดคุยทั่วไป\n• `strawberry-talkೀ`: คุยสบายๆ ฟีลคาเฟ่\n• `galleryೀ`: แชร์รูปภาพ\n• `game-chatೀ`: พูดคุยเรื่องเกม\n• `music-roomೀ`: แชร์เพลง/เพลย์ลิสต์\n• `friend-zoneೀ`: หาเพื่อนใหม่",
                inline=False
            )

            embed_channels.add_field(
                name="꒰🎀꒱ Ⅲ・SWEET EVENTS (กิจกรรม)",
                value="• `eventsೀ`: แจ้งกิจกรรมเซิร์ฟเวอร์\n• `giveawaysೀ`: กิจกรรมแจกของ\n• `event-resultsೀ`: สรุปผลกิจกรรม\n• `event-scheduleೀ`: ตารางกิจกรรม",
                inline=False
            )

            embed_channels.add_field(
                name="꒰💌꒱ Ⅳ・SUPPORT (ศูนย์ช่วยเหลือ)",
                value="• `open-ticketೀ`: เปิดตั๋วติดต่อทีมงาน\n• `help-centerೀ`: สอบถามข้อสงสัย\n• `contact-staffೀ`: ติดต่อทีมงานโดยตรง",
                inline=False
            )

            embed_channels.add_field(
                name="꒰🧁꒱ Ⅴ・STAFF BACKSTAGE (เฉพาะ Staff)",
                value="• `staff-chatೀ`: พูดคุยทีมงาน\n• `staff-boardೀ`: มอบหมายงาน\n• `staff-newsೀ`: ประกาศภายใน\n• `member-reportsೀ`: รายงานสมาชิก\n• `staff-ideasೀ`: เสนอไอเดีย\n• `server-logೀ`: บันทึกข้อมูลเซิร์ฟ",
                inline=False
            )

            embed_channels.add_field(
                name="꒰👑꒱ Ⅵ・ADMIN ROOM (เฉพาะ Manager / Admin / Owner)",
                value="• `admin-chatೀ`: พูดคุยระดับสูง\n• `server-managementೀ`: จัดการระบบ/สรุปงาน\n• `admin-logೀ`: ประวัติการทำงานแอดมิน\n• `server-statsೀ`: สถิติเซิร์ฟเวอร์\n• `serious-reportsೀ`: รายงานเรื่องร้ายแรง",
                inline=False
            )

            embed_channels.add_field(
                name="꒰🎧꒱ Ⅶ・VOICE LOUNGE (ห้องพูดคุยด้วยเสียง)",
                value="• `Strawberry-Caféೀ` / `Whipping-Creamೀ` / `Cake-Roomೀ` / `Sweet-Roomೀ` / `Gaming-Roomೀ`: ห้องเสียงสำหรับสมาชิก\n• `🔒・Staff-Loungeೀ`: ห้องเสียงเฉพาะทีมงาน",
                inline=False
            )

            embed_channels.set_footer(text="ขอบคุณจากเบล 🍓🤍 | Strawberry Cake Community", icon_url=guild.icon.url if guild.icon else None)

            await report_channel.send(embed=embed_roles)
            await report_channel.send(embed=embed_channels)

        return

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
