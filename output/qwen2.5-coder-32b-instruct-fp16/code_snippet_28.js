let axios = require('axios');

data = { user: 'smith' };  // This is correct and matches the FastAPI model.

axios.post('http://localhost:8000', data)
    .then(response => console.log(response.data))
    .catch(error => console.error(error.response.data));