import asyncio, pathlib, sys
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome')
VIEWS={
 'portaD': ((2.15,0.5,0.2),(2.15,-2.2,0.45)),
 'portaE': ((2.15,-0.5,0.2),(2.15,2.2,0.45)),
 'casa':   ((3.2,0.3,0.2),(3.2,-2.3,0.5)),
 'rodaT':  ((5.0,0.6,0.4),(4.4,-0.1,1.5)),
 'pes':    ((1.45,0.4,0.3),(2.2,0.0,1.3)),
 'degr':   ((5.0,0.3,0.35),(4.3,-0.2,1.3)),
}
async def main():
    sel=sys.argv[1].split(',') if len(sys.argv)>1 else list(VIEWS)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':900,'height':600})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e)))
        await pg.goto('file://'+str(SITE/'teste_3d.html')); await pg.wait_for_timeout(14000)
        await pg.evaluate("for(const id of ['portaE','portaD','portaCasa']) document.querySelector(`[data-abre=${id}]`).click()")
        await pg.wait_for_timeout(4000)
        for n in sel:
            t,c=VIEWS[n]
            await pg.evaluate(f"window.__cam({list(t)},{list(c)})"); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'v_{n}.png')
        print('\n'.join(logs)); await b.close()
asyncio.run(main())
