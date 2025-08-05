let axios = require('axios');
let data = { user: 'smith' };
axios.post('http://localhost:8000', data, { headers: {'content-type': 'application/json'} })
    .then(response => (console.log(response.url)));