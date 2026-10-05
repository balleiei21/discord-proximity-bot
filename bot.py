import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ใส่ Discord User ID ของคุณที่ได้รับอนุญาตให้กดสั่ง
ALLOWED_USER_ID = 933529869487321161  
NEW_SERVER_NAME = "Minecraft Magic School RP"

# ----------------------------------------------------
# 1. รายการยศ (เรียงจากต่ำ -> สูง)
# ----------------------------------------------------
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
    {"name": "🎙️・กรรมการสัมภาษณ์", "color": discord.Color.from_rgb(211, 84, 0), "admin": False},
    {"name": "🔮・สภาเวทมนตร์", "color": discord.Color.from_rgb(142, 68, 173), "admin": False},
    {"name": "💼・Staff", "color": discord.Color.from_rgb(52, 152, 219), "admin": True},
    {"name": "👑・รองอธิการ", "color": discord.Color.from_rgb(192, 57, 43), "admin": True},
    {"name": "🏰・อธิการโรงเรียน", "color": discord.Color.from_rgb(128, 0, 0), "admin": True},
    {"name": "⚜️・ผู้บริหาร", "color": discord.Color.from_rgb(255, 215, 0), "admin": True},
    {"name": "👑・ผู้ก่อตั้ง", "color": discord.Color.from_rgb(255, 223, 0), "admin": True},
]

