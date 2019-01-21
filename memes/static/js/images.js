function ogMemeLive() {
//  alert('ding');
  var top = $('#id_top').val() || ' ';
  var bottom = $('#id_bottom').val() || ' ';
  var slug = $('#main_template').attr('data-slug');
  $('#main_template').attr('src',
     '/adhoc_meme/' + slug + '/' + top + '/' + bottom + '/'); 
}

$( document ).ready(function() {
  $('#id_top').on('input', function(){
    ogMemeLive();
  });
  $('#id_bottom').on('input', function(){
    ogMemeLive();
  });
});
