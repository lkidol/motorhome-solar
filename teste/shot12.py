import asyncio, pathlib, sys
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome')
VIEWS={'rodaFD':((1.2,-0.9,0.35),(1.0,-2.7,0.75)),'rodaTE':((5.2,0.9,0.35),(5.0,2.7,0.75)),'rodaTD':((5.2,-0.9,0.35),(5.4,-2.7,0.75)),'portasD':((2.8,-1.0,0.8),(2.6,-5.0,1.4)),'portaE':((2.1,1.0,0.8),(2.4,4.2,1.3))}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':900,'height':600})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        await pg.goto('file://'+str(SITE/'teste_3d.html')); await pg.wait_for_timeout(14000)
        await pg.evaluate("for(const id of ['portaE','portaD','portaCasa']) document.querySelector(`[data-abre=${id}]`).click()"); await pg.wait_for_timeout(5000)
        for n in (sys.argv[1].split(',') if len(sys.argv)>1 else VIEWS):
            t,c=VIEWS[n]; await pg.evaluate(f"window.__cam({list(t)},{list(c)})"); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'c_{n}.png')
        print('\n'.join(logs)); await b.close()
asyncio.run(main())
