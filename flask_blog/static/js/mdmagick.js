/*
  # MDMagick

  * url: https://github.com/fguillen/MDMagick
  * author: http://fernandoguillen.info
  * demo page: http://fguillen.github.com/MDMagick/

  ## Version

      v0.0.3

  ## Documentation

  * README: https://github.com/fguillen/MDMagick/blob/master/README.md
*/

var MDM_VERSION = "0.0.3";

function MDM( inputElement ) {
  this.inputElement = inputElement;

  this.initialize = function(){
    this.controlsElement = MDM.Utils.appendControls( inputElement );
    this.previewElement  = MDM.Utils.appendPreview( inputElement );

    this.activatePreview( this.inputElement, this.previewElement );
    this.activateControls( this.controlsElement );
    this.activateInput( this.inputElement, this.controlsElement, this.previewElement );

    this.updatePreview();
  };

  this.click_on_control = false;

  this.activateControls = function( controlsElement ){
    var _self = this;
    ["bold", "italic", "link", "title", "list", "quote", "code", "multilineCode", "img", "strike", "gist"].forEach( function( actionName ){
      $( controlsElement ).find( ".mdm-" + actionName ).click( function( event ){ _self.action( actionName, event ) } );
    });
  };

  this.activatePreview = function( inputElement, previewElement ) {
    $(inputElement).keyup( $.proxy( this.updatePreview, this ) );
  };

  this.activateInput = function( inputElement, controlsElement, previewElement ){
    var _self = this;

    $(controlsElement).mousedown( function(){
      _self.click_on_control = true;
    });

    $(inputElement).focus( function(){
      _self.click_on_control = false;
      $(controlsElement).addClass( "focus" );
      $(previewElement).addClass( "focus" );
      $(controlsElement).removeClass( "blur" );
      $(previewElement).removeClass( "blur" );
    });

    $(inputElement).blur( function(){
      if (!_self.click_on_control) {
        $(controlsElement).removeClass( "focus" );
        $(previewElement).removeClass( "focus" );
        $(controlsElement).addClass( "blur" );
        $(previewElement).addClass( "blur" );
      }
    });
  };

  this.updatePreview = function(){
    var converter = new Attacklab.showdown.converter();
    $( this.previewElement ).html(
      converter.makeHtml( $( this.inputElement ).val().replace(/</g,'&lt;').replace(/>/g,'&gt;') )
    );
  };

  this.action = function( actionName, event ){
    event.preventDefault();
    MDM.Actions[ actionName ]( this.inputElement );
    this.updatePreview();
  };

  this.initialize();
}


/*
  The logic of each of the control buttons
*/
MDM.Actions = {
  bold: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    $( inputElement ).replaceSelection( "**" + selection.text + "**" );
  },

  italic: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    $( inputElement ).replaceSelection( "_" + selection.text + "_" );
  },

  link: function( inputElement ){
    var link = prompt( "Link to URL", "http://" );
    if(link) {
        var selection = $( inputElement ).getSelection();
        var objectValue = $(inputElement).val();
        if(!selection.text){
            $(inputElement).val(objectValue + "\n" + 'link description');
            $(inputElement).setCaretPos(-1);
            MDM.Utils.selectWholeLines( inputElement );
            selection = $( inputElement ).getSelection();
        }

        $( inputElement ).replaceSelection( "[" + selection.text + "](" + link + ")" );
        $( inputElement ).setSelection(selection.start + 1, selection.end + 1); //select description text
    }
  },

  title: function( inputElement ){
    MDM.Utils.selectWholeLines( inputElement );
    var selection = $( inputElement ).getSelection();
    var hash = (selection.text.charAt( 0 ) == "#") ? "#" : "# ";
    $( inputElement ).replaceSelection( hash + selection.text );
  },

  list: function( inputElement ){
    MDM.Utils.selectWholeLines( inputElement );
    var selection = $( inputElement ).getSelection();
    var text = selection.text;
    var result = "";
    var lines = text.split( "\n" );
    for( var i = 0; i < lines.length; i++ ){
      var line = $.trim( lines[i] );
      if( line.length > 0 ) result += "- " + line + "\n";
    }

    $( inputElement ).replaceSelection( result );
  },

  quote: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    $( inputElement ).replaceSelection( "~~" + selection.text + "~~" );
  },

  strike: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    $( inputElement ).replaceSelection( "--" + selection.text + "--" );
  },

  code: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    $( inputElement ).replaceSelection( "`" + selection.text + "`" );
  },

  multilineCode: function( inputElement ){
    var selection = $( inputElement ).getSelection();
    //TODO: cut all empty lines from selection.text
    $( inputElement ).replaceSelection( "[code]\n" + selection.text + "\n[/code]" );
  },

  img: function( inputElement ){
    var link = prompt( "Image URL", "http://" );
    if(link) {
        var selection = $( inputElement ).getSelection();
        var objectValue = $(inputElement).val();
        if(!selection.text){
            $(inputElement).val(objectValue + "\n" + 'img description');
            $(inputElement).setCaretPos(-1);
            MDM.Utils.selectWholeLines( inputElement );
            selection = $( inputElement ).getSelection();
        }

        $( inputElement ).replaceSelection( "![" + selection.text + "](" + link + ")" );
        $( inputElement ).setSelection(selection.start + 2, selection.end + 2); //select description text
    }
  },

  gist: function( inputElement ){
    var string = prompt( "GitHub Gist ID", "" );
    if(string) {
        var selection = $( inputElement ).getSelection();
        var objectValue = $(inputElement).val();
        if(!selection.text){
            $(inputElement).val(objectValue + "\n" + 'link description');
            $(inputElement).setCaretPos(-1);
            MDM.Utils.selectWholeLines( inputElement );
        }
        $( inputElement ).replaceSelection( "\n[gist]" + string + "[/gist]\n" );
    }
  }
}

