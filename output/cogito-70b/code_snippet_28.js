let axios = require('axios');
axios.post('http://localhost:8000/?user=smith')
    .then(response => console.log(response.data));