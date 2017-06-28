var reload = function() {
  $.ajax({
    type: "GET",
    url: "/help/",
    success: function(requestRows){
      var requestsHolder = $('.request-holder');
      requestRows.forEach(function(row){
        requestsHolder.append('<div class="request-row" id="' + row.id +'">'+row.text+'</div>');
      });
    }
  });
};

$(document).ready(function() {
  reload();
});