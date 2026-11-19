import asyncio, pathlib
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1100,'height':700})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'): await r.fulfill(path=str(SITE/u[len('http://local/'):]))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(6000)
        c=lambda sel: pg.evaluate(f"document.querySelector('{sel}').click()")
        await c('#entrar'); await pg.wait_for_timeout(2500); await pg.screenshot(path='k_dentro.png')
        await pg.keyboard.down('ArrowLeft'); await pg.wait_for_timeout(1500); await pg.keyboard.up('ArrowLeft')
        await pg.keyboard.down('KeyW'); await pg.wait_for_timeout(1200); await pg.keyboard.up('KeyW'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='k_anda.png')
        await c('#fp-sair'); await pg.wait_for_timeout(2500); await pg.screenshot(path='k_sai.png')
        print('\n'.join(logs)); await b.close()
asyncio.run(main())
