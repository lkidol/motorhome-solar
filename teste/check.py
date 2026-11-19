import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':600,'height':400})
        await pg.goto('file:///home/claude/motorhome/teste_3d.html'); await pg.wait_for_timeout(12000)
        r=await pg.evaluate("window.__check()"); print(json.dumps(r,indent=0)); await b.close()
asyncio.run(main())
