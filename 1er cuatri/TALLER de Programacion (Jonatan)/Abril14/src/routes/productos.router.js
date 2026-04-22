const express  = require('express')
const productos = require('../data/productos')

const productosRouter = express.Router()

productosRouter.get('/', (req, res) =>{
    res.end(JSON.stringify(productos.infoProductos))
})

productosRouter.get('/:categoria', (req, res) =>{ //:x significa un valor variable.
    const categoria = req.params.categoria //aca me quedo con el id que puse en /productos/:id
    // const producto = lista.find(p => p.id == id)
    const productosCategoria = productos.infoProductos[categoria]
    if (productosCategoria){
        res.end(JSON.stringify(productosCategoria))
    }else{
        res.statusCode = 404
        res.end('la categoria ' + categoria + ' no existe')
    }
})

productosRouter.post('/:categoria', (req, res) =>{
    const categoria = req.params.categoria
    const body = req.body
    productos.infoProductos[productos].push(body)
    res.statusCode = 201
    res.end(JSON.stringify(body))
})

module.exports = productosRouter