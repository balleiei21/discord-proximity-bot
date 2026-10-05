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
NEW_SERVER_NAME = "Minecraft World of Prophecy RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - World of Prophecy Theme)
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
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครเข้าสู่โลกแห่งคำทำนาย"},
    {"name": "🧳 ประชาชน", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ชาวเมืองและผู้ใช้ชีวิตในโลกคำทำนาย"},
    {"name": "⭐ บุคคลสำคัญ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "บุคคลที่มีบทบาทสำคัญในคำทำนาย"},

    # --- สายคำทำนาย ---
    {"name": "🔮 นักพยากรณ์ฝึกหัด", "color": discord.Color.from_rgb(175, 122, 196), "permissions": perm_member, "desc": "ผู้เริ่มต้นศึกษาคำทำนาย"},
    {"name": "📜 นักพยากรณ์", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ อ่านและทำนายชะตากรรม"},
    {"name": "👁️ นักพยากรณ์อาวุโส", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_member, "desc": "ผู้หยั่งรู้อนาคตและอ่านคำทำนายต้องห้าม"},
    {"name": "🌟 มหาพยากรณ์", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้สื่อสารกับดวงดาวและชะตากรรม"},
    {"name": "👑 ผู้นำสภานักพยากรณ์", "color": discord.Color.from_rgb(212, 172, 13), "permissions": perm_member, "desc": "ผู้ปกครองวิหารแห่งคำทำนาย"},

    # --- ฝ่ายผู้พิทักษ์ ---
    {"name": "🛡️ ผู้พิทักษ์ฝึกหัด", "color": discord.Color.from_rgb(133, 193, 233), "permissions": perm_member, "desc": "ทหารฝึกหัดผู้ปกป้องคำทำนาย"},
    {"name": "⚔️ ผู้พิทักษ์", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผู้ปกป้องโชคชะตาและความสงบสุข"},
    {"name": "🏆 ผู้พิทักษ์อาวุโส", "color": discord.Color.from_rgb(41, 128, 185), "permissions": perm_member, "desc": "ยอดนักรบแห่งสภาผู้พิทักษ์"},
    {"name": "👑 แม่ทัพผู้พิทักษ์", "color": discord.Color.from_rgb(21, 67, 96), "permissions": perm_member, "desc": "ผู้นำกองทัพผู้พิทักษ์"},

    # --- ฝ่ายต่อต้าน ---
    {"name": "🕶️ ผู้ต่อต้าน", "color": discord.Color.from_rgb(120, 144, 156), "permissions": perm_member, "desc": "ผู้พยายามบิดเบือนและเปลี่ยนอนาคต"},
    {"name": "⚔️ นักรบเงา", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "นักรบไร้ตัวตนผู้ทำลายชะตากรรม"},
    {"name": "🌑 ผู้ต่อต้านระดับสูง", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_member, "desc": "แกนนำผู้ปฏิเสธคำทำนาย"},
    {"name": "👑 ผู้นำฝ่ายต่อต้าน", "color": discord.Color.from_rgb(100, 30, 22), "permissions": perm_member, "desc": "ผู้บัญชาการกองกำลังต่อต้านชะตากรรม"},

    # --- อาชีพ ---
    {"name": "⚔️ นักผจญภัย", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้เดินทางตามหาความจริงและภารกิจ"},
    {"name": "📚 นักวิชาการ", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ผู้ศึกษาคัมภีร์และอารยธรรมเก่า"},
    {"name": "🧙 นักเวท", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ควบคุมเวทมนตร์แห่งอนาคต"},
    {"name": "🧑‍🌾 ชาวนา", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "ผู้กสิกรแห่งเมืองชะตา"},
    {"name": "🔨 ช่างตีเหล็ก", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_member, "desc": "ผู้สร้างศาสตราวุธ"},
    {"name": "🧑‍⚕️ แพทย์", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "หมอเยียวยาบาดแผล"},
    {"name": "🛍️ พ่อค้า", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "วานิชผู้แลกเปลี่ยนสินค้า"},
    {"name": "🏛️ ขุนนาง", "color": discord.Color.from_rgb(243, 156, 18), "permissions": perm_member, "desc": "ผู้บริหารเมืองแห่งชะตา"},

    # --- ทีมงาน ---
    {"name": "🎙️ กรรมการ", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้ตรวจใบสมัครและสัมภาษณ์"},
    {"name": "🧩 ทีมเนื้อเรื่อง", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ผู้สร้างคำทำนายและเหตุการณ์ลับ"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้ดูแลเบื้องหลังและประวัติศาสตร์โลก"},
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
            r_citizen = get_r("🧳 ประชาชน")
            r_vip_person = get_r("⭐ บุคคลสำคัญ")

            # ยศสายคำทำนาย
            r_oracle_apprentice = get_r("🔮 นักพยากรณ์ฝึกหัด")
            r_oracle = get_r("📜 นักพยากรณ์")
            r_snr_oracle = get_r("👁️ นักพยากรณ์อาวุโส")
            r_grand_oracle = get_r("🌟 มหาพยากรณ์")
            r_leader_oracle = get_r("👑 ผู้นำสภานักพยากรณ์")

            # ยศฝ่ายผู้พิทักษ์
            r_guard_apprentice = get_r("🛡️ ผู้พิทักษ์ฝึกหัด")
            r_guard = get_r("⚔️ ผู้พิทักษ์")
            r_snr_guard = get_r("🏆 ผู้พิทักษ์อาวุโส")
            r_commander_guard = get_r("👑 แม่ทัพผู้พิทักษ์")

            # ยศฝ่ายต่อต้าน
            r_rebel = get_r("🕶️ ผู้ต่อต้าน")
            r_shadow_warrior = get_r("⚔️ นักรบเงา")
            r_high_rebel = get_r("🌑 ผู้ต่อต้านระดับสูง")
            r_leader_rebel = get_r("👑 ผู้นำฝ่ายต่อต้าน")

            # ยศอาชีพ
            r_adventurer = get_r("⚔️ นักผจญภัย")
            r_scholar = get_r("📚 นักวิชาการ")
            r_mage = get_r("🧙 นักเวท")
            r_farmer = get_r("🧑‍🌾 ชาวนา")
            r_blacksmith = get_r("🔨 ช่างตีเหล็ก")
            r_doctor = get_r("🧑‍⚕️ แพทย์")
            r_merchant = get_r("🛍️ พ่อค้า")
            r_noble = get_r("🏛️️ ขุนนาง")

            # ยศทีมงาน
            r_interviewer = get_r("🎙️️ กรรมการ")
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
            oracle_roles = [r for r in [r_oracle_apprentice, r_oracle, r_snr_oracle, r_grand_oracle, r_leader_oracle] + staff_roles if r]
            high_oracle_roles = [r for r in [r_snr_oracle, r_grand_oracle, r_leader_oracle] + staff_roles if r]
            guard_roles = [r for r in [r_guard_apprentice, r_guard, r_snr_guard, r_commander_guard] + staff_roles if r]
            rebel_roles = [r for r in [r_rebel, r_shadow_warrior, r_high_rebel, r_leader_rebel] + staff_roles if r]
            scholar_roles = [r for r in [r_scholar] + staff_roles if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (World of Prophecy Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 🔮 ศูนย์กลางโลก ---
            cat_center = await safe_create_category(guild, "🔮 ศูนย์กลางโลก", overwrites=build_overwrites(everyone, read_only=True))
            if cat_center:
                for ch in ["📢・ประกาศโลก", "📖・กฎแห่งคำทำนาย", "🗺️・แผนที่โลก", "📜・ประวัติศาสตร์โลก", "🔮・ระบบคำทำนาย", "🌟・ระบบชะตากรรม", "⚖️・ระบบฝ่ายต่าง-ๆ", "📚・lore-โลก"]:
                    await safe_create_text(cat_center, ch)

            # --- 📝 สมัครตัวละคร ---
            cat_apply = await safe_create_category(guild, "📝 สมัครตัวละคร")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครตัวละคร", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "🪪・ข้อมูลตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "🔮・คำทำนายประจำตัว", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⭐・พรสวรรค์-ความสามารถ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⚔️・เลือกฝ่าย", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📜・ประวัติตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "⏳・รอตรวจสอบ", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🔮・ห้องอ่านชะตา", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))

            # --- 🏰 โซนโรล — เมืองแห่งชะตา ---
            cat_city_rp = await safe_create_category(guild, "🏰 โซนโรล — เมืองแห่งชะตา")
            if cat_city_rp:
                await safe_create_voice(cat_city_rp, "🏰・จัตุรัสกลางเมือง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "🏛️・ศาลากลาง", overwrites=build_overwrites(everyone, allowed_roles=[r_noble, r_citizen] + staff_roles))
                await safe_create_voice(cat_city_rp, "🛍️・ตลาดกลาง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "🍺・โรงเตี๊ยม", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "☕・ร้านน้ำชา", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "🏠・ย่านที่พักอาศัย", overwrites=build_overwrites(everyone, allowed_roles=[r_citizen] + staff_roles))
                await safe_create_voice(cat_city_rp, "🌳・สวนแห่งชะตา", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "⛲・ลานน้ำพุ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "🌙・เมืองยามค่ำคืน", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_city_rp, "🚪・ตรอกลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_shadow_warrior, r_rebel] + staff_roles))

            # --- 🔮 วิหารแห่งคำทำนาย ---
            cat_temple = await safe_create_category(guild, "🔮 วิหารแห่งคำทำนาย")
            if cat_temple:
                await safe_create_voice(cat_temple, "🔮・ห้องพยากรณ์", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "🕯️・ห้องประกอบพิธี", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "📜・ห้องคัมภีร์", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "👁️・ห้องมองอนาคต", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "🌙・แท่นบูชาจันทรา", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "☀️・แท่นบูชาสุริยา", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_temple, "⭐・ห้องดาวแห่งชะตา", overwrites=build_overwrites(everyone, allowed_roles=high_oracle_roles))
                await safe_create_voice(cat_temple, "🔐・ห้องคำทำนายต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_leader_oracle, r_story, r_exec, r_founder]))

            # --- 📜 หอคัมภีร์ ---
            cat_library = await safe_create_category(guild, "📜 หอคัมภีร์")
            if cat_library:
                await safe_create_voice(cat_library, "📚・ห้องสมุดกลาง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_library, "📖・คัมภีร์โบราณ", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_library, "🗿・บันทึกอารยธรรมเก่า", overwrites=build_overwrites(everyone, allowed_roles=scholar_roles))
                await safe_create_voice(cat_library, "🧭・บันทึกเหตุการณ์ในอดีต", overwrites=build_overwrites(everyone, allowed_roles=scholar_roles))
                await safe_create_voice(cat_library, "🔮・บันทึกคำทำนาย", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_library, "🩸・คัมภีร์สีเลือด", overwrites=build_overwrites(everyone, allowed_roles=[r_snr_oracle, r_story] + staff_roles))
                await safe_create_voice(cat_library, "🌑・คัมภีร์แห่งจุดจบ", overwrites=build_overwrites(everyone, allowed_roles=[r_leader_oracle, r_story] + staff_roles))
                await safe_create_voice(cat_library, "🔐・ห้องเก็บคัมภีร์ต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_scholar, r_leader_oracle] + staff_roles))

            # --- 🌌 ดินแดนแห่งโชคชะตา ---
            cat_lands = await safe_create_category(guild, "🌌 ดินแดนแห่งโชคชะตา")
            if cat_lands:
                await safe_create_voice(cat_lands, "🌳・ป่าแห่งคำทำนาย", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_lands, "🌙・ทะเลสาบจันทรา", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_lands, "⭐・หุบเขาดวงดาว", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_lands, "🏔️・ภูเขาศักดิ์สิทธิ์", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_lands, "🏜️・ทะเลทรายแห่งกาลเวลา", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer, r_story] + staff_roles))
                await safe_create_voice(cat_lands, "🌊・ทะเลแห่งอนาคต", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_lands, "🌫️・หุบเขาหมอก", overwrites=build_overwrites(everyone, allowed_roles=[r_rebel, r_adventurer] + staff_roles))
                await safe_create_voice(cat_lands, "🚪・ประตูแห่งชะตา", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))

            # --- ⚔️ ฝ่ายแห่งโชคชะตา ---
            cat_factions = await safe_create_category(guild, "⚔️ ฝ่ายแห่งโชคชะตา")
            if cat_factions:
                # ☀️ ฝ่ายผู้พิทักษ์
                await safe_create_voice(cat_factions, "🏰・ห้องประชุมผู้พิทักษ์", overwrites=build_overwrites(everyone, allowed_roles=guard_roles))
                await safe_create_voice(cat_factions, "⚔️・กองบัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=guard_roles))
                await safe_create_voice(cat_factions, "🛡️・ลานฝึก", overwrites=build_overwrites(everyone, allowed_roles=guard_roles))
                await safe_create_voice(cat_factions, "🔐・ห้องบัญชาการลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_commander_guard, r_exec, r_founder]))
                
                # 🌑 ฝ่ายผู้ต่อต้านคำทำนาย
                await safe_create_voice(cat_factions, "🕶️・ฐานลับ", overwrites=build_overwrites(everyone, allowed_roles=rebel_roles))
                await safe_create_voice(cat_factions, "⚔️・ห้องประชุม", overwrites=build_overwrites(everyone, allowed_roles=rebel_roles))
                await safe_create_voice(cat_factions, "📜・แผนต่อต้านคำทำนาย", overwrites=build_overwrites(everyone, allowed_roles=rebel_roles))
                await safe_create_voice(cat_factions, "🔐・ห้องลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_leader_rebel, r_exec, r_founder]))
                
                # 🔮 ฝ่ายนักพยากรณ์
                await safe_create_voice(cat_factions, "🔮・สภานักพยากรณ์", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_factions, "📜・ห้องอ่านชะตา", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_factions, "👁️️・ห้องมองอนาคต", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_factions, "🌙・ห้องพิธีกรรม", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))

            # --- ⏳ เขตแห่งกาลเวลา ---
            cat_time = await safe_create_category(guild, "⏳ เขตแห่งกาลเวลา")
            if cat_time:
                await safe_create_voice(cat_time, "🕰️・หอนาฬิกา", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_time, "⌛・ห้องทรายแห่งเวลา", overwrites=build_overwrites(everyone, allowed_roles=oracle_roles))
                await safe_create_voice(cat_time, "🔄・สถานที่ที่เวลาวนซ้ำ", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_time, "👴・โลกอดีต", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_time, "👁️️・โลกอนาคต", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_time, "🌌・รอยแยกแห่งเวลา", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_time, "🔐・จุดกำเนิดเวลา", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))

            # --- 🌑 คำทำนายต้องห้าม ---
            cat_forbidden = await safe_create_category(guild, "🌑 คำทำนายต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
            if cat_forbidden:
                for vc in ["🩸・คำทำนายบทที่ 0", "👁️・ผู้ที่ไม่มีชะตา", "🌑・วันสิ้นโลก", "☠️・ผู้ทำลายคำทำนาย", "🕯️・พิธีกรรมต้องห้าม", "🚪・ประตูแห่งจุดจบ", "📜・คัมภีร์บทสุดท้าย", "🔐・ความจริงของผู้สร้างโลก"]:
                    await safe_create_voice(cat_forbidden, vc)

            # --- ⚔️ การผจญภัย ---
            cat_adventure = await safe_create_category(guild, "⚔️ การผจญภัย")
            if cat_adventure:
                await safe_create_text(cat_adventure, "📢・ประกาศภารกิจ", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_adventure, "🗺️・กระดานภารกิจ", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "🧭・กิลด์นักผจญภัย", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "⚔️・ลานฝึกนักผจญภัย", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "🏕️・ค่ายพักแรม", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "🏚️・ซากปรักหักพัง", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "🗿・วิหารโบราณ", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))
                await safe_create_voice(cat_adventure, "🐉・ดินแดนสัตว์อสูร", overwrites=build_overwrites(everyone, allowed_roles=[r_adventurer] + staff_roles))

            # --- 🩸 เหตุการณ์ตามคำทำนาย ---
            cat_events_prophecy = await safe_create_category(guild, "🩸 เหตุการณ์ตามคำทำนาย")
            if cat_events_prophecy:
                await safe_create_text(cat_events_prophecy, "📢・ประกาศเหตุการณ์", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_voice(cat_events_prophecy, "🔮・คำทำนายปรากฏ", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_events_prophecy, "🌑・สุริยุปราคา", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_events_prophecy, "🌕・จันทราสีเลือด", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_events_prophecy, "⚡・พลังแห่งคำทำนาย", overwrites=build_overwrites(everyone, allowed_roles=[r_story] + staff_roles))
                await safe_create_voice(cat_events_prophecy, "🚨・ชะตากรรมเปลี่ยนแปลง", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_events_prophecy, "☠️・การมาถึงของผู้ทำลาย", overwrites=build_overwrites(everyone))
                await safe_create_voice(cat_events_prophecy, "🌌・วันแห่งโชคชะตา", overwrites=build_overwrites(everyone))

            # --- 🎭 EVENT | เรื่องราวหลัก ---
            cat_event_main = await safe_create_category(guild, "🎭 EVENT | เรื่องราวหลัก")
            if cat_event_main:
                await safe_create_text(cat_event_main, "📢・ประกาศ event", overwrites=build_overwrites(everyone, read_only=True))
                await safe_create_text(cat_event_main, "📜・ตาราง event", overwrites=build_overwrites(everyone, read_only=True))
                for vc in ["🔮・คำทำนายบทที่ 1", "🌙・คำทำนายบทที่ 2", "🌑・คำทำนายบทที่ 3", "⚔️️・สงครามแห่งโชคชะตา", "⏳・การย้อนเวลาครั้งสุดท้าย", "🌌・บทสุดท้ายของคำทำนาย"]:
                    await safe_create_voice(cat_event_main, vc, overwrites=build_overwrites(everyone))

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎨・แฟนอาร์ต", "📸・รูปตัวละคร", "🎮・หาเพื่อนเล่นเกม", "📊・โหวต"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "🎵・ห้องฟังเพลง", "💤・afk"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff")
                report_channel = await safe_create_text(cat_staff_zone, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🔮・จัดการคำทำนาย", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・เขียน-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "⚔️・วางแผนฝ่ายต่าง-ๆ", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "🌑・จัดการความลับ", overwrites=build_overwrites(everyone, allowed_roles=[r_story, r_exec, r_founder]))
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
                        title="🔮 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft World of Prophecy RP",
                        description="โครงสร้างโลกแห่งคำทำนาย โซนโรลแบบห้องเสียง วิหารแห่งคำทำนาย หอคัมภีร์ เขตแห่งกาลเวลา และศูนย์บัญชาการติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.purple()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA[:25]]) + "\n...และยศอื่นๆ ครบถ้วน"
                    embed.add_field(name="🎭 รายชื่อยศหลัก", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมโลกแห่งคำทำนาย เสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ World of Prophecy RP เสร็จสิ้นสมบูรณ์ ===")

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
