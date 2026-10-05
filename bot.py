import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# รายชื่อ Discord User ID ที่มีสิทธิ์สั่งงานบอท
ALLOWED_USER_IDS = [933529869487321161, 932890657113145394]  
NEW_SERVER_NAME = "Minecraft Magic School RP"

ROLES_LIST = [
    {"name": "👤・ผู้มาเยือน", "color": discord.Color.from_rgb(149, 165, 166), "admin": False},
    {"name": "📝・ผู้สมัครเข้าเรียน", "color": discord.Color.from_rgb(230, 126, 34), "admin": False},
    {"name": "🎓・นักเรียนฝึกหัด", "color": discord.Color.from_rgb(52, 152, 219), "admin": False},
    {"name": "🎓・นักเรียน", "color": discord.Color.from_rgb(46, 204, 113), "admin": False},
    {"name": "🦅・สมาชิกหออัคคี", "color": discord.Color.from_rgb(231, 76, 60), "admin": False},
    {"name": "🐍・สมาชิกหอเงา", "color": discord.Color.from_rgb(155, 89, 182), "admin": False},
    {"name": "🦉・สมาชิกหอจันทรา", "color": discord.Color.from_rgb(52, 73, 94), "admin": False},
    {"name": "🦁・สมาชิกหอแสง", "color": discord.Color.from_rgb(241, 196, 15), "admin": False},
    {"name": "⭐・หัวหน้าหอ", "color": discord.Color.from_rgb(243, 156, 18), "admin": False},
    {"name": "📚・อาจารย์ฝึกสอน", "color": discord.Color.from_rgb(26, 188, 156), "admin": False},
    {"name": "🧙・อาจารย์", "color": discord.Color.from_rgb(22, 160, 133), "admin": False},
    {"name": "🎙️️・กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(211, 84, 0), "admin": False},
    {"name": "🔮・สภาเวทมนตร์", "color": discord.Color.from_rgb(142, 68, 173), "admin": False},
    {"name": "💼・Staff", "color": discord.Color.from_rgb(52, 152, 219), "admin": True},
    {"name": "👑・รองอธิการ", "color": discord.Color.from_rgb(192, 57, 43), "admin": True},
    {"name": "🏰・อธิการโรงเรียน", "color": discord.Color.from_rgb(128, 0, 0), "admin": True},
    {"name": "⚜️・ผู้บริหาร", "color": discord.Color.from_rgb(255, 215, 0), "admin": True},
    {"name": "👑・ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 223, 0), "admin": True},
]

async def safe_run(func, *args, **kwargs):
    while True:
        try:
            res = await func(*args, **kwargs)
            await asyncio.sleep(0.8)
            return res
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ติดบล็อกชั่วคราว รอ {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 0.5)
            else:
                print(f"[API Error] {e}")
                return None
        except Exception as e:
            print(f"[Error] {e}")
            return None

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    cmd = message.content.strip()
    if cmd in ["เริ่มงาน", "เริ่มต้น"]:
        if message.author.id not in ALLOWED_USER_IDS:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"🚀 **รับทราบคำสั่ง! กำลังเริ่มจัดสร้างเซิร์ฟเวอร์ {NEW_SERVER_NAME}...**\n*(ระบบกำลังลบช่องเก่า -> สร้างยศ -> จัดหมวดหมู่และตั้งสิทธิ์ โปรดรอสักครู่)*")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        await safe_run(guild.edit, name=NEW_SERVER_NAME)

        # 2. ลบช่องเดิมทั้งหมด
        print("--- เริ่มลบช่องเดิม ---")
        for channel in list(guild.channels):
            await safe_run(channel.delete)

        # 3. ลบยศเดิมทั้งหมด
        print("--- เริ่มลบยศเดิม ---")
        for role in list(guild.roles):
            if not role.is_default() and not role.managed:
                await safe_run(role.delete)

        # 4. สร้างยศใหม่ทั้งหมด
        print("--- เริ่มสร้างยศใหม่ ---")
        roles = {}
        for r_info in ROLES_LIST:
            perms = discord.Permissions.all() if r_info["admin"] else discord.Permissions.default()
            r_obj = await safe_run(
                guild.create_role,
                name=r_info["name"],
                color=r_info["color"],
                permissions=perms,
                hoist=True
            )
            if r_obj:
                roles[r_info["name"]] = r_obj

        # มอบยศผู้ก่อตั้งให้ผู้กดสั่ง
        r_founder = roles.get("👑・ผู้ก่อตั้ง")
        if r_founder and message.author in guild.members:
            try:
                await message.author.add_roles(r_founder)
            except:
                pass

        everyone = guild.default_role

        # Helper สร้าง Overwrite ที่ปลอดภัย
        def make_overwrite(allowed_role_names, read_only=False):
            ow = {everyone: discord.PermissionOverwrite(view_channel=False)}
            for r_name in allowed_role_names:
                r_obj = roles.get(r_name)
                if r_obj:
                    if read_only:
                        ow[r_obj] = discord.PermissionOverwrite(view_channel=True, send_messages=False, connect=True)
                    else:
                        ow[r_obj] = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True, speak=True)
            return ow

        # ----------------------------------------------------
        # 5. สร้างหมวดหมู่และช่อง
        # ----------------------------------------------------

        # --- 📜・ศูนย์กลาง ---
        cat_1 = await safe_run(guild.create_category, "📜・ศูนย์กลาง")
        if cat_1:
            ow_pub = {everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False)}
            for ch_name in ["📢・ประกาศ", "📖・กฎเซิร์ฟเวอร์", "🏫・ข้อมูลโรงเรียน", "🗺️・แผนที่โรงเรียน", "🎭・ระบบโรลเพลย์", "❓・คำถามที่พบบ่อย"]:
                await safe_run(cat_1.create_text_channel, ch_name, overwrites=ow_pub)

        # --- 📝・สมัครเข้าเรียน ---
        cat_2 = await safe_run(guild.create_category, "📝・สมัครเข้าเรียน")
        if cat_2:
            await safe_run(cat_2.create_text_channel, "📨・ยื่นใบสมัคร", overwrites={everyone: discord.PermissionOverwrite(view_channel=True, send_messages=True)})
            await safe_run(cat_2.create_text_channel, "⏳・รอสัมภาษณ์", overwrites=make_overwrite(["📝・ผู้สมัครเข้าเรียน"]))
            await safe_run(cat_2.create_voice_channel, "🎙️・ห้องสัมภาษณ์", overwrites=make_overwrite(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_2.create_voice_channel, "🪄・รอเรียกสัม", overwrites=make_overwrite(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_2.create_text_channel, "✅・ผ่านการสัมภาษณ์", overwrites=make_overwrite(["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]))
            await safe_run(cat_2.create_text_channel, "❌・ผลสัมภาษณ์", overwrites=make_overwrite(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))

        # --- 🎓・เขตโรงเรียน ---
        cat_3 = await safe_run(guild.create_category, "🎓・เขตโรงเรียน")
        if cat_3:
            student_teacher = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด", "📚・อาจารย์ฝึกสอน", "🧙・อาจารย์"]
            students = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]
            
            await safe_run(cat_3.create_text_channel, "💬・พูดคุยนักเรียน", overwrites=make_overwrite(students))
            for ch_name in ["📚・ห้องเรียน", "🪄・วิชาเวทมนตร์", "🧪・ห้องปรุงยา", "⚔️・ฝึกเวทมนตร์", "📜・การบ้าน"]:
                await safe_run(cat_3.create_text_channel, ch_name, overwrites=make_overwrite(student_teacher))
            
            await safe_run(cat_3.create_text_channel, "🎒・ภารกิจนักเรียน", overwrites=make_overwrite(students))
            await safe_run(cat_3.create_text_channel, "🏆・กิจกรรมโรงเรียน", overwrites=make_overwrite(students))
            await safe_run(cat_3.create_voice_channel, "🔊・ห้องเรียนเสียง", overwrites=make_overwrite(student_teacher))
            await safe_run(cat_3.create_voice_channel, "🗣️・ห้องสนทนา", overwrites=make_overwrite(students))

        # --- 🔮・หอพักนักเรียน ---
        cat_4 = await safe_run(guild.create_category, "🔮・หอพักนักเรียน")
        if cat_4:
            students = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]
            await safe_run(cat_4.create_text_channel, "🏠・หอพักรวม", overwrites=make_overwrite(students))
            await safe_run(cat_4.create_voice_channel, "🛏️・ห้องพัก", overwrites=make_overwrite(students))
            
            await safe_run(cat_4.create_text_channel, "🦅・หออัคคี", overwrites=make_overwrite(["🦅・สมาชิกหออัคคี"]))
            await safe_run(cat_4.create_voice_channel, "🔥・ห้องนั่งเล่น", overwrites=make_overwrite(["🦅・สมาชิกหออัคคี"]))
            
            await safe_run(cat_4.create_text_channel, "🐍・หอเงา", overwrites=make_overwrite(["🐍・สมาชิกหอเงา"]))
            await safe_run(cat_4.create_voice_channel, "🌑・ห้องนั่งเล่น", overwrites=make_overwrite(["🐍・สมาชิกหอเงา"]))
            
            await safe_run(cat_4.create_text_channel, "🦉・หอจันทรา", overwrites=make_overwrite(["🦉・สมาชิกหอจันทรา"]))
            await safe_run(cat_4.create_voice_channel, "🌙・ห้องนั่งเล่น", overwrites=make_overwrite(["🦉・สมาชิกหอจันทรา"]))
            
            await safe_run(cat_4.create_text_channel, "🦁・หอแสง", overwrites=make_overwrite(["🦁・สมาชิกหอแสง"]))
            await safe_run(cat_4.create_voice_channel, "☀️・ห้องนั่งเล่น", overwrites=make_overwrite(["🦁・สมาชิกหอแสง"]))

        # --- 🌐・COMMUNITY | นอกโรล ---
        cat_5 = await safe_run(guild.create_category, "🌐・COMMUNITY | นอกโรล")
        if cat_5:
            await safe_run(cat_5.create_text_channel, "📣・ประกาศคอมมู", overwrites={everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False)})
            
            ow_comm_text = {everyone: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
            for ch_name in ["💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・งานแฟนอาร์ต", "📊・โหวตและกิจกรรม", "🎉・กิจกรรมคอมมู"]:
                await safe_run(cat_5.create_text_channel, ch_name, overwrites=ow_comm_text)
                
            ow_comm_vc = {everyone: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)}
            for vc_name in ["🎙️・ห้องคุยเล่น 1", "🎙️・ห้องคุยเล่น 2", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                await safe_run(cat_5.create_voice_channel, vc_name, overwrites=ow_comm_vc)

        # --- 👑・ฝ่ายบริหารโรงเรียน ---
        cat_6 = await safe_run(guild.create_category, "👑・ฝ่ายบริหารโรงเรียน")
        if cat_6:
            await safe_run(cat_6.create_text_channel, "🏛・ห้องอธิการ", overwrites=make_overwrite(["🏰・อธิการโรงเรียน", "👑・รองอธิการ"]))
            await safe_run(cat_6.create_text_channel, "📋・ห้องอาจารย์", overwrites=make_overwrite(["🧙・อาจารย์", "📚・อาจารย์ฝึกสอน"]))
            await safe_run(cat_6.create_text_channel, "🧙・สภาเวทมนตร์", overwrites=make_overwrite(["🔮・สภาเวทมนตร์"]))
            await safe_run(cat_6.create_text_channel, "📑・งานฝ่ายบริหาร", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_6.create_text_channel, "🚨・แจ้งปัญหา", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_6.create_voice_channel, "🔊・ห้องประชุม", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_6.create_voice_channel, "🎙️・ประชุมสภา", overwrites=make_overwrite(["🔮・สภาเวทมนตร์"]))

        # --- 🔐・STAFF ZONE ---
        cat_7 = await safe_run(guild.create_category, "🔐・STAFF ZONE")
        report_ch = None
        if cat_7:
            report_ch = await safe_run(cat_7.create_text_channel, "💼・ห้อง Staff", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_7.create_text_channel, "📝・บันทึกสัมภาษณ์", overwrites=make_overwrite(["🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_7.create_text_channel, "📂・ข้อมูลนักเรียน", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_7.create_text_channel, "⚖️・พิจารณาโทษ", overwrites=make_overwrite(["⚜️️・ผู้บริหาร", "🏰・อธิการโรงเรียน", "👑・รองอธิการ"]))
            await safe_run(cat_7.create_text_channel, "🤖・ห้องบอท", overwrites=make_overwrite(["💼・Staff"]))
            await safe_run(cat_7.create_voice_channel, "🔊・ห้อง Staff", overwrites=make_overwrite(["💼・Staff"]))

        # 6. รายงานสรุปเมื่อสร้างเสร็จสมบูรณ์
        target_send = report_ch if report_ch else guild.system_channel
        if target_send:
            embed = discord.Embed(
                title="🏰 จัดตั้ง Magic School RP เรียบร้อยแล้ว!",
                description=f"สร้างยศ หมวดหมู่ และห้องทั้งหมดสำหรับ **{NEW_SERVER_NAME}** เรียบร้อยแล้วครับ",
                color=discord.Color.purple()
            )
            await safe_run(target_send.send, embed=embed)

        print("=== สร้าง Magic School RP เสร็จสิ้นสมบูรณ์ ===")

@bot.event
async def on_ready():
    print(f"บอท {bot.user} ออนไลน์พร้อมใช้งานแล้ว!")

async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ไม่พบ TOKEN ในระบบ")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
