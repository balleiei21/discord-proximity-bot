import discord
from discord.ext import commands

# วาง TOKEN ของบอทตรงนี้
TOKEN = "YOUR_BOT_TOKEN_HERE"

# ไอดีที่อนุญาตให้ใช้คำสั่งได้เท่านั้น
ALLOWED_USER_ID = 933529869487321161

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

# ข้อมูลบทบาท (Roles) เรียงลำดับจากสูงไปต่ำ
ROLES_DATA = [
    {"name": "👑・Owner", "color": discord.Color.gold(), "hoist": True},
    {"name": "💎・Co-Owner", "color": discord.Color.purple(), "hoist": True},
    {"name": "🏆・Executive", "color": discord.Color.dark_purple(), "hoist": True},
    {"name": "⚜️・Manager", "color": discord.Color.blue(), "hoist": True},
    {"name": "🔧・Admin", "color": discord.Color.red(), "hoist": True},
    {"name": "🛡️・Moderator", "color": discord.Color.dark_red(), "hoist": True},
    {"name": "🎧・Support", "color": discord.Color.green(), "hoist": True},
    {"name": "🎫・Ticket Staff", "color": discord.Color.dark_green(), "hoist": True},
    {"name": "👕・Skin Designer", "color": discord.Color.teal(), "hoist": True},
    {"name": "🧱・Map Builder", "color": discord.Color.dark_teal(), "hoist": True},
    {"name": "⚙️・Addon Developer", "color": discord.Color.dark_orange(), "hoist": True},
    {"name": "💻・Discord Developer", "color": discord.Color.orange(), "hoist": True},
    {"name": "🎨・Commission Artist", "color": discord.Color.magenta(), "hoist": True},
    {"name": "💳・Topup Staff", "color": discord.Color.blurple(), "hoist": True},
    {"name": "🤖・Roblox Service", "color": discord.Color.dark_blue(), "hoist": True},
    {"name": "🔥・Free Fire Service", "color": discord.Color.red(), "hoist": True},
    {"name": "⚔️・AOV Service", "color": discord.Color.dark_gold(), "hoist": True},
    {"name": "👑・VIP", "color": discord.Color.gold(), "hoist": True},
    {"name": "💎・Premium", "color": discord.Color.purple(), "hoist": True},
    {"name": "⭐・Customer", "color": discord.Color.green(), "hoist": True},
    {"name": "🛍️・Buyer", "color": discord.Color.light_grey(), "hoist": True},
    {"name": "👤・Member", "color": discord.Color.default(), "hoist": False},
    {"name": "🤖・Bot", "color": discord.Color.dark_grey(), "hoist": False},
    {"name": "🔇・Muted", "color": discord.Color.default(), "hoist": False},
]

@bot.event
async def on_ready():
    print(f"ล็อกอินเข้าใช้งานในชื่อ {bot.user.name} (ID: {bot.user.id})")

