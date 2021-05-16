import time


async def _ping():
    start = time.perf_counter()
    msg = await _ping.message.channel.send("Pinging...")
    stop = time.perf_counter()

    ms = int((stop - start) * 1000.0)
    await msg.edit(
        content=f"Pong!, {ms}ms\nAPI: {int(_ping.client.latency * 1000.0)}ms"
    )
