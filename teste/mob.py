import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page(); logs=[]; pg.on('pageerror',lambda e: logs.append(str(e)))
        await pg.goto('file:///home/claude/motorhome/motorhome_solar_3d.html'); await pg.wait_for_timeout(15000)
        await pg.screenshot(path='mob.png'); print(logs); await b.close()
asyncio.run(main())
