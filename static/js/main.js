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
    if($('#post-short').length && $('#post-full').length) {
        $('#post-short').mdmagick();
        $('#post-full').mdmagick();
    }

    $('a[data-target="_blank"]').attr('target', '_blank');
    $('a.icon').on('click', function(){
        return confirm('Are you shure?');
    });
});
