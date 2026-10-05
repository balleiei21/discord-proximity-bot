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
NEW_SERVER_NAME = "Minecraft Magic School RP"

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

ROLES_DATA = [
    {"name": "👤 ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "permissions": perm_member, "desc": "ผู้เข้าชมทั่วไป"},
    {"name": "📝 ผู้สมัครเข้าเรียน", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ที่กำลังยื่นใบสมัคร/รอสัมภาษณ์"},
    {"name": "🎓 นักเรียนฝึกหัด", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "นักเรียนที่เพิ่งผ่านสัมภาษณ์"},
    {"name": "🎓 นักเรียน", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "นักเรียนประจำโรงเรียน"},
    {"name": "🦅 สมาชิกหออัคคี", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_member, "desc": "นักเรียนหออัคคี"},
    {"name": "🐍 สมาชิกหอเงา", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_member, "desc": "นักเรียนหอเงา"},
    {"name": "🦉 สมาชิกหอจันทรา", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "นักเรียนหอจันทรา"},
    {"name": "🦁 สมาชิกหอแสง", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "นักเรียนหอแสง"},
    {"name": "⭐ หัวหน้าหอ", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "หัวหน้าประจำหอพัก"},
    {"name": "📚 อาจารย์ฝึกสอน", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_staff, "desc": "อาจารย์ผู้ช่วย/ฝึกสอน"},
    {"name": "🧙 อาจารย์", "color": discord.Color.from_rgb(22, 160, 133), "permissions": perm_staff, "desc": "อาจารย์ผู้สอนวิชาต่างๆ"},
    {"name": "🎙️ กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_staff, "desc": "ทีมงานดูแลการรับสมัครและสัมภาษณ์"},
    {"name": "🔮 สภาเวทมนตร์", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ทีมงานดูแลระบบเวทมนตร์และกฎระเบียบ"},
    {"name": "👑 รองอธิการ", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_admin, "desc": "ผู้ช่วยผู้บริหารโรงเรียน"},
    {"name": "🏰 อธิการโรงเรียน", "color": discord.Color.from_rgb(120, 40, 31), "permissions": perm_admin, "desc": "ผู้ดูแลสูงสุดฝ่ายวิชาการและโรงเรียน"},
    {"name": "⚜️ ผู้บริหาร", "color": discord.Color.from_rgb(243, 156, 18), "permissions": perm_admin, "desc": "ผู้บริหารระบบและเซิร์ฟเวอร์"},
    {"name": "👑 ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_owner, "desc": "เจ้าของเซิร์ฟเวอร์/ผู้ก่อตั้ง"}
]

# ----------------------------------------------------
# 2. ฟังก์ชันช่วยสร้างช่องอย่างปลอดภัย (พร้อมระบบ Retry จำกัดรอบ)
# ----------------------------------------------------
async def safe_create_category(guild, name, overwrites=None):
    for attempt in range(5):
        try:
            cat = await guild.create_category(name, overwrites=overwrites)
            print(f"✅ สร้างหมวดหมู่: {name}")
            await asyncio.sleep(0.8) # เพิ่มเวลาชะลอเล็กน้อยเพื่อไม่ให้โดน Rate limit
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
    print(f"⚠️ ลองสร้างหมวดหมู่ {name} ครบ 5 ครั้งแล้วยังไม่ได้ ข้ามการสร้าง...")
    return None

async def safe_create_text(category, name, overwrites=None):
    if not category:
        print(f"⚠️ ข้ามการสร้างช่องข้อความ {name} เนื่องจากไม่มีหมวดหมู่")
        return None
    for attempt in range(5):
        try:
            ch = await category.create_text_channel(name, overwrites=overwrites)
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
    for attempt in range(5):
        try:
            vc = await category.create_voice_channel(name, overwrites=overwrites)
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
            r_student = get_r("🎓 นักเรียน")
            r_apprentice = get_r("🎓 นักเรียนฝึกหัด")
            r_fire = get_r("🦅 สมาชิกหออัคคี")
            r_shadow = get_r("🐍 สมาชิกหอเงา")
            r_moon = get_r("🦉 สมาชิกหอจันทรา")
            r_sun = get_r("🦁 สมาชิกหอแสง")
            r_teacher_apprentice = get_r("📚 อาจารย์ฝึกสอน")
            r_teacher = get_r("🧙 อาจารย์")
            r_interviewer = get_r("🎙️ กรรมการสัมภาษณ์")
            r_council = get_r("🔮 สภาเวทมนตร์")
            r_sub_principal = get_r("👑 รองอธิการ")
            r_principal = get_r("🏰 อธิการโรงเรียน")
            r_exec = get_r("⚜️ ผู้บริหาร")
            r_founder = get_r("👑 ผู้ก่อตั้ง")

            if r_founder and message.author in guild.members:
                try:
                    await message.author.add_roles(r_founder)
                except:
                    pass

            staff_roles = [r for r in [r_interviewer, r_teacher_apprentice, r_teacher, r_council, r_sub_principal, r_principal, r_exec, r_founder] if r]
            student_roles = [r for r in [r_student, r_apprentice] if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 📜・ศูนย์กลาง ---
            cat_hub = await safe_create_category(guild, "📜・ศูนย์กลาง", build_overwrites(everyone, read_only=True))
            if cat_hub:
                for ch in ["📢・ประกาศ", "📖・กฎเซิร์ฟเวอร์", "🏫・ข้อมูลโรงเรียน", "🗺️・แผนที่โรงเรียน", "🎭・ระบบโรลเพลย์", "❓・คำถามที่พบบ่อย"]:
                    await safe_create_text(cat_hub, ch)

            # --- 📝・สมัครเข้าเรียน ---
            cat_apply = await safe_create_category(guild, "📝・สมัครเข้าเรียน")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・ยื่นใบสมัคร", build_overwrites(everyone))
                await safe_create_text(cat_apply, "⏳・รอสัมภาษณ์", build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🪄・รอเรียกสัม", build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการสัมภาษณ์", build_overwrites(everyone, allowed_roles=student_roles, read_only=True))
                await safe_create_text(cat_apply, "❌・ผลสัมภาษณ์", build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🎓・เขตโรงเรียน ---
            cat_school = await safe_create_category(guild, "🎓・เขตโรงเรียน", build_overwrites(everyone, allowed_roles=student_roles + staff_roles))
            if cat_school:
                await safe_create_text(cat_school, "💬・พูดคุยนักเรียน", build_overwrites(everyone, allowed_roles=student_roles))
                for ch in ["📚・ห้องเรียน", "🪄・วิชาเวทมนตร์", "🧪・ห้องปรุงยา", "⚔️・ฝึกเวทมนตร์", "📜・การบ้าน"]:
                    await safe_create_text(cat_school, ch, build_overwrites(everyone, allowed_roles=student_roles + [r_teacher, r_teacher_apprentice]))
                for ch in ["🎒・ภารกิจนักเรียน", "🏆・กิจกรรมโรงเรียน"]:
                    await safe_create_text(cat_school, ch, build_overwrites(everyone, allowed_roles=student_roles))
                    
                await safe_create_voice(cat_school, "🔊・ห้องเรียนเสียง", build_overwrites(everyone, allowed_roles=student_roles + [r_teacher, r_teacher_apprentice]))
                await safe_create_voice(cat_school, "🗣️・ห้องสนทนา", build_overwrites(everyone, allowed_roles=student_roles))

            # --- 🔮・หอพักนักเรียน ---
            cat_dorm = await safe_create_category(guild, "🔮・หอพักนักเรียน", build_overwrites(everyone, allowed_roles=student_roles))
            if cat_dorm:
                await safe_create_text(cat_dorm, "🏠・หอพักรวม", build_overwrites(everyone, allowed_roles=student_roles))
                await safe_create_voice(cat_dorm, "🛏️・ห้องพัก", build_overwrites(everyone, allowed_roles=student_roles))

                async def create_house(house_name, role_obj, txt_icon, vc_icon):
                    ow_h = build_overwrites(everyone, allowed_roles=[role_obj] if role_obj else None)
                    await safe_create_text(cat_dorm, f"{txt_icon}・{house_name}", ow_h)
                    await safe_create_voice(cat_dorm, f"{vc_icon}・ห้องนั่งเล่น", ow_h)

                await create_house("หออัคคี", r_fire, "🦅", "🔥")
                await create_house("หอเงา", r_shadow, "🐍", "🌑")
                await create_house("หอจันทรา", r_moon, "🦉", "🌙")
                await create_house("หอแสง", r_sun, "🦁", "☀️")

            # --- 🌐・COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐・COMMUNITY | นอกโรล", build_overwrites(everyone))
            if cat_comm:
                for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・งานแฟนอาร์ต", "📊・โหวตและกิจกรรม", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น 1", "🎙️・ห้องคุยเล่น 2", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 👑・ฝ่ายบริหารโรงเรียน ---
            cat_admin = await safe_create_category(guild, "👑・ฝ่ายบริหารโรงเรียน", build_overwrites(everyone, allowed_roles=staff_roles))
            if cat_admin:
                await safe_create_text(cat_admin, "🏛️・ห้องอธิการ", build_overwrites(everyone, allowed_roles=[r_principal, r_sub_principal]))
                await safe_create_text(cat_admin, "📋・ห้องอาจารย์", build_overwrites(everyone, allowed_roles=[r_teacher, r_teacher_apprentice]))
                await safe_create_text(cat_admin, "🧙・สภาเวทมนตร์", build_overwrites(everyone, allowed_roles=[r_council]))
                await safe_create_text(cat_admin, "📑・งานฝ่ายบริหาร", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_admin, "🚨・แจ้งปัญหา", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_voice(cat_admin, "🔊・ห้องประชุม", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_voice(cat_admin, "🎙️・ประชุมสภา", build_overwrites(everyone, allowed_roles=[r_council]))

            # --- 🔐・STAFF ZONE ---
            cat_staff = await safe_create_category(guild, "🔐・STAFF ZONE", build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff:
                await safe_create_text(cat_staff, "💼・ห้อง Staff", build_overwrites(everyone, allowed_roles=staff_roles))
                report_channel = await safe_create_text(cat_staff, "📝・บันทึกสัมภาษณ์", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff, "📂・ข้อมูลนักเรียน", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff, "⚖️・พิจารณาโทษ", build_overwrites(everyone, allowed_roles=[r_exec, r_principal, r_sub_principal]))
                await safe_create_text(cat_staff, "🤖・ห้องบอท", build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_voice(cat_staff, "🔊・ห้อง Staff", build_overwrites(everyone, allowed_roles=staff_roles))

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="🏰 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Magic School RP",
                        description="โครงสร้างหมวดหมู่ ห้องข้อความ ช่องเสียง และยศทั้งหมดติดตั้งสมบูรณ์เรียบร้อยแล้ว!",
                        color=discord.Color.gold()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA])
                    embed.add_field(name="🏅 รายชื่อยศทั้งหมด", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord เสร็จสมบูรณ์เรียบร้อยแล้วครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบเสร็จสิ้นสมบูรณ์ ===")

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
