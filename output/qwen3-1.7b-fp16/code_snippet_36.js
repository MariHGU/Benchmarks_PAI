const data = { user: 'Smith' };
     fetch('/api/endpoint', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
     });