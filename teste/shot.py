import asyncio, sys, pathlib
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1500,'height':900})
        logs=[]; pg.on('console',lambda m: logs.append(m.type+': '+m.text)); pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u:
                f=TH/u.split('three@0.160.0/')[1]; await r.fulfill(path=str(f),content_type='application/javascript')
            elif u.startswith('http://local/'):
                f=SITE/u[len('http://local/'):]; await r.fulfill(path=str(f))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(6000)
        await pg.screenshot(path='ext.png')
        for js,name in sys.argv[1:] and [] or []: pass
        print("\n".join(logs[:30]))
        await pg.evaluate("document.querySelector('[data-view=lado]').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='lado.png')
        await pg.evaluate("document.querySelector('[data-view=frente]').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='frente.png')
        await pg.evaluate("document.querySelector('[data-p=salvia]').click(); document.getElementById('p-estac').click()"); await pg.wait_for_timeout(2500); await pg.screenshot(path='estac.png')
        await pg.evaluate("document.getElementById('p-geral').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='geral.png')
        print('\n'.join(logs[:30])); await b.close()
asyncio.run(main())
