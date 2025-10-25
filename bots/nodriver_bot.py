import nodriver as uc
import asyncio

async def main():
    # Use specific Chrome arguments for better stealth
    browser = await uc.start(
        headless=False,
        browser_args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
            '--disable-web-security',
            '--disable-features=UserAgentClientHint',
            '--window-size=1920,1080',
            '--start-maximized',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-background-timer-throttling',
            '--disable-ipc-flooding-protection',
            '--password-store=basic',
            '--use-mock-keychain',
            '--disable-dev-shm-usage',
            '--no-sandbox',
        ]
    )
    
    page = await browser.get('https://pixelscan.net/bot-check')
    
    # Execute additional stealth scripts
    await page.evaluate('''
        () => {
            // Remove webdriver traces
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Spoof plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Spoof languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Chrome runtime
            window.chrome = {
                runtime: {}
            };
            
            // Permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        }
    ''')
    
    await page.sleep(5)
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(main())