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
NEW_SERVER_NAME = "Minecraft Talking Animals Kingdom RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Animal Kingdom Theme)
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
    # --- ผู้เล่นทั่วไป ---
    {"name": "👤 ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้เข้าชมทั่วไป"},
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครเข้าสู่สังกัด"},
    {"name": "🏙️ พลเมือง", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้อยู่อาศัยในอาณาจักร"},

    # --- เผ่าพันธุ์ ---
    {"name": "🦊 เผ่าจิ้งจอก", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "เผ่าจิ้งจอก"},
    {"name": "🐺 เผ่าหมาป่า", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "เผ่าหมาป่า"},
    {"name": "🐰 เผ่ากระต่าย", "color": discord.Color.from_rgb(241, 148, 138), "permissions": perm_member, "desc": "เผ่ากระต่าย"},
    {"name": "🐯 เผ่าเสือ", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_member, "desc": "เผ่าเสือ"},
    {"name": "🐻 เผ่าหมี", "color": discord.Color.from_rgb(120, 66, 18), "permissions": perm_member, "desc": "เผ่าหมี"},
    {"name": "🦌 เผ่ากวาง", "color": discord.Color.from_rgb(187, 143, 206), "permissions": perm_member, "desc": "เผ่ากวาง"},
    {"name": "🦅 เผ่านก", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "เผ่านก"},
    {"name": "🐍 เผ่างู", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_member, "desc": "เผ่างู"},
    {"name": "🐲 สัตว์ในตำนาน", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "เผ่าสัตว์ในตำนานพิเศษ"},

    # --- อาชีพ ---
    {"name": "🧑‍🌾 เกษตรกร", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้เพาะปลูกและกสิกรรม"},
    {"name": "⛏️ คนงานเหมือง", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้ขุดแร่และทรัพยากร"},
    {"name": "🔨 ช่างตีเหล็ก", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_member, "desc": "ผู้รังสรรค์อาวุธและชุดเกราะ"},
    {"name": "🧑‍🍳 พ่อครัว", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้ปรุงอาหาร"},
    {"name": "🧑‍⚕️ หมอ", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ผู้รักษาพยาบาล"},
    {"name": "🏹 นักล่า", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_member, "desc": "นักล่าพรานป่า"},
    {"name": "🧙 นักเวท", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ใช้เวทมนตร์"},
    {"name": "🧭 นักผจญภัย", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "นักสำรวจภารกิจ"},
    {"name": "⭐ นักผจญภัยอาวุโส", "color": discord.Color.from_rgb(243, 156, 18), "permissions": perm_member, "desc": "นักผจญภัยชั้นสูงรับงานลับ"},
    {"name": "🛡️ ทหาร", "color": discord.Color.from_rgb(41, 128, 185), "permissions": perm_member, "desc": "ทหารพิทักษ์อาณาจักร"},
    {"name": "⚔️ แม่ทัพ", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_member, "desc": "ผู้บัญชาการกองทัพ"},

    # --- ชนชั้น ---
    {"name": "🧑‍🌾 ชาวบ้าน", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "สามัญชนคนทั่วไป"},
    {"name": "🏰 อัศวิน", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "นักรบเกียรติยศแห่งราชสำนัก"},
    {"name": "⚜️ ขุนนาง", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ชนชั้นปกครองส่วนบริหาร"},
    {"name": "👑 ราชวงศ์", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "พระราชวงศ์และผู้ปกครองสูงสุด"},

    # --- ทีมงาน ---
    {"name": "🎙️ กรรมการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้ตรวจใบสมัครและสัมภาษณ์"},
    {"name": "🧩 ทีมเนื้อเรื่อง", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ผู้สร้างคดีและภารกิจ Event"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้ดูแลเบื้องหลังและประวัติศาสตร์"},
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

            # ยศพื้นฐาน
            r_visitor = get_r("👤 ผู้มาเยือน")
            r_applicant = get_r("📝 ผู้สมัคร")
            r_citizen = get_r("🏙️ พลเมือง")

            # ยศเผ่าพันธุ์
            r_fox = get_r("🦊 เผ่าจิ้งจอก")
            r_wolf = get_r("🐺 เผ่าหมาป่า")
            r_rabbit = get_r("🐰 เผ่ากระต่าย")
            r_tiger = get_r("🐯 เผ่าเสือ")
            r_bear = get_r("🐻 เผ่าหมี")
            r_deer = get_r("🦌 เผ่ากวาง")
            r_bird = get_r("🦅 เผ่านก")
            r_snake = get_r("🐍 เผ่างู")
            r_mythic = get_r("🐲 สัตว์ในตำนาน")

            # ยศอาชีพ & ชนชั้น
            r_adventurer = get_r("🧭 นักผจญภัย")
            r_senior_adv = get_r("⭐ นักผจญภัยอาวุโส")
            r_soldier = get_r("🛡️ ทหาร")
            r_general = get_r("⚔️ แม่ทัพ")
            r_nobles = get_r("⚜️ ขุนนาง")
            r_royalty = get_r("👑 ราชวงศ์")

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

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Animal Kingdom Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🏰 ศูนย์กลางอาณาจักร ---
            cat_center = await safe_create_category(guild, "🏰 ศูนย์กลางอาณาจักร", overwrites=build_overwrites(everyone, read_only=True))
            if cat_center:
                for ch in ["📢・ประกาศอาณาจักร", "📖・กฎของอาณาจักร", "🗺️・แผนที่อาณาจักร", "📜・ประวัติอาณาจักร", "👑・ราชวงศ์", "⚖️・กฎหมายอาณาจักร", "📚・lore-โลก", "🧬・ระบบเผ่าพันธุ์", "💰・ระบบเศรษฐกิจ", "🎭・ระบบ-roleplay"]:
                    await safe_create_text(cat_center, ch)

            # --- 📝 สมัครเป็นพลเมือง ---
            cat_apply = await safe_create_category(guild, "📝 สมัครเป็นพลเมือง")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครตัวละคร", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "🐾・เลือกเผ่าพันธุ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "💼・เลือกอาชีพ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⏳・รอตรวจสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจสอบใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🎙️・สัมภาษณ์ตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการอนุมัติ", overwrites=build_overwrites(everyone, allowed_roles=[r_citizen], read_only=True))
                await safe_create_text(cat_apply, "❌・ต้องแก้ไขใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🐾 เผ่าพันธุ์สัตว์ ---
            cat_tribes = await safe_create_category(guild, "🐾 เผ่าพันธุ์สัตว์")
            if cat_tribes:
                await safe_create_text(cat_tribes, "🦊・เผ่าจิ้งจอก", overwrites=build_overwrites(everyone, allowed_roles=[r_fox] + staff_roles))
                await safe_create_text(cat_tribes, "🐺・เผ่าหมาป่า", overwrites=build_overwrites(everyone, allowed_roles=[r_wolf] + staff_roles))
                await safe_create_text(cat_tribes, "🐰・เผ่ากระต่าย", overwrites=build_overwrites(everyone, allowed_roles=[r_rabbit] + staff_roles))
                await safe_create_text(cat_tribes, "🐯・เผ่าเสือ", overwrites=build_overwrites(everyone, allowed_roles=[r_tiger] + staff_roles))
                await safe_create_text(cat_tribes, "🐻・เผ่าหมี", overwrites=build_overwrites(everyone, allowed_roles=[r_bear] + staff_roles))
                await safe_create_text(cat_tribes, "🦌・เผ่ากวาง", overwrites=build_overwrites(everyone, allowed_roles=[r_deer] + staff_roles))
                await safe_create_text(cat_tribes, "🦅・เผ่านก", overwrites=build_overwrites(everyone, allowed_roles=[r_bird] + staff_roles))
                await safe_create_text(cat_tribes, "🐍・เผ่างู", overwrites=build_overwrites(everyone, allowed_roles=[r_snake] + staff_roles))
                await safe_create_text(cat_tribes, "🐲・เผ่าสัตว์ในตำนาน", overwrites=build_overwrites(everyone, allowed_roles=[r_mythic] + staff_roles))
                await safe_create_text(cat_tribes, "🧬・ทะเบียนเผ่าพันธุ์", overwrites=build_overwrites(everyone, read_only=True))

            # --- 👑 ราชสำนัก ---
            cat_court = await safe_create_category(guild, "👑 ราชสำนัก")
            if cat_court:
                await safe_create_voice(cat_court, "👑・พระราชวัง", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty] + staff_roles))
                await safe_create_voice(cat_court, "📜・พระราชโองการ", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty] + staff_roles))
                await safe_create_voice(cat_court, "🏰・สภาขุนนาง", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_nobles] + staff_roles))
                await safe_create_voice(cat_court, "⚖️・ราชสำนัก", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_nobles] + staff_roles))
                await safe_create_text(cat_court, "📂・เอกสารราชการ", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty] + staff_roles))
                await safe_create_text(cat_court, "🤝・การทูต", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_nobles] + staff_roles))
                await safe_create_voice(cat_court, "🔐・ห้องลับราชวงศ์", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty] + staff_roles))
                await safe_create_voice(cat_court, "🔊・ห้องประชุมราชสำนัก", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_nobles] + staff_roles))

            # --- 🏘️ เมืองและหมู่บ้าน ---
            cat_city = await safe_create_category(guild, "🏘️ เมืองและหมู่บ้าน", overwrites=build_overwrites(everyone, allowed_roles=[r_citizen] + staff_roles))
            if cat_city:
                for vc in ["🏙️・เมืองหลวง", "🏘️・หมู่บ้าน", "🏪・ตลาดกลาง", "🍖・ร้านอาหาร", "☕・ร้านกาแฟ", "🏨・โรงแรม", "🏥・โรงพยาบาล", "🌳・สวนกลางเมือง", "⛲・จัตุรัสกลางเมือง", "🚉・สถานีเดินทาง", "🔊・จัตุรัสกลางเมือง", "🔊・ตลาด"]:
                    await safe_create_voice(cat_city, vc)

            # --- 💼 อาชีพและการดำรงชีวิต ---
            cat_jobs = await safe_create_category(guild, "💼 อาชีพและการดำรงชีวิต")
            if cat_jobs:
                for ch in ["🧑‍🌾・เกษตรกร", "⛏️・คนงานเหมือง", "🔨・ช่างตีเหล็ก", "🧑‍🍳・พ่อครัว", "🧑‍⚕️・หมอ", "🛡️・ทหาร", "🏹・นักล่า", "🧙・นักเวท", "🧭・นักผจญภัย"]:
                    await safe_create_text(cat_jobs, ch, overwrites=build_overwrites(everyone, allowed_roles=[r_citizen] + staff_roles))
                await safe_create_text(cat_jobs, "📋・ทะเบียนอาชีพ", overwrites=build_overwrites(everyone, read_only=True))

            # --- ⚔️ นักผจญภัย ---
            cat_guild = await safe_create_category(guild, "⚔️ นักผจญภัย", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer, r_senior_adv] + staff_roles))
            if cat_guild:
                for vc in ["🧭・กิลด์นักผจญภัย", "📜・กระดานภารกิจ", "💰・รางวัลภารกิจ", "🗺️・พื้นที่สำรวจ", "🐉・สัตว์ประหลาด", "💎・สมบัติลึกลับ"]:
                    await safe_create_voice(cat_guild, vc)
                await safe_create_voice(cat_guild, "🔐・ภารกิจลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_senior_adv] + staff_roles))
                await safe_create_voice(cat_guild, "🔊・กิลด์นักผจญภัย")

            # --- 🛡️ กองทหารอาณาจักร ---
            cat_military = await safe_create_category(guild, "🛡️ กองทหารอาณาจักร", overwrites=build_overwrites(everyone, allowed_roles=[r_soldier, r_general] + staff_roles))
            if cat_military:
                await safe_create_voice(cat_military, "🛡️・กองทัพ")
                await safe_create_voice(cat_military, "📋・รายงานเหตุการณ์")
                await safe_create_text(cat_military, "⚔️・คำสั่งทหาร", overwrites=build_overwrites(everyone, allowed_roles=[r_general] + staff_roles))
                await safe_create_voice(cat_military, "🗺️・แผนที่สงคราม", overwrites=build_overwrites(everyone, allowed_roles=[r_general] + staff_roles))
                await safe_create_text(cat_military, "🚨・ประกาศฉุกเฉิน", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_military, "🔒・คุกหลวง")
                await safe_create_text(cat_military, "📂・แฟ้มผู้ต้องหา")
                await safe_create_voice(cat_military, "🔊・ห้องบัญชาการ")

            # --- 🌲 ดินแดนภายนอก ---
            cat_wild = await safe_create_category(guild, "🌲 ดินแดนภายนอก", overwrites=build_overwrites(everyone, allowed_roles=[r_citizen] + staff_roles))
            if cat_wild:
                for vc in ["🌳・ป่าใหญ่", "🏔️・เทือกเขา", "🏜️・ทะเลทราย", "🌊・ชายฝั่ง", "🏝️・เกาะร้าง", "🕳️・ถ้ำลึกลับ", "🏚️・ซากอาณาจักรเก่า", "🔊・พื้นที่ผจญภัย"]:
                    await safe_create_voice(cat_wild, vc)

            # --- 🌙 ความลับของอาณาจักร ---
            cat_secrets = await safe_create_category(guild, "🌙 ความลับของอาณาจักร", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_lore, r_exec, r_founder]))
            if cat_secrets:
                for ch in ["❓・ปริศนาแห่งอาณาจักร", "📜・เอกสารลับ", "🕯️・ลัทธิลึกลับ", "🩸・เหตุการณ์ต้องห้าม"]:
                    await safe_create_text(cat_secrets, ch)
                await safe_create_text(cat_secrets, "🔐・ความลับของราชวงศ์", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_story, r_exec, r_founder]))
                await safe_create_text(cat_secrets, "🧩・ปริศนาหลัก", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))

            # --- 🎭 EVENT | เหตุการณ์ในโลก ---
            cat_event = await safe_create_category(guild, "🎭 EVENT | เหตุการณ์ในโลก", overwrites=build_overwrites(everyone))
            if cat_event:
                for ch in ["📢・ประกาศ-event", "📜・ตาราง-event", "⚔️・สงครามอาณาจักร", "🎪・เทศกาลอาณาจักร", "🏆・การแข่งขัน", "🎭・event-พิเศษ"]:
                    await safe_create_text(cat_event, ch)
                await safe_create_voice(cat_event, "🔊・พื้นที่-event")

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมสัตว์", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "🐾・อวดตัวละคร", "📊・โหวต", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "🎵・ห้องฟังเพลง", "💤・AFK"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff")
                await safe_create_text(cat_staff_zone, "📂・ข้อมูลตัวละคร")
                report_channel = await safe_create_text(cat_staff_zone, "📝・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🧬・จัดการเผ่าพันธุ์", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🗺️・จัดการแผนที่", overwrites=build_overwrites(everyone, allowed_roles=[r_builder, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・เขียน-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🎭・วางแผน-event", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "⚔️・วางแผนสงคราม", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "👑・จัดการราชวงศ์", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📋・บันทึกเหตุการณ์")
                await safe_create_voice(cat_staff_zone, "🔊・ประชุม-staff")

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="🐾 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Talking Animals Kingdom RP",
                        description="โครงสร้างอาณาจักรสัตว์พูดได้ ศูนย์กลาง เผ่าพันธุ์ ราชสำนัก กิลด์นักผจญภัย ดินแดนภายนอก ความลับ และศูนย์บัญชาการติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.green()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA[:25]]) + "\n...และยศอื่นๆ ครบถ้วน"
                    embed.add_field(name="🎭 รายชื่อยศหลัก", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมอาณาจักรสัตว์พูดได้ เสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Talking Animals Kingdom RP เสร็จสิ้นสมบูรณ์ ===")

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
