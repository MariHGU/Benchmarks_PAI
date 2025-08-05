const data = {
       user: 'Smith',
       email: 'smith@example.com'
     };
     fetch('/api/endpoint', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
     });