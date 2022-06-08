// import the data from data.js
const tableData = data;

// Reference the HTML table using d3
var tbody = d3.select("tbody");

// Function to clean the table
function buildTable(data) {
    // First, clear out any existing data
    tbody.html("");

    // Next, loop through each object in the data
    // and append a row and cells for each value in the row
    data.forEach((dataRow) => {
        // Create a variable that will append a row to the table body
        let row = tbody.append("tr");
    
        // Loop through each field in the dataRow and add
        // each value as a table cell (td)
        Object.values(dataRow).forEach((val) => {
            // Append each value of the object to a cell in the table     
            let cell = row.append("td");
            // Add the values
            cell.text(val);
            }
        );
    });
}

// Set up a function that handle after an input is given
// function handleClick() {
//     Create a variable to hold the data 
//     let state = d3.select("#State").property("value");
//     Set a default filter and save it to a new variable.
//     let filteredData = tableData;

//     Set the statement "If there is a date already set, then use that date as a filter. If not, then return the default data."
//     if (state) {
//         "Show only the rows where the date is equal to the date filter we created above."
//         filteredData = filteredData.filter(row => row.State === state);
//     };

//     Rebuild the table using the filtered data
//     @NOTE: If no date was entered, then filteredData will
//     just be the original tableData.
//     buildTable(filteredData);
// };

// Create a tied code to the filter button in the webpage.
// d3.selectAll("#filter-btn").on("click", handleClick)

// Call the original table
buildTable(tableData);
