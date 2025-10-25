import botright
import asyncio

async def main():
    botright_client = await botright.Botright()
    browser = await botright_client.new_browser()
    page = await browser.new_page()
    
    await page.goto('https://pixelscan.net/bot-check')
    await asyncio.sleep(5)
    
    await botright_client.close()

if __name__ == '__main__':
    asyncio.run(main())