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
NEW_SERVER_NAME = "Minecraft Apocalypse RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data - Apocalypse Theme)
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
    {"name": "📝 ผู้สมัคร", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member, "desc": "ผู้ยื่นใบสมัครรอสัมภาษณ์"},
    {"name": "☣️ ผู้รอดชีวิตใหม่", "color": discord.Color.from_rgb(52, 152, 219), "permissions": perm_member, "desc": "ผ่านสัมภาษณ์กำลังเริ่มต้น RP"},
    {"name": "🏕️ ผู้รอดชีวิต", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member, "desc": "สมาชิกหลักของเขตปลอดภัย"},
    {"name": "⭐ ผู้รอดชีวิตอาวุโส", "color": discord.Color.from_rgb(230, 126, 34), "permissions": perm_member, "desc": "ผู้รอดชีวิตที่มีประสบการณ์สูง"},
    {"name": "🛡️ หน่วยรักษาความปลอดภัย", "color": discord.Color.from_rgb(52, 73, 94), "permissions": perm_member, "desc": "ฝ่ายคุ้มกันและรักษาความสงบ"},
    {"name": "🔧 กลุ่มช่าง", "color": discord.Color.from_rgb(211, 84, 0), "permissions": perm_member, "desc": "ฝ่ายประดิษฐ์และซ่อมบำรุง"},
    {"name": "🧪 นักวิจัย", "color": discord.Color.from_rgb(26, 188, 156), "permissions": perm_member, "desc": "ฝ่ายค้นคว้าวิจัยยารักษาและไวรัส"},
    {"name": "🗡️ นักล่า", "color": discord.Color.from_rgb(192, 57, 43), "permissions": perm_member, "desc": "ฝ่ายออกล่าและจัดหาเสบียงนอกกำแพง"},
    {"name": "🏴 กลุ่มอิสระ", "color": discord.Color.from_rgb(127, 140, 141), "permissions": perm_member, "desc": "ผู้รอดชีวิตเร่ร่อนไม่ฝักใฝ่ฝ่ายใด"},
    {"name": "👑 หัวหน้ากลุ่ม", "color": discord.Color.from_rgb(243, 156, 18), "permissions": perm_member, "desc": "ผู้นำของกลุ่ม/ฝ่ายต่างๆ"},
    {"name": "🎙️ กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(155, 89, 182), "permissions": perm_staff, "desc": "ทีมงานดูแลการรับสมัครและสัมภาษณ์"},
    {"name": "📜 Lore Team", "color": discord.Color.from_rgb(142, 68, 173), "permissions": perm_staff, "desc": "ทีมงานดูแลเนื้อเรื่องและกิจกรรม RP"},
    {"name": "🛠️ Staff", "color": discord.Color.from_rgb(39, 174, 96), "permissions": perm_staff, "desc": "ทีมงานผู้ดูแลความเรียบร้อยทั่วไป"},
    {"name": "⚜️ ผู้บริหาร", "color": discord.Color.from_rgb(231, 76, 60), "permissions": perm_admin, "desc": "ผู้บริหารระดับสูง"},
    {"name": "☢️ ผู้ดูแลสูงสุด", "color": discord.Color.from_rgb(120, 40, 31), "permissions": perm_admin, "desc": "ผู้ดูแลระบบและเซิร์ฟเวอร์"},
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

            r_applicant = get_r("📝 ผู้สมัคร")
            r_new_survivor = get_r("☣️ ผู้รอดชีวิตใหม่")
            r_survivor = get_r("🏕️ ผู้รอดชีวิต")
            r_senior = get_r("⭐ ผู้รอดชีวิตอาวุโส")
            
            r_guard = get_r("🛡️ หน่วยรักษาความปลอดภัย")
            r_engineer = get_r("🔧 กลุ่มช่าง")
            r_researcher = get_r("🧪 นักวิจัย")
            r_hunter = get_r("🗡️ นักล่า")
            r_indie = get_r("🏴 กลุ่มอิสระ")
            r_leader = get_r("👑 หัวหน้ากลุ่ม")

            r_interviewer = get_r("🎙️ กรรมการสัมภาษณ์")
            r_lore = get_r("📜 Lore Team")
            r_staff = get_r("🛠️ Staff")
            r_exec = get_r("⚜️ ผู้บริหาร")
            r_head = get_r("☢️️ ผู้ดูแลสูงสุด")
            r_founder = get_r("👑 ผู้ก่อตั้ง")

            if r_founder and message.author in guild.members:
                try:
                    await message.author.add_roles(r_founder)
                except:
                    pass

            staff_roles = [r for r in [r_interviewer, r_lore, r_staff, r_exec, r_head, r_founder] if r]
            survivor_roles = [r for r in [r_new_survivor, r_survivor, r_senior, r_guard, r_engineer, r_researcher, r_hunter, r_indie, r_leader] if r]

            # ----------------------------------------------------
            # 5. สร้างโครงสร้างช่องและหมวดหมู่ (Apocalypse Theme)
            # ----------------------------------------------------
            print("--- เริ่มสร้างหมวดหมู่และช่อง ---")

            # --- 📢・ศูนย์กลางผู้รอดชีวิต ---
            cat_hub = await safe_create_category(guild, "📢・ศูนย์กลางผู้รอดชีวิต", overwrites=build_overwrites(everyone, read_only=True))
            if cat_hub:
                for ch in ["📢・ประกาศ", "📖・กฎเซิร์ฟเวอร์", "🌍・ข้อมูลโลก", "📜・lore-โลกหลังหายนะ", "🗺️・แผนที่พื้นที่", "⚙️・ระบบ-rp"]:
                    await safe_create_text(cat_hub, ch)

            # --- 📝・ลงทะเบียนผู้รอดชีวิต ---
            cat_apply = await safe_create_category(guild, "📝・ลงทะเบียนผู้รอดชีวิต")
            if cat_apply:
                await safe_create_text(cat_apply, "📨・สมัครเข้าเซิร์ฟ", overwrites=build_overwrites(everyone))
                await safe_create_text(cat_apply, "⏳・รอสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant]))
                await safe_create_text(cat_apply, "📋・ตรวจสอบใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_voice(cat_apply, "🪑・รอเรียกสัม", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer]))
                await safe_create_text(cat_apply, "✅・ผ่านการสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles, read_only=True))
                await safe_create_text(cat_apply, "❌・ผลสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_applicant, r_interviewer], read_only=True))

            # --- 🏚️・เขตปลอดภัย ---
            cat_safe = await safe_create_category(guild, "🏚️・เขตปลอดภัย", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles + staff_roles))
            if cat_safe:
                for ch in ["🏘️・จัตุรัสผู้รอดชีวิต", "🏪・ตลาดแลกเปลี่ยน", "📦・คลังเสบียง", "🏥・สถานพยาบาล", "🔧・โรงซ่อม", "📜・ประกาศภารกิจ", "💬・พูดคุยในแคมป์"]:
                    await safe_create_text(cat_safe, ch)
                await safe_create_voice(cat_safe, "🔊・ลานพักผู้รอดชีวิต")

            # --- ☣️️・เขตอันตราย ---
            cat_danger = await safe_create_category(guild, "☣️️・เขตอันตราย", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles + staff_roles))
            if cat_danger:
                for ch in ["🏙️・เมืองร้าง", "☢️・เขตปนเปื้อน", "🏭・โรงงานร้าง", "🚇・อุโมงค์ใต้ดิน", "🌲・เขตป่าเถื่อน", "🏚️・อาคารร้าง", "⚠️️・เขตต้องห้าม", "📡・สัญญาณฉุกเฉิน"]:
                    await safe_create_text(cat_danger, ch)

            # --- 🎒・ระบบเอาตัวรอด ---
            cat_survival = await safe_create_category(guild, "🎒・ระบบเอาตัวรอด", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles + staff_roles))
            if cat_survival:
                for ch in ["🍖・เสบียง", "🔧・ไอเทมและทรัพยากร", "🧭・ภารกิจสำรวจ", "📦・ของที่พบเจอ", "🩹・สถานะตัวละคร", "🏆・บันทึกภารกิจ"]:
                    await safe_create_text(cat_survival, ch)

            # --- 🏴・กลุ่มผู้รอดชีวิต ---
            cat_groups = await safe_create_category(guild, "🏴・กลุ่มผู้รอดชีวิต", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles + staff_roles))
            if cat_groups:
                async def create_faction_channels(faction_name, role_obj, txt_icon):
                    ow_f = build_overwrites(everyone, allowed_roles=[role_obj] if role_obj else None)
                    await safe_create_text(cat_groups, f"{txt_icon}・{faction_name}", overwrites=ow_f)
                    await safe_create_voice(cat_groups, f"🔊・วิทยุ-{faction_name}", overwrites=ow_f)

                await safe_create_text(cat_groups, "🏕️・ค่ายผู้รอดชีวิต", overwrites=build_overwrites(everyone, allowed_roles=survivor_roles))
                await create_faction_channels("หน่วยรักษาความปลอดภัย", r_guard, "🛡️")
                await create_faction_channels("กลุ่มช่าง", r_engineer, "🔧")
                await create_faction_channels("กลุ่มนักวิจัย", r_researcher, "🧪")
                await create_faction_channels("กลุ่มนักล่า", r_hunter, "🗡️")
                await create_faction_channels("กลุ่มอิสระ", r_indie, "🏴")

            # --- 🌐・COMMUNITY | นอกโรล ---
            cat_comm = await safe_create_category(guild, "🌐・COMMUNITY | นอกโรล", overwrites=build_overwrites(everyone))
            if cat_comm:
                for ch in ["💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・รูปภาพ", "🎨・แฟนอาร์ต", "📊・โหวต", "🎉・กิจกรรมคอมมู"]:
                    await safe_create_text(cat_comm, ch)
                for vc in ["🎙️・ห้องคุยเล่น", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                    await safe_create_voice(cat_comm, vc)

            # --- 🔐・STAFF | ศูนย์บัญชาการ ---
            cat_staff_zone = await safe_create_category(guild, "🔐・STAFF | ศูนย์บัญชาการ", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
            report_channel = None
            if cat_staff_zone:
                await safe_create_text(cat_staff_zone, "💼・ห้อง-staff", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff_zone, "📋・ตรวจใบสมัคร", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                report_channel = await safe_create_text(cat_staff_zone, "📝・บันทึกสัมภาษณ์", overwrites=build_overwrites(everyone, allowed_roles=[r_interviewer, r_staff, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "👤・ข้อมูลผู้รอดชีวิต", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_text(cat_staff_zone, "📜・จัดการ-lore", overwrites=build_overwrites(everyone, allowed_roles=[r_lore, r_exec, r_founder]))
                await safe_create_text(cat_staff_zone, "⚖️・พิจารณาโทษ", overwrites=build_overwrites(everyone, allowed_roles=[r_exec, r_head, r_founder]))
                await safe_create_text(cat_staff_zone, "🚨・เหตุการณ์ฉุกเฉิน", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))
                await safe_create_voice(cat_staff_zone, "🔊・ห้องประชุม-staff", overwrites=build_overwrites(everyone, allowed_roles=staff_roles))

            # ----------------------------------------------------
            # 6. ส่งรายงานสรุปโครงสร้าง
            # ----------------------------------------------------
            target_ch = report_channel or guild.system_channel
            if target_ch:
                try:
                    embed = discord.Embed(
                        title="☣️ รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Apocalypse RP",
                        description="โครงสร้างเขตปลอดภัย เขตอันตราย ระบบสมัคร และยศทั้งหมดติดตั้งสมบูรณ์เรียบร้อยแล้ว!",
                        color=discord.Color.dark_gold()
                    )
                    roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA])
                    embed.add_field(name="🏅 รายชื่อยศทั้งหมด", value=roles_str, inline=False)
                    
                    await target_ch.send(embed=embed)
                    await target_ch.send("✅ **การติดตั้งโครงสร้าง Discord ธีมโลกหลังหายนะเสร็จสมบูรณ์ครับ!**")
                except Exception as e:
                    print(f"ส่งรายงานไม่สำเร็จ: {e}")

            print("=== 🎉 สร้างระบบ Apocalypse RP เสร็จสิ้นสมบูรณ์ ===")

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
