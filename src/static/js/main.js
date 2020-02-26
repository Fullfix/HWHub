const getUserId = function() {
	return fetch('/api/get_user_id', { // Your POST endpoint
    method: 'GET',
    headers: {
      // Content-Type may need to be completely **omitted**
      // or you may need something
    },
  	}).then(response => response.json())
};