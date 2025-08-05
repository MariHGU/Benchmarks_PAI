let axios = require('axios');
data = { "user": "smith" };
axios.post('http://localhost:8000', data).then(response => (console.log(response.url)));