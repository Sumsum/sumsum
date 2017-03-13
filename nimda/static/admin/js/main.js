$( document ).ready(function() {


  // ======================================================================================
  //  Change List Filters
  // ======================================================================================
  $('#changelist-filter select').each(function(i) {
    if ( !$(this).find('option').first().is(':selected') ) {
      $(this).parent().addClass('active')
    }
  })

  // ======================================================================================
  //  Change List Actions
  // ======================================================================================
  var $changelistForm = $('#changelist-form')
  var $changelistFormCheckboxes = $changelistForm.find('input[type=checkbox]')

  $changelistFormCheckboxes.on('change', function(e) {
    if ( $changelistFormCheckboxes.is(':checked') ) {
      $changelistForm.find('.actions').slideDown(200)
    } else {
      $changelistForm.find('.actions').slideUp(100)
    }
  })


  // ======================================================================================
  //  Tabbed
  // ======================================================================================
  var $tabbedModules = $('.module.tabbed')
  var tabbedModulesLength = $tabbedModules.length
  var $tabs = $('<ul>')


  if ( tabbedModulesLength > 0 ) {
    var tabbedIndex = 0
    var h1 = $('#content h1').first().text()

    // Create tab ul
    $('fieldset.module').first().before($tabs)
    $tabs.addClass('tabs').append('<li data-target="untabbed" class="active">'+ h1 + '</li>')

    $('fieldset.module').each(function(i) {
      var thisTitle = $(this).find('h2').first().text()
      if ( $(this).hasClass('tabbed') ) {
        tabbedIndex++
        $(this).addClass('tab-'+tabbedIndex)
        $tabs.append('<li data-target="tab-'+tabbedIndex+'">'+thisTitle+'</li>')
      } else {
        $(this).addClass('untabbed')
      }
    })
  }

  // Events
  $tabs.find('li').on('click', function(e) {
    $tabs.find('li').removeClass('active')
    $(this).addClass('active')
    $('fieldset.module').attr('style','display:none !important'); /* so it doesnt interfere with .collapsed */
    $('.'+$(this).data('target')).show()
  })

});