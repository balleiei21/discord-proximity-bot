import discord
from discord.ext import commands
import asyncio
import os
import traceback

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_USER_IDS = [933529869487321161, 932890657113145394]  
NEW_SERVER_NAME = "Minecraft Haunted Hotel RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Haunted Hotel Theme)
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
    # --- ผู้เล่น ---
    {"name": "👤 ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้เข้าชมทั่วไป"},
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครเข้าสู่โรงแรม"},
    {"name": "🧳 แขก", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้เข้าพักในโรงแรม"},
    {"name": "⭐ VIP", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "แขกห้องพักพิเศษ"},

    # --- พนักงานโรงแรม ---
    {"name": "🛎️ พนักงานต้อนรับ", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "เจ้าหน้าที่ต้อนรับล็อบบี้"},
    {"name": "🧹 แม่บ้าน", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ผู้ดูแลทำความสะอาดห้องพัก"},
    {"name": "👨‍🍳 เชฟ", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "พ่อครัวประจำห้องอาหาร"},
    {"name": "🛠️ ช่าง", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ฝ่ายซ่อมบำรุงโรงแรม"},
    {"name": "🛡️ รปภ.", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "เจ้าหน้าที่รักษาความปลอดภัย"},
    {"name": "👔 ผู้จัดการ", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้จัดการโรงแรม"},
    {"name": "👑 เจ้าของโรงแรม", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ครอบครองกิจการโรงแรม"},

    # --- ตัวละครเหนือธรรมชาติ ---
    {"name": "👻 ผี", "color": discord.Color.from_rgb(189, 195, 199), "permissions": perm_member, "desc": "วิญญาณสิงสถิตในโรงแรม"},
    {"name": "🕯️ ผีประจำโรงแรม", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "วิญญาณดั้งเดิม"},
    {"name": "🌑 วิญญาณอาฆาต", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_member, "desc": "วิญญาณเต็มไปด้วยความแค้น"},
    {"name": "👑 วิญญาณผู้ดูแล", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ผู้ปกครองเหล่าวิญญาณ"},
    {"name": "☠️ ผีอาวุโส", "color": discord.Color.from_rgb(44, 62, 80), "permissions": perm_member, "desc": "วิญญาณต้องห้ามโบราณ"},

    # --- อาชีพพิเศษ ---
    {"name": "🔎 นักสืบ", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผู้สืบหาความจริง"},
    {"name": "⭐ นักสืบอาวุโส", "color": discord.Color.from_rgb(41, 128, 185), "permissions": perm_member, "desc": "นักสืบผู้รับคดีลับ"},
    {"name": "🕵️ นักสืบอาถรรพ์", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ผู้เชี่ยวชาญคดีเหนือธรรมชาติ"},
    {"name": "📸 นักข่าว", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้ติดตามและทำข่าว"},
    {"name": "🧑‍⚕️ แพทย์", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "หมอชันสูตรและชันสูตรศพ"},
    {"name": "⛪ นักบวช", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ประกอบพิธีกรรมทางศาสนา"},
    {"name": "🧙 ผู้เชี่ยวชาญเรื่องวิญญาณ", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ปราบและสื่อสารกับวิญญาณ"},

    # --- ทีมงาน ---
    {"name": "🎙️ กรรมการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้ตรวจใบสมัครและสัมภาษณ์"},
    {"name": "🧩 ทีมเนื้อเรื่อง", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ผู้สร้างคดีและปริศนาในโรงแรม"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้ดูแลเบื้องหลังและประวัติโรงแรม"},
    {"name": "🗺️ Builder", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_staff, "desc": "ทีมสร้างสิ่งก่อสร้างในเกม"},
    {"name": "🔨 Moderator", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_staff, "desc": "ผู้ดูแลระเบียบทั่วไป"},
    {"name": "🔐 Staff", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_staff, "desc": "ทีมงานดูแลระบบทั้งหมด"},
    {"name": "👑 ผู้บริหาร", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_admin, "desc": "ผู้บริหารระดับสูง"},
    {"name": "👑 ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "ผู้สร้าง/เจ้าของเซิร์ฟเวอร์"}
]

# ----------------------------------------------------
# 2. ฟังก์ชันช่วยสร้างช่องอย่างปลอดภัย (Safe Creation)
# ----------------------------------------------------
async def safe_create_category(guild, name, overwrites=None):
    kw = {"overwrites": overwrites} if isinstance(overwrites, dict) else {}
    for _ in range(5):
        try:
            cat = await guild.create_category(name, **kw)
            print(f"✅ สร้างหมวดหมู่: {name}")
            await asyncio.sleep(0.8)
            return cat
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] หมวดหมู่ {name} รอ {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
            else:
                print(f"❌ ไม่สามารถสร้างหมวดหมู่ {name} ได้: {e}")
                return None
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดไม่คาดคิดที่หมวดหมู่ {name}: {e}")
            return None
    return None

async def safe_create_text(category, name, overwrites=None):
    if not category:
        print(f"⚠️ ข้ามการสร้างช่องข้อความ {name} เนื่องจากไม่มีหมวดหมู่")
        return None
    kw = {"overwrites": overwrites} if isinstance(overwrites, dict) else {}
    for _ in range(5):
        try:
            ch = await category.create_text_channel(name, **kw)
            print(f"  └─ 💬 สร้างช่องข้อความ: {name}")
            await asyncio.sleep(0.8)
            return ch
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ช่องข้อความ {name} รอ {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
            else:
                print(f"❌ ไม่สามารถสร้างช่องข้อความ {name} ได้: {e}")
                return None
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดไม่คาดคิดที่ช่อง {name}: {e}")
            return None
    return None

async def safe_create_voice(category, name, overwrites=None):
    if not category:
        print(f"⚠️ ข้ามการสร้างช่องเสียง {name} เนื่องจากไม่มีหมวดหมู่")
        return None
    kw = {"overwrites": overwrites} if isinstance(overwrites, dict) else {}
    for _ in range(5):
        try:
            vc = await category.create_voice_channel(name, **kw)
            print(f"  └─ 🔊 สร้างช่องเสียง: {name}")
            await asyncio.sleep(0.8)
            return vc
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ช่องเสียง {name} รอ {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
            else:
                print(f"❌ ไม่สามารถสร้างช่องเสียง {name} ได้: {e}")
                return None
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดไม่คาดคิดที่ช่องเสียง {name}: {e}")
            return None
    return None

def build_overwrites(everyone, allowed_roles=None, denied_roles=None, read_only=False):
    ow = {}
    if everyone:
        if allowed_roles is None and denied_roles is None:
            ow[everyone] = discord.PermissionOverwrite(view_channel=True)
        else:
            ow[everyone] = discord.PermissionOverwrite(view_channel=False)

    if allowed_roles:
        for r in allowed_roles:
            if r is not None:
                if read_only:
                    ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=False, connect=True)
                else:
                    ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True, speak=True)

    if denied_roles:
        for r in denied_roles:
            if r is not None:
                ow[r] = discord.PermissionOverwrite(view_channel=False)

    return ow

# ----------------------------------------------------
# 3. คำสั่งระบบทำงาน
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() in ["เริ่มงาน", "เริ่มต้น"]:
        if message.author.id not in ALLOWED_USER_IDS:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"⏳ **กำลังดำเนินการสร้างโครงสร้าง {NEW_SERVER_NAME}...**\n*(ระบบกำลังทำงาน ตรวจสอบ Log บน Railway ได้เลย)*")

        try:
            # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
            try:
                await guild.edit(name=NEW_SERVER_NAME)
            except Exception as e:
                print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

            # 2. ลบช่องเดิมทั้งหมด
            print("--- เริ่มลบช่องเดิม ---")
            for channel in list(guild.channels):
                try:
                    await channel.delete()
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"ลบช่อง {channel.name} ไม่สำเร็จ: {e}")

            # 3. ลบยศเดิมทั้งหมด
            print("--- เริ่มลบยศเดิม ---")
            for role in list(guild.roles):
                if role.is_default() or role.managed:
                    continue
                try:
                    await role.delete()
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"ลบยศ {role.name} ไม่สำเร็จ: {e}")

            # 4. สร้างยศใหม่ตามลำดับ
            print("--- เริ่มสร้างยศใหม่ ---")
            created_roles = {}
            for role_info in reversed(ROLES_DATA):
                while True:
                    try:
                        role_obj = await guild.create_role(
                            name=role_info["name"],
                            color=role_info["color"],
                            permissions=role_info["permissions"],
                            hoist=True
                        )
                        created_roles[role_info["name"]] = role_obj
                        print(f"สร้างยศสำเร็จ: {role_info['name']}")
                        await asyncio.sleep(0.4)
                        break
                    except discord.HTTPException as e:
                        if e.status == 429:
                            retry_after = getattr(e, 'retry_after', 5.0)
                            await asyncio.sleep(retry_after + 0.5)
                        else:
                            print(f"สร้างยศ {role_info['name']} ไม่สำเร็จ: {e}")
                            break

            everyone = guild.default_role

            def get_r(name): return created_roles.get(name)

            # ยศผู้เล่น
            r_visitor = get_r("👤 ผู้มาเยือน")
            r_applicant = get_r("📝 ผู้สมัคร")
            r_guest = get_r("🧳 แขก")
            r_vip = get_r("⭐ VIP")

            # ยศพนักงาน
            r_receptionist = get_r("🛎️️ พนักงานต้อนรับ")
            r_maid = get_r("🧹 แม่บ้าน")
            r_chef = get_r("👨‍🍳 เชฟ")
            r_technician = get_r("🛠️ ช่าง")
            r_security = get_r("🛡️ รปภ.")
            r_manager = get_r("👔 ผู้จัดการ")
            r_owner_hotel = get_r("👑 เจ้าของโรงแรม")

            # ยศผี
            r_ghost = get_r("👻 ผี")
            r_ghost_hotel = get_r("🕯️ ผีประจำโรงแรม")
            r_ghost_wrath = get_r("🌑 วิญญาณอาฆาต")
            r_ghost_keeper = get_r("👑 วิญญาณผู้ดูแล")
            r_ghost_senior = get_r("☠️ ผีอาวุโส")

            # ยศอาชีพพิเศษ
            r_detective = get_r("🔎 นักสืบ")
            r_senior_det = get_r("⭐ นักสืบอาวุโส")
            r_occult_det = get_r("🕵️ นักสืบอาถรรพ์")
            r_reporter = get_r("📸 นักข่าว")
            r_doctor = get_r("🧑‍⚕️ แพทย์")
            r_priest = get_r("⛪ นักบวช")
            r_ghost_expert = get_r("🧙 ผู้เชี่ยวชาญเรื่องวิญญาณ")

            # ยศทีมงาน
            r_interviewer = get_r("🎙️ กรรมการ")
            r_story = get_r("🧩 ทีมเนื้อเรื่อง")
            r_lore = get_r("📜 Lore Team")
            r_builder = get_r("🗺️ Builder")
            r_mod = get_r("🔨 Moderator")
            r_staff = get_r("🔐 Staff")
            r_exec = get_r("👑 ผู้บริหาร")
            r_founder = get_r("👑 ผู้ก่อตั้ง")

            if r_founder and message.author in guild.members:
                try:
                    await message.author.add_roles(r_founder)
                except:
                    pass

            staff_roles = [r for r in [r_interviewer, r_story, r_lore, r_builder, r_mod, r_staff, r_exec, r_founder] if r]
            staff_and_detective = [r for r in [r_detective, r_senior_det, r_occult_det] + staff_roles if r]
            all_staff_and_ghost = [r for r in [r_ghost, r_ghost_hotel, r_ghost_wrath, r_ghost_keeper, r_ghost_senior] + staff_roles if r]
            employee_roles = [r for r in [r_receptionist, r_maid, r_chef, r_technician, r_security, r_manager, r_owner_hotel] + staff_roles if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Haunted Hotel Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🏨 ศูนย์กลางโรงแรม ---
            cat_center = await safe_create_category(guild, "🏨 ศูนย์กลางโรงแรม", overwrites=build_overwrites(everyone, read_only=True))
            if cat_center:
                for ch in ["📢・ประกาศโรงแรม", "📖・กฎของโรงแรม", "🗺️・แผนผังโรงแรม", "📜・ประวัติโรงแรม", "🏨・ข้อมูลโรงแรม", "🕯️・เรื่องเล่าของโรงแรม", "👻・ระบบผีและวิญญาณ", "🔑・ระบบห้องพัก", "🎭・ระบบ-roleplay"]:
                    await safe_create_text(cat_center, ch)

            # --- 📝 สมัครเข้าพัก / สมัครตัวละคร ---
            cat_apply = await safe_create_category(guild, "📝 สมัครเข้าพัก / สมัครตัวละคร")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครตัวละคร", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "🪪・ข้อมูลตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "🛏️・เลือกห้องพัก", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "💼・เลือกอาชีพ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "👻・สมัครเป็นวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⏳・รอตรวจสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจสอบใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการอนุมัติ", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip], read_only=True))
                await safe_create_text(cat_apply, "❌・ต้องแก้ไขใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🛎️ ล็อบบี้โรงแรม ---
            cat_lobby = await safe_create_category(guild, "🛎️ ล็อบบี้โรงแรม")
            if cat_lobby:
                await safe_create_voice(cat_lobby, "🛎️・ล็อบบี้", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + staff_roles))
                await safe_create_voice(cat_lobby, "🔑・เคาน์เตอร์ต้อนรับ", overwrites=build_overwrites(everyone, allowed_roles=employee_roles))
                await safe_create_voice(cat_lobby, "🧳・รับฝากสัมภาระ", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + employee_roles))
                await safe_create_voice(cat_lobby, "💳・ชำระค่าห้อง", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + employee_roles))
                await safe_create_voice(cat_lobby, "🔔・เรียกพนักงาน", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + employee_roles))
                await safe_create_voice(cat_lobby, "🕰️・นาฬิกาโบราณ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_lobby, "🪞・โถงกระจก", overwrites=build_overwrites(everyone))

            # --- 🛏️ ห้องพักแขก ---
            cat_rooms = await safe_create_category(guild, "🛏️️ ห้องพักแขก")
            if cat_rooms:
                for vc in ["🛏️・ชั้น-1", "🛏️・ชั้น-2", "🛏️・ชั้น-3", "🛏️・ชั้น-4", "🛏️・ชั้น-5"]:
                    await safe_create_voice(cat_rooms, vc, overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + staff_roles))
                await safe_create_voice(cat_rooms, "🔑・ห้อง-vip", overwrites=build_overwrites(everyone, allowed_roles=[r_vip] + staff_roles))
                await safe_create_voice(cat_rooms, "🌹・ห้องฮันนีมูน", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + staff_roles))
                await safe_create_voice(cat_rooms, "🚪・ห้องต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_voice(cat_rooms, "👻・ห้องหมายเลข-13", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_rooms, "🕯️・ห้องร้าง", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_rooms, "🚪・โถงทางเดิน", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + staff_roles))

            # --- 🍽️ สิ่งอำนวยความสะดวก ---
            cat_facility = await safe_create_category(guild, "🍽️ สิ่งอำนวยความสะดวก", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip] + staff_roles))
            if cat_facility:
                for vc in ["🍽️・ห้องอาหาร", "☕・คาเฟ่", "🍸・บาร์", "🏊・สระว่ายน้ำ", "🏋️・ห้องออกกำลังกาย", "📚・ห้องสมุด", "🎹・ห้องดนตรี", "🎭・ห้องจัดเลี้ยง", "🌳・สวนโรงแรม"]:
                    await safe_create_voice(cat_facility, vc)

            # --- 👔 พนักงานโรงแรม ---
            cat_staff_emp = await safe_create_category(guild, "👔 พนักงานโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=employee_roles))
            if cat_staff_emp:
                await safe_create_voice(cat_staff_emp, "🛎️・ฝ่ายต้อนรับ", overwrites=build_overwrites(everyone, allowed_roles=[r_receptionist] + staff_roles))
                await safe_create_voice(cat_staff_emp, "🧹・แม่บ้าน", overwrites=build_overwrites(everyone, allowed_roles=[r_maid] + staff_roles))
                await safe_create_voice(cat_staff_emp, "👨‍🍳・ห้องครัว", overwrites=build_overwrites(everyone, allowed_roles=[r_chef] + staff_roles))
                await safe_create_voice(cat_staff_emp, "🛠️・ฝ่ายซ่อมบำรุง", overwrites=build_overwrites(everyone, allowed_roles=[r_technician] + staff_roles))
                await safe_create_voice(cat_staff_emp, "🛡️・รักษาความปลอดภัย", overwrites=build_overwrites(everyone, allowed_roles=[r_security] + staff_roles))
                await safe_create_voice(cat_staff_emp, "📋・ตารางงาน")
                await safe_create_voice(cat_staff_emp, "📢・คำสั่งผู้จัดการ", overwrites=build_overwrites(everyone, allowed_roles=[r_manager, r_owner_hotel] + staff_roles))
                await safe_create_voice(cat_staff_emp, "🔐・ห้องพักพนักงาน")

            # --- 👻 โลกวิญญาณ ---
            cat_ghost_world = await safe_create_category(guild, "👻 โลกวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_ghost, r_ghost_hotel, r_ghost_wrath, r_ghost_keeper, r_ghost_senior] + staff_roles))
            if cat_ghost_world:
                await safe_create_voice(cat_ghost_world, "👻・ห้องโถงวิญญาณ")
                await safe_create_voice(cat_ghost_world, "🕯️・โลกหลังความตาย")
                await safe_create_voice(cat_ghost_world, "📜・ประวัติวิญญาณ")
                await safe_create_voice(cat_ghost_world, "🪦・สุสานเก่า")
                await safe_create_voice(cat_ghost_world, "🌫️・หมอกนิรันดร์")
                await safe_create_voice(cat_ghost_world, "🩸・ห้องแห่งความทรงจำ", overwrites=build_overwrites(everyone, allowed_roles=[r_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_ghost_world, "🔐・วิญญาณต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_ghost_senior] + staff_roles))
                await safe_create_voice(cat_ghost_world, "👻・ห้องรวมวิญญาณ")

            # --- 🔎 ห้องสืบสวน ---
            cat_detective = await safe_create_category(guild, "🔎 ห้องสืบสวน", overwrites=build_overwrites(everyone, allowed_roles=staff_and_detective))
            if cat_detective:
                await safe_create_voice(cat_detective, "🔎・สำนักงานนักสืบ")
                await safe_create_voice(cat_detective, "📂・แฟ้มเหตุการณ์")
                await safe_create_voice(cat_detective, "🧩・กระดานปริศนา")
                await safe_create_voice(cat_detective, "📸・ภาพหลักฐาน")
                await safe_create_voice(cat_detective, "🕵️️・ผู้ต้องสงสัย")
                await safe_create_voice(cat_detective, "📜・บันทึกคำให้การ")
                await safe_create_voice(cat_detective, "🔐・คดีลับของโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=[r_senior_det] + staff_roles))
                await safe_create_voice(cat_detective, "🔎・ห้องประชุมนักสืบ")

            # --- 🩸 คดีและเหตุการณ์ประหลาด ---
            cat_cases = await safe_create_category(guild, "🩸 คดีและเหตุการณ์ประหลาด")
            if cat_cases:
                await safe_create_voice(cat_cases, "📢・ประกาศเหตุการณ์", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cases, "👻・พบเห็นวิญญาณ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cases, "🩸・เหตุการณ์ผิดปกติ", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_detective] + staff_roles))
                await safe_create_voice(cat_cases, "🚪・ห้องที่เปิดเอง", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_detective] + staff_roles))
                await safe_create_voice(cat_cases, "🪞・เหตุการณ์ในกระจก", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_detective] + staff_roles))
                await safe_create_voice(cat_cases, "🔔・เสียงระฆังยามเที่ยงคืน", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_ghost, r_detective] + staff_roles))
                await safe_create_voice(cat_cases, "🕯️・คดีคนหาย", overwrites=build_overwrites(everyone, allowed_roles=staff_and_detective))
                await safe_create_voice(cat_cases, "🧩・ปริศนาประจำโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=[r_detective, r_story] + staff_roles))
                await safe_create_voice(cat_cases, "✅・คดีที่คลี่คลาย", overwrites=build_overwrites(everyone))

            # --- 🌑 ชั้นต้องห้าม ---
            cat_forbidden = await safe_create_category(guild, "🌑 ชั้นต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_ghost, r_detective, r_story] + staff_roles))
            if cat_forbidden:
                for vc in ["🚪・บันไดลับ", "🕯️・ชั้นที่-6", "🩸・ห้อง-666", "🪞・ห้องกระจก-ต้องห้าม", "🪦・ห้องเก็บศพเก่า"]:
                    await safe_create_voice(cat_forbidden, vc)
                await safe_create_voice(cat_forbidden, "📜・บันทึกผู้เสียชีวิต", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_forbidden, "🔐・ความลับของเจ้าของโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_forbidden, "🌑・ชั้นต้องห้าม")

            # --- 🎭 EVENT | เหตุการณ์โรงแรม ---
            cat_event = await safe_create_category(guild, "🎭 EVENT | เหตุการณ์โรงแรม", overwrites=build_overwrites(everyone))
            if cat_event:
                for ch in ["📢・ประกาศ-event", "📜・ตาราง-event", "🎃・คืนฮาโลวีน", "🕯️・คืนแห่งวิญญาณ", "🔔・เที่ยงคืนต้องห้าม", "🩸・คดีพิเศษ"]:
                    await safe_create_text(cat_event, ch)
                await safe_create_text(cat_event, "👻・คืนล่าผี")
                await safe_create_voice(cat_event, "🔊・พื้นที่-event")

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "👻・เรื่องผีจากสมาชิก", "📊・โหวต", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "🎵・ห้องฟังเพลง", "💤・afk"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff")
                await safe_create_text(cat_staff_zone, "📂・ข้อมูลตัวละคร")
                report_channel = await safe_create_text(cat_staff_zone, "📝・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "👻・จัดการตัวละครผี", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🏨・จัดการโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🗺️・จัดการแผนที่", overwrites=build_overwrites(everyone, allowed_roles=[r_builder, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・เขียน-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🩸・สร้างคดี", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🧩・จัดการปริศนา", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🎭・วางแผน-event", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📋・บันทึกเหตุการณ์")
                await safe_create_voice(cat_staff_zone, "🔊・ประชุม-staff")

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="👻 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Haunted Hotel RP",
                        description="โครงสร้างโรงแรมผีสิง ล็อบบี้ ห้องพัก วิญญาณ นักสืบ ชั้นต้องห้าม คดีประหลาด และศูนย์บัญชาการติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.purple()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA[:25]]) + "\n...และยศอื่นๆ ครบถ้วน"
                    embed.add_field(name="🎭 รายชื่อยศหลัก", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมโรงแรมผีสิง เสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Haunted Hotel RP เสร็จสิ้นสมบูรณ์ ===")

        except Exception as err:
            print(f"❌ เกิดข้อผิดพลาดร้ายแรงระหว่างทำงาน: {err}")
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f"บอท {bot.user} ออนไลน์พร้อมใช้งานแล้ว!")

async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ไม่พบ TOKEN ในระบบ กรุณาตรวจสอบ Environment Variable บน Railway")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
