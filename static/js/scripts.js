var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  return new bootstrap.Toast(toastEl)
});

$('.modal button.btn-close').click(function () {
  console.log("2")
  let iframeContainer = $(this).parent().parent().find('.modal-body iframe');
  iframeContainer.removeAttr('src');
});


