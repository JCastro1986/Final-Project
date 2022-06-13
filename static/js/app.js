// import the data from data.js
var sel = d3.selectAll(".tablaD3")
console.log(sel)

var tableData;

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

// 1. Create a variable to keep track of all the filters as an object.
var filters = {};

// 3. Use this function to update the filters. 
function updateFilters() {

    // 4a. Save the element that was changed as a variable.
    let filter = d3.select(this);

    // 4b. Save the value that was changed as a variable.
    let filterValue = filter.property("value");
    console.log(filterValue);

    // 4c. Save the id of the filter that was changed as a variable.
    let filterId = filter.attr("id");
    console.log(filterId);

    // 5. If a filter value was entered then add that filterId and value
    // to the filters list. Otherwise, clear that filter from the filters object.
    if (filterValue) {
        filters[filterId] = filterValue;
    } else {
        delete filters[filterId];
    };
  
    // 6. Call function to apply all filters and rebuild the table
    filterTable();
  
  }
  
  // 7. Use this function to filter the table when data is entered.
  function filterTable() {
  
    // 8. Set the filtered data to the tableData.
    let filteredData = tableData;
    console.log(filteredData)
  
    // 9. Loop through all of the filters and keep any data that
    // matches the filter values
    Object.keys(filters).forEach((key, index) => {
      filteredData = filteredData.filter(row => row[key] === filters[key]);
    });
      
    // 10. Finally, rebuild the table using the filtered data
    buildTable(filteredData);
    
  }

// 2. Attach an event to listen for changes to each filter
sel.on("change", updateFilters);


// Call the original table
d3.json("/get-data", function(d){
    console.log(d)
    let d2 = d.map(function(x) {
        return {tipo: x.tipo,
            entidad: x.entidad, 
            municipio_x: x.municipio_x,
            precio: x.precio,
            predPrices: x.predPrices,  
            diffPrices: x.diffPrices,
            percentDiff: x.percentDiff, 
            m2Terreno: x.m2Terreno,
            m2Construccion: x.m2Construccion,
            estacionamientos: x.estacionamientos,
            Banos: x.Banos,
            antiguedad: x.antiguedad
            }
         });
    buildTable(d2)
    tableData = d2
});

// buildTable(tableData);
