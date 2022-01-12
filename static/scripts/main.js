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
        $("#errorAlert").text(data.error).show();
        $("#successAlert").hide();
      } else {
        $("#successAlert").show("slow");
        $("#result").text(data.name);
        $("#errorAlert").hide();
      }
    });

    event.preventDefault();
  });
});
function change() {
  $("#successAlert").hide("slow");
  $("#errorAlert").hide();
  $("#wordInput").css("margin-top", "0");
}
