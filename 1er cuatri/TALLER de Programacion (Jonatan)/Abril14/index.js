const express = require('express')
const productos = require('./src/data/productos.js')
const productosRouter = require('./src/routes/productos.router.js')
//exponer los routers
const categoriaRouter = require('./src/routes/categorias.router.js')

const app = express()

app.use(express.json())//antes de empezar a declarar todos los get. Esto es el middleware. 
app.use('/productos', productosRouter)//uso del router productos
app.use('/categorias', categoriaRouter)//uso del router categoria

app.get('/', (req, res) =>{
    res.end('servidor desarrollado con modulo nativo http')
}) //Hace referencia al metodo http

const puerto = 3000
app.listen(puerto, () =>{
    console.log(`Servidor escuchando en el puerto `+ puerto)
})