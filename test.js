const fs = require('fs');
const path = require('path');

// Function to write data to a file
function updateFile(newData) {
  // Define the path to the JSON file
  const filePath = path.join(__dirname,'frontend', 'public', 'data.json'); // Ensure 'public' folder is relative to the script location

  // Write the new data to the JSON file
  fs.writeFile(filePath, JSON.stringify(newData, null, 2), 'utf8', (err) => {
    if (err) {
      console.error('Error writing file:', err);
      return;
    }
    console.log('File updated successfully');
  });
}

// Example data to write
const newData = { message: 'RBC Oasis Tent' };

// Call the function to update the file
updateFile(newData);
