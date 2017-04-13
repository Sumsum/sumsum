'use strict';


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

$.AdminLTE.options.animationSpeed = 100
$('.select2').select2()
// remove select2 from the inline templates (we add this later)
$('.inline-related.empty-form').find('select.select2').select2('destroy')
$('.datepickerInput').datepicker({
  autoclose: true,
  format: 'yyyy-mm-dd', 
})
$(".timepickerInput").timepicker({
  showInputs: false,
  showMeridian: false,
  defaultTime: false,
})


// https://github.com/almasaeed2010/AdminLTE/blob/b5f4bba4e61914b1460723d951a4b117bd9dedd1/dist/js/app.js#L571
$(function() {
  $.AdminLTE.boxWidget.collapse = function (element) {
    var _this = this;
    //Find the box parent
    var box = element.parents(".box").first();
    //Find the body and the footer
    var box_content = box.find("> .box-body, > .box-footer, > form  >.box-body, > form > .box-footer");
    if (!box.hasClass("collapsed-box")) {
      //Convert minus into plus
      element.children(":first")
        .removeClass(_this.icons.collapse)
        .addClass(_this.icons.open);
      //Hide the content
      box_content.slideUp(_this.animationSpeed, function () {
        box.addClass("collapsed-box");
      });
    } else {
      //Convert plus into minus
      element.children(":first")
        .removeClass(_this.icons.open)
        .addClass(_this.icons.collapse);
      //Show the content
      box_content.slideDown(_this.animationSpeed, function () {
        box.removeClass("collapsed-box");
        // this is the only line that has been added, to trigger the select2
        // after the box is opened
        box.find('.select2').select2()
      });
    }
  }
})
