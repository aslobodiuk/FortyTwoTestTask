Array.prototype.diff = function(a) {
  return this.filter(function(i) {
    return a.indexOf(i) < 0;
  });
};

var reload = function() {
  $.ajax({
    type: "GET",
    url: "/help/",
    success: function(requestRows){
      var requestsHolder = $('.request-holder');

      var oldIDs = $(".request-row[id]")
        .map(function() { return this.id; })
        .get();

      requestsHolder.empty();

      var newIDs = requestRows.map(function(row){return '' + row.id;})

      var differentCount = newIDs.diff(oldIDs).length;

      var currentI = differentCount;

      if (oldIDs.length > 0 & differentCount != 0) {
        var bracket = document.title.lastIndexOf('(');
        if (bracket > -1) {
          var nextBracket = document.title.lastIndexOf(')');
          currentI = parseInt(document.title.slice(bracket + 1, nextBracket)) + differentCount;
          document.title = document.title.slice(nextBracket+1);
        }
        document.title ='(' + currentI + ')' + document.title;
      }

      requestRows.forEach(function(row){
        requestsHolder.append('<div class="request-row" id="' + row.id +'">'+row.link+'</div>');
      });
    }
  });
};

$(document).ready(function() {

  reload();

  var timerId = setInterval(reload, 1000);

  $(window).focus(function() {
    if (document.title.includes(')')){
      document.title = document.title.slice(document.title.lastIndexOf(')') + 1);
    }
  });

});