import asyncio, pathlib, sys
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1100,'height':700})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e))); pg.on('console',lambda m: logs.append(m.text) if m.type=='error' and 'ERR_FAILED' not in m.text else None)
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'): await r.fulfill(path=str(SITE/u[len('http://local/'):]))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_function('document.querySelector("#p-ext").getAttribute("aria-pressed")==="true" && window.performance.now()>1', timeout=60000); await pg.wait_for_timeout(9000)
        print('\n'.join(logs)); logs.clear()
        c=lambda sel: pg.evaluate(f"document.querySelector('{sel}').click()")
        await c('#p-interior'); await pg.wait_for_timeout(6000); await pg.screenshot(path='m_interior.png')
        print('\n'.join(logs)); await b.close()
asyncio.run(main())
