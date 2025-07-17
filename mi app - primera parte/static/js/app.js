
function agregarGenero(){
    const genero = {
        nombre: document.getElementById('txtGenero').value
    };
    const url = "/genero/";
    fetch(url, {
        method: "POST",
        body: JSON.stringify(genero),
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(respuesta => respuesta.json())
    .then(resultado => {
        if (resultado.estado){
            location.href = "/generos/";
        } else {
            swal.fire("Agregar Genero", resultado.mensaje, "warning");
        }
    })
    .catch(error =>
        console.error(error)
    );
}


function agregarPelicula(){
    const pelicula = {
        codigo: document.getElementById('txtCodigo').value,
        titulo: document.getElementById('txtTitulo').value,
        protagonista: document.getElementById('txtProtagonista').value,
        duracion: document.getElementById('txtDuracion').value,
        resumen: document.getElementById('txtResumen').value,
        genero: document.getElementById('cmbGenero').value,
        
    };
    const url = "/pelicula/"; 

    fetch(url, {
        method: "POST",
        body: JSON.stringify(pelicula),
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(respuesta => respuesta.json())
    .then(resultado => {
        if (resultado.estado){
            location.href = "/peliculas/"; 
        } else {
            swal.fire("Agregar Pelicula", resultado.mensaje, "warning");
        }
    })
    .catch(error =>
        console.error(error)
    );
}