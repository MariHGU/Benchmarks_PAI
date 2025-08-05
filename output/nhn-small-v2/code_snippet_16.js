let axios = require('axios');
data = { user: 'smith' };
axios.post('http://localhost:8000', data, { headers: {'Content-Type': 'application/json' } })
    .then(response => (console.log(response.url)))