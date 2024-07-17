$(document).ready(function(){
    // AGREGANDO CLASE ACTIVE AL PRIMER ENLACE
    $('.category_list .category_item[category="all"]').addClass('ct_item-active');

    // FILTRANDO PRODUCTOS
    $('.category_item').click(function(){
        var catProduct = $(this).attr('category');

        // AGREGANDO CLASE ACTIVE AL ENLACE SELECCIONADO
        $('.category_item').removeClass('ct_item-active');
        $(this).addClass('ct_item-active');

        // OCULTANDO Y MOSTRANDO PRODUCTOS SEGÚN LA CATEGORÍA
        $('.product-item').each(function(){
            if($(this).attr('category') === catProduct || catProduct === 'all'){
                $(this).parent().show();
                $(this).css('transform', 'scale(1)');
            } else {
                $(this).parent().hide();
            }
        });
    });
    // Get the modal
	var modal = document.getElementById('id01');

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
	}
});


