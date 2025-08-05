let axios = require('axios');
let data = { user: 'smith' };
axios.post('http://localhost:8000', data)
     .then(response => console.log(response.url))
     .catch(error => console.error(error));