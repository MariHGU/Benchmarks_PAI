let axios = require('axios');
data = { user: 'smith' };
const jsonData = JSON.stringify(data); // This line is added
axios.post('http://localhost:8000', jsonData, {headers: {'Content-Type': 'application/json'}}) // This line is modified
  .then(response => (console.log(response.url)))