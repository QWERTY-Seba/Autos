var cantidad_request_sesion = 0
//SABER SI ESTAMOS EN BUSQUEDA O PATENTES
let ES_PAGINA_BUSQUEDA = window.location.href == '...'
if (/complete|interactive|loaded/.test(document.readyState)) {
    scrapear();
} else {
    document.addEventListener('DOMContentLoaded', scrapear, false);
}
async function scrapear(){
    if(ES_PAGINA_BUSQUEDA){
        let patente_scrapear = await obtener_patente()
        let elemt_input = document.querySelector('#valid > div > input')
        let elemt_boton = document.querySelector('#valid > div > span > button')
        elemt_input.value = patente_scrapear + '%'
        await sleeps()
        elemt_boton.click()
    }else{
        extraer_datos()
        await sleeps()
        window.location.href = '...'
    }
}
//FALTA DETECTAR CLOUDFARE Y la posterior pagina de error
function sleeps() {
    return new Promise(resolve => setTimeout(resolve,  3000));
}
//FALTA IMPLETAR EL SISTEMA PARA CONEXION ENTRE MULTIPLES PCS
async function obtener_patente(){
    let res  = null
    await fetch('http://localhost:5000/endpoint', {
        method: 'GET',
        mode: 'cors'
    })
    .then(response =>
        {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text()   
        }
        )
    .then(data => {
        res = String(data)
    })
    .catch(error => {
        console.error('Error:', error);
    })

    return res
}
function extraer_datos(){
    let registros = []

    document.querySelectorAll('tbody > tr').forEach(fila => {
        datos_fila = fila.querySelectorAll('td')
        var registro = {
            Patente : datos_fila[0].innerText,
            Tipo : datos_fila[1].innerText,
            Marca : datos_fila[2].innerText,
            Modelo : datos_fila[3].innerText,
            Rut : datos_fila[4].innerText,
            NroMotor : datos_fila[5].innerText,
            Año : datos_fila[6].innerText,
            Propietario : datos_fila[7].innerText,
            
        }
        registros.push(registro)
    })
    fetch('http://localhost:5000/endpoint', {
        method: 'POST',
        mode: 'cors',
        headers: {
            "Content-Type": "application/json",
            "patente" : document.querySelector('body > div.container > p > i').innerText.replace('%','')  
          },
        body : JSON.stringify(registros)
    })
}
