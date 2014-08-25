$(document).ready(function() {
  // init fancybox
  $("a.fancybox").fancybox();

  // when mouse enter the table : display buttons
  $(".table tr").on('mouseenter', function() {
    var overlay = $(this).find('span.overlay');
    overlay.css('visibility', 'visible');
  });

  // when mouse leave the table : remove buttons
  $(".table tr").on('mouseleave', function() {
    var overlay = $(this).find('span.overlay');
    overlay.css('visibility', 'hidden');
  });

  // on delete : triggered when modal is about to be shown
  $('#deleteModal').on('show.bs.modal', function(event) {
    // get data attribute of the clicked element
    var filePath = $(event.relatedTarget).data('delete-file-path');
    var lineId = $(event.relatedTarget).data('line-id');
    // populate textbox
    $(event.currentTarget).find('span[id="fileName"]').text(filePath.split('/').slice(-1));
    $(event.currentTarget).find('span[id="filePath"]').text(filePath);
    $(event.currentTarget).find('span[id="lineId"]').val(lineId);
  });

  // on delete : when clicks "yes" from modal
  $('#deleteFile').on('click', function(event) {
    // hide modal, get line id, remove line from table
    $('#deleteModal').modal('hide');
    var lineId = $('#lineId').val();
    thisRow = $('.table tr[id='+lineId+']').remove();
    // and trigger file removal
    var filePath = $('#filePath').text();
    $.ajax({
      url: "delete?path="+filePath,
      context: document.body
    });
  });

  // when renaming element
  $('.renameElement').on('click', function(event) {
    // disable previous renaming
    $('.no-href').attr('class', '');                // remove no-href class
    $('.no-input').attr('class', 'hidden');         // remove no-input class
    $('.no-overlay').css('visibility', 'hidden');   // restore hidden class
    $('.no-overlay').attr('class', 'overlay');      // remove no-overlay class
    // new renaming
    var elementPath = $(this).attr('data-element-path');
    var linkId = $(this).attr('data-link-id');
    $('#href'+linkId).attr('class', 'hidden no-href');      // hide link
    $('#input'+linkId).attr('class', 'no-input');           // enable input
    $('#overlay'+linkId).attr('class', 'no-overlay hidden');// disable overlay
  });
});
