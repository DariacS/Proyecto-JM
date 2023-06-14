function deletepro(id) {
    Swal.fire({
        title: '¿ Estas seguro ?',
        icon: 'success',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Eliminar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire('Eliminado!', 'Producto Eliminado Correctamente', 'success').then(function () {
                window.location.href = "/eliminarproducto/" + id + "/";
            })
        }
    })
}