# ----------------------------------------------------
# ฟังก์ชันช่วยเรียก API ป้องกัน ติด Rate Limit (429)
# ----------------------------------------------------
async def safe_run(func, *args, **kwargs):
    while True:
        try:
            res = await func(*args, **kwargs)
            await asyncio.sleep(1.0) # หน่วงเวลา 1 วินาทีต่อการสร้าง 1 ครั้ง
            return res
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5.0)
                print(f"[Rate Limit] ติดบล็อกชั่วคราว รอ {retry_after:.1f} วินาที...")
                await asyncio.sleep(retry_after + 1.0)
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
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return

        guild = message.guild
        await message.channel.send(f"🚀 **รับทราบคำสั่ง! กำลังจัดสร้างเซิร์ฟเวอร์ {NEW_SERVER_NAME}...**\n*(ระบบจะทยอยลบช่องเก่า -> สร้างยศ -> สร้างหมวดหมู่และเซ็ตสิทธิ์การมองเห็น โปรดรอสักครู่)*")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        await safe_run(guild.edit, name=NEW_SERVER_NAME)

        # 2. ลบช่องเดิมทั้งหมด
        print("--- ลบช่องเดิม ---")
        for channel in list(guild.channels):
            await safe_run(channel.delete)

        # 3. ลบยศเดิมทั้งหมด
        print("--- ลบยศเดิม ---")
        for role in list(guild.roles):
            if not role.is_default() and not role.managed:
                await safe_run(role.delete)

        # 4. สร้างยศใหม่ทั้งหมด
        print("--- สร้างยศใหม่ ---")
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

        # มอบยศสูงสุดให้ผู้สั่งงาน
        r_founder = roles.get("👑・ผู้ก่อตั้ง")
        if r_founder and message.author in guild.members:
            try:
                await message.author.add_roles(r_founder)
            except:
                pass

        everyone = guild.default_role

        # Helper ปิดสิทธิ์ไม่ให้ @everyone เห็น
        def hide_everyone():
            return {everyone: discord.PermissionOverwrite(read_messages=False, connect=False)}

        # Helper เปิดสิทธิ์ให้ยศที่ระบุ
        def allow_roles(role_names, text_only_read=False):
            ow = hide_everyone()
            for r_name in role_names:
                r_obj = roles.get(r_name)
                if r_obj:
                    if text_only_read:
                        ow[r_obj] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
                    else:
                        ow[r_obj] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
            return ow

        # ----------------------------------------------------
        # 5. สร้างหมวดหมู่และช่องพร้อมเซ็ต Permissions
        # ----------------------------------------------------

        # --- 📜・ศูนย์กลาง ---
        cat_1 = await safe_run(guild.create_category, "📜・ศูนย์กลาง")
        if cat_1:
            for ch_name in ["📢・ประกาศ", "📖・กฎเซิร์ฟเวอร์", "🏫・ข้อมูลโรงเรียน", "🗺️・แผนที่โรงเรียน", "🎭・ระบบโรลเพลย์", "❓・คำถามที่พบบ่อย"]:
                # @ทุกคน เห็นได้ แต่อ่านได้อย่างเดียว
                ow = {everyone: discord.PermissionOverwrite(read_messages=True, send_messages=False)}
                await safe_run(cat_1.create_text_channel, ch_name, overwrites=ow)

        # --- 📝・สมัครเข้าเรียน ---
        cat_2 = await safe_run(guild.create_category, "📝・สมัครเข้าเรียน")
        if cat_2:
            await safe_run(cat_2.create_text_channel, "📨・ยื่นใบสมัคร", overwrites={everyone: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
            await safe_run(cat_2.create_text_channel, "⏳・รอสัมภาษณ์", overwrites=allow_roles(["📝・ผู้สมัครเข้าเรียน"]))
            await safe_run(cat_2.create_voice_channel, "🎙️・ห้องสัมภาษณ์", overwrites=allow_roles(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_2.create_voice_channel, "🪄・รอเรียกสัม", overwrites=allow_roles(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_2.create_text_channel, "✅・ผ่านการสัมภาษณ์", overwrites=allow_roles(["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]))
            await safe_run(cat_2.create_text_channel, "❌・ผลสัมภาษณ์", overwrites=allow_roles(["📝・ผู้สมัครเข้าเรียน", "🎙️・กรรมการสัมภาษณ์"]))

        # --- 🎓・เขตโรงเรียน ---
        cat_3 = await safe_run(guild.create_category, "🎓・เขตโรงเรียน")
        if cat_3:
            student_teacher = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด", "📚・อาจารย์ฝึกสอน", "🧙・อาจารย์"]
            students = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]
            
            await safe_run(cat_3.create_text_channel, "💬・พูดคุยนักเรียน", overwrites=allow_roles(students))
            for ch_name in ["📚・ห้องเรียน", "🪄・วิชาเวทมนตร์", "🧪・ห้องปรุงยา", "⚔️・ฝึกเวทมนตร์", "📜・การบ้าน"]:
                await safe_run(cat_3.create_text_channel, ch_name, overwrites=allow_roles(student_teacher))
            
            await safe_run(cat_3.create_text_channel, "🎒・ภารกิจนักเรียน", overwrites=allow_roles(students))
            await safe_run(cat_3.create_text_channel, "🏆・กิจกรรมโรงเรียน", overwrites=allow_roles(students))
            await safe_run(cat_3.create_voice_channel, "🔊・ห้องเรียนเสียง", overwrites=allow_roles(student_teacher))
            await safe_run(cat_3.create_voice_channel, "🗣️・ห้องสนทนา", overwrites=allow_roles(students))

        # --- 🔮・หอพักนักเรียน ---
        cat_4 = await safe_run(guild.create_category, "🔮・หอพักนักเรียน")
        if cat_4:
            students = ["🎓・นักเรียน", "🎓・นักเรียนฝึกหัด"]
            await safe_run(cat_4.create_text_channel, "🏠・หอพักรวม", overwrites=allow_roles(students))
            await safe_run(cat_4.create_voice_channel, "🛏️・ห้องพัก", overwrites=allow_roles(students))
            
            # หออัคคี
            await safe_run(cat_4.create_text_channel, "🦅・หออัคคี", overwrites=allow_roles(["🦅・สมาชิกหออัคคี"]))
            await safe_run(cat_4.create_voice_channel, "🔥・ห้องนั่งเล่น", overwrites=allow_roles(["🦅・สมาชิกหออัคคี"]))
            
            # หอเงา
            await safe_run(cat_4.create_text_channel, "🐍・หอเงา", overwrites=allow_roles(["🐍・สมาชิกหอเงา"]))
            await safe_run(cat_4.create_voice_channel, "🌑・ห้องนั่งเล่น", overwrites=allow_roles(["🐍・สมาชิกหอเงา"]))
            
            # หอจันทรา
            await safe_run(cat_4.create_text_channel, "🦉・หอจันทรา", overwrites=allow_roles(["🦉・สมาชิกหอจันทรา"]))
            await safe_run(cat_4.create_voice_channel, "🌙・ห้องนั่งเล่น", overwrites=allow_roles(["🦉・สมาชิกหอจันทรา"]))
            
            # หอแสง
            await safe_run(cat_4.create_text_channel, "🦁・หอแสง", overwrites=allow_roles(["🦁・สมาชิกหอแสง"]))
            await safe_run(cat_4.create_voice_channel, "☀️・ห้องนั่งเล่น", overwrites=allow_roles(["🦁・สมาชิกหอแสง"]))

        # --- 🌐・COMMUNITY | นอกโรล ---
        cat_5 = await safe_run(guild.create_category, "🌐・COMMUNITY | นอกโรล")
        if cat_5:
            # ประกาศคอมมู อ่านได้อย่างเดียว
            await safe_run(cat_5.create_text_channel, "📣・ประกาศคอมมู", overwrites={everyone: discord.PermissionOverwrite(read_messages=True, send_messages=False)})
            
            for ch_name in ["💬・แชทพูดคุย", "🤣・มีมและความฮา", "🎮・เล่นเกมด้วยกัน", "📸・แกลเลอรี", "🎨・งานแฟนอาร์ต", "📊・โหวตและกิจกรรม", "🎉・กิจกรรมคอมมู"]:
                await safe_run(cat_5.create_text_channel, ch_name, overwrites={everyone: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
                
            for vc_name in ["🎙️・ห้องคุยเล่น 1", "🎙️・ห้องคุยเล่น 2", "🎮・ห้องเล่นเกม", "💤・AFK"]:
                await safe_run(cat_5.create_voice_channel, vc_name, overwrites={everyone: discord.PermissionOverwrite(read_messages=True, connect=True)})

        # --- 👑・ฝ่ายบริหารโรงเรียน ---
        cat_6 = await safe_run(guild.create_category, "👑・ฝ่ายบริหารโรงเรียน")
        if cat_6:
            await safe_run(cat_6.create_text_channel, "🏛️️・ห้องอธิการ", overwrites=allow_roles(["🏰・อธิการโรงเรียน", "👑・รองอธิการ"]))
            await safe_run(cat_6.create_text_channel, "📋・ห้องอาจารย์", overwrites=allow_roles(["🧙・อาจารย์", "📚・อาจารย์ฝึกสอน"]))
            await safe_run(cat_6.create_text_channel, "🧙・สภาเวทมนตร์", overwrites=allow_roles(["🔮・สภาเวทมนตร์"]))
            await safe_run(cat_6.create_text_channel, "📑・งานฝ่ายบริหาร", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_6.create_text_channel, "🚨・แจ้งปัญหา", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_6.create_voice_channel, "🔊・ห้องประชุม", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_6.create_voice_channel, "🎙️・ประชุมสภา", overwrites=allow_roles(["🔮・สภาเวทมนตร์"]))

        # --- 🔐・STAFF ZONE ---
        cat_7 = await safe_run(guild.create_category, "🔐・STAFF ZONE")
        report_ch = None
        if cat_7:
            report_ch = await safe_run(cat_7.create_text_channel, "💼・ห้อง Staff", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_7.create_text_channel, "📝・บันทึกสัมภาษณ์", overwrites=allow_roles(["🎙️・กรรมการสัมภาษณ์"]))
            await safe_run(cat_7.create_text_channel, "📂・ข้อมูลนักเรียน", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_7.create_text_channel, "⚖️・พิจารณาโทษ", overwrites=allow_roles(["⚜️・ผู้บริหาร", "🏰・อธิการโรงเรียน", "👑・รองอธิการ"]))
            await safe_run(cat_7.create_text_channel, "🤖・ห้องบอท", overwrites=allow_roles(["💼・Staff"]))
            await safe_run(cat_7.create_voice_channel, "🔊・ห้อง Staff", overwrites=allow_roles(["💼・Staff"]))

        # 6. ส่งข้อความแจ้งรายงานสรุปการสร้างเสร็จสมบูรณ์
        target_send = report_ch if report_ch else guild.system_channel
        if target_send:
            embed = discord.Embed(
                title="🏰 จัดตั้ง Magic School RP เรียบร้อยแล้ว!",
                description=f"ระบบทำการล้างเซิร์ฟเวอร์ และสร้างหมวดหมู่ ห้องพิมพ์/เสียง รวมถึงเซ็ตสิทธิ์ (Permissions) สำหรับ **{NEW_SERVER_NAME}** เรียบร้อยแล้วครับ",
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