MDM.Utils = {
  appendControls: function( inputElement ){
    var element = $( MDM.Utils.controlsTemplate() );
    $(inputElement).before( element );

    return element;
  },

  appendPreview: function( inputElement ){
    return false;
    var element = $( MDM.Utils.previewTemplate() );
    element.css( "width", $( inputElement ).css( "width" ) );
    // element.css( "padding", $( inputElement ).css( "padding" ) );
    element.css( "font-size", $( inputElement ).css( "font-size" ) );
    $(inputElement).after( element );

    return element;
  },

  selectWholeLines: function( inputElement ){
    var content = $( inputElement ).val();
    var selection = $( inputElement ).getSelection();
    var iniPosition = (selection.start > 0) ? (selection.start - 1) : 0;
    var endPosition = selection.end;

    // going back until a "\n"
    while( content[iniPosition] != "\n" && iniPosition >= 0 ) {
      iniPosition--;
    }

    while( content[endPosition] != "\n" && endPosition <= content.length ) {
      endPosition++;
    }

    $( inputElement ).setSelection( iniPosition + 1, endPosition );
  },

  controlsTemplate: function(){

    var template =
      "<div class=\"mdm-buttons mdm-control\">" +
      "  <ul>" +
      "    <li class=\"mdm-bold\"><a tabindex=\"-1\" title=\"bold\" class=\"icon-bold\" href=\"#mdm-bold\"><span>B</span></a></li>" +
      "    <li class=\"mdm-italic\"><a tabindex=\"-1\" title=\"italic\" class=\"icon-italic\" href=\"#mdm-italic\"><span>I</span></a></li>" +
      "    <li class=\"mdm-strike\"><a tabindex=\"-1\" title=\"strikethrough\" class=\"icon-strikethrough\" href=\"#mdm-strike\"><span>S</span></a></li>" +
      "    <li class=\"mdm-title\"><a tabindex=\"-1\" title=\"height\" class=\"icon-text-height\" href=\"#mdm-title\"><span>T</span></a></li>" +
      "    <li class=\"mdm-quote\"><a tabindex=\"-1\" title=\"blockquote\" class=\"icon-comment-alt\" href=\"#mdm-quote\"><span>Q</span></a></li>" +
      "    <li class=\"mdm-code\"><a tabindex=\"-1\" title=\"code\" class=\"icon-code\" href=\"#mdm-code\"><span>C</span></a></li>" +
      "    <li class=\"mdm-multilineCode\"><a tabindex=\"-1\" title=\"multiline-code\" class=\"icon-terminal\" href=\"#mdm-multilineCode\"><span>MLC</span></a></li>" +
      "    <li class=\"mdm-list\"><a tabindex=\"-1\" title=\"list\" class=\"icon-list-ul\" href=\"#mdm-list\"><span>l</span></a></li>" +
      "    <li class=\"mdm-link\"><a tabindex=\"-1\" title=\"link\" class=\"icon-link\" href=\"#mdm-link\"><span>a</span></a></li>" +
      "    <li class=\"mdm-img\"><a tabindex=\"-1\" title=\"img\" class=\"icon-picture\" href=\"#mdm-img\"><span>Img</span></a></li>" +
      "    <li class=\"mdm-gist\"><a tabindex=\"-1\" title=\"GitHub Gist\" class=\"icon-github bigger\" href=\"#mdm-gist\"><span>G</span></a></li>" +
      "  </ul>" +
      "</div>";

    return template;
  },

  previewTemplate: function(){
    var template = "<div class=\"mdm-preview mdm-control\"></div>";

    return template;
  }
}

$(function(){
  if( typeof window.MDM_SILENT == 'undefined' || window.MDM_SILENT == false ) {
    console.debug( "loading MDMagick v" + MDM_VERSION + "..." );
  }

  jQuery.fn.mdmagick = function(){
    this.each( function( index, inputElement ){
      var mdm = new MDM( inputElement );
    });
  };

  $(".mdm-input").mdmagick();
});
