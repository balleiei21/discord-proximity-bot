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
NEW_SERVER_NAME = "Minecraft Hotel & Cafe of Spirits RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Hotel & Cafe of Spirits Theme)
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
    {"name": "🧳 แขก", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "คนเป็นที่เข้ามาพักผ่อนในโรงแรม"},
    {"name": "⭐ แขก VIP", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "แขกคนสำคัญของโรงแรม"},

    # --- วิญญาณ ---
    {"name": "👻 วิญญาณหน้าใหม่", "color": discord.Color.from_rgb(218, 225, 231), "permissions": perm_member, "desc": "วิญญาณที่เพิ่งมาถึงโรงแรม"},
    {"name": "🕯️ วิญญาณ", "color": discord.Color.from_rgb(189, 195, 199), "permissions": perm_member, "desc": "วิญญาณที่มีเรื่องค้างคาในใจ"},
    {"name": "🌙 วิญญาณอาวุโส", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "วิญญาณที่อยู่อาศัยในโรงแรมมานาน"},
    {"name": "🖤 วิญญาณอาฆาต", "color": discord.Color.from_rgb(146, 43, 33), "permissions": perm_member, "desc": "วิญญาณที่มีความแค้นหรืออดีตมืดมน"},
    {"name": "🕊️ วิญญาณใกล้ไปสู่สุขคติ", "color": discord.Color.from_rgb(235, 245, 251), "permissions": perm_member, "desc": "วิญญาณที่พร้อมจะบอกลาและปล่อยวาง"},

    # --- พนักงาน ---
    {"name": "🛎️ พนักงานต้อนรับ", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "พนักงานดูแลเคาน์เตอร์และต้อนรับแขก"},
    {"name": "☕ บาริสต้า", "color": discord.Color.from_rgb(160, 100, 57), "permissions": perm_member, "desc": "ผู้ชงเครื่องดื่มประจำคาเฟ่"},
    {"name": "🍰 พนักงานทำขนม", "color": discord.Color.from_rgb(236, 112, 99), "permissions": perm_member, "desc": "ผู้รังสรรค์ของหวานประจำคาเฟ่"},
    {"name": "👨‍🍳 เชฟ", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_member, "desc": "พ่อครัวประกอบอาหาร"},
    {"name": "🧹 แม่บ้าน", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ผู้ดูแลความสะอาดของห้องพัก"},
    {"name": "🛠️ ช่างซ่อม", "color": discord.Color.from_rgb(120, 144, 156), "permissions": perm_member, "desc": "ฝ่ายบำรุงรักษาอาคาร"},
    {"name": "🛡️ รปภ.", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "ผู้รักษาความสงบเรียบร้อย"},
    {"name": "👔 ผู้จัดการ", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ผู้บริหารจัดการระบบโรงแรม"},
    {"name": "👑 เจ้าของโรงแรม", "color": discord.Color.from_rgb(212, 172, 13), "permissions": perm_member, "desc": "ผู้ดูแลโรงแรมและคาเฟ่แห่งวิญญาณ"},

    # --- อาชีพพิเศษ ---
    {"name": "📖 นักเล่าเรื่อง", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้ถ่ายทอดความทรงจำและเรื่องราว"},
    {"name": "🔮 หมอดู", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ทำนายชะตาและมองเห็นสิ่งที่มองไม่เห็น"},
    {"name": "⛪ นักบวช", "color": discord.Color.from_rgb(244, 208, 63), "permissions": perm_member, "desc": "ผู้ประกอบพิธีกรรมและส่งวิญญาณ"},
    {"name": "👻 ผู้สื่อสารกับวิญญาณ", "color": discord.Color.from_rgb(93, 173, 226), "permissions": perm_member, "desc": "ร่างทรงหรือผู้ที่สื่อสารกับผีได้"},
    {"name": "🕵️ นักสืบ", "color": discord.Color.from_rgb(84, 110, 122), "permissions": perm_member, "desc": "ผู้สืบหาเบาะแสและอดีตที่หายไป"},
    {"name": "📸 นักข่าว", "color": discord.Color.from_rgb(46, 134, 193), "permissions": perm_member, "desc": "ผู้บันทึกข่าวสารและเรื่องราว"},

    # --- ทีมงาน ---
    {"name": "🎙️ กรรมการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้ตรวจใบสมัครและสัมภาษณ์"},
    {"name": "🧩 ทีมเนื้อเรื่อง", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ผู้สร้างเรื่องราวและเหตุการณ์ของวิญญาณ"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้ดูแลความลับและเบื้องหลังของโรงแรม"},
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
            r_vip_guest = get_r("⭐ แขก VIP")

            # ยศวิญญาณ
            r_new_ghost = get_r("👻 วิญญาณหน้าใหม่")
            r_ghost = get_r("🕯️ วิญญาณ")
            r_snr_ghost = get_r("🌙 วิญญาณอาวุโส")
            r_wrath_ghost = get_r("🖤 วิญญาณอาฆาต")
            r_peace_ghost = get_r("🕊️ วิญญาณใกล้ไปสู่สุขคติ")

            # ยศพนักงาน
            r_receptionist = get_r("🛎️ พนักงานต้อนรับ")
            r_barista = get_r("☕ บาริสต้า")
            r_baker = get_r("🍰 พนักงานทำขนม")
            r_chef = get_r("👨‍🍳 เชฟ")
            r_maid = get_r("🧹 แม่บ้าน")
            r_technician = get_r("🛠️ ช่างซ่อม")
            r_guard = get_r("🛡️ รปภ.")
            r_manager = get_r("👔 ผู้จัดการ")
            r_hotel_owner = get_r("👑 เจ้าของโรงแรม")

            # ยศอาชีพพิเศษ
            r_storyteller = get_r("📖 นักเล่าเรื่อง")
            r_fortune_teller = get_r("🔮 หมอดู")
            r_priest = get_r("⛪ นักบวช")
            r_medium = get_r("👻 ผู้สื่อสารกับวิญญาณ")
            r_detective = get_r("🕵️ นักสืบ")
            r_reporter = get_r("📸 นักข่าว")

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
            ghost_roles = [r for r in [r_new_ghost, r_ghost, r_snr_ghost, r_wrath_ghost, r_peace_ghost] + staff_roles if r]
            staff_hotel_roles = [r for r in [r_receptionist, r_barista, r_baker, r_chef, r_maid, r_technician, r_guard, r_manager, r_hotel_owner] + staff_roles if r]
            living_roles = [r for r in [r_guest, r_vip_guest, r_storyteller, r_fortune_teller, r_priest, r_medium, r_detective, r_reporter] + staff_roles if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Hotel & Cafe of Spirits Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🏨 ศูนย์กลางโรงแรม ---
            cat_center = await safe_create_category(guild, "🏨 ศูนย์กลางโรงแรม", overwrites=build_overwrites(everyone, read_only=True))
            if cat_center:
                for ch in ["📢・ประกาศโรงแรม", "📖・กฎของโรงแรม", "🗺️・แผนผังโรงแรม", "📜・เรื่องราวของโรงแรม", "👻・ระบบวิญญาณ", "☕・ระบบคาเฟ่", "🕯️・ระบบการระบาย", "📚・lore-ของโลก"]:
                    await safe_create_text(cat_center, ch)

            # --- 📝 สมัครตัวละคร ---
            cat_apply = await safe_create_category(guild, "📝 สมัครตัวละคร")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครตัวละคร", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "🪪・ข้อมูลตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "👻・สมัครเป็นวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "👤・สมัครเป็นคนเป็น", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📜・ประวัติก่อนเสียชีวิต", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "🕯️・เรื่องที่ยังค้างคา", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "💭・เหตุผลที่ยังอยู่บนโลก", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⏳・รอตรวจสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "👻・ห้องสัมภาษณ์วิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))

            # --- 🏨 โซนโรล — โรงแรม ---
            cat_hotel_rp = await safe_create_category(guild, "🏨 โซนโรล — โรงแรม")
            if cat_hotel_rp:
                await safe_create_voice(cat_hotel_rp, "🛎️・ล็อบบี้โรงแรม", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🔑・เคาน์เตอร์ต้อนรับ", overwrites=build_overwrites(everyone, allowed_roles=[r_receptionist, r_manager, r_hotel_owner] + staff_roles))
                await safe_create_voice(cat_hotel_rp, "🧳・ห้องรับฝากสัมภาระ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🛋️・ห้องรับแขก", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🕰️・โถงทางเดิน", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🪞・โถงกระจก", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🛏️・ห้องพัก-101", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip_guest] + staff_roles))
                await safe_create_voice(cat_hotel_rp, "🛏️・ห้องพัก-202", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip_guest] + staff_roles))
                await safe_create_voice(cat_hotel_rp, "🛏️・ห้องพัก-303", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip_guest] + staff_roles))
                await safe_create_voice(cat_hotel_rp, "🌙・ห้องพักวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
                await safe_create_voice(cat_hotel_rp, "🔑・ห้องพัก-vip", overwrites=build_overwrites(everyone, allowed_roles=[r_vip_guest, r_hotel_owner] + staff_roles))
                await safe_create_voice(cat_hotel_rp, "🕯️・ห้องพักต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_lore, r_exec, r_founder]))
                await safe_create_voice(cat_hotel_rp, "🌃・ระเบียงโรงแรม", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🌳・สวนหลังโรงแรม", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_hotel_rp, "🌧️・ศาลานั่งเล่น", overwrites=build_overwrites(everyone))

            # --- ☕ โซนโรล — คาเฟ่ ---
            cat_cafe_rp = await safe_create_category(guild, "☕ โซนโรล — คาเฟ่")
            if cat_cafe_rp:
                await safe_create_voice(cat_cafe_rp, "☕・เคาน์เตอร์คาเฟ่", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🍰・โต๊ะขนมหวาน", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🪑・โต๊ะริมหน้าต่าง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🌧️・โต๊ะวันฝนตก", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🌙・โต๊ะกลางคืน", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🕯️・โต๊ะสำหรับวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
                await safe_create_voice(cat_cafe_rp, "💭・มุมระบายความรู้สึก", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "📖・มุมเล่าเรื่อง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🎹・มุมดนตรี", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "🪟・มุมชมวิว", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_cafe_rp, "☕・โต๊ะพูดคุยส่วนตัว", overwrites=build_overwrites(everyone, allowed_roles=[r_guest, r_vip_guest] + ghost_roles))
                await safe_create_voice(cat_cafe_rp, "🌌・คาเฟ่ยามเที่ยงคืน", overwrites=build_overwrites(everyone))

            # --- 👻 ห้องของเหล่าวิญญาณ ---
            cat_ghost_zone = await safe_create_category(guild, "👻 ห้องของเหล่าวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
            if cat_ghost_zone:
                await safe_create_voice(cat_ghost_zone, "👻・ห้องรวมวิญญาณ")
                await safe_create_voice(cat_ghost_zone, "🕯️・ห้องระบาย")
                await safe_create_voice(cat_ghost_zone, "💭・ห้องเล่าเรื่องชีวิต")
                await safe_create_voice(cat_ghost_zone, "😭・ห้องร้องไห้")
                await safe_create_voice(cat_ghost_zone, "💔・ห้องเรื่องที่ค้างคา")
                await safe_create_voice(cat_ghost_zone, "📜・ห้องเล่าความทรงจำ")
                await safe_create_voice(cat_ghost_zone, "🌙・ห้องคุยยามดึก")
                await safe_create_voice(cat_ghost_zone, "🫂・ห้องปลอบโยน")
                await safe_create_voice(cat_ghost_zone, "🕊️・ห้องบอกลา")
                await safe_create_voice(cat_ghost_zone, "🔐・ห้องส่วนตัวของวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_snr_ghost, r_story] + staff_roles))

            # --- 💭 ห้องระบายและเล่าเรื่อง ---
            cat_vent_zone = await safe_create_category(guild, "💭 ห้องระบายและเล่าเรื่อง")
            if cat_vent_zone:
                for vc in ["🫂・มานั่งคุยกัน", "💭・วันนี้ฉันรู้สึก...", "😭・ขอระบายหน่อย", "📖・เรื่องราวของฉัน", "🕯️・เรื่องที่ไม่เคยบอกใคร", "💔・เรื่องที่ยังลืมไม่ได้", "🌧️・คืนที่แสนเศร้า", "🌤️・เรื่องราวดี-ๆ", "🫶・กำลังใจจากคนแปลกหน้า"]:
                    await safe_create_voice(cat_vent_zone, vc, overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_vent_zone, "🕊️・คำพูดสุดท้าย", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_lore] + staff_roles))

            # --- 🕯️ ห้องแห่งความทรงจำ ---
            cat_memory = await safe_create_category(guild, "🕯️ ห้องแห่งความทรงจำ")
            if cat_memory:
                await safe_create_voice(cat_memory, "📸・ภาพในอดีต", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
                for vc in ["🏠・บ้านหลังเก่า", "👨‍👩‍👧・ครอบครัว", "❤️・คนที่รัก", "💔・ความสัมพันธ์ที่จบลง", "🎂・วันเกิดครั้งสุดท้าย", "🌧️・วันที่เสียชีวิต", "🕯️・ความทรงจำสุดท้าย"]:
                    await safe_create_voice(cat_memory, vc, overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_lore] + ghost_roles))

            # --- 🌙 โลกของคนเป็น ---
            cat_living_world = await safe_create_category(guild, "🌙 โลกของคนเป็น")
            if cat_living_world:
                await safe_create_voice(cat_living_world, "🏙️・ถนนหน้าโรงแรม", overwrites=build_overwrites(everyone, allowed_roles=living_roles))
                await safe_create_voice(cat_living_world, "🛍️・ร้านค้าใกล้โรงแรม", overwrites=build_overwrites(everyone, allowed_roles=living_roles))
                await safe_create_voice(cat_living_world, "🚶・สวนสาธารณะ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_living_world, "☕・คาเฟ่ข้างโรงแรม", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_living_world, "🏠・บ้านของแขก", overwrites=build_overwrites(everyone, allowed_roles=living_roles))
                await safe_create_voice(cat_living_world, "🚉・สถานีรถไฟ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_living_world, "🌃・เมืองยามค่ำคืน", overwrites=build_overwrites(everyone))

            # --- 🕯️ เรื่องราวของวิญญาณ ---
            cat_ghost_stories = await safe_create_category(guild, "🕯️ เรื่องราวของวิญญาณ")
            if cat_ghost_stories:
                await safe_create_voice(cat_ghost_stories, "📖・เรื่องเล่าวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
                await safe_create_voice(cat_ghost_stories, "👻・วิญญาณหน้าใหม่", overwrites=build_overwrites(everyone, allowed_roles=ghost_roles))
                await safe_create_voice(cat_ghost_stories, "🕰️・วิญญาณที่อยู่นานที่สุด", overwrites=build_overwrites(everyone, allowed_roles=[r_snr_ghost] + staff_roles))
                await safe_create_voice(cat_ghost_stories, "🩸・วิญญาณที่มีอดีตมืดมน", overwrites=build_overwrites(everyone, allowed_roles=[r_wrath_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_ghost_stories, "💔・วิญญาณที่รอใครบางคน", overwrites=build_overwrites(everyone, allowed_roles=[r_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_ghost_stories, "🕊️・วิญญาณที่กำลังจะไป", overwrites=build_overwrites(everyone, allowed_roles=[r_peace_ghost, r_story] + staff_roles))
                await safe_create_voice(cat_ghost_stories, "🔐・เรื่องที่ไม่ควรถูกเปิดเผย", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_lore, r_exec, r_founder]))

            # --- 🧑‍🍳 พนักงานโรงแรมและคาเฟ่ ---
            cat_staff_hotel = await safe_create_category(guild, "🧑‍🍳 พนักงานโรงแรมและคาเฟ่")
            if cat_staff_hotel:
                await safe_create_voice(cat_staff_hotel, "🛎️・ฝ่ายต้อนรับ", overwrites=build_overwrites(everyone, allowed_roles=[r_receptionist, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "☕・บาริสต้า", overwrites=build_overwrites(everyone, allowed_roles=[r_barista, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "🍰・ห้องทำขนม", overwrites=build_overwrites(everyone, allowed_roles=[r_baker, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "👨‍🍳・ห้องครัว", overwrites=build_overwrites(everyone, allowed_roles=[r_chef, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "🧹・แม่บ้าน", overwrites=build_overwrites(everyone, allowed_roles=[r_maid, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "🛠️・ฝ่ายซ่อมบำรุง", overwrites=build_overwrites(everyone, allowed_roles=[r_technician, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "🛡️・รักษาความปลอดภัย", overwrites=build_overwrites(everyone, allowed_roles=[r_guard, r_manager] + staff_roles))
                await safe_create_voice(cat_staff_hotel, "📋・ห้องพักพนักงาน", overwrites=build_overwrites(everyone, allowed_roles=staff_hotel_roles))
                await safe_create_voice(cat_staff_hotel, "👔・ห้องผู้จัดการ", overwrites=build_overwrites(everyone, allowed_roles=[r_manager, r_hotel_owner] + staff_roles))

            # --- 🎭 EVENT | เรื่องราว ---
            cat_events = await safe_create_category(guild, "🎭 EVENT | เรื่องราว")
            if cat_events:
                await safe_create_text(cat_events, "📢・ประกาศ event", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_events, "📜・ตาราง event", overwrites=build_overwrites(everyone, read_only=True))
                for vc in ["☕・คืนคาเฟ่แห่งความทรงจำ", "👻・คืนรวมวิญญาณ", "🕯️・คืนเล่าเรื่อง", "🌧️・คืนฝนตก", "🌙・คาเฟ่เที่ยงคืน", "🕊️・คืนแห่งการบอกลา"]:
                    await safe_create_voice(cat_events, vc, overwrites=build_overwrites(everyone))

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "📖・เล่าเรื่องนอกโรล", "🎮・หาเพื่อนเล่นเกม"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "🎵・ห้องฟังเพลง", "💤・afk"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff")
                report_channel = await safe_create_text(cat_staff_zone, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "👻・ข้อมูลวิญญาณ", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📖・ประวัติตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・เขียน-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "💭・จัดการเรื่องราว", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🎭・วางแผน-event", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🗺️・จัดการแผนที่", overwrites=build_overwrites(everyone, allowed_roles=[r_builder, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📋・บันทึกเหตุการณ์")
                await safe_create_voice(cat_staff_zone, "🎙️・ประชุม-staff")

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="🏨☕ รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Hotel & Cafe of Spirits RP",
                        description="โครงสร้างโรงแรมคาเฟ่แห่งวิญญาณ โซนโรลเพลย์เน้นห้องเสียง พื้นที่ระบายความรู้สึก ห้องความทรงจำ และศูนย์บัญชาการติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.from_rgb(160, 100, 57)
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA[:25]]) + "\n...และยศอื่นๆ ครบถ้วน"
                    embed.add_field(name="🎭 รายชื่อยศหลัก", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมโรงแรมคาเฟ่แห่งวิญญาณ เสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Hotel & Cafe of Spirits RP เสร็จสิ้นสมบูรณ์ ===")

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
