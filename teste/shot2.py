import asyncio, pathlib
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1500,'height':900})
        logs=[]; pg.on('console',lambda m: logs.append(m.type+': '+m.text) if 'GL Driver' not in m.text else None); pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'): await r.fulfill(path=str(SITE/u[len('http://local/'):]))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(7000)
        await pg.screenshot(path='v_ext.png')
        print('\n'.join(logs))
        cams={
          'v_tras': "setView('3d',new THREE.Vector3(2.8,0.9,0),new THREE.Vector3(9.5,2.4,5.5))",
        }
        await pg.evaluate("document.querySelector('[data-view=lado]').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='v_lado.png')
        await pg.evaluate("document.querySelector('[data-view=ladoE]').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='v_ladoE.png')
        await pg.evaluate("document.querySelector('[data-view=tras]').click()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='v_tras.png')
        await pg.evaluate("document.getElementById('p-estac').click()"); await pg.wait_for_timeout(3000); await pg.screenshot(path='v_estac.png')
        await b.close()
asyncio.run(main())
