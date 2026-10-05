import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Discord User ID สำหรับเรียกใช้คำสั่ง "เริ่มงาน"
ALLOWED_USER_ID = 932890657113145394  

NEW_SERVER_NAME = "Minecraft Magic School RP"

# ----------------------------------------------------
# 1. ข้อมูลยศและสิทธิ์ (Roles Data) - เรียงจากต่ำไปสูง
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
# 2. ฟังก์ชันช่วยสร้างช่องอย่างปลอดภัย (Prevent Rate Limit)
# ----------------------------------------------------
async def safe_create_category(guild, name, overwrites=None):
    while True:
        try:
            cat = await guild.create_category(name, overwrites=overwrites)
            await asyncio.sleep(0.4)
            return cat
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                await asyncio.sleep(retry_after)
            else:
                print(f"ไม่สามารถสร้างหมวดหมู่ {name} ได้: {e}")
                return None

async def safe_create_text(category, name, overwrites=None):
    while True:
        try:
            ch = await category.create_text_channel(name, overwrites=overwrites)
            await asyncio.sleep(0.4)
            return ch
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                await asyncio.sleep(retry_after)
            else:
                print(f"ไม่สามารถสร้างช่องข้อความ {name} ได้: {e}")
                return None

async def safe_create_voice(category, name, overwrites=None):
    while True:
        try:
            vc = await category.create_voice_channel(name, overwrites=overwrites)
            await asyncio.sleep(0.4)
            return vc
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                await asyncio.sleep(retry_after)
            else:
                print(f"ไม่สามารถสร้างช่องเสียง {name} ได้: {e}")
                return None

