import asyncio, pathlib
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome'); TH=pathlib.Path('/home/claude/teste/node_modules/three')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1300,'height':800})
        async def route(r):
            u=r.request.url
            if 'cdn.jsdelivr.net/npm/three@0.160.0/' in u: await r.fulfill(path=str(TH/u.split('three@0.160.0/')[1]),content_type='application/javascript')
            elif u.startswith('http://local/'): await r.fulfill(path=str(SITE/u[len('http://local/'):]))
            else: await r.abort()
        await pg.route('**/*',route)
        await pg.goto('http://local/index.html'); await pg.wait_for_timeout(7000)
        # orbit by dragging to approach the front-left wheel: use wheel zoom
        box=await pg.locator('#vp canvas').bounding_box()
        await pg.mouse.move(box['x']+box['width']*0.55, box['y']+box['height']*0.72)
        for _ in range(6): await pg.mouse.wheel(0,-300); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(1200); await pg.screenshot(path='v_zoom.png')
        await b.close()
asyncio.run(main())
