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
NEW_SERVER_NAME = "Minecraft Mysterious Island RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Mysterious Island Theme)
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
    # --- ยศพื้นฐานและผู้มาเยือน ---
    {"name": "👤 ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้เข้าชมทั่วไป"},
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครเดินทางสู่เกาะ"},
    {"name": "🏝️ ผู้มาใหม่", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ผู้รอดชีวิต/ผู้มาใหม่ที่เพิ่งมาถึงเกาะ"},
    
    # --- สายอาชีพและนักสำรวจ ---
    {"name": "🧭 นักสำรวจ", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "นักสำรวจพื้นฐาน"},
    {"name": "⭐ นักสำรวจอาวุโส", "color": discord.Color.from_rgb(243, 156, 18), "permissions": perm_member, "desc": "นักสำรวจผู้มีประสบการณ์ สามารถเข้าถึงเขตอันตราย"},
    {"name": "🔬 นักวิจัย", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผู้ศึกษาพืช สัตว์ และปรากฏการณ์บนเกาะ"},
    {"name": "⚔️ นักล่า", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_member, "desc": "ผู้ปกป้องค่ายและล่าสิ่งมีชีวิตบนเกาะ"},
    {"name": "🩺 แพทย์", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้รักษาและปฐมพยาบาลผู้รอดชีวิต"},
    {"name": "🧙 ผู้ศึกษาเรื่องลึกลับ", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "ผู้ไขรหัสโบราณ เวทมนตร์ และคำสาป"},
    {"name": "🏕️ หัวหน้ากลุ่ม", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้นำกลุ่มผู้รอดชีวิต"},
    
    # --- ทีมงานบริหารระบบและผู้ดูแล Lore ---
    {"name": "🎙️ กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_staff, "desc": "ผู้คัดเลือกผู้รอดชีวิตเข้าสู่เกาะ"},
    {"name": "🧩 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ผู้สร้างเนื้อเรื่อง เบาะแส และไขปริศนาเกาะ"},
    {"name": "🔐 Staff", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_staff, "desc": "ทีมงานดูแลความเรียบร้อย"},
    {"name": "👑 ผู้บริหาร", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_admin, "desc": "ผู้บริหารระดับสูง"},
    {"name": "👑 ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "ผู้สร้าง/เจ้าของเซิร์ฟเวอร์"}
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

            r_applicant = get_r("📝 ผู้สมัคร")
            r_newcomer = get_r("🏝️ ผู้มาใหม่")
            r_explorer = get_r("🧭 นักสำรวจ")
            r_senior_explorer = get_r("⭐ นักสำรวจอาวุโส")
            r_researcher = get_r("🔬 นักวิจัย")
            r_hunter = get_r("⚔️ นักล่า")
            r_doctor = get_r("🩺 แพทย์")
            r_mystic = get_r("🧙 ผู้ศึกษาเรื่องลึกลับ")
            r_leader = get_r("🏕️ หัวหน้ากลุ่ม")
            
            r_interviewer = get_r("🎙️ กรรมการสัมภาษณ์")
            r_lore = get_r("🧩 Lore Team")
            r_staff = get_r("🔐 Staff")
            r_exec = get_r("👑 ผู้บริหาร")
            r_founder = get_r("👑 ผู้ก่อตั้ง")

            if r_founder and message.author in guild.members:
                try:
                    await message.author.add_roles(r_founder)
                except:
                    pass

            staff_roles = [r for r in [r_interviewer, r_lore, r_staff, r_exec, r_founder] if r]
            explorer_roles = [r for r in [r_newcomer, r_explorer, r_senior_explorer, r_researcher, r_hunter, r_doctor, r_mystic, r_leader] if r]
            high_explorer_roles = [r for r in [r_senior_explorer, r_researcher, r_mystic, r_leader] if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Mysterious Island Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 📢 ศูนย์กลางเกาะ ---
            cat_hub = await safe_create_category(guild, "📢 ศูนย์กลางเกาะ", overwrites=build_overwrites(everyone, read_only=True))
            if cat_hub:
                for ch in ["📢・ประกาศจากเกาะ", "📖・กฎของเกาะ", "🗺️・แผนที่เกาะ", "📜・ประวัติเกาะลึกลับ", "🔮・ตำนานและคำทำนาย", "⚙️・ระบบโรลเพลย์"]:
                    await safe_create_text(cat_hub, ch)

            # --- 📝 ลงทะเบียนผู้มาเยือน ---
            cat_apply = await safe_create_category(guild, "📝 ลงทะเบียนผู้มาเยือน")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ใบสมัครผู้มาเยือน", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "⏳・รอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจสอบใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_voice(cat_apply, "🪑・ห้องรอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการคัดเลือก", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles, read_only=True))
                await safe_create_text(cat_apply, "❌・ไม่ผ่านการคัดเลือก", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🏖️ เขตชายฝั่ง ---
            cat_coast = await safe_create_category(guild, "🏖️ เขตชายฝั่ง", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_coast:
                for ch in ["⚓・ท่าเรือ", "🏕️・ค่ายผู้รอดชีวิต", "🛖・หมู่บ้านริมทะเล", "🐚・ชายหาดลึกลับ", "🌊・หน้าผาริมทะเล"]:
                    await safe_create_text(cat_coast, ch)
                await safe_create_voice(cat_coast, "🔊・ท่าเรือ")
                await safe_create_voice(cat_coast, "🔊・ค่ายพัก")

            # --- 🌴 ป่าต้องห้าม ---
            cat_jungle = await safe_create_category(guild, "🌴 ป่าต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_jungle:
                for ch in ["🌲・ป่าลึกลับ", "🐾・ร่องรอยปริศนา", "🌿・พืชประหลาด", "🕳️・ถ้ำใต้ดิน", "🗿・รูปปั้นโบราณ"]:
                    await safe_create_text(cat_jungle, ch)
                await safe_create_voice(cat_jungle, "🔊・ป่าลึก")

            # --- 🏛️ ซากอารยธรรมโบราณ ---
            cat_ruins = await safe_create_category(guild, "🏛️ ซากอารยธรรมโบราณ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_ruins:
                await safe_create_text(cat_ruins, "🗿・วิหารโบราณ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
                await safe_create_text(cat_ruins, "🔐・ห้องปริศนา", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_text(cat_ruins, "📜・จารึกโบราณ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
                await safe_create_text(cat_ruins, "💎・ห้องสมบัติ", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_text(cat_ruins, "👁️・แท่นบูชาต้องสาป", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_text(cat_ruins, "🚪・ประตูลึกลับ", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_voice(cat_ruins, "🔊・วิหารโบราณ")

            # --- ☠️ เขตอันตราย ---
            cat_danger = await safe_create_category(guild, "☠️ เขตอันตราย", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_danger:
                await safe_create_text(cat_danger, "🌋・ภูเขาไฟ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
                await safe_create_text(cat_danger, "💀・หุบเขามรณะ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
                await safe_create_text(cat_danger, "🌊・ทะเลต้องห้าม", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
                await safe_create_text(cat_danger, "🐉・ถ้ำสัตว์ประหลาด", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_text(cat_danger, "👹・เขตคำสาป", overwrites=build_overwrites(everyone, allowed_roles=high_explorer_roles + staff_roles))
                await safe_create_voice(cat_danger, "🔊・เขตอันตราย")

            # --- 🧭 ระบบสำรวจ ---
            cat_system = await safe_create_category(guild, "🧭 ระบบสำรวจ", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_system:
                for ch in ["📌・ภารกิจสำรวจ", "🔎・เบาะแสที่ค้นพบ", "📦・ของที่ค้นพบ", "📖・บันทึกการเดินทาง", "🧩・กระดานไขปริศนา"]:
                    await safe_create_text(cat_system, ch)
                await safe_create_text(cat_system, "🚨・แจ้งเหตุฉุกเฉิน", overwrites=build_overwrites(everyone))

            # --- 🏕️ กลุ่มผู้รอดชีวิต ---
            cat_survivors = await safe_create_category(guild, "🏕️ กลุ่มผู้รอดชีวิต", overwrites=build_overwrites(everyone, allowed_roles=explorer_roles + staff_roles))
            if cat_survivors:
                await safe_create_text(cat_survivors, "🏕️・ฐานกลุ่ม")
                await safe_create_text(cat_survivors, "📜・แผนงานกลุ่ม")
                await safe_create_voice(cat_survivors, "🔊・ห้องพักกลุ่ม")

            # --- 🌐 COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐 COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・แฟนอาร์ต", "📊・โหวต", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐 STAFF | ศูนย์ควบคุม ---
            cat_staff_zone = await safe_create_category(guild, "🔐 STAFF | ศูนย์ควบคุม", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                report_channel = await safe_create_text(cat_staff_zone, "📝・บันทึกสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📂・ข้อมูลตัวละคร", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff_zone, "🧩・จัดการปริศนา", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "📜・จัดการ-lore-เกาะ", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
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
                        title="🏝️ รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Mysterious Island RP",
                        description="โครงสร้างเกาะลึกลับ เขตสำรวจ ซากอารยธรรมโบราณ ระบบภารกิจ และยศสายอาชีพติดตั้งเรียบร้อยแล้ว!",
                        color=discord.Color.teal()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA])
                    embed.add_field(name="🎭 รายชื่อยศทั้งหมด", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมเกาะลึกลับเสร็จสมบูรณ์เรียบร้อยครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Mysterious Island RP เสร็จสิ้นสมบูรณ์ ===")

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
