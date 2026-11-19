import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1100,'height':700})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e))); pg.on('console',lambda m: logs.append(m.type+': '+m.text) if m.type in('error','warning') and 'GL Driver' not in m.text else None)
        net=[]; 
        async def route(r): net.append(r.request.url[:80]); await r.continue_() if r.request.url.startswith('file:') else await r.abort()
        await pg.route('**/*',route)
        await pg.goto('file:///home/claude/motorhome/motorhome_solar_3d.html'); await pg.wait_for_timeout(15000)
        await pg.screenshot(path='f_ext.png')
        await pg.evaluate("document.querySelector('#p-camp').click()"); await pg.wait_for_timeout(6000); await pg.screenshot(path='f_camp.png')
        print('net',net); print('\n'.join(logs)); await b.close()
asyncio.run(main())
