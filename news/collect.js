import { init, stop } from "./setup.js";

export async function collectPosts() {
    const { browser, context, page } = await init();

    // Go to Moneycontrol Markets page
    await page.goto("https://www.moneycontrol.com/news/business/markets/", {
        waitUntil: "domcontentloaded",
    });

    // Extract today sensex link
    const sensex_today_link = await page.evaluate(() => {
        return document.querySelectorAll("li.trendingList a[title='Sensex Today']")[0].href
    });

    // Go to Today Live Sensex Page
    await page.goto(sensex_today_link)

    // Get All Today's post
    const liveBlogPosting = await page.evaluate(() => {
        let all_scripts = Array.from(document.querySelectorAll("script[type='application/ld+json']").values())
        console.log("all_scripts", all_scripts)
        for (let script of all_scripts) {
            const script_content = JSON.parse(script.textContent)
            if (script_content["@type"] == "LiveBlogPosting")
                return script_content
        }
    });
    await stop()
    
    return liveBlogPosting
}