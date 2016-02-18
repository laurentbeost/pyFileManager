<!doctype html>
<head>
  <meta charset="utf-8"/>
  <title>File manager</title>
  <meta name="description" content="pyFileManager - Python web file manager">
  <link rel="stylesheet" href="css/bootstrap.min-3.3.6.css">
  <link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/jquery.fancybox-2.1.5.pack.css" type="text/css" media="screen" />
  <link rel="stylesheet" href="css/jquery.fancybox-buttons-1.0.5.pack.css" type="text/css" media="screen" />
  <link rel="stylesheet" href="css/style.css">
  <script type="text/javascript" src="js/jquery-2.2.0.min.js"></script>
  <script type="text/javascript" src="js/jquery.fancybox-2.1.5.pack.js"></script>
  <script type="text/javascript" src="js/jquery.fancybox-buttons-1.0.5.pack.js"></script>
  <script type="text/javascript" src="js/bootstrap.min-3.3.6.js"></script>
  <script type="text/javascript" src="js/main.js"></script>
</head>
<body>
  <div class="container">
    %if data['is_auth']:
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"> <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">${data['title']}</a>
        </div>
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <p class="navbar-text navbar-right">
              <a href="logout" class="navbar-link">Log out<i class="fa fa-sign-out" style="margin-left: 5px"></i></a>&nbsp;
            </p>
          </div>
      </div>
    </nav>
    <span id="alertMarker"></span>
    <div class="panel panel-default" id="main">
      <div class="panel-heading">Browse files : ${data['title']}</div>
      <table class="table">
        <tr>
          <th style="width: 300px;">Name</th>
          <th>Permissions</th>
          <th>Size</th>
          <th>Modified</th>
        </tr>
        %if data['toplevel']:
          <tr>
            <td>
              <a href="?path=${data['toplevel']}" title="Parent directory"><i class="fa fa-folder-open-o" style="margin-right: 5px; color: #000"></i>..</a>
            </td>
            <td><td><td></td>
          </tr>
        %endif
        %for row in data['fileList']:
          <tr id="${row['id']}">
            <td>
            <%
            thisLink = '#'
            thisClass = ''
            thisFancyGroup = ''
            if row["filetype"] == 'folder-o':
              thisLink = '?path='+row['path']
            else:
              if row["filetype"] == 'file-image-o':
                thisLink = 'img/view?path='+row['path']
                thisClass = 'fancyLink'
                thisFancyGroup = 'group'
              end
            end%>
            <a href="${thisLink}" id="hrefId${row['id']}" class="${thisClass}" data-fancybox-group="${thisFancyGroup}"><i class="fa fa-${row["filetype"]}" style="margin-right: 5px; color: #000"></i>${row['name']}</a>
            <input id="inputId${row['id']}" class="hidden" value="${row['name']}" />
            %if data['is_admin']:
              <span class="overlay" style="float: right;" id="overlayId${row['id']}">
                <a href="#" class="renameElement" data-element-path="${row['path']}" data-link-id="Id${row['id']}"><i class="fa fa-pencil-square-o" title="Rename"></i></a>
                %if row["filetype"] != 'folder-o':
                  <a href="download?path=${row['path']}"><i class="fa fa-arrow-circle-o-down" title="Download"></i></a>
                  <a href="#" data-toggle="modal" data-target="#deleteModal" data-line-id="${row['id']}" data-delete-file-path="${row['path']}"><i class="fa fa-trash-o" title="Remove"></i></a>
                %endif
              </span>
            %endif
            </td>
            <td>${row['chmod']}</td>
            <td>
              %if row["filetype"] != 'folder-o':
                ${row['size']}
              %endif
            </td>
            <td>${row['date']}</td>
          </tr>
        %endfor
      </table>
    </div>
    <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
            <h4 class="modal-title" id="deleteModalLabel">Are you sure ?</h4>
          </div>
          <div class="modal-body">
            Remove &laquo; <span id="fileName"></span> &raquo; ?
            <span class="hidden" id="lineId"></span>
            <span class="hidden" id="filePath"></span>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-dismiss="modal">No</button>
            <button type="button" class="btn btn-danger" id="deleteFile">Yes</button>
          </div>
        </div>
      </div>
    </div>
    %else:
    <form class="form-horizontal" action="${data['app_dir']}/login" method="POST">
      <div id="loginbox" style="margin-top:50px;" class="mainbox col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2">
          <div class="panel panel-default">
            <div class="panel-body">
              <fieldset>
                <legend>Please sign in</legend>
                <div class="input-group" style="margin-bottom: 25px">
                  <span class="input-group-addon"><i class="fa fa-user"></i></span>
                  <input id="login" type="text" class="form-control" name="login" value="" placeholder="username">
                </div>
                <div class="input-group" style="margin-bottom: 25px">
                  <span class="input-group-addon"><i class="fa fa-lock"></i></span>
                  <input id="password" type="password" class="form-control" name="password" value="" placeholder="password">
                </div>

                %if data['error'] == 'badpass':
                  <div class="alert alert-danger" role="alert">
                    <p><strong>Wrong password !</strong> Please try again.</p>
                  </div>
                %endif
                %if data['error'] == 'empty':
                  <div class="alert alert-danger" role="alert">
                    <p><strong>Enter your username and password !</strong></p>
                  </div>
                %endif
                %if data['error'] == 'badlogin':
                 <div class="alert alert-danger" role="alert">
                   <p><strong>Wrong login !</strong> Please try again.</p>
                 </div>
                %endif

                <button type="submit" class="btn btn-primary">Sign in</button>
              </fieldset>
            </div>
          </div>
        </div>
    </form>
    %endif
  </div>
</body>
</html>
