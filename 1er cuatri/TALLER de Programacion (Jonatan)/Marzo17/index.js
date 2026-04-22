/*
instalar node
npm i-g nodemon
npm i
*/

const fs = require('node:fs')
const isOdd = require('is-odd')
const os = require('node:os')


function suma(n1, n2, callback){
    const resultado = n1 + n2
    callback(resultado)
}

console.log("Hola Mundo")

suma(2, 4, (resultado) => {
    console.log(resultado)
})

console.log("Nombre OS: " + os.platform)
console.log("Version OS: " + os.release)
console.log("Arquitectura: " + os.arch)

console.log(isOdd('1')) //true
console.log(isOdd(2)) //false

console.log("Vamos a leer el archivo...")
fs.readFile('./Archivo.txt', 'utf-8', (err, data) => {
    if(err){
        console.log('No se pudo leer el archivo')
    }
    else{
    console.log(data)
    console.log('Termine de leer el arhivo')
    }
    console.log("Adios")
})


/*
Eliminar node_modules y package-lock para enviar
*/