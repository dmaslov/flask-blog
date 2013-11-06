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
    $('.post .no-lightbox img').addClass('col-lg-12');
    $('.post .article img').each(function(index, el){
        var anchor = '<a href="'+$(el).attr('src')+'" title="'+$(el).attr('alt')+'" data-lightbox="'+$(el).attr('src')+'"><img src="'+$(el).attr('src')+'" alt="'+$(el).attr('alt')+'" class="col-lg-12"></a>';
        $(el).replaceWith(anchor);
    });
    $('a.icon').on('click', function(){
        return confirm('Are you shure?');
    });
});