@bot.command(name="เริ่มงาน")
async def start_setup(ctx):
    # ตรวจสอบ ID ผู้ใช้งาน
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
        return

    guild = ctx.guild
    await ctx.send("🚀 **กำลังเริ่มงาน...** ระบบกำลังดำเนินการสร้างยศ หมวดหมู่ และจัดสรรสิทธิ์ห้องทั้งหมด กรุณารอ สักครู่ครับ")

    # 1. สร้าง ยศ (Roles)
    created_roles = {}
    for role_info in reversed(ROLES_DATA):
        role = discord.utils.get(guild.roles, name=role_info["name"])
        if not role:
            role = await guild.create_role(
                name=role_info["name"],
                color=role_info["color"],
                hoist=role_info["hoist"]
            )
        created_roles[role_info["name"]] = role

    everyone_role = guild.default_role

    def get_role(name):
        return created_roles.get(name)

    staff_roles = [
        get_role("👑・Owner"), get_role("💎・Co-Owner"), get_role("🏆・Executive"),
        get_role("⚜️・Manager"), get_role("🔧・Admin"), get_role("🛡️・Moderator"),
        get_role("🎧・Support"), get_role("🎫・Ticket Staff")
    ]
    staff_roles = [r for r in staff_roles if r is not None]

    manager_roles = [get_role("👑・Owner"), get_role("💎・Co-Owner"), get_role("🏆・Executive"), get_role("⚜️・Manager")]
    manager_roles = [r for r in manager_roles if r is not None]

    log_channel = None

    # 2. สร้าง หมวดหมู่ และ ห้องต่างๆ
    
    # 📌 INFORMATION
    cat_info = await guild.create_category("📌 INFORMATION")
    for ch_name in ["꒰📢꒱・ยินดีต้อนรับ", "꒰📜꒱・กฎของร้าน", "꒰📋꒱・รายละเอียดบริการ", "꒰💳꒱・ช่องทางชำระเงิน", "꒰⭐꒱・รีวิวจากลูกค้า"]:
        await guild.create_text_channel(ch_name, category=cat_info)

    # 🛒 SHOP
    cat_shop = await guild.create_category("🛒 SHOP")
    for ch_name in ["꒰🛍️꒱・ร้านค้า", "꒰🎮꒱・เติมเกม", "꒰💎꒱・ไอเทมเกม", "꒰🎁꒱・โปรโมชั่น"]:
        await guild.create_text_channel(ch_name, category=cat_shop)

    # 🎨 SERVICES
    cat_services = await guild.create_category("🎨 SERVICES")
    for ch_name in ["꒰👕꒱・รับทำสกิน", "꒰🧱꒱・รับทำแมพมายคราฟ", "꒰⚙️꒱・รับทำแอดออน", "꒰💻꒱・รับทำดิส", "꒰🎨꒱・รับทำคอมช", "꒰💳꒱・รับเติมเกม", "꒰🤖꒱・รับฟาร์ม Roblox", "꒰🔥꒱・รับดันแรงค์ Free Fire", "꒰⚔️꒱・รับดันแรงค์ AOV"]:
        await guild.create_text_channel(ch_name, category=cat_services)

    # 📂 PORTFOLIO
    cat_portfolio = await guild.create_category("📂 PORTFOLIO")
    for ch_name in ["꒰🖼️꒱・ผลงานสกิน", "꒰🗺️꒱・ผลงานแมพ", "꒰⚙️꒱・ผลงานแอดออน", "꒰💬꒱・ผลงานดิส", "꒰🎨꒱・ผลงานคอมช"]:
        await guild.create_text_channel(ch_name, category=cat_portfolio)

    # 🧾 CUSTOMER
    cat_customer = await guild.create_category("🧾 CUSTOMER")
    await guild.create_text_channel("꒰🎫꒱・เปิด Ticket", category=cat_customer)
    await guild.create_text_channel("꒰💬꒱・สอบถามบริการ", category=cat_customer)
    await guild.create_text_channel("꒰📜꒱・เครดิตลูกค้า", category=cat_customer)
    
    status_overwrites = {
        everyone_role: discord.PermissionOverwrite(read_messages=False),
        get_role("⭐・Customer"): discord.PermissionOverwrite(read_messages=True)
    }
    for r in staff_roles:
        status_overwrites[r] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰📦꒱・สถานะงาน", category=cat_customer, overwrites=status_overwrites)

    # 💬 COMMUNITY
    cat_community = await guild.create_category("💬 COMMUNITY")
    for ch_name in ["꒰💬꒱・พูดคุย", "꒰🎮꒱・คุยเรื่องเกม", "꒰📸꒱・แชร์ผลงาน", "꒰🤝꒱・หาเพื่อนเล่นเกม"]:
        await guild.create_text_channel(ch_name, category=cat_community)
    await guild.create_voice_channel("🔊・ห้องคุยเล่น 1", category=cat_community)
    await guild.create_voice_channel("🔊・ห้องคุยเล่น 2", category=cat_community)

    # 🏆 CREDIT
    cat_credit = await guild.create_category("🏆 CREDIT")
    for ch_name in ["꒰🏆꒱・เครดิตร้าน", "꒰💖꒱・ขอบคุณลูกค้า", "꒰📸꒱・ผลงานลูกค้า"]:
        await guild.create_text_channel(ch_name, category=cat_credit)

    # 🔒 STAFF
    staff_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    for r in staff_roles:
        staff_overwrites[r] = discord.PermissionOverwrite(read_messages=True)
        
    cat_staff = await guild.create_category("🔒 STAFF", overwrites=staff_overwrites)
    await guild.create_text_channel("꒰🔧꒱・ห้องทีมงาน", category=cat_staff)
    await guild.create_text_channel("꒰📋꒱・จัดการออเดอร์", category=cat_staff)
    
    income_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    for r in manager_roles:
        income_overwrites[r] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰💰꒱・รายรับ", category=cat_staff, overwrites=income_overwrites)
    
    # ห้องบันทึกงาน
    log_channel = await guild.create_text_channel("꒰📝꒱・บันทึกงาน", category=cat_staff)

    # 🔐 MANAGEMENT
    mgmt_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    cat_mgmt = await guild.create_category("🔐 MANAGEMENT", overwrites=mgmt_overwrites)

    owner_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    for r_name in ["👑・Owner", "💎・Co-Owner"]:
        if get_role(r_name):
            owner_overwrites[get_role(r_name)] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰👑꒱・ห้อง Owner", category=cat_mgmt, overwrites=owner_overwrites)

    for r in manager_roles:
        mgmt_overwrites[r] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰💼꒱・ห้องบริหาร", category=cat_mgmt, overwrites=mgmt_overwrites)

    exec_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    for r_name in ["👑・Owner", "💎・Co-Owner", "🏆・Executive"]:
        if get_role(r_name):
            exec_overwrites[get_role(r_name)] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰📊꒱・รายงานร้าน", category=cat_mgmt, overwrites=exec_overwrites)

    admin_setup_overwrites = {everyone_role: discord.PermissionOverwrite(read_messages=False)}
    for r_name in ["👑・Owner", "💎・Co-Owner", "🔧・Admin"]:
        if get_role(r_name):
            admin_setup_overwrites[get_role(r_name)] = discord.PermissionOverwrite(read_messages=True)
    await guild.create_text_channel("꒰⚙️꒱・ตั้งค่าระบบ", category=cat_mgmt, overwrites=admin_setup_overwrites)

    # แจ้งเตือนผู้ใช้ว่าเสร็จสิ้นแล้ว
    await ctx.send(f"✅ **สร้างดิสคอร์ดเรียบร้อยแล้ว!** สรุปรายงานการสร้างถูกส่งไปที่ห้อง {log_channel.mention} แล้วครับ")

    # 3. ส่งรายงานสรุปการสร้างดิสไปที่ห้อง ꒰📝꒱・บันทึกงาน
    if log_channel:
        report_msg_1 = (
            "📋 **[รายงานสรุปการสร้างดิสคอร์ด NEXORA SHOP]**\n\n"
            "**👑 ยศทั้งหมดที่ถูกสร้างเรียบร้อยแล้ว (เรียบร้อยตามลำดับสิทธิ์):**\n"
            "• `👑 MANAGEMENT`: Owner → Co-Owner → Executive → Manager\n"
            "• `🛡️ STAFF`: Admin → Moderator → Support → Ticket Staff\n"
            "• `🎨 CREATOR TEAM`: Skin Designer → Map Builder → Addon Developer → Discord Developer → Commission Artist\n"
            "• `🎮 GAME SERVICE`: Topup Staff → Roblox Service → Free Fire Service → AOV Service\n"
            "• `💎 CUSTOMER`: VIP → Premium → Customer → Buyer → Member\n"
            "• `🤖 SYSTEM`: Bot → Muted\n\n"
            "----------------------------------------\n"
            "📌 **รายละเอียดหมวดหมู่ และยศที่สามารถใช้งานได้:**\n\n"
            "**📌 INFORMATION** (หน้าที่: ประชาสัมพันธ์ข้อมูลร้านค้า)\n"
            "• `꒰📢꒱・ยินดีต้อนรับ`, `꒰📜꒱・กฎของร้าน`, `꒰📋꒱・รายละเอียดบริการ`, `꒰💳꒱・ช่องทางชำระเงิน`, `꒰⭐꒱・รีวิวจากลูกค้า`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n\n"
            "**🛒 SHOP** (หน้าที่: แสดงรายการสินค้าและโปรโมชั่น)\n"
            "• `꒰🛍️꒱・ร้านค้า`, `꒰🎮꒱・เติมเกม`, `꒰💎꒱・ไอเทมเกม`, `꒰🎁꒱・โปรโมชั่น`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n\n"
            "**🎨 SERVICES** (หน้าที่: เมนูรวมบริการต่างๆ ของร้าน)\n"
            "• `꒰👕꒱・รับทำสกิน`, `꒰🧱꒱・รับทำแมพมายคราฟ`, `꒰⚙️꒱・รับทำแอดออน`, `꒰💻꒱・รับทำดิส`, `꒰🎨꒱・รับทำคอมช`, `꒰💳꒱・รับเติมเกม`, `꒰🤖꒱・รับฟาร์ม Roblox`, `꒰🔥꒱・รับดันแรงค์ Free Fire`, `꒰⚔️꒱・รับดันแรงค์ AOV`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n\n"
            "**📂 PORTFOLIO** (หน้าที่: โชว์ผลงานเพื่อประกอบการตัดสินใจ)\n"
            "• `꒰🖼️꒱・ผลงานสกิน`, `꒰🗺️꒱・ผลงานแมพ`, `꒰⚙️꒱・ผลงานแอดออน`, `꒰💬꒱・ผลงานดิส`, `꒰🎨꒱・ผลงานคอมช`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n"
        )

        report_msg_2 = (
            "**🧾 CUSTOMER** (หน้าที่: ช่องทางบริการลูกค้า ติดตามสถานะงาน)\n"
            "• `꒰🎫꒱・เปิด Ticket`, `꒰💬꒱・สอบถามบริการ`, `꒰📜꒱・เครดิตลูกค้า`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n"
            "• `꒰📦꒱・สถานะงาน`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* Customer + Staff ทุกตำแหน่งขึ้นไป\n\n"
            "**💬 COMMUNITY** (หน้าที่: พื้นที่พูดคุยแลกเปลี่ยนของสมาชิก)\n"
            "• `꒰💬꒱・พูดคุย`, `꒰🎮꒱・คุยเรื่องเกม`, `꒰📸꒱・แชร์ผลงาน`, `꒰🤝꒱・หาเพื่อนเล่นเกม`, `🔊・ห้องคุยเล่น 1`, `🔊・ห้องคุยเล่น 2`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n\n"
            "**🏆 CREDIT** (หน้าที่: เก็บหลักฐานเครดิตและความไว้วางใจ)\n"
            "• `꒰🏆꒱・เครดิตร้าน`, `꒰💖꒱・ขอบคุณลูกค้า`, `꒰📸꒱・ผลงานลูกค้า`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* ทุกคน\n\n"
            "**🔒 STAFF** (หน้าที่: จัดการงานภายในร้านค้า)\n"
            "• `꒰🔧꒱・ห้องทีมงาน`, `꒰📋꒱・จัดการออเดอร์`, `꒰📝꒱・บันทึกงาน`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* Staff ขึ้นไป (Admin, Moderator, Support, Ticket Staff, ฯลฯ)\n"
            "• `꒰💰꒱・รายรับ`\n"
            "↳ *ยศที่เห็น/ใช้งาน:* Manager ขึ้นไป (Owner, Co-Owner, Executive, Manager)\n\n"
            "**🔐 MANAGEMENT** (หน้าที่: ส่วนผู้บริหารและตั้งค่าระบบ)\n"
            "• `꒰👑꒱・ห้อง Owner` → *ยศที่เห็น:* Owner / Co-Owner\n"
            "• `꒰💼꒱・ห้องบริหาร` → *ยศที่เห็น:* Owner / Co-Owner / Executive / Manager\n"
            "• `꒰📊꒱・รายงานร้าน` → *ยศที่เห็น:* Owner / Co-Owner / Executive\n"
            "• `꒰⚙️꒱・ตั้งค่าระบบ` → *ยศที่เห็น:* Owner / Co-Owner / Admin\n\n"
            "----------------------------------------\n"
            "✅ *บันทึกสถานะงาน: เสร็จสิ้นเรียบร้อยแล้วโดยระบบอัตโนมัติ*"
        )

        await log_channel.send(report_msg_1)
        await log_channel.send(report_msg_2)

bot.run(TOKEN)
