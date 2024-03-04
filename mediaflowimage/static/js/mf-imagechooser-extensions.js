// This is the js-file that is used by our custom FileInput widget import_button.html
// the widget is a django FileInput with an extra button to open
// 'Insert from Mediaflow' modal

$(document).ready(function () {
  if (!window.mfImageModal) {
    console.error('Mf Image Modal failed to initialize')
    return
  }

  function uploadAndUse(imageFile, title) {
    let formData = new FormData()
    let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    let collectionId = 1
    let chooserParts = window.mfImageModal.url.split('?')
    let createUrl = chooserParts[0] + 'create/'
    if (chooserParts.length > 0) {
      createUrl += '?' + chooserParts[1]
    }

    if ($('#id_image-chooser-upload-collection').length) {
      collectionId = $('#id_image-chooser-upload-collection').val()
    }
    formData.append('image-chooser-upload-title', title)
    formData.append('image-chooser-upload-collection', collectionId)
    formData.append('image-chooser-upload-file', imageFile)
    formData.append('image-chooser-upload-tags', '')
    formData.append('image-chooser-upload-focal_point_x', '')
    formData.append('image-chooser-upload-focal_point_y', '')
    formData.append('image-chooser-upload-focal_point_width', '')
    formData.append('image-chooser-upload-focal_point_height', '')

    $.ajax({
      beforeSend: function (request) {
        request.setRequestHeader('X-CSRFToken', csrfToken)
      },
      contentType: false,
      data: formData,
      processData: false,
      type: 'POST',
      url: createUrl,
    }).done(function (data) {
      $('#tab-label-upload')[0].click()
      // This will 'magically' move the modalWorkflow along...
      window.mfImageModal.loadResponseText(JSON.stringify(data))
    })
  }

  function startImport(downloadURL, title) {
    $.ajax({
      url: downloadURL,
      cache: false,
      xhr: function () {
        var xhr = new XMLHttpRequest()
        xhr.responseType = 'blob'
        return xhr
      },
      success: function (data) {
        // TODO: How come we don't get the full filename with extension from fileselector?
        uploadAndUse(new File([data], title + '.jpg'), title)
      },
      error: function (e) {
        console.error(e)
      },
    })
  }

  // Inject our own tab + click behaviour (not so stylish approach but it works)
  let tabLink = $(
      '<a id="tab-label-mfp-insert" href="#tab-mfp-insert" class="w-tabs__tab">Insert from Mediaflow</a>',
    ),
    newSection = $(
      '<section role="tabpanel" class="w-tabs__panel" id="tab-mfp-insert" hidden></section>',
    ),
    fileSelectorElement = $(
      '<div id="mf-fileselector" style="position:relative;min-height:460px" class="light"></div>',
    )

  newSection.append(fileSelectorElement)
  $('.modal-body .tab-content').append(newSection)
  $('.modal-body [role=tablist]').append(tabLink)

  tabLink.on('click', function (e) {
    e.preventDefault()
    $('.modal-body section').each(function () {
      if ($(this).attr('id') == 'tab-mfp-insert') {
        $(this).removeAttr('hidden')
      } else {
        $(this).attr('hidden', '')
      }
    })
    $('.modal-body .w-tabs a').each(function () {
      $(this).attr(
        'aria-selected',
        ($(this).attr('id') == 'tab-label-mfp-insert').toString(),
      )
    })
  })

  $('.modal-body a.w-tabs__tab').each(function () {
    if ($(this).attr('id') != 'tab-label-mfp-insert') {
      $(this).on('click', function () {
        $('#tab-mfp-insert').attr('hidden', '')
        $('#tab-label-mfp-insert').attr('aria-selected', 'false')
      })
    }
  })

  // Attach the fileselector to our own tab
  new FileSelector('mf-fileselector', {
    auth: 'token',
    // These are the same for all customers but should perhaps
    // be moved to app config / wagtail conf
    client_id: '8b62ca84',
    client_secret: 'rZpA0vP7oKOSJw3lZBX1e4EVElHsbQ',
    refresh_token: $('#mf-server-key').val(),
    showDoneButton: false,
    limitFileType: 'jpg',
    viewLayout: 'thumbnails',
    allowCrop: true,
    noCropButton: false,
    showDoneButton: true,
    locale: 'sv-se',
    downloadFormat: 'original',
    ready: function () {},
    success: function (o) {
      startImport(o.url, filename)
    },
    events: function (eventName, eventData) {
      if (eventName === 'fileClick') {
        filename = eventData.name
      }
    },
  })
})
