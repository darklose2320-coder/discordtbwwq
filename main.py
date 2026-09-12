import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord.ui import Button, View

# Render'ın uyutmaması için mini web sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Ticket Botu aktif ve çalışıyor!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot Ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Ticket Kapatma Butonu (Görselli Embed ile)
class TicketCloseView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Talebi Kapat 🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Talep kapatılıyor, kanal birazdan silinecek...", ephemeral=True)
        await interaction.channel.delete()

# Ticket Oluşturma Butonu
class TicketCreateView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Destek Talebi Aç 📩", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_button(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="DESTEK TALEPLERI")
        if not category:
            category = await guild.create_category("DESTEK TALEPLERI")

        channel_name = f"ticket-{interaction.user.name}".lower()
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"Zaten açık bir destek kanalın var: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)
        
        # İçeride açılan özel embed mesajı
        embed = discord.Embed(
            title="Destek Talebi Oluşturuldu",
            description=f"Hoş geldin {interaction.user.mention}! Yetkililerimiz en kısa sürede seninle ilgilenecektir.\n\nİşlemin bittiğinde aşağıdaki butonu kullanarak talebi kapatabilirsin.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Qvantis Destek Sistemi")

        await ticket_channel.send(embed=embed, view=TicketCloseView())
        await interaction.response.send_message(f"Destek kanalın başarıyla oluşturuldu: {ticket_channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user.name} başarıyla giriş yaptı ve çalışıyor!")

@bot.command(name="ticketkur")
@commands.has_permissions(administrator=True)
async def ticketkur(ctx):
    # Ana Kurulum Paneli (Görselli ve Embed Tasarımlı)
    embed = discord.Embed(
        title="🛡️ Qvantis Destek ve Yardım Merkezi",
        description="Sunucumuzda herhangi bir sorunla karşılaştığında, ceza itirazında bulunmak istediğinde veya yardıma ihtiyacın olduğunda aşağıdaki **Destek Talebi Aç** butonuna tıklayabilirsin.\n\n*Lütfen gereksiz yere talep açmaktan kaçınınız.*",
        color=discord.Color.blurple()
    )
    # İstersen buraya sunucunun banner/logo linkini de koyabilirsin
    embed.set_image(url="https://cdn.discordapp.com/attachments/1462082482726899764/1546708958348054538/a0dce774-c4bc-40dd-9bd7-c94032851d15.jpg?ex=6aa0c478&is=6a9f72f8&hm=d8b96d48fdb75606d60427b03bc9aef2896bd494fef12d6e9c2d6b0740441857&") 
    embed.set_footer(text="Qvantis Security & Support System")

    await ctx.send(embed=embed, view=TicketCreateView())

@ticketkur.error
async def ticketkur_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu kullanmak için Yönetici yetkisine sahip olmalısın!")

# Sadece yetkililerin/YT'lerin göreceği kanala rapor düş
        yetkili_kanal = bot.get_channel(YETKILI_LOG_ID)
        if yetkili_kanal:
            await yetkili_kanal.send(f"🎮 **Yeni Oyun İsteği!**\n🔹 **Oyun:** {oyun_adi}\n👤 **İsteyen:** {message.author.mention}\n🔗 **Steam:** https://store.steampowered.com/app/{app_id}")

        return

    await bot.process_commands(message)

# ==========================================
# DOSYANIN EN ALTINDAKİ ESKİ KISMI SİL VE BURAYI EKLE:
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    def run_flask():
        app.run(host='0.0.0.0', port=port)
        
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    bot.run(os.getenv("BOT_TOKEN"))
