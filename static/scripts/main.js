$(document).ready(function () {
  $("form").on("submit", function (event) {
    $.ajax({
      data: {
        name: $("#wordInput").val(),
      },
      type: "POST",
      url: "/process",
    }).done(function (data) {
      if (data.error) {
        $("#errorAlert").show();
        $("#successAlert").hide();
      } else {
        $("#successAlert").show();
        $("#result").text(data.result);
        $("#errorAlert").hide();
      }
    });

    event.preventDefault();
  });
});
