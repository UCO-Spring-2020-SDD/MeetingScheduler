$(document).ready(function() {

  // do this only for the projects page
  if($('#project-pane').length && $('#active-pane').length) {
    var hasEdited = false;
    var canceledURL = '';
    
    $('.do-discard').click(function() {
      window.location = canceledURL;
    });
    
    Split(["#project-pane","#active-pane"], {
      elementStyle: function (dimension, size, gutterSize) { 
        $(window).trigger('resize'); // Optional
        $("#projects").height($(window).height()
            - $("#titular-nav").height()
            - parseFloat($("#titular-nav").css('padding-top'))
            - parseFloat($("#titular-nav").css('padding-bottom')));
        return { 'flex-basis': 'calc(' + size + '% - ' + gutterSize + 'px)' }
      },
      gutterStyle: function (dimension, gutterSize) { return {'flex-basis':  gutterSize + 'px'} },
      sizes: [20,60,20],
      minSize: 200,
      gutterSize: 0, // meh
      cursor: 'col-resize'
    });

    $('#create-project-btn').on('click', function() {
      if(hasEdited) {
        canceledURL = '/meeting/projects/create';
        $("#confirm-discard-modal").modal();
      } else window.location = '/meeting/projects/create';
    });
    
    $('#edit-project-btn').on('click', function() {
      if(window.location.href.endsWith('/edit'))
        window.location = window.location
      else window.location += '/edit';
    });

    $('#new-meeting-btn').on('click', function() {
      if(window.location.href.endsWith('/edit'))
        window.location = window.location.href.slice(0, -5) + '/meetings/create';
      else window.location += '/meetings/create';
    });
    
    $('.project-card').click(function() {
      if(hasEdited) {
        canceledURL = '/meeting/projects/' + $(this).attr('project');
        $("#confirm-discard-modal").modal();
      } else window.location = '/meeting/projects/' + $(this).attr('project');
    });
    
    // do this only for the view, create, or edit panes
    if($('#active-pane-view').length || $('#active-pane-create').length || $('#active-pane-edit').length) {
      if($('#current-project').length) {
        let currentProject = $('#current-project').html();
        $(`#project-card-${currentProject} > div`).attr('class', function(i, c){
          return c.replace(/(^|\s)bg-\S+/g, ' bg-success');
        });
      }
    }
    
    // do this only for the view pane
    if($('#active-pane-view').length) {
      let leYeetBtn;
      
      $('#invite-member-btn').on('click', function() {
        $("#invite-member-modal").modal();
      });
      
      $('#delete-project-btn').on('click', function() {
        $("#confirm-remove-project-modal").modal();
      });
      
      $('#leave-project-btn').on('click', function() {
        $("#confirm-leave-project-modal").modal();
      });
      
      $('button.remove-member').on('click', function() { // pre-yeet
        leYeetBtn = $(this);
        $("#confirm-yeet-modal").modal();
      });
      
      $('#yeet-member').on('click', function() {
        console.log("member -> yeet");
        $("#passback-action").val("remove");
        $("#passback-user").val(leYeetBtn.attr("datum"));
        $("#passback-form").submit();
      });
      
      $('#yeet-project').on('click', function() {
        console.log("member -> yeet");
        $("#passback-action").val("delete");
        $("#passback-form").submit();
      });
      
      $('#yeet-self').on('click', function() {
        console.log("self -> yeet");
        $("#passback-action").val("leave");
        $("#passback-form").submit();
      });
      
      $('#yoink-member').on('click', function() {
        console.log("member -> yoink");
        
        let username = $("#invite-username").val().trim();
        if(username.length == 0) {
          $("#yoink-error").text("Username cannot be blank.");
        } else {
          let existsInTeam = false;
          $(".das-username").each(function() {
            if(username == $(this).text()) existsInTeam = true;
          });
          
          let existsAtAll = false;
          $("#potential-yoinks span").each(function() {
            if(username == $(this).text()) existsAtAll = true;
          });
          
          if(existsInTeam) $("#yoink-error").text("That user is already in the project.");
          else if(!existsAtAll) $("#yoink-error").text("That user doesn't exist.");
          else $("#yoink-error").text("");
        }
        
        if($("#yoink-error").text().length > 0) $("#yoink-error").show();
        else {
          $("#yoink-error").hide();
          $("#passback-action").val("invite");
          $("#passback-user").val($("#invite-username").val());
          $("#invite-member-modal").modal('toggle');
          $("#passback-form").submit();
        }
      });
      
      $('#yeet-invite').on('click', function() {
        console.log("invite -> yeet");
        $("#passback-action").val("reject");
        $("#passback-form").submit();
      });
      
      $('#yoink-invite').on('click', function(){
        console.log("invite -> yoink");
        $("#passback-action").val("accept");
        $("#passback-form").submit();
      });
    }
    
    // do this only for the create or edit panes
    if($('#active-pane-create').length || $('#active-pane-edit').length) {
      $('input[type="text"], textarea').on('keydown', function() {
        hasEdited = true; 
      });
    }
  }
  
  // notification demo
  if($('#notification-demo').length) {
    $('#notify-btn').on('click', function() {
      let user = $('#notify-user').val() == 0 ? null : $('#notify-user').val();
      let message = $('#notify-message').val();
      let link = $('#notify-link').val().trim() ? $('#notify-link').val().trim() : null;
      notify(user, message, link);
    });
  }

});