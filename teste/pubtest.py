import asyncio, pathlib
from playwright.async_api import async_playwright
TH=pathlib.Path('/home/claude/teste/node_modules/three'); PUB=pathlib.Path('/home/claude/pub'); SITE=pathlib.Path('/home/claude/motorhome')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':900,'height':600}); logs=[]
        pg.on('pageerror',lambda e: logs.append('ERR '+str(e))); pg.on('console',lambda m: logs.append(m.text) if m.type=='error' else None)
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'):
                f=u[len('http://local/'):]; await r.fulfill(path=str(PUB/f if (PUB/f).exists() else SITE/f))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(18000)
        n=await pg.evaluate("document.querySelectorAll('canvas').length"); 
        await pg.evaluate("document.querySelector('#entrar').click()"); await pg.wait_for_timeout(4000); await pg.evaluate("document.querySelector('[data-lugar=mot]').click()"); await pg.wait_for_timeout(3000)
        await pg.screenshot(path='pub_mot.png'); print(n,logs); await b.close()
asyncio.run(main())
