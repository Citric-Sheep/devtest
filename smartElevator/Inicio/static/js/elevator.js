/*==========================================================================
    Funciones Plantas
==========================================================================*/
/* -- Función para editar registros -- */
function editData(value) {
    items = document.getElementsByClassName(value);                             // Obtener datos de la fila del botón editar 
    /* -- Editar datos de la ventana modal -- */
    document.getElementById('editId').value = items[0].innerHTML;                     // Llenar campo: id del modal editar
    const fecha = new Date(items[1].innerHTML);
    document.getElementById('editDate').valueAsDate = fecha;                 // Llenar campo: nombre del modal editar
    document.getElementById('editTime').value = items[2].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('editDemandFloor').value = items[3].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('editEndFloor').value = items[4].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('editPeople').value = items[5].innerHTML;     // Llenar campo: abreviación del modal editar
    $("#modalEditData").modal('show');                                              // Abrir la ventana modal
}
/* -- Función para eliminar registros -- */
function deleteData(value) {
    items = document.getElementsByClassName(value);                                         // Obtener datos de la fila del botón eliminar 
    /* -- Editar datos de la ventana modal -- */
    document.getElementById('deleteId').value = items[0].innerHTML;                       // Llenar campo: id del modal eliminar
    const fecha = new Date(items[1].innerHTML);
    document.getElementById('deleteDate').valueAsDate = fecha;                 // Llenar campo: nombre del modal editar
    document.getElementById('deleteTime').value = items[2].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('deleteDemandFloor').value = items[3].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('deleteEndFloor').value = items[4].innerHTML;         // Llenar campo: abreviación del modal editar
    document.getElementById('deletePeople').value = items[5].innerHTML;     // Llenar campo: abreviación del modal editar
    $("#modalDeleteData").modal('show');                                                // Abrir la ventana modal
}
