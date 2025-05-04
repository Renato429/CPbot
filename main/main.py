import discord
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos globales registrados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# Menú desplegable con las opciones en orden personalizado
class ControlDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="IPv4 (Switch)", description="Configurar IPv4 en un switch", emoji="🔌"),
            discord.SelectOption(label="IPv4 (Router)", description="Configurar IPv4 en un router", emoji="🛰️"),
            discord.SelectOption(label="IPv6 (Switch)", description="Configurar IPv6 en un switch", emoji="🔌"),
            discord.SelectOption(label="IPv6 (Router)", description="Configurar IPv6 en un router", emoji="🛰️"),
            discord.SelectOption(label="DHCP (IPv4)", description="Configurar DHCP en IPv4", emoji="📶"),
            discord.SelectOption(label="DHCP (IPv6)", description="Configurar DHCP en IPv6", emoji="🌐"),
            discord.SelectOption(label="Telnet", description="Asignar contraseña Telnet", emoji="🔐"),
            discord.SelectOption(label="SSH", description="Configurar acceso SSH con contraseña", emoji="🛡️"),
        ]
        super().__init__(placeholder="Selecciona un comando...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "IPv4 (Switch)":
            texto = (
                "**Comandos para asignar una IP de iPv4 a un Switch:**\n"
                "```\n"
                "Switch> Enable\n"
                "Switch# config\n"
                "Switch(config)# interface vlan1\n"
                "Switch(config-ip)# ip address (la ip que quieres ponerle) (la mascara)\n"
                "Switch(config-ip)# no shutdown\n"
                "Switch(config-ip)# exit\n"
                "Switch(config)# exit\n"
                "Switch# copy running-config startup-config\n"
                "```"
            )
        elif self.values[0] == "IPv4 (Router)":
            texto = (
                "**Comandos para asignar una IP de iPv4 a un Router:**\n"
                "```\n"
                "Router> Enable\n"
                "Router# config\n"
                "Router(config)# interface Gig0/0 (dependiendo de la interface que quieras)\n"
                "Router(config-ip)# ip address (la ip que quieres ponerle) (la mascara)\n"
                "Router(config-ip)# no shutdown\n"
                "Router(config-ip)# exit\n"
                "Router(config)# exit\n"
                "Router# copy running-config startup-config\n"
                "```"
            )
        elif self.values[0] == "IPv6 (Switch)":
            texto = (
                "**Comandos para asignar una IP de iPv6 a un Switch:**\n"
                "```\n"
                "Switch> enable\n"
                "Switch# config\n"
                "Switch(config)# interface vlan1\n"
                "Switch(config-if)# ipv6 address 2001:db8:acad:a::2/64\n"
                "Switch(config-if)# no shutdown\n"
                "Switch(config-if)# exit\n"
                "Switch(config)# ipv6 unicast-routing\n"
                "Switch(config)# exit\n"
                "Switch# copy running-config startup-config\n"
                "```"
            )
        elif self.values[0] == "IPv6 (Router)":
            texto = (
                "**Comandos para asignar una IP de iPv6 a un Router:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# interface g0/0\n"
                "Router(config-if)# ipv6 address 2001:db8:acad:a::1/64\n"
                "Router(config-if)# no shutdown\n"
                "Router(config-if)# exit\n"
                "Router(config)# ipv6 unicast-routing\n"
                "Router(config)# exit\n"
                "Router# copy running-config startup-config\n"
                "```"
            )
        elif self.values[0] == "DHCP (IPv4)":
            texto = (
                "**Comandos para poner IPs mediante DHCP en IPv4:**\n"
                "```\n"
                "Router>Enable\n"
                "Router# config\n"
                "Router(config)# interface gig0/0/0\n"
                "Router(config-if)# ip address 192.168.6.1 255.255.255.0\n"
                "Router(config-if)# no shutdown\n"
                "Router(config-if)# exit\n"
                "Router(config)# ip dhcp excluded-address 192.168.6.1 192.168.6.5\n"
                "Router(config)# ip dhcp excluded-address 192.168.6.254\n"
                "Router(config)# ip dhcp pool Insano1\n"
                "Router(dhcp-config)# network 192.168.6.0 255.255.255.0\n"
                "Router(dhcp-config)# default-router 192.168.6.1\n"
                "Router(dhcp-config)# dns-server 9.9.9.9\n"
                "Router(dhcp-config)# domain-name insano.com\n"
                "Router(dhcp-config)# exit\n"
                "Router(config)# exit\n"
                "Router# show running-config | section dhcp\n"
                "```"
            )
        elif self.values[0] == "DHCP (IPv6)":
            texto = (
                "**Comandos para poner IPs mediante DHCP en IPv6:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# ipv6 unicast-routing\n"
                "Router(config)# ipv6 dhcp pool DHCP1\n"
                "Router(config-dhcpv6)# dns-server 2001:1234:A:B::2\n"
                "Router(config-dhcpv6)# exit\n"
                "Router(config)# exit\n"
                "Router# config\n"
                "Router(config)# interface gig0/0/0\n"
                "Router(config-if)# ipv6 enable\n"
                "Router(config-if)# ipv6 address 2001:1234:A:B::1/64\n"
                "Router(config-if)# ipv6 nd other-config-flag\n"
                "Router(config-if)# ipv6 dhcp server DHCP1\n"
                "Router(config-if)# no shutdown\n"
                "Router(config-if)# exit\n"
                "Router(config)# exit\n"
                "Router# copy running-config startup-config\n"
                "Router# show ipv6 interface brief\n"
                "```"
            )
        elif self.values[0] == "Telnet":
            texto = (
                "**Comandos para asignar una contraseña Telnet a un Router:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# line vty 0 4\n"
                "Router(config-line)# password cisco\n"
                "Router(config-line)# login\n"
                "Router(config-line)# exit\n"
                "Router(config)# enable secret cisco\n"
                "Router(config)# exit\n"
                "```\n"
                "> _Este procedimiento funciona igual para conexiones Telnet por IPv4 o IPv6._"
            )
        elif self.values[0] == "SSH":
            texto = (
                "**Comandos para poner una contraseña SSH:**\n"
                "```\n"
                "Router>enable\n"
                "Router#config\n"
                "Router(config)# hostname R1\n"
                "R1(config)# ip domain-name cisco.com\n"
                "R1(config)# crypto key generate rsa\n"
                "How many bits in the modulus [512]: 1024\n"
                "R1(config)# line vty 0 4\n"
                "R1(config-line)# login local\n"
                "R1(config-line)# username cisco password cisco\n"
                "R1(config)# ip ssh version 2\n"
                "R1(config)# enable secret cisco\n"
                "R1(config)# exit\n"
                "R1# copy running-config startup-config\n"
                "```\n"
                "> **Para probarlo en la RUN de una PC:**\n"
                "> SSH -l (username) (ip del router)"
            )

        await interaction.response.send_message(texto)
        await interaction.message.delete()

class ControlPanelView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ControlDropdown())

