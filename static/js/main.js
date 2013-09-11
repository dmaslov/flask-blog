window.MDM_SILENT = true;
$(function(){
    $('#post-preview').on('click', function(){
        var postForm = $('#post-form');
        postForm.find('#preview').val('1');
    });
    $('#post-submit').on('click', function(){
        var postForm = $('#post-form');
        postForm.find('#preview').val('');
    });
    $('#preview-goback').on('click', function(event){
        event.preventDefault();
        window.history.back(1);
    });
    if($('#post-short').length && $('#post-full').length) {
        $('#post-short').mdmagick();
        $('#post-full').mdmagick();
    }

    $('a[data-target="_blank"]').attr('target', '_blank');
});
