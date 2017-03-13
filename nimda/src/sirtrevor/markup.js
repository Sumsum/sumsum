import $ from 'jquery'


export default {
  type: 'markup',

  icon_name: 'ion-code',

  title: function() { return 'Markup' },

  loadData: function(data) {
    var markup = $(this.editor).find('.markup').val(data.markup)
  },

  save: function() {
    var markup = $(this.editor).find('.markup').val()
    var data = {
      markup: markup
    }
    if (markup) {
      this.setData(data)
    }
  },

  // editorHTML: '',
  editorHTML: function() {
    return [
      '<div class="st-block__editor">',
      '<div class="form-group">',
      '<textarea class="form-control markup" style="width:100%;height:200px;font-family:monaco,courier,monospace;color:#fff;background-color:#333;padding:6px 12px;margin-bottom:40px;"></textarea>',
    //'<code class="language-markup markup" contenteditable></code>',
      '</div>',
      '</div>'
    ].join('\n')
  }

}