$(document).ready(function () {
  $("form").submit(function (event) {
    $.ajax({
      type: "POST",
      url: "/process",
      data: {
        text: $(".search_input").val(),
      },
    }).done(function (data) {
      if (data.error) {
        $("#error").show();
        $("#success").hide();
      } else {
        $("#success").show();
        $("#result").text(data.result);
        $("#error").hide();
      }
    });
    event.preventDefault();
  });
  $(".search_icon").click(function (event) {
    $.ajax({
      type: "POST",
      url: "/process",
      data: {
        text: $(".search_input").val(),
      },
    }).done(function (data) {
      if (data.error) {
        $("#error").show();
        $("#success").hide();
      } else {
        $("#success").show();
        $("#result").text(data.result);
        $("#error").hide();
      }
    });
    event.preventDefault();
  });
});
