const axios = require('axios');

const data = {
    name: 'Smith'
};

axios.post('http://localhost:8000/user', data)
    .then(response => console.log(response.data))
    .catch(error => console.error(error));