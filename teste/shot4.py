import asyncio, pathlib
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1500,'height':900})
        logs=[]; pg.on('console',lambda m: logs.append(m.type+': '+m.text) if 'GL Driver' not in m.text and 'ERR_FAILED' not in m.text else None); pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'): await r.fulfill(path=str(SITE/u[len('http://local/'):]))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(7000)
        print('\n'.join(logs)); logs.clear()
        c=lambda sel: pg.evaluate(f"document.querySelector('{sel}').click()")
        await c('[data-abre=portaE]'); await c('[data-abre=portaD]'); await c('[data-abre=portaCasa]'); await c('[data-abre=janela]'); await c('[data-luz=limp]')
        await pg.wait_for_timeout(1800); await pg.screenshot(path='i_portas.png')
        await c('[data-view=frente]'); await pg.wait_for_timeout(1500); await pg.screenshot(path='i_limp.png')
        await c('#p-camp'); await pg.wait_for_timeout(3500); await pg.screenshot(path='i_camp.png')
        await c('#p-ext'); await c('[data-farol=alto]'); await c('[data-luz=alerta]'); await pg.wait_for_timeout(2500); await pg.screenshot(path='i_noite.png')
        await c('#entrar'); await pg.wait_for_timeout(2500); await pg.screenshot(path='i_dentro.png')
        await c('[data-lugar=mot]'); await pg.wait_for_timeout(600); await pg.screenshot(path='i_mot.png')
        await c('[data-lugar=sala]'); await pg.wait_for_timeout(600); await pg.screenshot(path='i_sala.png')
        print('\n'.join(logs)); await b.close()
asyncio.run(main())