# ----------------------------------------------------
# 3. คำสั่งระบบทำงาน
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "เริ่มงาน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"⏳ **กำลังดำเนินการสร้างโครงสร้าง {NEW_SERVER_NAME}...**\n*(ระบบจะสร้างยศ หมวดหมู่ และปรับแต่งสิทธิ์อย่างสมบูรณ์)*")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # 2. ลบช่องเดิมทั้งหมด
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่สำเร็จ: {e}")

        # 3. ลบยศเดิมทั้งหมด
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"ลบยศ {role.name} ไม่สำเร็จ: {e}")

        # 4. สร้างยศใหม่ตามลำดับ (ยศสูงสร้างก่อนเพื่อให้ Hierarchy ถูกต้อง)
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
                    await asyncio.sleep(0.3)
                    break
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = getattr(e, 'retry_after', 5.0)
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"สร้างยศ {role_info['name']} ไม่สำเร็จ: {e}")
                        break

        everyone = guild.default_role

        # ฟังก์ชันช่วยดึงยศ
        def get_r(name): return created_roles.get(name)

        r_applicant = get_r("📝 ผู้สมัครเข้าเรียน")
        r_student = get_r("🎓 นักเรียน")
        r_fire = get_r("🦅 สมาชิกหออัคคี")
        r_shadow = get_r("🐍 สมาชิกหอเงา")
        r_moon = get_r("🦉 สมาชิกหอจันทรา")
        r_sun = get_r("🦁 สมาชิกหอแสง")
        r_teacher = get_r("🧙 อาจารย์")
        r_interviewer = get_r("🎙️ กรรมการสัมภาษณ์")
        r_council = get_r("🔮 สภาเวทมนตร์")
        r_principal = get_r("🏰 อธิการโรงเรียน")
        r_exec = get_r("⚜️ ผู้บริหาร")

        # กลุ่มยศทีมงาน (Staff)
        staff_roles = [r for r in [r_interviewer, r_teacher, r_council, get_r("👑 รองอธิการ"), r_principal, r_exec, get_r("👑 ผู้ก่อตั้ง")] if r]

        report_channel = None

        # ----------------------------------------------------
        # 5. สร้างโครงสร้างช่องและหมวดหมู่
        # ----------------------------------------------------

        # --- 📜・ศูนย์กลาง ---
        cat_hub = await safe_create_category(guild, "📜・ศูนย์กลาง", {
            everyone: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        })
        for ch in ["📢・ประกาศ", "📖・กฎเซิร์ฟเวอร์", "🏫・ข้อมูลโรงเรียน", "🗺️・แผนที่โรงเรียน", "🎭・ระบบโรลเพลย์", "❓・คำถามที่พบบ่อย"]:
            await safe_create_text(cat_hub, ch)

        # --- 📝・สมัครเข้าเรียน ---
        cat_apply = await safe_create_category(guild, "📝・สมัครเข้าเรียน")
        await safe_create_text(cat_apply, "📨・ยื่นใบสมัคร", {everyone: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
        
        ov_app = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_applicant: ov_app[r_applicant] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        await safe_create_text(cat_apply, "⏳・รอสัมภาษณ์", ov_app)

        ov_int_v = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_applicant: ov_int_v[r_applicant] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)
        if r_interviewer: ov_int_v[r_interviewer] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)
        await safe_create_voice(cat_apply, "🎙️・ห้องสัมภาษณ์", ov_int_v)
        await safe_create_voice(cat_apply, "🪄・รอเรียกสัม", ov_int_v)

        ov_pass = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_student: ov_pass[r_student] = discord.PermissionOverwrite(read_messages=True)
        await safe_create_text(cat_apply, "✅・ผ่านการสัมภาษณ์", ov_pass)

        ov_fail = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_applicant: ov_fail[r_applicant] = discord.PermissionOverwrite(read_messages=True)
        if r_interviewer: ov_fail[r_interviewer] = discord.PermissionOverwrite(read_messages=True)
        await safe_create_text(cat_apply, "❌・ผลสัมภาษณ์", ov_fail)

        # --- 🎓・เขตโรงเรียน ---
        cat_school = await safe_create_category(guild, "🎓・เขตโรงเรียน", {everyone: discord.PermissionOverwrite(read_messages=False)})
        
        ov_student = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_student: ov_student[r_student] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        
        ov_class = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_student: ov_class[r_student] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        if r_teacher: ov_class[r_teacher] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        await safe_create_text(cat_school, "💬・พูดคุยนักเรียน", ov_student)
        for ch in ["📚・ห้องเรียน", "🪄・วิชาเวทมนตร์", "🧪・ห้องปรุงยา", "⚔️・ฝึกเวทมนตร์", "📜・การบ้าน"]:
            await safe_create_text(cat_school, ch, ov_class)
        for ch in ["🎒・ภารกิจนักเรียน", "🏆・กิจกรรมโรงเรียน"]:
            await safe_create_text(cat_school, ch, ov_student)
            
        ov_class_v = {everyone: discord.PermissionOverwrite(read_messages=False)}
        if r_student: ov_class_v[r_student] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)
        if r_teacher: ov_class_v[r_teacher] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)
        
        await safe_create_voice(cat_school, "🔊・ห้องเรียนเสียง", ov_class_v)
        await safe_create_voice(cat_school, "🗣️・ห้องสนทนา", ov_student)

        # --- 🔮・หอพักนักเรียน ---
        cat_dorm = await safe_create_category(guild, "🔮・หอพักนักเรียน", {everyone: discord.PermissionOverwrite(read_messages=False)})
        await safe_create_text(cat_dorm, "🏠・หอพักรวม", ov_student)
        await safe_create_voice(cat_dorm, "🛏️・ห้องพัก", ov_student)

        # ฟังก์ชันช่วยสร้างหอพักประจำบ้าน
        async def create_house(house_name, role_obj, txt_icon, vc_icon):
            ov_h = {everyone: discord.PermissionOverwrite(read_messages=False)}
            if role_obj: ov_h[role_obj] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
            await safe_create_text(cat_dorm, f"{txt_icon}・{house_name}", ov_h)
            await safe_create_voice(cat_dorm, f"{vc_icon}・ห้องนั่งเล่น", ov_h)

        await create_house("หออัคคี", r_fire, "🦅", "🔥")
        await create_house("หอเงา", r_shadow, "🐍", "🌑")
        await create_house("หอจันทรา", r_moon, "🦉", "🌙")
        await create_house("หอแสง", r_sun, "🦁", "☀️")

        # --- 🌐・COMMUNITY | นอกโรล ---
        cat_comm = await safe_create_category(guild, "🌐・COMMUNITY | นอกโรล", {everyone: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)})
        for ch in ["📣・ประกาศคอมมู", "💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・งานแฟนอาร์ต", "📊・โหวตและกิจกรรม", "🎉・กิจกรรมคอมมู"]:
            await safe_create_text(cat_comm, ch)
        for vc in ["🎙️・ห้องคุยเล่น 1", "🎙️・ห้องคุยเล่น 2", "🎮・ห้องเล่นเกม", "💤・AFK"]:
            await safe_create_voice(cat_comm, vc)

        # --- 👑・ฝ่ายบริหารโรงเรียน ---
        cat_admin = await safe_create_category(guild, "👑・ฝ่ายบริหารโรงเรียน", {everyone: discord.PermissionOverwrite(read_messages=False)})
        
        def make_ov(allowed_roles):
            ov = {everyone: discord.PermissionOverwrite(read_messages=False)}
            for r in allowed_roles:
                if r: ov[r] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
            return ov

        await safe_create_text(cat_admin, "🏛️・ห้องอธิการ", make_ov([r_principal]))
        await safe_create_text(cat_admin, "📋・ห้องอาจารย์", make_ov([r_teacher]))
        await safe_create_text(cat_admin, "🧙・สภาเวทมนตร์", make_ov([r_council]))
        await safe_create_text(cat_admin, "📑・งานฝ่ายบริหาร", make_ov(staff_roles))
        await safe_create_text(cat_admin, "🚨・แจ้งปัญหา", make_ov(staff_roles))
        await safe_create_voice(cat_admin, "🔊・ห้องประชุม", make_ov(staff_roles))
        await safe_create_voice(cat_admin, "🎙️・ประชุมสภา", make_ov([r_council]))

        # --- 🔐・STAFF ZONE ---
        cat_staff = await safe_create_category(guild, "🔐・STAFF ZONE", {everyone: discord.PermissionOverwrite(read_messages=False)})
        await safe_create_text(cat_staff, "💼・ห้อง Staff", make_ov(staff_roles))
        
        report_channel = await safe_create_text(cat_staff, "📝・บันทึกสัมภาษณ์", make_ov([r_interviewer] + staff_roles))
        await safe_create_text(cat_staff, "📂・ข้อมูลนักเรียน", make_ov(staff_roles))
        await safe_create_text(cat_staff, "⚖️・พิจารณาโทษ", make_ov([r_exec, r_principal]))
        await safe_create_text(cat_staff, "🤖・ห้องบอท", make_ov(staff_roles))
        await safe_create_voice(cat_staff, "🔊・ห้อง Staff", make_ov(staff_roles))

        # ----------------------------------------------------
        # 6. ส่งรายงานสรุปโครงสร้างลงห้อง 📝・บันทึกสัมภาษณ์
        # ----------------------------------------------------
        if report_channel:
            try:
                embed = discord.Embed(
                    title="🏰 รายงานการตั้งค่าเซิร์ฟเวอร์ Minecraft Magic School RP",
                    description="โครงสร้างห้องและยศทั้งหมดถูกติดตั้งและจัดตั้งสิทธิ์เรียบร้อยแล้ว!",
                    color=discord.Color.gold()
                )

                roles_str = "\n".join([f"• **{r['name']}** — {r['desc']}" for r in ROLES_DATA])
                embed.add_field(name="🏅 รายชื่อยศทั้งหมด (เรียงจากสูงไปต่ำ)", value=roles_str, inline=False)
                
                await report_channel.send(embed=embed)
                await report_channel.send("✅ **การติดตั้งโครงสร้าง Discord เสร็จสมบูรณ์แล้วครับ!**")
            except Exception as e:
                print(f"ส่งรายงานไม่สำเร็จ: {e}")

@bot.event
async def on_ready():
    print(f"บอท {bot.user} ออนไลน์พร้อมใช้งานแล้ว!")

# โครงสร้างสำหรับ Python 3.13+ และ Railway
async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ไม่พบ TOKEN ในระบบ กรุณาตรวจสอบ Environment Variable บน Railway")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
