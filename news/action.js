'use strict';

import { collectPosts } from "./collect.js";
import { DatabaseSync } from 'node:sqlite';

async function action() {
    const posts = await collectPosts()
    const database = new DatabaseSync('./news.db');

    database.exec(`
        CREATE TABLE IF NOT EXISTS news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data TEXT
        )
    `);

    const insert = database.prepare('INSERT INTO news (timestamp, data) VALUES (?, ?)');
    let liveBlog = posts.liveBlogUpdate
    console.log("Total Post:", liveBlog.length)

    for (let post of liveBlog) {
        insert.run(new Date().toISOString(), JSON.stringify(post));
    }
}

action()