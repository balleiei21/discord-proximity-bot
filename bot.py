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

NEW_SERVER_NAME = "🍓 Strawberry Cake Community 🎂"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data)
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
    {"name": "🌟・Strawberry Admin", "color": discord.Color.from_rgb(255, 165, 0), "permissions": perm_admin, "desc": "ดูแลระบบและสิทธิ์ทั้งหมด"},
    {"name": "🍰・Cake Manager", "color": discord.Color.from_rgb(255, 182, 193), "permissions": perm_manager, "desc": "ดูแลทีมงานและบริหารจัดการเซิร์ฟเวอร์"},
    {"name": "🎀・Sweet Moderator", "color": discord.Color.from_rgb(240, 128, 128), "permissions": perm_staff, "desc": "ดูแลสมาชิกและแชตทั่วไป"},
    {"name": "🧁・Event Team", "color": discord.Color.from_rgb(221, 160, 221), "permissions": perm_staff, "desc": "ดูแลและจัดกิจกรรม"},
    {"name": "🍓・Whipping Cream", "color": discord.Color.from_rgb(255, 240, 245), "permissions": perm_member, "desc": "สมาชิกทั่วไป พูดคุย แชร์รูป MC แนะนำตัว RP ดู/แจ้งสตรีม และเข้า VC"},
    {"name": "🌸・Fresh Strawberry", "color": discord.Color.from_rgb(255, 192, 203), "permissions": perm_member, "desc": "สมาชิกใหม่"},
    {"name": "🤍・Muted", "color": discord.Color.from_rgb(128, 128, 128), "permissions": perm_muted, "desc": "สมาชิกที่ถูกจำกัดการพูดและพิมพ์"},
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่องทั้งหมด (แก้ไขป้ายชื่อห้องเสียงครบถ้วน)
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
            "꒰🤍꒱・friend-zoneೀ",
            "꒰🎵꒱・music-roomೀ",
            "꒰🎮꒱・game-chatೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰🎭꒱ Ⅲ・ROLEPLAY WORLD": {
        "text": [
            "꒰📖꒱・character-introೀ",
            "꒰🪪꒱・character-cardೀ",
            "꒰📜꒱・character-loreೀ",
            "꒰✨꒱・character-showcaseೀ",
            "꒰🎭꒱・roleplay-chatೀ",
            "꒰🌎꒱・rp-worldೀ",
            "꒰📚꒱・rp-storyೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰⛏️꒱ Ⅳ・MINECRAFT": {
        "text": [
            "꒰📷꒱・minecraft-galleryೀ",
            "꒰🏠꒱・build-showcaseೀ",
            "꒰👤꒱・skin-showcaseೀ",
            "꒰🗺️꒱・map-showcaseೀ",
            "꒰🎬꒱・minecraft-clipsೀ",
            "꒰💡꒱・minecraft-ideasೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰📺꒱ Ⅴ・CREATOR ZONE": {
        "text": [
            "꒰🔴꒱・stream-alertೀ",
            "꒰📹꒱・video-alertೀ",
            "꒰🎬꒱・content-showcaseೀ",
            "꒰📷꒱・creator-galleryೀ",
            "꒰📢꒱・creator-talkೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰🎀꒱ Ⅵ・SWEET EVENTS": {
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
    "꒰💌꒱ Ⅶ・SUPPORT": {
        "text": [
            "꒰🎫꒱・open-ticketೀ",
            "꒰❓꒱・help-centerೀ",
            "꒰📩꒱・contact-staffೀ"
        ],
        "voice": [],
        "access": "public",
        "read_only": False
    },
    "꒰🧁꒱ Ⅷ・STAFF BACKSTAGE": {
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
    "꒰👑꒱ Ⅸ・ADMIN ROOM": {
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
    "꒰🎧꒱ Ⅹ・VOICE LOUNGE": {
        "text": [],
        "voice": [
            "꒰🍓꒱・Strawberry-Caféೀ",
            "꒰🧁꒱・Whipping-Creamೀ",
            "꒰🍰꒱・Cake-Roomೀ",
            "꒰🌸꒱・Sweet-Roomೀ",
            "꒰🎮꒱・Gaming-Roomೀ",
            "꒰🎭꒱・Roleplay-Roomೀ",
            "꒰🔒꒱・Staff-Loungeೀ"
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
                    if "server-management" in txt_name:
                        report_channel = ch
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(f"สร้างช่อง {txt_name} ไม่สำเร็จ: {e}")

            # --- สร้าง Voice Channels ---
            for vc_name in data["voice"]:
                try:
                    vc_overwrites = {}
                    if "Staff-Lounge" in vc_name:
                        vc_overwrites = {
                            everyone_role: discord.PermissionOverwrite(connect=False),
                            role_mod: discord.PermissionOverwrite(connect=True),
                            role_event: discord.PermissionOverwrite(connect=True),
                            role_manager: discord.PermissionOverwrite(connect=True),
                            role_admin: discord.PermissionOverwrite(connect=True),
                            role_owner: discord.PermissionOverwrite(connect=True)
                        }

                    await category.create_voice_channel(
                        name=vc_name,
                        overwrites=vc_overwrites if vc_overwrites else None
                    )
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"สร้างช่องเสียง {vc_name} ไม่สำเร็จ: {e}")

        # 6. ส่ง Embed รายงานไปยังห้อง server-management
        if report_channel:
            try:
                embed_roles = discord.Embed(
                    title="🎀 รายงานบทบาทประจำเซิร์ฟเวอร์ (Roles List)",
                    description="สรุปบทบาทและหน้าที่ของแต่ละยศในเซิร์ฟเวอร์:",
                    color=discord.Color.from_rgb(255, 105, 180)
                )
                for r in ROLES_DATA:
                    embed_roles.add_field(name=r["name"], value=f"• **หน้าที่:** {r['desc']}", inline=False)

                embed_summary = discord.Embed(
                    title="⚔️ รายงานการจัดตั้งเซิร์ฟเวอร์สำเร็จ ⚔️",
                    description=f"🏰 **{NEW_SERVER_NAME}** ได้รับการตั้งค่าโครงสร้าง 🍓 Community + 🎭 Roleplay + ⛏️ Minecraft เรียบร้อยแล้ว!",
                    color=discord.Color.from_rgb(255, 182, 193)
                )

                embed_summary.add_field(
                    name="꒰🌸꒱ Ⅰ・WELCOME",
                    value="• `꒰🌷꒱・welcomeೀ` | `꒰📜꒱・rulesೀ` | `꒰🎀꒱・rolesೀ` | `꒰📢꒱・announcementsೀ` | `꒰🍓꒱・introductionsೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰🍰꒱ Ⅱ・STRAWBERRY GARDEN",
                    value="• `꒰💬꒱・general-chatೀ` | `꒰🍓꒱・strawberry-talkೀ` | `꒰🤍꒱・friend-zoneೀ` | `꒰🎵꒱・music-roomೀ` | `꒰🎮꒱・game-chatೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰🎭꒱ Ⅲ・ROLEPLAY WORLD",
                    value="• `꒰📖꒱・character-introೀ` | `꒰🪪꒱・character-cardೀ` | `꒰📜꒱・character-loreೀ` | `꒰✨꒱・character-showcaseೀ` | `꒰🎭꒱・roleplay-chatೀ` | `꒰🌎꒱・rp-worldೀ` | `꒰📚꒱・rp-storyೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰⛏️꒱ Ⅳ・MINECRAFT",
                    value="• `꒰📷꒱・minecraft-galleryೀ` | `꒰🏠꒱・build-showcaseೀ` | `꒰👤꒱・skin-showcaseೀ` | `꒰🗺️꒱・map-showcaseೀ` | `꒰🎬꒱・minecraft-clipsೀ` | `꒰💡꒱・minecraft-ideasೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰📺꒱ Ⅴ・CREATOR ZONE",
                    value="• `꒰🔴꒱・stream-alertೀ` | `꒰📹꒱・video-alertೀ` | `꒰🎬꒱・content-showcaseೀ` | `꒰📷꒱・creator-galleryೀ` | `꒰📢꒱・creator-talkೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰🎀꒱ Ⅵ・SWEET EVENTS",
                    value="• `꒰🎉꒱・eventsೀ` | `꒰🎁꒱・giveawaysೀ` | `꒰🏆꒱・event-resultsೀ` | `꒰📅꒱・event-scheduleೀ`",
                    inline=False
                )
                embed_summary.add_field(
                    name="꒰💌꒱ Ⅶ・SUPPORT",
                    value="• `꒰🎫꒱・open-ticketೀ` | `꒰❓꒱・help-center
