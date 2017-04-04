import $ from 'jquery'


String.prototype.format = function() {
  var args = arguments
  return this.replace(/{(\d+)}/g, function(match, j) {
    return args[j]
  })
}


$('ul.sidebar-menu a:path').parent().addClass('active')
$("tr input.action-select").actions()
$('.actions select').addClass('form-control')
$('.actions .all').hide()
$('.actions .question').hide()
$('.actions .clear').hide()
$($('.actions select[name=action] option')[0]).text('Action')

$('#id_published_at_0').datepicker({
  autoclose: true
});
