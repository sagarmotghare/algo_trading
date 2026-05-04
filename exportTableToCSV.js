function exportTableToCSV() {
    const tables = document.getElementsByTagName("table");
    const csvData = [];

    // Iterate through rows
    for (const t in tables) {
        const table = tables[t]
        console.log("table",table)
        for (const row of table.rows) {
            const rowData = [];
            // Iterate through cells (both th and td)
            for (const cell of row.cells) {
                let data = cell.innerText.replace(/"/g, '""'); // Escape double quotes
                // Wrap in quotes if data contains comma, newline, or quote
                if (data.search(/("|,|\n)/) >= 0) {
                    data = `"${data}"`;
                }
                rowData.push(data);
            }
            csvData.push(rowData.join(','));
        }

        const csvContent = csvData.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `export-${t}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
}   