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
NEW_SERVER_NAME = "Minecraft Power Experiment Institute RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Power Experiment Theme)
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
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครสถาบัน"},
    {"name": "🧪 ผู้ทดลอง", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้เข้าร่วมการทดลอง"},
    {"name": "🎓 นักเรียน", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "นักเรียนในสถาบัน"},
    {"name": "⭐ ผู้ทดลองพิเศษ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ทดลองที่มีพลังพิเศษหรือระดับสูง"},

    # --- ระดับพลัง ---
    {"name": "⚪ ระดับ E", "color": discord.Color.from_rgb(236, 240, 241), "permissions": perm_member, "desc": "พลังระดับเริ่มต้น"},
    {"name": "🟢 ระดับ D", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "พลังระดับทั่วไป"},
    {"name": "🔵 ระดับ C", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "พลังระดับปานกลาง"},
    {"name": "🟣 ระดับ B", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "พลังระดับสูง"},
    {"name": "🟠 ระดับ A", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "พลังระดับอันตราย"},
    {"name": "🔴 ระดับ S", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_member, "desc": "พลังระดับภัยพิบัติ"},
    {"name": "⚫ ระดับ EX", "color": discord.Color.from_rgb(44, 62, 80), "permissions": perm_member, "desc": "พลังระดับไร้ขีดจำกัด/ประเมินค่าไม่ได้"},

    # --- บุคลากร ---
    {"name": "🧑‍🏫 อาจารย์", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผู้สอนและควบคุมการฝึก"},
    {"name": "🔬 นักวิจัย", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "เจ้าหน้าที่วิเคราะห์และทดลอง"},
    {"name": "🧬 นักวิจัยอาวุโส", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ผู้ดูแลโครงการทดลองลับ"},
    {"name": "🩺 แพทย์", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้ดูแลรักษาสุขภาพและฟื้นฟู"},
    {"name": "🛡️ เจ้าหน้าที่รักษาความปลอดภัย", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "ผู้คุ้มกันและรักษาความสงบ"},
    {"name": "🔒 เจ้าหน้าที่กักกัน", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_member, "desc": "ผู้ดูแลเขตกักกันและภัยคุกคาม"},
    {"name": "👔 ผู้อำนวยการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้บริหารสูงสุดของสถาบัน"},

    # --- ทีมงาน ---
    {"name": "🎙️ กรรมการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้ตรวจใบสมัครและสัมภาษณ์"},
    {"name": "🧩 ทีมเนื้อเรื่อง", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ผู้สร้างกิจกรรมและเนื้อเรื่องลับ"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้เขียนเบื้องหลังและประวัติสถาบัน"},
    {"name": "🗺️ Builder", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_staff, "desc": "ทีมสร้างแผนที่ในเกม"},
    {"name": "🔨 Moderator", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_staff, "desc": "ผู้ดูแลความเรียบร้อย"},
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
            r_subject = get_r("🧪 ผู้ทดลอง")
            r_student = get_r("🎓 นักเรียน")
            r_special_subject = get_r("⭐ ผู้ทดลองพิเศษ")

            # ยศระดับพลัง
            r_rank_e = get_r("⚪ ระดับ E")
            r_rank_d = get_r("🟢 ระดับ D")
            r_rank_c = get_r("🔵 ระดับ C")
            r_rank_b = get_r("🟣 ระดับ B")
            r_rank_a = get_r("🟠 ระดับ A")
            r_rank_s = get_r("🔴 ระดับ S")
            r_rank_ex = get_r("⚫ ระดับ EX")

            # ยศบุคลากร
            r_teacher = get_r("🧑‍🏫 อาจารย์")
            r_researcher = get_r("🔬 นักวิจัย")
            r_snr_researcher = get_r("🧬 นักวิจัยอาวุโส")
            r_doctor = get_r("🩺 แพทย์")
            r_security = get_r("🛡️ เจ้าหน้าที่รักษาความปลอดภัย")
            r_containment = get_r("🔒 เจ้าหน้าที่กักกัน")
            r_director = get_r("👔 ผู้อำนวยการ")

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
            staff_and_researcher = [r for r in [r_researcher, r_snr_researcher] + staff_roles if r]
            staff_and_doctor = [r for r in [r_doctor] + staff_roles if r]
            staff_and_containment = [r for r in [r_containment, r_security] + staff_roles if r]
            staff_and_teacher = [r for r in [r_teacher] + staff_roles if r]
            all_subjects = [r for r in [r_subject, r_student, r_special_subject] + staff_roles if r]
            high_rank_subjects = [r for r in [r_special_subject, r_rank_a, r_rank_s, r_rank_ex] + staff_roles if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Power Experiment Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🏢 ศูนย์กลางสถาบัน ---
            cat_center = await safe_create_category(guild, "🏢 ศูนย์กลางสถาบัน", overwrites=build_overwrites(everyone, read_only=True))
            if cat_center:
                for ch in ["📢・ประกาศสถาบัน", "📖・กฎของสถาบัน", "🗺️・แผนผังสถาบัน", "📜・ประวัติสถาบัน", "⚡・ระบบพลัง", "🧬・ประเภทพลัง", "🎓・ระบบการฝึก", "🏅・ระดับพลัง"]:
                    await safe_create_text(cat_center, ch)

            # --- 📝 สมัครเข้าเป็นผู้ทดลอง ---
            cat_apply = await safe_create_category(guild, "📝 สมัครเข้าเป็นผู้ทดลอง")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครตัวละคร", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "🪪・ข้อมูลตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⚡・ข้อมูลพลัง", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "🧬・ประเภทพลัง", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "🩸・ประวัติผู้ทดลอง", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⏳・รอตรวจสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการทดลอง", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant], read_only=True))
                await safe_create_text(cat_apply, "❌・ต้องแก้ไขข้อมูล", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant], read_only=True))

            # --- 🏫 โซนโรล — สถาบัน (ห้องเสียงทั้งหมด) ---
            cat_school_rp = await safe_create_category(guild, "🏫 โซนโรล — สถาบัน")
            if cat_school_rp:
                await safe_create_voice(cat_school_rp, "🏫・โถงสถาบัน", overwrites=build_overwrites(everyone, allowed_roles=[r_student, r_teacher, r_director] + staff_roles))
                await safe_create_voice(cat_school_rp, "🎓・ห้องเรียน", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))
                await safe_create_voice(cat_school_rp, "📚・ห้องเรียนพิเศษ", overwrites=build_overwrites(everyone, allowed_roles=high_rank_subjects))
                await safe_create_voice(cat_school_rp, "🧑‍🏫・ห้องอาจารย์", overwrites=build_overwrites(everyone, allowed_roles=staff_and_teacher))
                await safe_create_voice(cat_school_rp, "📝・ห้องสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))
                await safe_create_voice(cat_school_rp, "☕・โรงอาหาร", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_school_rp, "🏪・ร้านค้าสถาบัน", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_school_rp, "🏥・ห้องพยาบาล", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_school_rp, "🌳・สวนกลาง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_school_rp, "🏟️・สนามฝึก", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))
                await safe_create_voice(cat_school_rp, "🏆・สนามประลอง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_school_rp, "🛏️・หอพักนักเรียน", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))
                await safe_create_voice(cat_school_rp, "🛋️・ห้องพักรวม", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))
                await safe_create_voice(cat_school_rp, "🌙・หอพักกลางคืน", overwrites=build_overwrites(everyone, allowed_roles=[r_student] + staff_roles))

            # --- ⚡ โซนทดลองพลัง ---
            cat_power = await safe_create_category(guild, "⚡ โซนทดลองพลัง")
            if cat_power:
                await safe_create_voice(cat_power, "⚡・ห้องทดสอบพลัง", overwrites=build_overwrites(everyone, allowed_roles=all_subjects))
                await safe_create_voice(cat_power, "🔥・ห้องพลังธาตุ", overwrites=build_overwrites(everyone, allowed_roles=all_subjects))
                await safe_create_voice(cat_power, "🧠・ห้องพลังจิต", overwrites=build_overwrites(everyone, allowed_roles=all_subjects))
                await safe_create_voice(cat_power, "🌀・ห้องพลังมิติ", overwrites=build_overwrites(everyone, allowed_roles=high_rank_subjects))
                await safe_create_voice(cat_power, "💥・ห้องจำลองการต่อสู้", overwrites=build_overwrites(everyone, allowed_roles=all_subjects))
                await safe_create_voice(cat_power, "🎯・สนามฝึกควบคุมพลัง", overwrites=build_overwrites(everyone, allowed_roles=all_subjects))
                await safe_create_voice(cat_power, "🔬・ห้องวิเคราะห์พลัง", overwrites=build_overwrites(everyone, allowed_roles=staff_and_researcher))
                await safe_create_voice(cat_power, "📊・ห้องวัดระดับพลัง", overwrites=build_overwrites(everyone, allowed_roles=[r_researcher, r_subject, r_special_subject] + staff_roles))
                await safe_create_voice(cat_power, "🧪・ห้องทดลองพิเศษ", overwrites=build_overwrites(everyone, allowed_roles=staff_and_researcher))
                await safe_create_voice(cat_power, "☢️・ห้องทดลองอันตราย", overwrites=build_overwrites(everyone, allowed_roles=[r_snr_researcher, r_director] + staff_roles))

            # --- 🧬 ศูนย์วิจัย ---
            cat_research = await safe_create_category(guild, "🧬 ศูนย์วิจัย", overwrites=build_overwrites(everyone, allowed_roles=staff_and_researcher))
            if cat_research:
                await safe_create_voice(cat_research, "🔬・ห้องวิจัยหลัก")
                await safe_create_voice(cat_research, "🧫・ห้องทดลองชีวภาพ")
                await safe_create_voice(cat_research, "🧬・ห้องพันธุกรรม")
                await safe_create_voice(cat_research, "🧠・ห้องศึกษาสมอง")
                await safe_create_voice(cat_research, "📊・ห้องวิเคราะห์ข้อมูล")
                await safe_create_voice(cat_research, "💉・ห้องทดลองยา")
                await safe_create_voice(cat_research, "🩸・ห้องเก็บตัวอย่าง")
                await safe_create_voice(cat_research, "🔐・ห้องวิจัยลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_snr_researcher, r_director] + staff_roles))

            # --- 🏥 ศูนย์การแพทย์ ---
            cat_medical = await safe_create_category(guild, "🏥 ศูนย์การแพทย์")
            if cat_medical:
                await safe_create_voice(cat_medical, "🏥・ห้องรักษา", overwrites=build_overwrites(everyone, allowed_roles=staff_and_doctor))
                await safe_create_voice(cat_medical, "💊・ห้องจ่ายยา", overwrites=build_overwrites(everyone, allowed_roles=staff_and_doctor))
                await safe_create_voice(cat_medical, "🩺・ห้องตรวจร่างกาย", overwrites=build_overwrites(everyone, allowed_roles=staff_and_doctor))
                await safe_create_voice(cat_medical, "🧠・ห้องตรวจพลัง", overwrites=build_overwrites(everyone, allowed_roles=[r_doctor, r_researcher] + staff_roles))
                await safe_create_voice(cat_medical, "🛏️・ห้องพักผู้ป่วย", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_medical, "🚑・ห้องฉุกเฉิน", overwrites=build_overwrites(everyone, allowed_roles=staff_and_doctor))
                await safe_create_voice(cat_medical, "🔒・ห้องกักกันผู้ป่วย", overwrites=build_overwrites(everyone, allowed_roles=[r_doctor, r_snr_researcher, r_director] + staff_roles))

            # --- 🔒 โซนกักกัน ---
            cat_containment = await safe_create_category(guild, "🔒 โซนกักกัน", overwrites=build_overwrites(everyone, allowed_roles=staff_and_containment))
            if cat_containment:
                await safe_create_voice(cat_containment, "🚪・ห้องกักกัน 01")
                await safe_create_voice(cat_containment, "🚪・ห้องกักกัน 02")
                await safe_create_voice(cat_containment, "🚪・ห้องกักกัน 03")
                await safe_create_voice(cat_containment, "☢️・ห้องกักกันอันตราย", overwrites=build_overwrites(everyone, allowed_roles=[r_containment, r_snr_researcher, r_director] + staff_roles))
                await safe_create_voice(cat_containment, "⛓️・ห้องกักกันพิเศษ", overwrites=build_overwrites(everyone, allowed_roles=[r_containment, r_director] + staff_roles))
                await safe_create_voice(cat_containment, "👁️・ผู้ทดลองหมายเลข 001", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_voice(cat_containment, "🩸・ผู้ทดลองหมายเลข 000", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_voice(cat_containment, "🔐・เขตกักกันสูงสุด", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_director, r_story, r_founder]))

            # --- 🌑 โครงการลับ ---
            cat_projects = await safe_create_category(guild, "🌑 โครงการลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
            if cat_projects:
                for vc in ["📁・Project A", "🧬・Project Genesis", "⚡・Project Overload", "🧠・Project Mind", "🩸・Project Blood", "☢️・Project Zero", "👁️️・ห้องทดลองหมายเลข 0"]:
                    await safe_create_voice(cat_projects, vc)
                await safe_create_voice(cat_projects, "🔐・ความลับของผู้อำนวยการ", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_director, r_founder]))
                await safe_create_voice(cat_projects, "💀・การทดลองที่ถูกลบ", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))

            # --- 🚨 เหตุการณ์ผิดปกติ ---
            cat_incidents = await safe_create_category(guild, "🚨 เหตุการณ์ผิดปกติ")
            if cat_incidents:
                await safe_create_voice(cat_incidents, "📢・ประกาศเหตุการณ์", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_incidents, "⚡・พลังระเบิด", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_incidents, "🚨・ระบบรักษาความปลอดภัย", overwrites=build_overwrites(everyone, allowed_roles=staff_and_containment))
                await safe_create_voice(cat_incidents, "🔒・ระบบกักกันล้มเหลว", overwrites=build_overwrites(everyone, allowed_roles=staff_and_containment))
                await safe_create_voice(cat_incidents, "🩸・ผู้ทดลองหลบหนี", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_incidents, "☢️・สารทดลองรั่วไหล", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_incidents, "👁️・พบสิ่งมีชีวิตไม่ทราบชนิด", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_incidents, "🌑・เหตุการณ์ระดับภัยพิบัติ", overwrites=build_overwrites(everyone))

            # --- 🏆 การแข่งขันพลัง ---
            cat_tournament = await safe_create_category(guild, "🏆 การแข่งขันพลัง")
            if cat_tournament:
                await safe_create_text(cat_tournament, "📢・ประกาศการแข่งขัน", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_tournament, "📋・ตารางการแข่งขัน", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_voice(cat_tournament, "⚔️・สนามประลอง 01", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_tournament, "⚔️・สนามประลอง 02", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_tournament, "🔥・รอบคัดเลือก", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_tournament, "⚡・รอบชิงชนะเลิศ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_tournament, "🏆・ห้องแชมป์", overwrites=build_overwrites(everyone))

            # --- 🎭 EVENT | เนื้อเรื่อง ---
            cat_event = await safe_create_category(guild, "🎭 EVENT | เนื้อเรื่อง")
            if cat_event:
                await safe_create_text(cat_event, "📢・ประกาศ Event", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_event, "📜・ตาราง Event", overwrites=build_overwrites(everyone, read_only=True))
                for vc in ["⚡・การทดลองครั้งใหญ่", "🚨・วันสถาบันถูกโจมตี", "🩸・การทดลองต้องห้าม", "☢️・วิกฤตพลังงาน", "🌑・คืนแห่ง Project Zero"]:
                    await safe_create_voice(cat_event, vc, overwrites=build_overwrites(everyone))

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "🎮・หาเพื่อนเล่นเกม", "📊・โหวต"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "🎵・ห้องฟังเพลง", "💤・afk"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff")
                report_channel = await safe_create_text(cat_staff_zone, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🧬・ข้อมูลผู้ทดลอง")
                await safe_create_text(cat_staff_zone, "⚡・ข้อมูลพลัง", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・เขียน-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🧪・วางแผนการทดลอง", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🚨・จัดการเหตุการณ์")
                await safe_create_text(cat_staff_zone, "🗺️・จัดการแผนที่", overwrites=build_overwrites(everyone, allowed_roles=[r_builder, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🔐・ข้อมูลลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_founder]))
                await safe_create_voice(cat_staff_zone, "🎙️・ประชุม-staff")

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="🧪 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Power Experiment Institute RP",
                        description="โครงสร้างสถาบันทดลองพลัง โซนโรลแบบห้องเสียง ศูนย์วิจัย เขตกักกัน โครงการลับ และศูนย์บัญชาการติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.blue()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA[:25]]) + "\n...และยศอื่นๆ ครบถ้วน"
                    embed.add_field(name="🎭 รายชื่อยศหลัก", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมสถาบันทดลองพลัง เสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Power Experiment Institute RP เสร็จสิ้นสมบูรณ์ ===")

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