@bot.tree.command(name="cp", description="Panel de comandos interactivo con menú desplegable")
async def cp(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ Panel de Comandos ⚡",
        description="Elije qué comando necesitas bro",
        color=discord.Color.green()
    )
    embed.set_footer(text="Selecciona el comando ⬇️")
    await interaction.response.send_message(embed=embed, view=ControlPanelView())

class ConfigDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Cambiar Hostname", description="Cambia el nombre del dispositivo", emoji="🏷️"),
            discord.SelectOption(label="Manejo de errores", description="Evita congelamiento por comando mal escrito", emoji="❌"),
            discord.SelectOption(label="Ver tabla ARP", description="Ver ARP en Router y PC", emoji="📋"),
            discord.SelectOption(label="Ver dirección MAC", description="Ver MAC en Router y PC", emoji="🔍"),
            discord.SelectOption(label="Ver interfaces activas", description="Resumen rápido de interfaces", emoji="📶"),
            discord.SelectOption(label="Cambiar contraseña consola", description="Seguridad en el acceso físico", emoji="🔐"),
        ]
        super().__init__(placeholder="Selecciona una opción...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Cambiar Hostname":
            texto = (
                "**Cambiar el nombre (hostname) del dispositivo:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# hostname NOMBRE_QUE_QUIERAS\n"
                "```"
            )
        elif self.values[0] == "Manejo de errores":
            texto = (
                "**Evitar que el dispositivo se congele por errores de comando:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# no ip domain-lookup\n"
                "```"
            )
        elif self.values[0] == "Ver tabla ARP":
            texto = (
                "**Ver y limpiar la tabla ARP:**\n\n"
                "__📟 En un Router o Switch:__\n"
                "```\n"
                "Router# show ip arp        ← Ver tabla ARP\n"
                "Router# clear arp          ← Limpiar tabla ARP\n"
                "```\n"
                "__💻 En una PC (CMD de Windows):__\n"
                "```\n"
                "arp -a    ← Ver tabla ARP\n"
                "arp -d    ← Limpiar tabla ARP\n"
                "```"
            )
        elif self.values[0] == "Ver dirección MAC":
            texto = (
                "**Ver y limpiar la tabla MAC de interfaces:**\n\n"
                "__📟 En un Router o Switch:__\n"
                "```\n"
                "Router# show interfaces                  ← Ver detalles de interfaces\n"
                "Router# show mac address-table          ← Ver tabla MAC\n"
                "Router# clear mac address-table         ← Limpiar tabla MAC\n"
                "```\n"
                "__💻 En una PC (CMD de Windows):__\n"
                "```\n"
                "ipconfig /all      ← Ver direcciones MAC de interfaces locales\n"
                "```"
            )

        elif self.values[0] == "Ver interfaces activas":
            texto = (
                "**Ver un resumen del estado de todas las interfaces:**\n"
                "```\n"
                "Router# show ip interface brief\n"
                "Router# show ipv6 interface brief\n"
                "```"
            )
        elif self.values[0] == "Cambiar contraseña consola":
            texto = (
                "**Cambiar o agregar contraseña de acceso por consola:**\n"
                "```\n"
                "Router> enable\n"
                "Router# config\n"
                "Router(config)# line console 0\n"
                "Router(config-line)# password cisco\n"
                "Router(config-line)# login\n"
                "Router(config-line)# exit\n"
                "Router(config)# enable secret cisco\n"
                "```"
            )

        await interaction.response.send_message(texto)
        await interaction.message.delete()

# Vista del menú de /cpb
class ConfigPanelView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfigDropdown())

# Comando slash /cpb
@bot.tree.command(name="cpb", description="Panel de configuración básica del router")
async def cpb(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛠️ Panel de Configuración Básica 🛠️",
        description="Elije qué comando necesitas configurar",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Selecciona una opción del menú ⬇️")
    await interaction.response.send_message(embed=embed, view=ConfigPanelView())


@bot.command()
async def copiar(ctx, *, texto):
    await ctx.send(texto)

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar el archivo .env desde la raíz del proyecto
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
print("Ruta del .env:", dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

# Obtener el token desde la variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"TOKEN CARGADO: {TOKEN}")

if TOKEN is None:
    raise ValueError("El TOKEN no se cargó. ¿Está bien escrito en el .env?")

bot.run(TOKEN)

