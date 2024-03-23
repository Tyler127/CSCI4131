var stocks = new Stocks("4AE762SGAUI1JV4B");

async function getStockData() {
    var stockSymbol = document.getElementById('stock-symbol').value;

    var options = {
        symbol: stockSymbol,
        interval: 'daily',
        amount: 1
    };

    var result = await stocks.timeSeries(options);
    document.getElementById('stocks-api-reponse').innerHTML = JSON.stringify(result, null, 1);
}
