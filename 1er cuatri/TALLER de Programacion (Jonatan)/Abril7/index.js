const http = require('node:http')
const productos = require('./productos.js')

const server = http.createServer((req, res) => {
    console.log(req.method)
    console.log(req.url)
    if (req.method === 'GET') {
        procesarGET(req, res)
    } else if (req.method === 'POST') {
        procesarPOST(req, res)
    } else if (req.method === 'PUT') {
        procesarPUT(req, res)
    } else if (req.method === 'DELETE') {
        procesarDELETE(req, res)
    } else {
        res.statusCode = 501
        res.end(`Método ${req.method} no implementado`)
    }
})

function procesarGET(req, res) {
    if (req.url === '/') {
        res.end('Servidor desarrollado con modulo nativo http')

    } else if (req.url === '/productos') {
        res.setHeader('Content-Type', 'application/json')
        res.end(JSON.stringify(productos.infoProductos.productos))

    } else if (req.url.startsWith('/productos/')) {
        const partesPath = req.url.split('/')
        const idprod = parseInt(partesPath[2])
        const producto = productos.infoProductos.productos.find(p => p.id == id)

        res.setHeader('Content-Type', 'application/json')

        if (producto) {
            res.end(JSON.stringify(producto))
        } else {
            res.statusCode = 404
            res.end(JSON.stringify({ error: `No existe un producto con id ${idprod}` }))
        }

    } else {
        res.statusCode = 404
        res.end(`El path ${req.url} no existe`)
    }
}

function procesarPost(req, res){
    if(req.url=== '/productos'){
        let body = ''
        req.on('data', contenido =>{
            body += contenido
        })
        req.on('end', ()=>{
            body = JSON.parse(body)
            productos.infoProductos.productos.push(body)
            res.statusCode = 201
            res.end(JSON.stringify(body))
        })
    }
}

const puerto = 3000
server.listen(puerto, () => {
    console.log(`Servidor escuchando en el puerto ${puerto}`)
})