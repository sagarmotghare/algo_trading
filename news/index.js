'use strict'

import puppeteer from 'puppeteer-core';

const lpdopts = {
    host: '127.0.0.1',
    port: 9222,
};

const puppeteeropts = {
    browserWSEndpoint: 'ws://' + lpdopts.host + ':' + lpdopts.port,
};

(async () => {
    // Connect Puppeteer to the browser.
    const browser = await puppeteer.connect(puppeteeropts);
    const context = await browser.createBrowserContext();
    const page = await context.newPage();

    // Go to Moneycontrol Markets page
    await page.goto("https://www.moneycontrol.com/news/business/markets/", {
        waitUntil: "networkidle2",
        timeout:60000
    });

    const allLinks = document.querySelectorAll("a");
    console.log("allLinks", allLinks)


    // Disconnect Puppeteer.
    //   await page.close();
    //   await context.close();
    //   await browser.disconnect();
}) ();