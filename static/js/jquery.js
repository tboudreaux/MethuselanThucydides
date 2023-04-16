$(document).ready(function() {
  $('.question-form').submit(function(event) {
    // Prevent the form from submitting normally
    event.preventDefault();
    
    // Get the user's question from the input field
    const query = $(this).find('#question-input').val();
    
    // Get the arxiv_id from the data attribute on the form
    const arxiv_id = $(this).data('arxiv-id');
    
    // Call the API endpoint with the user's query and arxiv_id as parameters
    fetch(`/api/query/complex/${arxiv_id}/${encodeURIComponent(query)}`, {
      method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
      // Update the DOM with the API response
      $(this).siblings('.result').text(data.result);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
});

