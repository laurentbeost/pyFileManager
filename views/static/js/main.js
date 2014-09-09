$(document).ready(function() {
  // init fancybox
  $("a.fancyLink").fancybox({
    openEffect: 'fade',
    prevEffect: 'fade',
    nextEffect: 'fade'
  });


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


  // renaming : disable renaming mode
  var disableRenaming = function(linkId) {
    $('.no-href').attr('class', '');                // remove no-href class
    $('.no-input').attr('class', 'hidden');         // remove no-input class
    $('.no-overlay').css('visibility', 'hidden');   // restore hidden class
    $('.no-overlay').attr('class', 'overlay');      // remove no-overlay class
    // reset input field
    originLink = $('#href'+linkId).text();
    inputArea = $('#input'+linkId);
    inputArea.val(originLink);
  }


  // renaming
  var renamingProcess = function(srcPath, dstPath) {
    // don't uselessly send request
    if (srcPath == dstPath) {
      return;
    }
    // display loading gif
    showHideLoading(".no-input")
    // send request
    $.ajax({
      url: "rename?srcPath="+srcPath+"&dstPath="+dstPath,
      context: document.body,
      error: function(result, statut, error) {
        // display message
        displayAlertBox('<strong>Error!</strong> Could not rename this element : check your network connectivity.')
      },
      complete: function(http_code, statut){
        // after success/error : remove loading gif
        showHideLoading()
      }
    });
  }

  // display or hide loading gif
  var showHideLoading = function(selector) {
        if ($("#loading").size() == 0) {
          $(selector).after('<img src="img/icons/load.gif" alt="loading" id="loading" />')
        } else {
          $("#loading").remove();
        }
  }

  var displayAlertBox = function(message) {
    $('#alertMarker').after('<div class="alert alert-warning alert-dismissible" role="alert" id="alertBox">'
      +'<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'
      +message
    +'</div>');
  }

  // renaming : click to rename
  $('.renameElement').on('click', function(event) {
    // disable previous renaming
    disableRenaming();

    // new renaming
    var elementPath = $(this).attr('data-element-path');
    var linkId = $(this).attr('data-link-id');
    $('#href'+linkId).attr('class', 'hidden no-href');      // hide link
    $('#input'+linkId).attr('class', 'no-input');           // enable input
    $('#input'+linkId).select();                            // select text
    $('#overlay'+linkId).attr('class', 'no-overlay hidden');// disable overlay

    // add handler : when leaving input the input field
    $('#input'+linkId).focusout(function() {
      disableRenaming(linkId);
    });

    // add handler : when pressing [ENTER] or [ESC]
    $('#input'+linkId).keypress(function(event) {
      // when [ENTER] is pressed : validate
      if (event.which == 13 || event.keyCode == 13) {
        // get previous name and new name
        srcPath = $('#href'+linkId).text();
        dstPath = $('#input'+linkId).val();
        // rename
        renamingProcess(srcPath, dstPath);
        // change name on href link
        inputArea = $('#input'+linkId);
        $('#href'+linkId).text(inputArea.val());
        // remove input
        disableRenaming(linkId);
      }
      // when [ESC] is pressed : cancel everything
      else if (event.which == 27 || event.keyCode == 27) {
        disableRenaming(linkId);
      }
    });
  });

});
