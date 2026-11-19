import asyncio, pathlib, sys
from playwright.async_api import async_playwright
SITE=pathlib.Path('/home/claude/motorhome')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':900,'height':600})
        logs=[]; pg.on('pageerror',lambda e: logs.append('ERR '+str(e))); pg.on('console',lambda m: logs.append(m.type+' '+m.text) if m.type in ('error','warning') else None)
        await pg.goto('file://'+str(SITE/'teste_3d.html')); await pg.wait_for_timeout(16000)
        c=lambda sel: pg.evaluate(f"document.querySelector('{sel}').click()")
        lugs=sys.argv[1].split(';') if len(sys.argv)>1 else ['mot','pas','sala','banho','porta']
        if not lugs[0].startswith('cam:'): await c('#entrar'); await pg.wait_for_timeout(5000)
        else: await c('[data-abre=banho]'); await pg.wait_for_timeout(3000)
        for lug in lugs:
            if lug.startswith('clk:'):
                await c(lug[4:]); await pg.wait_for_timeout(4000); continue
            if lug.startswith('preset:'):
                n=lug.split(':')[1]; await c('#'+n); await pg.wait_for_timeout(5000); await pg.screenshot(path=f'm_{n}.png'); continue
            if lug.startswith('cam:'):
                _,nome,t,cc=lug.split(':'); await pg.evaluate(f"window.__cam([{t}],[{cc}])"); await pg.wait_for_timeout(2500); await pg.screenshot(path=f'm_{nome}.png'); continue
            await c(f'[data-lugar={lug}]'); await pg.wait_for_timeout(3000); await pg.screenshot(path=f'm_{lug}.png')
        r=await pg.evaluate("window.__check()"); print('check',r)
        import os
        if os.environ.get('RAY'):
            for q in os.environ['RAY'].split(';'): print(q, await pg.evaluate(f"window.__ray({q})"))
        if os.environ.get('DBG'): print(await pg.evaluate(f"window.__dbg('{os.environ['DBG']}')"))
        print('\n'.join(logs[:20])); await b.close()
asyncio.run(main())
