function fetchData() {
    var watchquery = "{{query}}";
    fetch(`/api/watchlist/${watchquery}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the fetched data here
            var currentPriceElement = document.getElementById('currentPrice');
            var changepercentage = document.getElementById('changePercentage')

            var form = document.getElementById('updatestocksform');
            if (currentPriceElement) {
                // Extract the Current Price from the fetched data
                var stocks = data.stocks;
                if (stocks && stocks.length > 0) {
                    var currentPrice = stocks[0][1]; // Assuming the price is always at index 1
                    // Update the text content of the element to display the new Current Price
                    currentPriceElement.textContent = "Current Price: $" + currentPrice;
                    var changeper = stocks[0][2];
                    var market = stocks[0][4];
                    document.getElementById("marketstatus").innerHTML = market;
                    if(changeper>0){
                        changepercentage.classList.add('dark:text-green-500');
                    }
                    else{
                        changepercentage.classList.add('dark:text-red-500');
                    }
                    changepercentage.textContent = changeper + " %" ;
                    document.getElementById("currentprice").value=currentPrice;

                }
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Call the fetchData function immediately
fetchData();

// Call the fetchData function every 5 seconds
setInterval(fetchData, 5000); // Adjust the interval as needed