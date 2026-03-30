'use strict';

import puppeteer from 'puppeteer-core';

const lpdopts = {
    host: '127.0.0.1',
    port: 9222,
};

const puppeteeropts = {
    browserWSEndpoint: 'ws://' + lpdopts.host + ':' + lpdopts.port,
};

let browser, context, page;

export async function init() {
    browser = await puppeteer.launch({
        executablePath: "C:\\Users\\sagar\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        headless: false,
        devtools: true
    });

    // Use incognito context if you want isolation
    context = await browser.createBrowserContext();
    page = await context.newPage();

    return { browser, context, page };
}

export async function stop() {
    await page.close();
    await context.close();
    await browser.close();
}