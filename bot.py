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
NEW_SERVER_NAME = "Minecraft Noble Academy RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Noble Academy Theme)
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
    # --- ยศพื้นฐานและผู้เล่น ---
    {"name": "👤 ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้เข้าชมทั่วไป"},
    {"name": "📝 ผู้สมัครเข้าเรียน", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครรอคัดเลือก"},
    {"name": "🎓 นักเรียนใหม่", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผ่านการคัดเลือก เพิ่งเข้าศึกษา"},
    {"name": "🎓 นักเรียน", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "นักเรียนประจำสถาบัน"},
    
    # --- บรรดาศักดิ์ขุนนางและตระกูล ---
    {"name": "🎓 บุตรหลานขุนนาง", "color": discord.Color.from_rgb(175, 122, 197), "permissions": perm_member, "desc": "ทายาทตระกูลขุนนาง"},
    {"name": "🎖️ บารอน / บารอนเนส", "color": discord.Color.from_rgb(165, 105, 189), "permissions": perm_member, "desc": "ขุนนางชั้นบารอน"},
    {"name": "🌹 ไวเคานต์ / ไวเคาน์เตส", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ขุนนางชั้นไวเคานต์"},
    {"name": "⚜️ เคานต์ / เคาน์เตส", "color": discord.Color.from_rgb(125, 60, 152), "permissions": perm_member, "desc": "ขุนนางชั้นเคานต์"},
    {"name": "🏵️ มาร์ควิส / มาร์เชียเนส", "color": discord.Color.from_rgb(108, 52, 131), "permissions": perm_member, "desc": "ขุนนางชั้นมาร์ควิส"},
    {"name": "💎 ดยุค / ดัชเชส", "color": discord.Color.from_rgb(88, 24, 69), "permissions": perm_member, "desc": "ขุนนางชั้นดยุค"},
    
    # --- อัศวินและวิชาการ ---
    {"name": "⚔️ อัศวินฝึกหัด", "color": discord.Color.from_rgb(93, 109, 126), "permissions": perm_member, "desc": "ผู้ฝึกฝนการเป็นอัศวิน"},
    {"name": "⚔️ อัศวิน", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "อัศวินแห่งราชอาณาจักร"},
    {"name": "📚 อาจารย์", "color": discord.Color.from_rgb(22, 160, 133), "permissions": perm_staff, "desc": "อาจารย์ผู้สอนวิชาต่างๆ"},
    
    # --- ฝ่ายบริหารราชการและสภา ---
    {"name": "⚖️ ผู้พิพากษา", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_staff, "desc": "ผู้ดูแลศาลหลวงและการพิจารณาโทษ"},
    {"name": "🎙️ กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_staff, "desc": "ผู้ดูแลการรับสมัครและทดสอบ"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(212, 172, 13), "permissions": perm_staff, "desc": "ผู้ดูแลเนื้อเรื่องและประวัติศาสตร์"},
    {"name": "🏛️ สภาขุนนาง", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "สมาชิกสภาบริหารประเทศ"},
    {"name": "👑 ราชวงศ์", "color": discord.Color.from_rgb(203, 67, 53), "permissions": perm_admin, "desc": "เชื้อพระวงศ์แห่งราชอาณาจักร"},
    
    # --- ทีมงานบริหารระบบ ---
    {"name": "🛠️ Staff", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_staff, "desc": "ทีมงานดูแลความเรียบร้อย"},
    {"name": "⚜️ ผู้บริหาร", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_admin, "desc": "ผู้บริหารระดับสูง"},
    {"name": "👑 ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "เจ้าของเซิร์ฟเวอร์/ผู้ก่อตั้ง"}
]

# ----------------------------------------------------
# 2. ฟังก์ชันช่วยสร้างช่องอย่างปลอดภัย
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

            r_applicant = get_r("📝 ผู้สมัครเข้าเรียน")
            r_new_student = get_r("🎓 นักเรียนใหม่")
            r_student = get_r("🎓 นักเรียน")
            r_noble_child = get_r("🎓 บุตรหลานขุนนาง")
            
            r_baron = get_r("🎖️ บารอน / บารอนเนส")
            r_viscount = get_r("🌹 ไวเคานต์ / ไวเคาน์เตส")
            r_count = get_r("⚜️ เคานต์ / เคาน์เตส")
            r_marquis = get_r("🏵️ มาร์ควิส / มาร์เชียเนส")
            r_duke = get_r("💎 ดยุค / ดัชเชส")
            
            r_knight_trainee = get_r("⚔️ อัศวินฝึกหัด")
            r_knight = get_r("⚔️ อัศวิน")
            r_teacher = get_r("📚 อาจารย์")
            
            r_judge = get_r("⚖️ ผู้พิพากษา")
            r_interviewer = get_r("🎙️ กรรมการสัมภาษณ์")
            r_lore = get_r("📜 Lore Team")
            r_council = get_r("🏛️ สภาขุนนาง")
            r_royalty = get_r("👑 ราชวงศ์")
            
            r_staff = get_r("🛠️ Staff")
            r_exec = get_r("⚜️ ผู้บริหาร")
            r_founder = get_r("👑 ผู้ก่อตั้ง")

            if r_founder and message.author in guild.members:
                try:
                    await message.author.add_roles(r_founder)
                except:
                    pass

            staff_roles = [r for r in [r_interviewer, r_lore, r_council, r_royalty, r_staff, r_exec, r_founder, r_judge] if r]
            student_roles = [r for r in [r_new_student, r_student, r_noble_child, r_baron, r_viscount, r_count, r_marquis, r_duke, r_knight_trainee, r_knight] if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Noble Academy Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🏰・พระราชวังและศูนย์กลาง ---
            cat_hub = await safe_create_category(guild, "🏰・พระราชวังและศูนย์กลาง", overwrites=build_overwrites(everyone, read_only=True))
            if cat_hub:
                for ch in ["📢・ประกาศราชสำนัก", "📖・กฎโรงเรียน", "🏰・ข้อมูลสถาบัน", "📜・ประวัติราชอาณาจักร", "🗺️・แผนที่อาณาจักร", "⚜️・ระบบโรลเพลย์"]:
                    await safe_create_text(cat_hub, ch)

            # --- 📝・สมัครเข้าโรงเรียน ---
            cat_apply = await safe_create_category(guild, "📝・สมัครเข้าโรงเรียน")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครขุนนาง", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "⏳・รอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจสอบใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัม", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "🎖️・ผ่านการคัดเลือก", overwrites=build_overwrites(everyone, allowed_roles=student_roles, read_only=True))
                await safe_create_text(cat_apply, "📜・ผลการคัดเลือก", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🎓・เขตการศึกษา ---
            cat_academy = await safe_create_category(guild, "🎓・เขตการศึกษา", overwrites=build_overwrites(everyone, allowed_roles=student_roles + [r_teacher] + staff_roles))
            if cat_academy:
                for ch in ["📚・ห้องเรียน", "👑・วิชามารยาทชนชั้นสูง", "📜・ประวัติศาสตร์ราชวงศ์", "⚔️・ศิลปะการต่อสู้", "🗡️・การใช้ดาบ", "🏇・การขี่ม้า", "💰・เศรษฐกิจและการปกครอง", "🗣️・การทูต", "🎭・ศิลปะและการเต้นรำ"]:
                    await safe_create_text(cat_academy, ch)
                await safe_create_voice(cat_academy, "🔊・ห้องเรียนเสียง")

            # --- 🏛️・สังคมชั้นสูง ---
            cat_society = await safe_create_category(guild, "🏛️・สังคมชั้นสูง", overwrites=build_overwrites(everyone, allowed_roles=student_roles + staff_roles))
            if cat_society:
                for ch in ["🥂・ห้องรับรอง", "☕・ห้องน้ำชา", "🎭・ห้องเต้นรำ", "🌹・สวนราชวงศ์", "🏛️・ห้องโถงกลาง"]:
                    await safe_create_text(cat_society, ch)
                await safe_create_voice(cat_society, "🔊・ห้องรับรอง")
                await safe_create_voice(cat_society, "🎻・ห้องดนตรี")

            # --- 🏠・ตระกูลขุนนาง ---
            cat_house = await safe_create_category(guild, "🏠・ตระกูลขุนนาง", overwrites=build_overwrites(everyone, allowed_roles=student_roles + staff_roles))
            if cat_house:
                await safe_create_text(cat_house, "🏰・คฤหาสน์ตระกูล", overwrites=build_overwrites(everyone, allowed_roles=student_roles))
                await safe_create_text(cat_house, "📜・ห้องโถงตระกูล", overwrites=build_overwrites(everyone, allowed_roles=student_roles))
                await safe_create_voice(cat_house, "🛏️・ห้องพักตระกูล", overwrites=build_overwrites(everyone, allowed_roles=student_roles))

            # --- 👑・ราชสำนัก ---
            cat_court = await safe_create_category(guild, "👑・ราชสำนัก", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_council, r_judge, r_knight, r_exec, r_founder]))
            if cat_court:
                await safe_create_text(cat_court, "👑・พระราชวัง", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_exec, r_founder]))
                await safe_create_text(cat_court, "🏛️・สภาขุนนาง", overwrites=build_overwrites(everyone, allowed_roles=[r_council, r_royalty, r_exec, r_founder]))
                await safe_create_text(cat_court, "📜・ราชกิจจานุเบกษา", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_council], read_only=True))
                await safe_create_text(cat_court, "⚖️・ศาลหลวง", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_judge, r_exec, r_founder]))
                await safe_create_text(cat_court, "🗡️・กองอัศวิน", overwrites=build_overwrites(everyone, allowed_roles=[r_knight, r_knight_trainee, r_royalty]))
                await safe_create_voice(cat_court, "🎙️・ห้องประชุมราชสำนัก", overwrites=build_overwrites(everyone, allowed_roles=[r_royalty, r_council]))

            # --- 🌐・COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐・COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "📊・โหวต", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐・STAFF | ฝ่ายบริหาร ---
            cat_staff_zone = await safe_create_category(guild, "🔐・STAFF | ฝ่ายบริหาร", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                report_channel = await safe_create_text(cat_staff_zone, "📝・บันทึกสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📂・ข้อมูลนักเรียน", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff_zone, "📜・จัดการ-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "⚖️・พิจารณาโทษ", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "👑・ห้องผู้บริหาร", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_founder]))
                await safe_create_voice(cat_staff_zone, "🔊・ประชุม-staff", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="👑 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Noble Academy RP",
                        description="โครงสร้างสถาบันขุนนาง เขตการศึกษา ราชสำนัก ระบบสมัคร และยศบรรดาศักดิ์ทั้งหมดติดตั้งสมบูรณ์เรียบร้อยแล้ว!",
                        color=discord.Color.gold()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA])
                    embed.add_field(name="🏅 รายชื่อยศทั้งหมด", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมโรงเรียนขุนนางเสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Noble Academy RP เสร็จสิ้นสมบูรณ์ ===")

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
