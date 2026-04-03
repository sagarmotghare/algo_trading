'use strict';

import puppeteer from 'puppeteer-core';

// const lpdopts = {
//     host: 'localhost',
//     port: 9222,
// };

// const puppeteeropts = {
//     browserWSEndpoint: `ws://${lpdopts.host}:${lpdopts.port}`
// };

let browser, context, page;

export async function init() {
    try {
        // browser = await puppeteer.connect(puppeteeropts)
        browser = await puppeteer.launch({
            executablePath: "C:\\Users\\sagar\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            headless: false
        })

        // Use incognito context if you want isolation
        context = await browser.createBrowserContext();
        page = await browser.newPage();

        return { browser, context, page };
    } catch (error) {
        console.error(error)
    }

}

export async function stop() {
    if (page && !page.isClosed()) {
        await page.close();
    }
    if (context) {
        await context.close();
    }
    if (browser) {
        await browser.disconnect(); // safer than close() when using connect()
    }
}