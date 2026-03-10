



from telethon import events
from session import ping
import time


def get_ping():
    start = time.time()
    # Simulate some work (like an API call or db query)
    time.sleep(0.05)  # 50 ms
    end = time.time()
    ping_ms = (end - start) * 1000
    return f"{int(ping_ms)}ms"



async def ping_handle(client, event):
  ts = ping.get("time")
  since = get_time(ts)
  ms = get_ping()
  msg = ("<blockquote>Pong! uptime details</blockquote>\n"
  f"➠ Ping – {ms} \n"
  f"➠ Uptime – {since} \n"
    )
  await event.respond(msg, parse_mode="html")



def get_time(old_timestamp):
    seconds = int(time.time()) - int(old_timestamp)

    # Define units
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day
    month = 30 * day
    year = 365 * day

    years = seconds // year
    seconds %= year

    months = seconds // month
    seconds %= month

    weeks = seconds // week
    seconds %= week

    days = seconds // day
    seconds %= day

    hours = seconds // hour
    seconds %= hour

    minutes = seconds // minute
    seconds %= minute

    # Build formatted string
    result = []
    if years: result.append(f"{years}y")
    if months: result.append(f"{months}M")
    if weeks: result.append(f"{weeks}w")
    if days: result.append(f"{days}d")
    if hours: result.append(f"{hours}h")
    if minutes: result.append(f"{minutes}m")
    if seconds or not result: result.append(f"{seconds}s")

    return " ".join(result)