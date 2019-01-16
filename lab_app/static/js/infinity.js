// Загрузка части фильмов
function loadFilms(pageNumber) {
    csrf_token = "{{ csrf_token }}";

    // Показываем загрузку
    $("#film-cards").append("<p id=\"progress\" style=\"text-align: center;\n\">🔎 Loading products..</p>");

    $.ajax({
        url: "page=" + pageNumber,
        type: "GET",
        headers: {'X-CSRFToken': csrf_token},
        success: function (response) {
            // Удаляем загрузку
            $("#progress").remove()

            // Добавляем новую порцию продуктов
            var rows = $(response).find('#row')
            $("#film-cards").append(rows);
        },
        error: function (response) {
            console.log("Error with response: " + response) // ошибка загрузки порции
        }
    });
}