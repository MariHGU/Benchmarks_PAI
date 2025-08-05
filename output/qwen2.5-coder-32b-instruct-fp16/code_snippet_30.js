let axios = require('axios');
data = { username: 'smith' }; // Match the field names in your Pydantic model
axios.post('http://localhost:8000', data)
    .then(response => console.log(response.data))
    .catch(error => console.error(error));