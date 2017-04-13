'use strict'


$.fn.formset = function(opts) {
  var options = $.extend({}, $.fn.formset.defaults, opts)
  var $this = $(this)
  var $parent = $this.parent()
  var updateElementIndex = function(el, prefix, ndx) {
    var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))")
    var replacement = prefix + "-" + ndx
    if ($(el).prop("for")) {
      $(el).prop("for", $(el).prop("for").replace(id_regex, replacement))
    }
    if (el.id) {
      el.id = el.id.replace(id_regex, replacement)
    }
    if (el.name) {
      el.name = el.name.replace(id_regex, replacement)
    }
  }
  var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off")
  var nextIndex = parseInt(totalForms.val(), 10)
  var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off")
  // only show the add button if we are allowed to add more items,
  // note that max_num = None translates to a blank string.
  var showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0
  $this.each(function(i) {
    $(this).not("." + options.emptyCssClass).addClass(options.formCssClass)
  })
  if ($this.length && showAddButton) {
    var addButton = options.addButton
    if (addButton === null) {
      if ($this.prop("tagName") === "TR") {
        // tabular
        var $el = $this.closest('.inline-group')
      } else {
        // stacked
        var $el = $this.filter(':last')
      }
      $el.after('<div class="' + options.addCssClass + '"><a href="#" class="btn btn-default btn-flat">' + options.addText + "</a></div>")
      addButton = $el.next()
    }
    addButton.click(function(e) {
      e.preventDefault()
      var template = $("#" + options.prefix + "-empty")
      var row = template.clone(true)
      row.removeClass(options.emptyCssClass)
      .addClass(options.formCssClass)
      .attr("id", options.prefix + "-" + nextIndex)
      if (row.is("tr")) {
        // If the forms are laid out in table rows, insert
        // the remove button into the last table cell:
        // XXX When is this?
        row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></div>")
      } else if (row.is("ul") || row.is("ol")) {
        // If they're laid out as an ordered/unordered list,
        // insert an <li> after the last list item:
        // XXX When is this?
        row.append('<li><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></li>")
      } else {
        // Otherwise, just insert the remove button as the
        // last child element of the form's container:
        // This is for stacked
        row.find('.inline_label').parent('.box-title').after('<span><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></span>")
      }
      row.find("*").each(function() {
        updateElementIndex(this, options.prefix, totalForms.val())
      })
      // Insert the new form when it has been fully edited
      row.insertBefore($(template))
      // Update number of total forms
      $(totalForms).val(parseInt(totalForms.val(), 10) + 1)
      nextIndex += 1
      // Hide add button in case we've hit the max, except we want to add infinitely
      if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
        addButton.parent().hide()
      }
      // The delete button of each row triggers a bunch of other things
      row.find("a." + options.deleteCssClass).click(function(e1) {
        e1.preventDefault()
        // Remove the parent form containing this button:
        row.remove()
        nextIndex -= 1
        // If a post-delete callback was provided, call it with the deleted form:
        if (options.removed) {
          options.removed(row)
        }
        $(document).trigger('formset:removed', [row, options.prefix])
        // Update the TOTAL_FORMS form count.
        var forms = $("." + options.formCssClass)
        $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length)
        // Show add button again once we drop below max
        if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
          addButton.parent().show()
        }
        // Also, update names and ids for all remaining form controls
        // so they remain in sequence:
        var i, formCount
        var updateElementCallback = function() {
          updateElementIndex(this, options.prefix, i)
        }
        for (i = 0, formCount = forms.length; i < formCount; i++) {
          updateElementIndex($(forms).get(i), options.prefix, i)
          $(forms.get(i)).find("*").each(updateElementCallback)
        }
      })
      // If a post-add callback was supplied, call it with the added form:
      if (options.added) {
        row.find('.select2').select2()
        options.added(row)
      }
      $(document).trigger('formset:added', [row, options.prefix])
    })
  }
  return this
}

// Setup plugin defaults
$.fn.formset.defaults = {
  prefix: "form",      // The form prefix for your django formset
  addText: "add another",    // Text for the add link
  deleteText: "remove",    // Text for the delete link
  addCssClass: "add-row",    // CSS class applied to the add link
  deleteCssClass: "inline-deletelink",  // CSS class applied to the delete link
  emptyCssClass: "empty-form",  // CSS class applied to the empty row
  formCssClass: "dynamic-form",  // CSS class applied to each form in a formset
  added: null,      // Function called each time a new form is added
  removed: null,      // Function called each time a form is deleted
  addButton: null     // Existing add button to use
}
