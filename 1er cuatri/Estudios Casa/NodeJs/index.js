const fs = require('fs')

console.log("Vamos a leer los archivos...");

async function escAr(archiv = '') {
    try {
        const data = await fs.promises.readFile(archiv, 'utf-8')
        console.log(data);
        console.log(`Terminé de leer el archivo ${archiv}`);
    } catch (err) {
        console.log(`No se pudo leer el archivo`);
    }
}

async function leerArchivos(desp = 'Adios') {
    for (let i = 0; i <= 4; i++) {
        let archiv = `./archivo${i}.txt`;
        await escAr(archiv); 
    }
    return desp
}

desp = leerArchivos();
console.log(desp);